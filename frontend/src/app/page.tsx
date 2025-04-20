import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import Image from "next/image";
import { Footer } from "@/components/footer/footer";
import { FEATURES, TESTIMONIALS } from "@/constants";
import { CheckCircle } from "lucide-react";

export default function Home() {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-primary/10 to-secondary/10 py-16 md:py-24">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row items-center gap-8">
            <div className="md:w-1/2 space-y-6 animate-fade-in">
              <Badge variant="secondary" className="text-sm">
                Next-Gen Learning Platform
              </Badge>
              <h1 className="text-4xl md:text-6xl font-bold tracking-tight">
                Streamline Education with Smart Management
              </h1>
              <p className="text-xl text-muted-foreground">
                Integrated LMS and attendance system for modern educational institutions.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 w-full max-w-md">
                <Input placeholder="Enter your email" />
                <Button size="lg" className="hover:scale-105 transition-transform">
                  Get Started
                </Button>
              </div>
            </div>
            <div className="md:w-1/2">
              <Image
                src="/Images/hero.jpeg"
                alt="Platform Preview"
                width={1000}
                height={400}
                className="rounded-lg shadow-2xl border-2 border-primary/10 hover:shadow-3xl transition-shadow w-full object-cover"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-16 md:py-24">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12 animate-fade-in">
            Key Features
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            {FEATURES.map((feature) => (
              <Card
                key={feature.title}
                className="hover:shadow-lg transition-shadow border border-muted hover:border-primary/20"
              >
                <CardHeader className="items-center">
                  <feature.icon className="w-12 h-12 mb-4 bg-gradient-to-r from-primary to-secondary text-transparent bg-clip-text" />
                  <h3 className="text-2xl font-semibold">{feature.title}</h3>
                </CardHeader>
                <CardContent className="text-center">
                  <p className="text-muted-foreground">{feature.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="bg-muted/50 py-16 md:py-24">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12 animate-fade-in">
            Trusted by Educators
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            {TESTIMONIALS.map((testimonial) => (
              <Card
                key={testimonial.author}
                className="p-6 border border-muted hover:border-primary/20 hover:shadow-lg transition-shadow"
              >
                <CardContent className="flex flex-col items-center text-center">
                  <Avatar className="w-16 h-16 mb-4">
                    <AvatarImage src={testimonial.avatar} />
                    <AvatarFallback>{testimonial.author[0]}</AvatarFallback>
                  </Avatar>
                  <blockquote className="text-lg italic mb-4">
                    {testimonial.text}
                  </blockquote>
                  <div className="font-medium">{testimonial.author}</div>
                  <div className="text-sm text-muted-foreground">{testimonial.role}</div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section
        className="bg-primary text-primary-foreground py-16 md:py-24 bg-fixed bg-cover bg-center"
      >
        <div className="container mx-auto px-4 text-center">
          <div className="max-w-3xl mx-auto space-y-6 animate-fade-in">
            <CheckCircle className="w-16 h-16 mx-auto" />
            <h2 className="text-3xl md:text-4xl font-bold">
              Ready to Transform Your Institution?
            </h2>
            <p className="text-lg text-primary-foreground/90">
              Join hundreds of educational organizations using our platform
            </p>
            <Button
              variant="secondary"
              className="mt-6 cursor-pointer"
              size="lg"
            >
              Start Free Trial
            </Button>
          </div>
        </div>
      </section>
      <Footer />
    </div>
  );
}

