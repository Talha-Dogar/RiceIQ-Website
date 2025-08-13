import React from 'react';

const LandscapeImage = () => {
  return (
    <div className="flex justify-center items-center">
      <div className="relative w-4/5 h-2/5">
        <img
          src="/images/rice9.png" 
          alt="Landscape"
          className="object-cover w-full h-full rounded-lg shadow-lg"
        />
      </div>
    </div>
  );
};

export default LandscapeImage;
