import React from 'react';
import { Card } from './ui/card';
import { Button } from './ui/button';

const examples = [
  {
    title: "Document Analysis",
    prompt: "Analyze this technical documentation and explain the key concepts.",
    description: "Upload technical documents and get instant analysis and explanations.",
    steps: [
      "Click 'Upload Document' button",
      "Select your technical documentation file",
      "Wait for processing to complete",
      "Ask questions about the content"
    ]
  },
  {
    title: "Code Understanding",
    prompt: "Explain how this code works and suggest improvements.",
    description: "Get detailed explanations of code snippets and improvement suggestions.",
    steps: [
      "Upload your code file",
      "Ask specific questions about the code",
      "Get explanations and suggestions",
      "Implement recommended improvements"
    ]
  },
  {
    title: "API Documentation",
    prompt: "Summarize the main endpoints and their usage in this API doc.",
    description: "Quickly understand API documentation and get usage examples.",
    steps: [
      "Upload API documentation",
      "Ask about specific endpoints",
      "Get example requests and responses",
      "Understand authentication methods"
    ]
  },
  {
    title: "Error Analysis",
    prompt: "What's causing this error in my logs and how can I fix it?",
    description: "Debug issues faster with intelligent error analysis.",
    steps: [
      "Upload error logs",
      "Ask about specific errors",
      "Get root cause analysis",
      "Receive fix suggestions"
    ]
  }
];

const features = [
  {
    title: "Real-time Processing",
    description: "Documents are processed instantly using advanced AI algorithms.",
    icon: "⚡"
  },
  {
    title: "Multi-format Support",
    description: "Support for PDF, Markdown, code files, and more.",
    icon: "📄"
  },
  {
    title: "Intelligent Responses",
    description: "Get context-aware answers to your questions.",
    icon: "🤖"
  },
  {
    title: "Code Integration",
    description: "Seamless integration with your development workflow.",
    icon: "💻"
  }
];

export function HowToUse() {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold mb-4">How to Use DocuBot AI</h1>
        <p className="text-xl text-gray-600">
          Get started with intelligent document processing and analysis
        </p>
      </div>

      <div className="grid md:grid-cols-2 gap-8 mb-12">
        {features.map((feature, index) => (
          <Card key={index} className="p-6 hover:shadow-lg transition-shadow">
            <div className="text-4xl mb-4">{feature.icon}</div>
            <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
            <p className="text-gray-600">{feature.description}</p>
          </Card>
        ))}
      </div>

      <h2 className="text-3xl font-bold mb-8 text-center">Example Use Cases</h2>
      
      <div className="grid md:grid-cols-2 gap-8">
        {examples.map((example, index) => (
          <Card key={index} className="p-6">
            <h3 className="text-xl font-semibold mb-4">{example.title}</h3>
            <div className="bg-gray-100 p-4 rounded-md mb-4">
              <p className="text-gray-700 italic">"{example.prompt}"</p>
            </div>
            <p className="text-gray-600 mb-4">{example.description}</p>
            <div className="space-y-2">
              {example.steps.map((step, stepIndex) => (
                <div key={stepIndex} className="flex items-center">
                  <span className="w-6 h-6 rounded-full bg-blue-500 text-white flex items-center justify-center mr-2 text-sm">
                    {stepIndex + 1}
                  </span>
                  <span>{step}</span>
                </div>
              ))}
            </div>
          </Card>
        ))}
      </div>

      <div className="text-center mt-12">
        <h2 className="text-3xl font-bold mb-4">Ready to Get Started?</h2>
        <p className="text-xl text-gray-600 mb-8">
          Try DocuBot AI with your documents now
        </p>
        <Button
          size="lg"
          className="bg-blue-500 hover:bg-blue-600 text-white px-8"
          onClick={() => window.location.href = '/'}
        >
          Start Processing
        </Button>
      </div>
    </div>
  );
}