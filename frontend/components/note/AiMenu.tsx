"use client";

import { useState } from "react";
import { type Editor } from "@tiptap/react";
import { Sparkles, Check, FileText, Loader2, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { correctText, summarizeText } from "@/lib/ai-api";
import { toast } from "sonner";

interface AiMenuProps {
  editor: Editor;
}

export function AiMenu({ editor }: AiMenuProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [summaryResult, setSummaryResult] = useState<string | null>(null);

  const handleCorrection = async () => {
    const text = editor.getText();
    if (!text.trim() || text.length < 1) {
      toast.error("Text is too short for AI");
      return;
    }

    setLoading(true);
    setIsOpen(false);
    const toastId = toast.loading("AI is fixing your text...");

try {
    const response = await correctText(text);
    const corrected = typeof response === 'object' && response !== null && 'result' in response ? (response as any).result : response;      
      if (!corrected || typeof corrected !== 'string' || corrected.trim() === "") {
        toast.error("AI returned invalid response", { id: toastId });
        return;
      }

      console.log("AI Result:", corrected);
      editor.chain().focus().setContent(corrected).run();
      toast.success("Text corrected!", { id: toastId });
      
    } catch (e) {
      console.error("Correction error:", e);
      toast.error("AI failed to correct text", { id: toastId });
    } finally {
      setLoading(false);
    }
  };

  const handleSummarization = async () => {
    const text = editor.getText();
    if (!text.trim() || text.length < 10) {
      toast.error("Write more text to summarize");
      return;
    }

    setLoading(true);
    setIsOpen(false);
    const toastId = toast.loading("AI is reading...");

    try {
      const response = await summarizeText(text);
      const summaryText =
        typeof response === "object" &&
        response !== null &&
        "result" in response &&
        typeof (response as any).result === "string"
          ? (response as any).result
          : typeof response === "string"
          ? response
          : "";
        setSummaryResult(summaryText);
      toast.dismiss(toastId);
    } catch (e) {
      toast.error("AI summarization failed", { id: toastId });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative">
      <Button
        variant="ghost"
        size="icon"
        onClick={() => setIsOpen(!isOpen)}
        className={`text-amber-400 hover:text-amber-300 hover:bg-neutral-900 transition-all ${loading ? "animate-pulse" : ""}`}
        title="AI Tools"
        disabled={loading}
      >
        {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Sparkles className="w-5 h-5" />}
      </Button>

      {isOpen && (
        <>
          <div className="fixed inset-0 z-40" onClick={() => setIsOpen(false)} />
          
          <div className="absolute right-0 top-full mt-2 w-48 bg-neutral-900 border border-neutral-800 rounded-lg shadow-xl z-50 overflow-hidden flex flex-col">
            <button
              onClick={handleCorrection}
              className="flex items-center gap-2 px-4 py-3 text-sm text-neutral-300 hover:bg-neutral-800 hover:text-white text-left transition-colors"
            >
              <Check className="w-4 h-4 text-green-500" />
              Fix Grammar
            </button>
            <div className="h-[1px] bg-neutral-800" />
            <button
              onClick={handleSummarization}
              className="flex items-center gap-2 px-4 py-3 text-sm text-neutral-300 hover:bg-neutral-800 hover:text-white text-left transition-colors"
            >
              <FileText className="w-4 h-4 text-blue-500" />
              Summarize
            </button>
          </div>
        </>
      )}

      {summaryResult && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
          <div className="bg-neutral-900 border border-neutral-800 rounded-xl p-6 max-w-lg w-full shadow-2xl relative">
            <button 
                onClick={() => setSummaryResult(null)}
                className="absolute top-4 right-4 text-neutral-500 hover:text-white"
            >
                <X className="w-5 h-5" />
            </button>
            
            <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-amber-500" /> Summary
            </h3>
            
            <div className="bg-neutral-950 p-4 rounded-lg text-neutral-300 leading-relaxed max-h-[60vh] overflow-y-auto border border-neutral-800">
                {summaryResult}
            </div>

            <div className="mt-6 flex gap-2 justify-end">
                <Button 
                    variant="outline" 
                    onClick={() => {
                        navigator.clipboard.writeText(summaryResult);
                        toast.success("Copied!");
                        setSummaryResult(null);
                    }}
className="border-neutral-700 bg-transparent text-white hover:bg-white hover:text-black transition-all duration-200"                >
                    Copy
                </Button>
                <Button 
                    onClick={() => {
                        editor.commands.insertContent(`\n\n> **Summary:** ${summaryResult}`);
                        setSummaryResult(null);
                    }}
                    className="bg-blue-600 hover:bg-blue-700 text-white"
                >
                    Append to Note
                </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}