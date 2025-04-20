"use client";

import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import { DarkModeToggle } from "@/components/dark-mode-toggle";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { cn } from "@/lib/utils";

const signUpSchema = z.object({
  name: z
    .string()
    .min(1, { message: "Name is required" })
    .max(100, { message: "Name must be less than 100 characters" }),
  email: z
    .string()
    .min(1, { message: "Email is required" })
    .email({ message: "Invalid email address" }),
  password: z
    .string()
    .min(6, { message: "Password must be at least 6 characters" })
    .max(100, { message: "Password must be less than 100 characters" }),
  role: z.enum(["teacher", "student"], { message: "Role is required" })
});

type SignUpFormData = z.infer<typeof signUpSchema>;

export default function SignUp() {
  const {
    register,
    handleSubmit,
    formState: { errors },
    clearErrors,
    setValue
  } = useForm<SignUpFormData>({
    resolver: zodResolver(signUpSchema),
    mode: "onSubmit"
  });

  const [loading, setLoading] = useState(false);

  // Manually clear errors when user starts typing in the fields
  const handleInputChange = (fieldName: keyof SignUpFormData) => {
    clearErrors(fieldName); // Clear errors for the specific field
  };

  const onSubmit = async (data: SignUpFormData) => {
    setLoading(true);
    try {
      // Signup Logic
      console.log("User signed up with data:", data);
    } catch (error) {
      console.error("Sign-up failed:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-background">
      <div className="fixed top-5 right-5">
        <DarkModeToggle />
      </div>
      <div className="w-full max-w-md p-6 bg-card rounded-2xl shadow-lg">
        <h2 className="text-2xl font-bold mb-6 text-center text-foreground">Sign Up</h2>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div>
            <Input
              type="text"
              placeholder="Name"
              {...register("name")}
              onChange={() => handleInputChange("name")}
              className={errors.name ? "border-destructive" : ""}
            />
            {errors.name && (
              <p className="text-destructive text-sm mt-1">{errors.name.message}</p>
            )}
          </div>

          <div>
            <Input
              type="email"
              placeholder="Email"
              {...register("email")}
              onChange={() => handleInputChange("email")}
              className={errors.email ? "border-destructive" : ""}
            />
            {errors.email && (
              <p className="text-destructive text-sm mt-1">{errors.email.message}</p>
            )}
          </div>

          <div>
            <Input
              type="password"
              placeholder="Password"
              {...register("password")}
              onChange={() => handleInputChange("password")}
              className={errors.password ? "border-destructive" : ""}
            />
            {errors.password && (
              <p className="text-destructive text-sm mt-1">{errors.password.message}</p>
            )}
          </div>

          <div>
            <Select
              onValueChange={(value) => {
                setValue("role", value as "student" | "teacher");
                handleInputChange("role");
              }}
            >
              <SelectTrigger className={cn('w-full', errors.role ? "border-destructive" : "")}>
                <SelectValue placeholder="Select Role" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="student">Student</SelectItem>
                <SelectItem value="teacher">Teacher</SelectItem>
              </SelectContent>
            </Select>
            {errors.role && (
              <p className="text-destructive text-sm mt-1">{errors.role.message}</p>
            )}
          </div>

          <Button type="submit" disabled={loading} className="w-full relative">
            {loading ? (
              <span className="absolute inset-0 flex justify-center items-center">
                <svg
                  className="animate-spin h-5 w-5 text-background"
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
              "Sign Up"
            )}
          </Button>
        </form>
        <div className="mt-4 text-center">
          <p className="text-foreground">
            Already have an account?{" "}
            <Link href="/login" className="text-primary hover:underline">
              Sign In
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
