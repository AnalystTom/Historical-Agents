import { Menu, X } from "lucide-react";
import { useState } from "react";
import logo from "../assets/logo.png";
import { navItems } from "../constants";
import { getButtonClass } from "./Button";
import { Link } from "react-router-dom";

const Navbar = () => {
  const [mobileDrawerOpen, setMobileDrawerOpen] = useState(false);

  const toggleNavbar = () => {
    setMobileDrawerOpen(!mobileDrawerOpen);
  };

  return (
    <nav className="sticky top-0 z-50 py-3 backdrop-blur-lg border-b border-neutral-700/80">
      <div className="container px-4 mx-auto relative lg:text-sm">
        <div className="flex justify-between items-center">
          <div className="flex items-center flex-shrink-0">
            <Link to="/" className="flex items-center">
              <img className="h-10 w-10 mr-2" src={logo} alt="Logo" />
              <span className="text-xl font-bold tracking-tight">HistAgents</span>
            </Link>
          </div>

          <ul className="hidden lg:flex ml-14 space-x-12">
            {navItems.map((item, index) => (
              <li key={index} className="relative group">
                <a href={item.href}>{item.label}</a>
                <span className="absolute bottom-0 left-0 w-0 h-[2px] bg-orange-600 transition-all duration-300 group-hover:w-full"></span>
              </li>
            ))}
          </ul>

          <div className="hidden lg:flex justify-center space-x-6 items-center">
            <Link to="/login" className={getButtonClass("default")}>
              Sign In
            </Link>
            <Link to="/register" className={getButtonClass("gradient")}>
              Create an account
            </Link>
          </div>

          <div className="lg:hidden md:flex flex-col justify-end">
            <button onClick={toggleNavbar}>{mobileDrawerOpen ? <X /> : <Menu />}</button>
          </div>
        </div>
        {mobileDrawerOpen && (
          <div className="fixed right-0 z-20 bg-neutral-900 w-full p-12 flex flex-col justify-center items-center lg:hidden">
            <ul>
              {navItems.map((item, index) => (
                <li key={index} className="py-4">
                  <a href={item.href}>{item.label}</a>
                </li>
              ))}
            </ul>
            <div className="flex space-x-6">
              <Link to="/login" className="py-2 px-3 border rounded-md">
                Sign In
              </Link>
              <Link to="/register" className="py-2 px-3 rounded-md bg-gradient-to-r from-orange-500 to-orange-800">
                Create an account
              </Link>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
