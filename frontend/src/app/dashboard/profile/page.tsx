"use client";

import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Label } from "@/components/ui/label";
import { useState } from "react";

const profileSchema = z.object({
  name: z.string().min(1, "Name is required"),
  email: z.string().email("Invalid email address"),
  password: z.string().min(6, "Password must be at least 6 characters"),
  role: z.enum(["student", "teacher"], { required_error: "Role is required" }),
});

type ProfileFormData = z.infer<typeof profileSchema>;

export default function ProfilePage() {
  const {
    register,
    handleSubmit,
    setValue,
  } = useForm<ProfileFormData>({
    resolver: zodResolver(profileSchema),
  });

  const [loading, setLoading] = useState(false);

  const onSubmit = async (data: ProfileFormData) => {
    setLoading(true);
    console.log("Form Submitted:", data);
    setTimeout(() => setLoading(false), 1000);
  };

  return (
    <div className="min-h-screen p-10 bg-gray-100">
      <h2 className="text-2xl font-bold mb-6">Profile</h2>
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        <div>
          <Label htmlFor="name" className="mb-1.5">Name</Label>
          <Input
            id="name"
            placeholder="Name"
            {...register("name")}
            className="border-black w-full md:w-[30%]"
          />
        </div>

        <div>
          <Label htmlFor="email" className="mb-1.5">Email</Label>
          <Input
            id="email"
            type="email"
            placeholder="abc@gmail.com"
            {...register("email")}
            className="border-black w-full md:w-[30%]"
          />
        </div>

        <div>
          <Label htmlFor="password" className="mb-1.5">Password</Label>
          <Input
            id="password"
            type="password"
            placeholder="************"
            {...register("password")}
            className="border-black w-full md:w-[30%]"
          />
        </div>

        <div>
          <Label className="mb-2">Role</Label>
          <RadioGroup
            defaultValue="student"
            onValueChange={(value) => setValue("role", value as "student" | "teacher")}
            className="flex flex-col space-y-2"
          >
            <div className="flex items-center space-x-2">
              <RadioGroupItem
                value="student"
                id="student"
                className="border-black text-black data-[state=checked]:bg-black data-[state=checked]:border-black"
              />
              <Label htmlFor="student">Student</Label>
            </div>
            <div className="flex items-center space-x-2">
              <RadioGroupItem
                value="teacher"
                id="teacher"
                className="border-black text-black data-[state=checked]:bg-black data-[state=checked]:border-black"
              />
              <Label htmlFor="teacher">Teacher</Label>
            </div>
          </RadioGroup>
        </div>

        <Button type="submit" disabled={loading} className="w-[130px] cursor-pointer">
          {loading ? "Updating..." : "Update Profile"}
        </Button>
      </form>
    </div>
  );
}
