'use client';

import { zodResolver } from '@hookform/resolvers/zod';
import { EyeIcon, EyeOffIcon, LockIcon } from 'lucide-react';
import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { toast } from 'sonner';
import { z } from 'zod';

import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { DarkModeToggle } from '@/components/dark-mode-toggle';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';

const resetPasswordFormSchema = z
  .object({
    newPassword: z.string().min(8, 'Password must be at least 8 characters'),
    confirmNewPassword: z
      .string()
      .min(8, 'Password must be at least 8 characters'),
  })
  .refine((data) => data.newPassword === data.confirmNewPassword, {
    message: "Passwords don't match",
    path: ['confirmNewPassword'],
  });

type ResetPasswordFormValues = z.infer<typeof resetPasswordFormSchema>;

export default function ResetPasswordPage() {
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const form = useForm<ResetPasswordFormValues>({
    resolver: zodResolver(resetPasswordFormSchema),
    defaultValues: {
      newPassword: '',
      confirmNewPassword: '',
    },
  });

  async function onSubmit(data: ResetPasswordFormValues) {
    try {
      setIsLoading(true);
      // Replace with your actual password reset API call
      await new Promise((resolve) => setTimeout(resolve, 1000));
      toast.success('Password reset successfully');
    } catch (error) {
      toast.error('Failed to reset password');
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
          <h1 className="text-2xl font-semibold">Reset your password</h1>
          <p className="text-sm text-muted-foreground">
            Please fill in the form to reset your password.
          </p>
        </CardHeader>
        <CardContent className="space-y-3">
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
              <FormField
                control={form.control}
                name="newPassword"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>New Password</FormLabel>
                    <FormControl>
                      <div className="relative">
                        <LockIcon className="absolute left-3 top-2.5 size-4 text-muted-foreground" />
                        <Input
                          type={showPassword ? 'text' : 'password'}
                          className="pl-9 pr-9"
                          placeholder="••••••••"
                          {...field}
                        />
                        <ShowPasswordToggle
                          className="absolute right-3 top-2.5"
                          showPassword={showPassword}
                          onTogglePassword={() => setShowPassword(!showPassword)}
                        />
                      </div>
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="confirmNewPassword"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Confirm New Password</FormLabel>
                    <FormControl>
                      <div className="relative">
                        <LockIcon className="absolute left-3 top-2.5 size-4 text-muted-foreground" />
                        <Input
                          type={showConfirmPassword ? 'text' : 'password'}
                          className="pl-9 pr-9"
                          placeholder="••••••••"
                          {...field}
                        />
                        <ShowPasswordToggle
                          className="absolute right-3 top-2.5"
                          showPassword={showConfirmPassword}
                          onTogglePassword={() =>
                            setShowConfirmPassword(!showConfirmPassword)
                          }
                        />
                      </div>
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <Button type="submit" className="w-full" disabled={isLoading}>
                Reset password
              </Button>
            </form>
          </Form>
        </CardContent>
      </Card>
    </div>
  );
}

function ShowPasswordToggle({
  showPassword,
  onTogglePassword,
  className,
}: {
  showPassword: boolean;
  onTogglePassword: () => void;
  className?: string;
}) {
  return showPassword ? (
    <EyeIcon
      className={`size-4 cursor-pointer text-muted-foreground ${className}`}
      onClick={onTogglePassword}
    />
  ) : (
    <EyeOffIcon
      className={`size-4 cursor-pointer text-muted-foreground ${className}`}
      onClick={onTogglePassword}
    />
  );
}
