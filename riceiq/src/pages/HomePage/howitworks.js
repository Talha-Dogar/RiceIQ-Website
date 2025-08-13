import React from "react";

const HowItWorks = () => {
  return (
    <section className="bg-green-50">
      <div className="max-w-7xl mx-auto px-6 lg:px-8">
        <h2 className="text-4xl font-extrabold text-center text-green-800 mb-12">
          How It Works
        </h2>
        <div className="grid md:grid-cols-4 gap-8">
          {[
            {
              step: 1,
              title: "Upload an Image",
              description: "Take a clear photo or scan of the rice sample.",
              icon: "📸",
            },
            {
              step: 2,
              title: "Run Analysis",
              description:
                "Execute analysis on images leveraging AI technology.",
              icon: "⚙️",
            },
            {
              step: 3,
              title: "Get Instant Results",
              description:
                "Receive detailed insights about the rice grains.",
              icon: "📊",
            },
            {
              step: 4,
              title: "Export & Save",
              description:
                "Download the report or save it to your dashboard.",
              icon: "💾",
            },
          ].map((item) => (
            <div
              key={item.step}
              className="bg-white shadow-lg rounded-lg p-6 text-center transition-transform hover:scale-105"
            >
              <div className="w-16 h-16 bg-green-200 text-white rounded-full flex items-center justify-center mx-auto mb-6 text-3xl">
                {item.icon}
              </div>
              <h3 className="text-xl font-semibold text-gray-800 mb-2">
                {item.title}
              </h3>
              <p className="text-gray-600">{item.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default HowItWorks;
