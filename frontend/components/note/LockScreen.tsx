"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Lock, Unlock, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
  CardFooter,
} from "@/components/ui/card";

interface PasswordGateProps {
  isLoading: boolean;
  onSubmit: (password: string) => void;
  error?: string;
}

export default function PasswordGate({
  isLoading,
  onSubmit,
  error,
}: PasswordGateProps) {
  const [password, setPassword] = useState("");
  const router = useRouter();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (password.trim()) {
      onSubmit(password);
    }
  };

  return (
    <div className="flex min-h-[60vh] items-center justify-center p-4 animate-in fade-in zoom-in-95 duration-300">
      <Card className="w-full max-w-md border-neutral-800 bg-neutral-900 shadow-2xl rounded-2xl">
        <CardHeader className="text-center space-y-6 pb-2">
          <div className="mx-auto w-16 h-16 bg-neutral-800 rounded-full flex items-center justify-center">
            <Lock className="w-8 h-8 text-amber-500" />
          </div>
          <div className="space-y-2">
            <CardTitle className="text-2xl font-bold tracking-tight text-white">
              Access restricted
            </CardTitle>
            <CardDescription className="text-neutral-400 text-base">
              Enter the password to view this document.
            </CardDescription>
          </div>
        </CardHeader>

        <form onSubmit={handleSubmit}>
          <CardContent className="space-y-4">
            <div className="space-y-3">
              <Input
                type="password"
                placeholder="Enter Password..."
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="bg-neutral-950 border-neutral-700 h-12 text-center text-lg focus-visible:ring-amber-500 placeholder:text-neutral-600"
                autoFocus
              />
            </div>

            {error && (
              <div className="p-3 rounded-lg bg-red-950/30 border border-red-900/50 text-red-400 text-sm text-center">
                {error}
              </div>
            )}
          </CardContent>

          <CardFooter className="flex flex-col gap-3 pt-2">
            <Button
              type="submit"
              disabled={isLoading || !password}
              className="w-full h-12 bg-amber-600 hover:bg-amber-700 text-white text-lg font-medium transition-all"
            >
              {isLoading ? (
                <>
                  <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                  Checking...
                </>
              ) : (
                <>
                  <Unlock className="w-5 h-5 mr-2" /> Unlock
                </>
              )}
            </Button>
            
            <Button 
              type="button" 
              variant="ghost" 
              onClick={() => router.push("/")}
              className="text-neutral-400 hover:text-white"
            >
              Back to main page
            </Button>
          </CardFooter>
        </form>
      </Card>
    </div>
  );
}