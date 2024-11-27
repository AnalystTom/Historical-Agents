export const getButtonClass = (variant = "default") => {
  const baseStyles = "py-2 px-3 rounded-md transition duration-300 ease-in-out transform hover:scale-105";

  const variants = {
    default: `${baseStyles} border border-white text-white hover:border-orange-500 hover:bg-gradient-to-r from-orange-200 to-orange-500 hover:text-transparent bg-clip-text`,
    gradient: `${baseStyles} bg-gradient-to-r from-orange-500 to-orange-800 text-white hover:from-orange-600 hover:to-orange-900 hover:shadow-lg`,
  };

  return variants[variant];
};
