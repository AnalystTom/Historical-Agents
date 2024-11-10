import * as React from "react";
import { cn } from "@/lib/utils"; // Assuming you have a utility for class names

const Input = React.forwardRef<
  HTMLInputElement,
  React.InputHTMLAttributes<HTMLInputElement>
>(({ className, ...props }, ref) => (
  <input
    ref={ref}
    className={cn("border rounded p-2", className)}
    {...props}
  />
));

Input.displayName = "Input";

export { Input };