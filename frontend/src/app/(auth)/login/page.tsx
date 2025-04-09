"use client";

import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import Link from "next/link";

const signInSchema = z.object({
  email: z
    .string({ required_error: "Email is required" })
    .min(1, { message: "Email is required" })
    .email({ message: "Invalid email address" }),
  password: z
    .string({ required_error: "Password is required" })
    .min(1, { message: "Password is required" })
    .min(6, { message: "Password must be at least 6 characters" })
});

type SignInFormData = z.infer<typeof signInSchema>;

export default function SignIn() {
  const {
    register,
    handleSubmit,
    formState: { errors },
    clearErrors
  } = useForm<SignInFormData>({
    resolver: zodResolver(signInSchema),
    mode: "onSubmit" // Validation will trigger only on submit
  });

  const [loading, setLoading] = useState(false);

  // Manually clear errors when user starts typing in the fields
  const handleInputChange = (fieldName: any) => {
    clearErrors(fieldName); // Clear errors for the specific field
  };

  const onSubmit = async (data: SignInFormData) => {
    setLoading(true);
    try {
      // TODO: Call your API here
      console.log("Signing in with", data);
    } catch (error) {
      console.error("Sign in failed", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="w-full max-w-md p-6 bg-white rounded-2xl shadow-lg">
        <h2 className="text-2xl font-bold mb-6 text-center">Sign In</h2>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div>
            <Input
              type="email"
              placeholder="Email"
              {...register("email")}
              onChange={() => handleInputChange("email")} // Clear email error on input change
              className={errors.email ? "border-red-500" : ""}
            />
            {errors.email && <p className="text-red-500 text-sm mt-1">{errors.email.message}</p>}
          </div>

          <div>
            <Input
              type="password"
              placeholder="Password"
              {...register("password")}
              onChange={() => handleInputChange("password")} // Clear password error on input change
              className={errors.password ? "border-red-500" : ""}
            />
            {errors.password && <p className="text-red-500 text-sm mt-1">{errors.password.message}</p>}
          </div>

          <div className="flex justify-between">
            <div>
              <Link href="/signup" className="text-sm text-blue-600 hover:underline">
                Don't have an account?
              </Link>
            </div>
            <div>
              <Link href="#" className="text-sm text-blue-600 hover:underline">
                Forgot Password?
              </Link>
            </div>
          </div>

          <Button type="submit" disabled={loading} className="w-full relative">
            {loading ? (
              <span className="absolute inset-0 flex justify-center items-center">
                <svg
                  className="animate-spin h-5 w-5 text-white"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                >
                  <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="4"
                    d="M4 12a8 8 0 0116 0"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  ></path>
                </svg>
              </span>
            ) : (
              "Sign In"
            )}
          </Button>
        </form>
      </div>
    </div>
  );
}
