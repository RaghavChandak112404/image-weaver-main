import { useState, useCallback } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Upload, Sparkles, Loader2, ImageIcon } from "lucide-react";

const CaptionPage = () => {
  const [image, setImage] = useState<string | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [fileName, setFileName] = useState("");
  const [caption, setCaption] = useState("");
  const [loading, setLoading] = useState(false);

  const handleUpload = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setSelectedFile(file);
    setFileName(file.name);
    setCaption("");
    const reader = new FileReader();
    reader.onload = (ev) => setImage(ev.target?.result as string);
    reader.readAsDataURL(file);
  }, []);

  const handleGenerate = useCallback(async () => {
    if (!image) return;
    setLoading(true);
    try {
      if (!selectedFile) throw new Error("No file selected");

      const formData = new FormData();
      formData.append('image', selectedFile);

      const response = await fetch('http://localhost:5000/predict_caption', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error("Failed to generate caption");
      
      const data = await response.json();
      setCaption(data.caption);
    } catch (error) {
      console.error(error);
      setCaption("Failed to generate caption. Please ensure backend is running.");
    } finally {
      setLoading(false);
    }
  }, [image]);

  return (
    <div className="container py-12 max-w-2xl space-y-8">
      <div className="text-center space-y-2">
        <h1 className="text-3xl font-bold">Image Caption Generator</h1>
        <p className="text-muted-foreground">
          Upload an image and generate an AI-powered caption
        </p>
      </div>

      {/* Upload area */}
      <Card className="p-0 overflow-hidden">
        {image ? (
          <div className="relative">
            <img src={image} alt={fileName} className="w-full max-h-96 object-contain bg-muted" />
            <button
              onClick={() => { setImage(null); setCaption(""); setFileName(""); setSelectedFile(null); }}
              className="absolute top-3 right-3 bg-card/80 backdrop-blur-sm rounded-full px-3 py-1 text-xs font-medium hover:bg-card transition-colors"
            >
              Change
            </button>
          </div>
        ) : (
          <label className="flex flex-col items-center justify-center h-64 cursor-pointer hover:bg-muted/50 transition-colors">
            <div className="p-4 rounded-full bg-secondary mb-4">
              <ImageIcon className="h-8 w-8 text-muted-foreground" />
            </div>
            <p className="font-medium">Click to upload an image</p>
            <p className="text-sm text-muted-foreground mt-1">JPG, PNG, WEBP supported</p>
            <input
              type="file"
              accept="image/*"
              className="hidden"
              onChange={handleUpload}
            />
          </label>
        )}
      </Card>

      {/* Generate button */}
      {image && (
        <Button
          onClick={handleGenerate}
          disabled={loading}
          className="w-full gradient-bg border-0"
          size="lg"
        >
          {loading ? (
            <>
              <Loader2 className="h-5 w-5 mr-2 animate-spin" />
              Generating Caption...
            </>
          ) : (
            <>
              <Sparkles className="h-5 w-5 mr-2" />
              Generate Caption
            </>
          )}
        </Button>
      )}

      {/* Caption result */}
      {caption && (
        <Card className="p-6 animate-fade-in border-primary/20 bg-primary/5">
          <p className="text-sm font-medium text-primary mb-2 flex items-center gap-2">
            <Sparkles className="h-4 w-4" /> Generated Caption
          </p>
          <p className="text-lg font-medium">{caption}</p>
        </Card>
      )}
    </div>
  );
};

export default CaptionPage;
