import React from "react";
import { useState } from "react";
import { Link } from "react-router-dom";
import { ChevronLeftIcon, ChevronRightIcon } from "@heroicons/react/24/outline";

import DashboardIcon from "../../assets/DashboardIcon";
import SettingsIcon from "../../assets/SettingsIcon";
import ImageUploadIcon from "../../assets/ImageUploadIcon";
export const Sidebar = ({ isOpen, toggleSidebar }) => {
  const [toggleBtnClick, settoggleBtnClcik] = useState(false);
    const menuItems = [
      { icon: <DashboardIcon className="w-6 h-6" />, label: 'Dashboard', link: '#' },
      { icon: <ImageUploadIcon className="w-6 h-6" />, label: 'Image Upload', link: '/upload' },
      { icon: <DashboardIcon className="w-6 h-6" />, label: 'Records', link: '/expandable-table' },
      { icon: <SettingsIcon className="w-6 h-6" />, label: 'Settings', link: '#' },
    ];
  // const menuItems = [
  //   { icon: <DashboardIcon className="w-6 h-6" />, label: "Dashboard" },
  //   { icon: <ImageUploadIcon className="w-6 h-6" />, label: "Image Upload" },
  //   { icon: <DashboardIcon className="w-6 h-6" />, label: "Records" },
  //   { icon: <SettingsIcon className="w-6 h-6" />, label: "Settings" },
  // ];

  // const handleMouseEnter = () => {
  //   if (!isOpen && !toggleBtnClick) toggleSidebar(true);
  // };

  // const handleMouseLeave = () => {
  //   if (isOpen) toggleSidebar(false);
  //   settoggleBtnClcik(false);
  // };

  return (
    <aside
      className={` bg-[var(--darkgreenblue)] text-white transition-all duration-300 ease-in-out ${
        isOpen ? "w-64" : "w-20"
      } min-h-screen`}
      // onMouseEnter={handleMouseEnter}
      // onMouseLeave={handleMouseLeave}
    >
      <div className="mt-[63.5px] p-4 flex items-center justify-between">
        <h2
          className={`flex justify-center align-middle text-[14px] font-bold font-[Lexend Mega] ${
            isOpen ? "block" : "hidden"
          }`}
          style={{ fontFamily: "Lexend Mega" }}
        >
          {/* <span className="mr-2 justify-center mt-0">
            <Logo />
          </span>{" "} */}
          RiceIQ
        </h2>
        <button
          onClick={() => {
            toggleSidebar(!isOpen);
            settoggleBtnClcik(true);
          }}
          className={`text-gray-700 bg-teal-300 translate-y-10 ${
            isOpen ? "translate-x-6 delay-0.5" : "translate-x-12 delay-0.5"
          } rounded-[16px]`}
        >
          {isOpen ? (
            <ChevronLeftIcon className="w-6 h-6" />
          ) : (
            <ChevronRightIcon className="w-6 h-6" />
          )}
        </button>
      </div>
      <nav  className="mt-[47.5px] flex flex-col align-middle gap-12  p-4 hover:cursor-pointer">
        {menuItems.map((item, index) => (
          <Link key={index} to={item.link}>
             <div key={index} className="flex items-center">
            {item.icon}
            <span className={`ml-4 ${isOpen ? 'block' : 'hidden'}`}>{item.label}

            </span>
            </div>
          </Link>
        ))}
      </nav>
      {/* <nav className="mt-[47.5px] flex flex-col align-middle gap-12  p-4 hover:cursor-pointer">
        {menuItems.map((item, index) => (
          <div key={index} className="flex items-center">
            {item.icon}
            <span className={`ml-4 ${isOpen ? "block" : "hidden"}`}>
              {item.label}
            </span>
          </div>
        ))}
      </nav> */}
    </aside>
  );
};
