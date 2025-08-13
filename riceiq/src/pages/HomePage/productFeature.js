import React from "react";
import {
  AcademicCapIcon,
  ShieldCheckIcon,
  ClockIcon,
  AdjustmentsHorizontalIcon,
} from "@heroicons/react/24/outline"; // Ensure you have Heroicons installed

const ProductFeatureSection = () => {
  return (
    <div className="bg-gradient-to-r from-white via-green-50 to-green-100 py-20 px-6" id="features">
      <div className="container mx-auto flex flex-col lg:flex-row items-center">
        {/* Left Section: Image */}
        <img
          src="/images/rice4.png"
          alt="Rice Adulteration and Identification"
          className="lg:w-1/2 w-full rounded-lg shadow-lg border-4"
        />

        {/* Right Section: Features */}
        <div className="lg:w-1/2 text-left lg:ml-10 mt-10 lg:mt-0">
          <h2 className="text-4xl font-bold text-green-800 leading-tight">
            What is RiceIQ?
          </h2>
          <p className="mt-6 text-lg text-gray-700">
            Our AI tool accurately identifies different Pakistani rice varieties, ensuring
            quality and authenticity. Exporters can trust our technology to
            detect adulteration and enhance their product integrity.
          </p>
          <div className="mt-10 space-y-6">
            {/* Feature 1 */}
            <div className="flex items-start space-x-4">
              <div className="w-12 h-12 bg-green-200 text-green-800 flex items-center justify-center rounded-lg shadow-md">
                <AcademicCapIcon className="w-6 h-6" />
              </div>
              <div>
                <h3 className="text-xl font-semibold text-green-800">
                  Variety Identification
                </h3>
                <p className="text-gray-600">
                  Identify rice types swiftly to meet market demands and standards.
                </p>
              </div>
            </div>

            {/* Feature 2 */}
            <div className="flex items-start space-x-4">
              <div className="w-12 h-12 bg-green-200 text-green-800 flex items-center justify-center rounded-lg shadow-md">
                <ShieldCheckIcon className="w-6 h-6" />
              </div>
              <div>
                <h3 className="text-xl font-semibold text-green-800">
                  Adulteration Detection
                </h3>
                <p className="text-gray-600">
                  Ensure product authenticity and compliance with international export regulations.
                </p>
              </div>
            </div>

            {/* Feature 3 */}
            <div className="flex items-start space-x-4">
              <div className="w-12 h-12 bg-green-200 text-green-800 flex items-center justify-center rounded-lg shadow-md">
                <ClockIcon className="w-6 h-6" />
              </div>
              <div>
                <h3 className="text-xl font-semibold text-green-800">
                  Analysis History
                </h3>
                <p className="text-gray-600">
                  Access and manage your past analyses for better record-keeping.
                </p>
              </div>
            </div>

            {/* Feature 4 */}
            <div className="flex items-start space-x-4">
              <div className="w-12 h-12 bg-green-200 text-green-800 flex items-center justify-center rounded-lg shadow-md">
                <AdjustmentsHorizontalIcon className="w-6 h-6" />
              </div>
              <div>
                <h3 className="text-xl font-semibold text-green-800">
                  User-Friendly Dashboard
                </h3>
                <p className="text-gray-600">
                  Intuitive design to streamline your quality assurance process.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductFeatureSection;
