import React from 'react';

const ImageUploadIcon = () => {
  return (
    <svg
      width="22"
      height="22"
      viewBox="0 0 24 24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      {/* Icon Outline */}
      <rect
        x="4"
        y="4"
        width="20"
        height="20"
        rx="4"
        stroke="#F1F1F1"
        strokeWidth="2"
      />
      {/* Upload Arrow */}
      <path
        d="M12 16V10"
        stroke="#F1F1F1"
        strokeWidth="3"
        strokeLinecap="round"
      />
      <path
        d="M9 13L12 10L15 13"
        stroke="#F1F1F1"
        strokeWidth="3"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
};

export default ImageUploadIcon;
