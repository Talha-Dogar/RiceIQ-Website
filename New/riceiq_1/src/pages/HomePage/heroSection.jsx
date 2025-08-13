import React from "react";
import { Link } from "react-router-dom";
const HeroSection = () => {
  return (
    <div id ="home"  className= "bg-gradient-to-r from-green-200 via-green-100 to-green-50 py-20 px-6">
      <div className="container mx-auto flex flex-col lg:flex-row items-center">
        {/* Left Section: Text Content */}
        <div className="lg:w-1/2 text-left">
          <h1 className="text-4xl lg:text-5xl font-bold text-green-800 leading-tight">
            Ensure Pure Rice with Our AI Solution
          </h1>
          <p className="mt-6 text-lg text-gray-700">
            Introducing our cutting-edge AI tool designed specifically for exporters to detect rice adulteration and identify varieties with precision. Protect your business and uphold quality standards effortlessly.
          </p>
            <Link to="/analysis_selection">
                <button className="mt-8 bg-green-700 hover:bg-green-800 text-white font-semibold py-3 px-6 rounded-lg shadow-md transition duration-300">
                Try Now
                </button>
                </Link>
        </div>

        {/* Right Section: Image */}
        <div className="lg:w-1/2 mt-10 lg:mt-0 flex justify-center">
          <img
            src="/images/rice7.png" // Replace with your rice-related image URL
            alt="Rice Adulteration Detection"
            className="rounded-lg shadow-lg w-full h-full"
          />
        </div>
      </div>
    </div>
  );
};

export default HeroSection;
