import logo from "../assets/logo.png";
import { getButtonClass } from "../components/Button";
import { Link } from "react-router-dom";

const Register = () => {
  return (
    <div>
      <div className="flex min-h-full flex-col justify-center px-6 py-12 lg:px-8">
        <div className="sm:mx-auto sm:w-full sm:max-w-sm">
          <img className="mx-auto h-20 w-auto" src={logo} alt="Your Company"></img>
          <h2 className="mt-10 text-center text-2xl font-bold leading-9 tracking-tight to-blue-500">Create a new account</h2>
        </div>

        <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
          <form className="space-y-6" action="#" method="POST">
            <div>
              <label htmlFor="email" className="block text-sm font-medium leading-6 text-balance">
                Email address
              </label>
              <div className="mt-2">
                <input
                  id="email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  className="block w-full rounded-md border-0 bg-white/5 py-1.5 text-cyan-600 shadow-sm ring-1 ring-inset ring-orange-500 focus:ring-2 focus:ring-inset focus:ring-balck sm:text-sm sm:leading-6"></input>
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between">
                <label htmlFor="password" className="block text-sm font-medium leading-6 text-balance">
                  Password
                </label>
                {/* <div className="text-sm">
            <a href="#" className="font-semibold text-orange-500 hover:text-orange-400">Forgot password?</a>
          </div> */}
              </div>
              <div className="mt-2">
                <input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="current-password"
                  required
                  className="block w-full rounded-md border-0 bg-white/5 py-1.5 text-white shadow-sm ring-1 ring-inset ring-orange-500 focus:ring-2 focus:ring-inset focus:ring-black sm:text-sm sm:leading-6"></input>
              </div>

              <div className="flex items-center justify-between pt-4">
                <label htmlFor="password" className="block text-sm font-medium leading-6 text-balance">
                  Re-type Password
                </label>
              </div>
              <div className="mt-2">
                <input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="current-password"
                  required
                  className="block w-full rounded-md border-0 bg-white/5 py-1.5 text-white shadow-sm ring-1 ring-inset ring-orange-500 focus:ring-2 focus:ring-inset focus:ring-black sm:text-sm sm:leading-6"></input>
              </div>
            </div>

            <div>
              <button
                type="submit"
                className={`flex w-full justify-center rounded-md bg-orange-500 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-orange-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-orange-500 ${getButtonClass(
                  "gradient"
                )}`}>
                Create Account
              </button>
            </div>
          </form>

          <p className="mt-10 text-center text-sm text-gray-400">
            Already have account?
            <Link to="/login" className="font-semibold leading-6 text-orange-500 hover:text-orange-400">
              {" "}
              Sign in{" "}
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Register;
