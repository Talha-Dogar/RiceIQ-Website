import React from "react";
import { FaLinkedin, FaFacebook } from "react-icons/fa";
import { FaXTwitter } from "react-icons/fa6";
import { scrollToFeatures } from "../scrollToSections/scroll";
import { scrollToContact } from "../scrollToContact/scrollContact";
import { scrollToHome } from "../scrollToHome/scrollHome";
import { useNavigate } from "react-router-dom";
const Footer = () => {
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
      };
  return (
    <footer className="bg-teal-50 text-black py-8">
      <div className="max-w-7xl mx-auto px-6 lg:px-8">
        <div className="grid md:grid-cols-3 gap-8">
          {/* Logo Section */}
          <div className="flex flex-col items-center md:items-start font-semibold text-2xl">
            {/* <img
              src="images/logo.png"
              alt="Logo"
              className="h-12 mb-4"
            /> */}
            RiceIQ
            <p className="text-sm text-gray-800">
              Delivering solutions with excellence and innovation.
            </p>
          </div>

          {/* Navigation Links */}
          <div className="flex flex-col items-center md:items-start">
            <h3 className="text-lg font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li>
              <button onClick={handleClickHome} className="hover:text-teal-400">
            
            Home
            
            </button>
              </li>
              <li>
                <button onClick={handleClickFeatures} className="hover:text-teal-400">
            
                Features
                
                </button>
              </li>
              <li>
              <button onClick={handleClickContact} className="hover:text-teal-400">
            
            Contact
            
            </button>
              </li>
            
            </ul>
          </div>

          {/* Copyright Section */}
          <div className="flex flex-col items-center md:items-start">
            <h3 className="text-lg font-semibold mb-4">Follow Us</h3>
            <div className="flex space-x-4 mb-4">
              <a href="https://facebook.com" target="_blank" rel="noreferrer">
              <FaFacebook className="w-6 h-6 text-blue-600" />
              </a>
              <a href="https://twitter.com" target="_blank" rel="noreferrer">
               <FaXTwitter className="w-6 h-6 text-blue-400" />
              </a>
              <a href="https://linkedin.com" target="_blank" rel="noreferrer">
              <FaLinkedin className="w-6 h-6 text-blue-800" />
              </a>
            </div>
            <p className="text-sm text-gray-400">
              © {new Date().getFullYear()} GrainIQ. All Rights Reserved.
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
