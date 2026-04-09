import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Image, Brain, ArrowRight } from "lucide-react";

const HomePage = () => {
  return (
    <div className="container py-16 space-y-20">
      {/* Hero */}
      <section className="text-center space-y-6 animate-fade-in max-w-3xl mx-auto">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-secondary text-sm font-medium text-secondary-foreground">
          <Brain className="h-4 w-4" />
          Deep Learning Project
        </div>
        <h1 className="text-4xl md:text-5xl font-bold leading-tight">
          AI-Powered <span className="gradient-text">Image Caption Generator</span>
        </h1>
        <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
          Automatically generate descriptive and meaningful captions for your images 
          using state-of-the-art Deep Learning models (CNN + LSTM).
        </p>
        <div className="flex flex-wrap justify-center gap-4 pt-4">
          <Button asChild size="lg" className="gradient-bg border-0 px-8">
            <Link to="/caption">
              <Image className="h-5 w-5 mr-2" />
              Caption an Image
            </Link>
          </Button>
        </div>
      </section>

      {/* Features */}
      <section className="grid md:grid-cols-3 gap-6">
        {[
          {
            icon: Image,
            title: "Image Captioning",
            desc: "Upload any image and get an AI-generated description using a CNN-LSTM model.",
          },
          {
            icon: Brain,
            title: "Smart AI",
            desc: "Understand the context and content of your photos with high precision.",
          },
          {
            icon: Brain,
            title: "Deep Learning",
            desc: "Powered by Convolutional Neural Networks and Long Short-Term Memory architecture.",
          },
        ].map((f) => (
          <div
            key={f.title}
            className="group p-6 rounded-xl bg-card border hover:shadow-lg transition-all duration-300 hover:-translate-y-1"
          >
            <div className="p-3 rounded-lg gradient-bg w-fit mb-4">
              <f.icon className="h-6 w-6 text-primary-foreground" />
            </div>
            <h3 className="font-semibold text-lg mb-2">{f.title}</h3>
            <p className="text-muted-foreground text-sm">{f.desc}</p>
          </div>
        ))}
      </section>

      {/* CTA */}
      <section className="text-center py-12 rounded-2xl gradient-bg text-primary-foreground">
        <h2 className="text-2xl font-bold mb-3">Ready to try it?</h2>
        <p className="mb-6 opacity-90">Upload an image and see the magic.</p>
        <Button asChild variant="secondary" size="lg">
          <Link to="/caption">
            Get Started <ArrowRight className="h-4 w-4 ml-2" />
          </Link>
        </Button>
      </section>
    </div>
  );
};

export default HomePage;
