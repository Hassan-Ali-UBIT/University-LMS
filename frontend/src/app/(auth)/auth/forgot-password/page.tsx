"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { MailIcon } from "lucide-react";
import Link from "next/link";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { toast } from "sonner";
import { z } from "zod";
import { DarkModeToggle } from "@/components/dark-mode-toggle";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";

import { cn } from "@/lib/utils";

const forgotPasswordFormSchema = z.object({
  email: z
    .string()
    .min(1, { message: "Email is required" })
    .email("Invalid email address"),
  redirectTo: z.string().optional()
});

type ForgotPasswordFormValues = z.infer<typeof forgotPasswordFormSchema>;

export default function ForgotPasswordPage() {
  const [isLoading, setIsLoading] = useState(false);

  const form = useForm<ForgotPasswordFormValues>({
    resolver: zodResolver(forgotPasswordFormSchema),
    defaultValues: {
      email: "",
      redirectTo: ""
    }
  });

  async function onSubmit(data: ForgotPasswordFormValues) {
    const redirectTo = getRedirectURL(window.location.origin);
    setIsLoading(true);

    try {
      // TODO: Implement forgot password action
      console.log("Forgot password data:", { ...data, redirectTo });
      toast.success("Reset link sent successfully");
    } catch (error) {
      toast.error("Failed to send reset link");
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-background">
      <div className="fixed top-5 right-5">
        <DarkModeToggle />
      </div>
      <Card className="w-full max-w-[400px]">
        <CardHeader className="text-center">
          <h1 className="text-2xl font-semibold">Forgot your password?</h1>
          <p className="text-sm text-muted-foreground">
            Please enter your email to receive a password reset link.
          </p>
        </CardHeader>
        <CardContent className="space-y-3">
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
              <FormField
                control={form.control}
                name="email"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Email</FormLabel>
                    <FormControl>
                      <div className="relative">
                        <MailIcon className="absolute left-3 top-1/2 -translate-y-1/2 size-4 text-muted-foreground" />
                        <Input
                          {...field}
                          type="email"
                          placeholder="johndoe@example.com"
                          className="pl-9"
                          autoComplete="email"
                          autoCapitalize="none"
                          autoCorrect="off"
                        />
                      </div>
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <Button type="submit" className="w-full" disabled={isLoading}>
                Send reset link
              </Button>
            </form>

            <p className="text-center text-sm text-muted-foreground">
              <span>Remember your password?</span>{" "}
              <Link
                href="/auth/login"
                className={cn("text-primary underline-offset-4 hover:underline")}
              >
                Sign in
              </Link>
            </p>
          </Form>
        </CardContent>
      </Card>
    </div>
  );
}

function getRedirectURL(origin: string) {
  // TODO: Configure reset password path
  const resetPasswordPath = "/reset-password";
  return new URL(resetPasswordPath, origin).href;
}
