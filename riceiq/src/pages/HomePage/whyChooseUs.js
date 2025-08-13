import React from "react";

const WhyChooseUs = () => {
  return (
    <section className="bg-gradient-to-b from-gray-100 to-white  py-16">
      <div className="max-w-7xl mx-auto px-6 lg:px-8">
        {/* Landscape Image */}
        <div className="mb-12">
          <img 
            src="/images/rice8.png" 
            alt="Why Choose Us" 
            className="w-full  h-[23rem] object-cover rounded-lg shadow-md"
          />
        </div>

        {/* Headline */}
        <h2 className="text-4xl font-extrabold text-center text-green-800 mb-12">
          Why Choose Us?
        </h2>
        
        {/* Features Grid */}
        <div className="grid md:grid-cols-3 gap-10">
          {[
            {
              title: "Cutting-Edge Technology",
              description: "AI-driven analysis for unmatched accuracy.",
              icon: "🤖",
            },
            {
              title: "User-Centric Design",
              description: "Intuitive interface for seamless experience.",
              icon: "✨",
            },
            {
              title: "Portablity",
              description: "You can run analysis or view previous records from anywhere",
              icon: "🌍",
            },
            {
              title: "Time-Saving",
              description:
                "Effortlessly process analyses within seconds, boosting productivity.",
              icon: "⏱️",
            },
            {
              title: "Cost Efficiency",
              description:
                "Reduce operational costs while maintaining high-quality standards.",
              icon: "💰",
            },
          ].map((item) => (
            <div
              key={item.title}
              className="bg-white shadow-lg rounded-lg p-6 text-center hover:shadow-xl transition-shadow duration-300"
            >
              <div className="w-16 h-16 bg-green-100 text-white rounded-full flex items-center justify-center mx-auto mb-6 text-3xl">
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

export default WhyChooseUs;
