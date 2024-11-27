import { getButtonClass } from "./Button";

const HeroSection = () => {
  return (
    <div className="flex flex-col items-center mt-6 lg:mt-20">
      <h1 className="text-4xl sm:text-6xl lg:text-7xl text-center tracking-wide">
      Engaging in debates
        <span className="bg-gradient-to-r from-orange-500 to-orange-800 text-transparent bg-clip-text"> across time and perspectives with AI.</span>
      </h1>
      <p className="mt-10 text-lg text-center text-neutral-500 max-w-4xl">
        Step into a world where AI brings historical debates to life. Moderate discussions between virtual figures or directly engage with AI-powered
        personas on topics that matter.
      </p>
      <div className="flex justify-center my-10 space-x-6">
        <a href="#" className={getButtonClass("default")}>
          Start for free
        </a>
        <a href="#" className={getButtonClass("gradient")}>
          Learn More
        </a>
      </div>
    </div>
  );
};

export default HeroSection;
