import React from 'react';

const Button = ({
  children,
  onClick,
  type = 'button',
  className = '',
  variant = 'primary', // Define variants: 'primary', 'secondary', etc.
  size = 'medium', // Define sizes: 'small', 'medium', 'large'
  ...props
}) => {
  // Define base styles
  const baseStyles = `
    inline-flex items-center justify-center rounded-[12px] 
    font-medium transition-colors duration-200
  `;

  // Define variant styles
  const variantStyles = {
    primary: 'bg-[var(--darkBlue)] font-[Mada] font-semiBold rounded-[12px] text-white hover:bg-blue-700',
    // secondary: 'bg-gray-600 text-white hover:bg-gray-700',
    // outline: 'border border-blue-600 text-blue-600 hover:bg-blue-600 hover:text-white',
  };

  // Define size styles
  const sizeStyles = {
    small: 'px-3 py-1.5 text-sm',
    medium: 'px-8 py-2 text-md',
    large: 'px-5 py-3 text-lg',
  };

  // Combine styles
  const combinedStyles = `${baseStyles} ${variantStyles[variant]} ${sizeStyles[size]} ${className}`;

  return (
    <button
      type={type}
      onClick={onClick}
      className={combinedStyles}
      {...props}
    >
      {children}
    </button>
  );
};

export default Button;
