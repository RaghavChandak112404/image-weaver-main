import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Brain, Layers, Database, Globe, Code2, Cpu } from "lucide-react";

const techs = [
  { icon: Brain, name: "CNN", desc: "Convolutional Neural Network for image feature extraction (VGG16/ResNet)" },
  { icon: Layers, name: "LSTM", desc: "Long Short-Term Memory for sequence-based caption generation" },
  { icon: Globe, name: "Flask", desc: "Python web framework for serving the model as REST API endpoints" },
  { icon: Code2, name: "React", desc: "Modern frontend framework for building the interactive user interface" },
  { icon: Database, name: "Flickr8k", desc: "Dataset of 8,000 images with 5 captions each, used for training" },
  { icon: Cpu, name: "TensorFlow", desc: "Deep learning framework used for building and training the model" },
];

const AboutPage = () => {
  return (
    <div className="container py-12 max-w-3xl space-y-10">
      <div className="text-center space-y-2">
        <h1 className="text-3xl font-bold">About the Project</h1>
        <Badge variant="secondary" className="text-sm">Deep Learning — Final Year Project</Badge>
      </div>

      {/* Overview */}
      <Card className="p-6 space-y-4">
        <h2 className="text-xl font-semibold">Project Overview</h2>
        <p className="text-muted-foreground leading-relaxed">
          This project implements an <strong className="text-foreground">Image Caption Generator</strong> using
          an encoder-decoder architecture. A pre-trained CNN (VGG16) extracts visual features from input images,
          which are then fed into an LSTM network to generate natural language descriptions.
        </p>
        <p className="text-muted-foreground leading-relaxed">
          Additionally, the system includes a <strong className="text-foreground">Document Figure Caption Automation</strong> module
          that extracts images embedded in PDF and Word documents, processes them through the captioning
          pipeline, and outputs labeled captions (Figure 1, Figure 2, etc.).
        </p>
      </Card>

      {/* Architecture */}
      <Card className="p-6 space-y-4">
        <h2 className="text-xl font-semibold">How It Works</h2>
        <div className="flex flex-wrap items-center justify-center gap-3 py-4">
          {["Input Image", "→", "CNN (Feature Extraction)", "→", "LSTM (Caption Generation)", "→", "Output Caption"].map(
            (step, i) =>
              step === "→" ? (
                <span key={i} className="text-muted-foreground text-xl">→</span>
              ) : (
                <Badge key={i} variant="outline" className="px-3 py-2 text-sm">
                  {step}
                </Badge>
              )
          )}
        </div>
      </Card>

      {/* Technologies */}
      <div>
        <h2 className="text-xl font-semibold mb-4">Technologies Used</h2>
        <div className="grid sm:grid-cols-2 gap-4">
          {techs.map((t) => (
            <Card key={t.name} className="p-4 flex items-start gap-3">
              <div className="p-2 rounded-lg bg-secondary shrink-0">
                <t.icon className="h-5 w-5 text-primary" />
              </div>
              <div>
                <p className="font-semibold">{t.name}</p>
                <p className="text-sm text-muted-foreground">{t.desc}</p>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AboutPage;
