"use client";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { FileText, ArrowRight } from "lucide-react";
import { useRouter } from "next/navigation";
import { nanoid } from "nanoid";

export default function Home() {
  const router = useRouter();

  const createNewDoc = () => {
    const id = nanoid(6);
    router.push(`/${id}`);
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-6 bg-neutral-950 text-white">
      <div className="absolute inset-0 bg-[url('/grid.svg')] bg-center [mask-image:linear-gradient(180deg,white,rgba(255,255,255,0))]" />
      
      <Card className="w-full max-w-md z-10 bg-neutral-900 border-neutral-800 text-neutral-100">
        <CardHeader className="text-center">
          <div className="mx-auto bg-neutral-800 p-3 rounded-full w-fit mb-4">
            <FileText className="w-8 h-8 text-blue-500" />
          </div>
          <CardTitle className="text-2xl font-bold">TextShare</CardTitle>
          <CardDescription className="text-neutral-400">
            Share your stupid notes instantly, we support Markdown.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Button 
            onClick={createNewDoc} 
            className="w-full bg-blue-600 hover:bg-blue-700 text-white py-6 text-lg"
          >
            Create new docs <ArrowRight className="ml-2 w-5 h-5" />
          </Button>
        </CardContent>
      </Card>
    </main>
  );
}