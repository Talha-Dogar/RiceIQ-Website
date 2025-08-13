import React from "react";
import { scrollToFeatures } from "../../components/scrollToSections/scroll";
import { scrollToContact } from "../../components/scrollToContact/scrollContact";
import { scrollToHome } from "../../components/scrollToHome/scrollHome";
import { useNavigate } from "react-router-dom";
const Navbar = () => {
    const navigate = useNavigate();
    const handleClickFeatures = () => {
        navigate("/");
        scrollToFeatures();
      };
      const handleClickContact = () => {
        navigate("/");
        scrollToContact();
      };
      const handleClickHome = () => {
        navigate("/");
        scrollToHome();
      }
  return (
    <nav className="bg-white shadow-md">
      <div className="container mx-auto px-6 py-4 flex justify-between items-center">
        {/* Logo Section */}
        <div className="text-2xl font-bold text-green-800">
          Rice<span className="text-green-600">IQ</span>
        </div>

        {/* Navigation Links */}
        <ul className="flex space-x-8 text-gray-700 font-medium">
          <li className="hover:text-green-700 transition duration-300">
            <button onClick={handleClickHome}>
              Home
            </button>
          </li>
          <li className="hover:text-green-700 transition duration-300">
            <button onClick={handleClickFeatures}>
              Features
            </button>
          </li>
          <li className="hover:text-green-700 transition duration-300">
            <button onClick={handleClickContact}>
              Contact
            </button>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
