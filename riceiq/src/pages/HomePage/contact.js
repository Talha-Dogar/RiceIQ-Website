import React from "react";

const Contact = () => {
  return (
    <section id ="contact" className="bg-[var(--darkgreenblue)] py-16">
      <div className="max-w-7xl mx-auto px-6 lg:px-8">
        <div className="grid lg:grid-cols-2 h-[600px]">
          {/* Contact Form */}
          <div className="bg-white text-gray-900 shadow-lg pl-8 pr-8 h-[40rem]  flex flex-col justify-center">
            <h2 className="text-3xl pt-6 font-extrabold mb-6 text-teal-800">
              Contact Us
            </h2>
            <form className="flex-grow">
              {/* Name Field */}
              <div className="mb-4">
                <label htmlFor="name" className="block text-sm font-medium mb-2">
                  Name
                </label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring focus:ring-teal-400"
                  placeholder="Your Name"
                />
              </div>

              {/* Email Field */}
              <div className="mb-4">
                <label htmlFor="email" className="block text-sm font-medium mb-2">
                  Email
                </label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring focus:ring-teal-400"
                  placeholder="Your Email"
                />
              </div>

              {/* Message Field */}
              <div className="mb-4">
                <label htmlFor="message" className="block text-sm font-medium mb-2">
                  Message
                </label>
                <textarea
                  id="message"
                  name="message"
                  rows="5"
                  className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring focus:ring-teal-400"
                  placeholder="Your Message"
                ></textarea>
              </div>

              {/* Submit Button */}
              <button
                type="submit"
                className="w-full bg-teal-700 text-white py-2 px-4 rounded-lg font-semibold hover:bg-teal-800 transition-colors"
              >
                Send Message
              </button>
            </form>
          </div>

          {/* Image */}
          <div className="flex items-center justify-center h-full">
            <img
              src="images/rice2.png"
              alt="Contact Us"
              className=" shadow-lg object-cover w-full h-[40rem]"
            />
          </div>
        </div>
      </div>
    </section>
  );
};

export default Contact;
