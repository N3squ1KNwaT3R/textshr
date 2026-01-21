"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { nanoid } from "nanoid";
import { getHistory, removeFromHistory, HistoryItem } from "@/lib/history";
import { getText, verifyPassword } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { toast } from "sonner";
import { FileText, ArrowRight, Clock, Trash2, Lock, Search, ShieldCheck, Loader2 } from "lucide-react";

export default function Home() {
  const router = useRouter();
  
  const [history, setHistory] = useState<HistoryItem[]>([]);

  const [inputCode, setInputCode] = useState("");
  const [inputPassword, setInputPassword] = useState("");
  const [loading, setLoading] = useState(false);
  
  const [step, setStep] = useState<"enter-code" | "enter-password">("enter-code");
 const updateHistory = () => {
    setHistory(getHistory());
  };
  useEffect(() => {
    updateHistory()
    window.addEventListener("history-change", updateHistory);
    return () => {
      window.removeEventListener("history-change", updateHistory);
    };
  }, []);

  const createNewDoc = () => {
    const id = nanoid(6);
    router.push(`/new`);
  };

  const handleCheckCode = async () => {
    if (!inputCode.trim()) return;
    setLoading(true);

    try {
      const doc = await getText(inputCode.trim());
      
      if (!doc) {
        router.push(`/${inputCode.trim()}`);
        return;
      }

      if (doc.password_required) {
        setStep("enter-password");
        toast.info("This document is password protected");
        setLoading(false);
        return;
      }

      router.push(`/${inputCode.trim()}`);
      
    } catch (error) {
      toast.error("Connection error");
      setLoading(false);
    }
  };

  const handleVerifyPassword = async () => {
    if (!inputPassword) return;
    setLoading(true);
    
    try {
      await verifyPassword(inputCode.trim(), inputPassword);
      sessionStorage.setItem(`pwd_${inputCode.trim()}`, inputPassword);
      
      toast.success("Access granted");
      router.push(`/${inputCode.trim()}`);
    } catch (error) {
      toast.error("Invalid password");
      setLoading(false);
    }
  };

  const handleDeleteHistory = (key: string, e: React.MouseEvent) => {
    e.stopPropagation();
    removeFromHistory(key);
    updateHistory();
  };

  return (
    <main className="flex min-h-screen items-center justify-center p-6 bg-neutral-950 text-white relative overflow-hidden">
      <div className="absolute inset-0 bg-[url('/grid.svg')] bg-center opacity-20 pointer-events-none" />
      
      <div className="z-10 w-full max-w-5xl bg-neutral-900/60 backdrop-blur-xl border border-neutral-800 rounded-3xl shadow-2xl overflow-hidden">
        <div className="grid grid-cols-1 md:grid-cols-[1.2fr_1px_0.8fr] min-h-[500px]">
          
          <div className="p-8 flex flex-col gap-8">
            <div>
              <div className="flex items-center gap-3 mb-2">
                <div className="bg-blue-600/20 p-2 rounded-lg">
                    <FileText className="w-6 h-6 text-blue-500" />
                </div>
                <h1 className="text-2xl font-bold tracking-tight">TextShare</h1>
              </div>
              <p className="text-neutral-400">
                Create secure, encrypted notes and share them instantly.
              </p>
            </div>

            <Button 
                onClick={createNewDoc} 
                className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white py-8 text-lg font-medium shadow-lg shadow-blue-900/20 transition-all hover:scale-[1.01]"
            >
                <div className="flex flex-col items-start">
                    <span className="flex items-center gap-2">Create New Note <ArrowRight className="w-5 h-5" /></span>
                </div>
            </Button>

            <div className="flex-1 flex flex-col min-h-0">
                <h3 className="text-xs font-bold text-neutral-500 uppercase tracking-wider mb-3 flex items-center gap-2">
                    <Clock className="w-3 h-3" /> Recent Notes
                </h3>
                
                <div className="flex-1 overflow-y-auto pr-2 space-y-2 max-h-[200px] scrollbar-thin scrollbar-thumb-neutral-800">
                    {history.length === 0 ? (
                        <div className="text-neutral-600 text-sm italic py-4">History is empty...</div>
                    ) : (
                        history.map((item) => (
                            <div 
                                key={item.key}
                                onClick={() => router.push(`/${item.key}`)}
                                className="group flex items-center justify-between p-3 rounded-xl bg-neutral-800/30 border border-neutral-800 hover:bg-neutral-800 hover:border-blue-900/50 cursor-pointer transition-all"
                            >
                                <div className="flex flex-col overflow-hidden">
                                    <span className="font-mono text-sm text-blue-400 font-bold tracking-wide">{item.key}</span>
                                    <span className="text-xs text-neutral-500 truncate max-w-[200px]">{item.summary || "No description"}</span>
                                </div>
                                <button 
                                    onClick={(e) => handleDeleteHistory(item.key, e)}
                                    className="p-2 text-neutral-600 hover:text-red-400 hover:bg-red-950/30 rounded-lg transition-colors"
                                >
                                    <Trash2 className="w-4 h-4" />
                                </button>
                            </div>
                        ))
                    )}
                </div>
            </div>
          </div>

          <div className="hidden md:block bg-gradient-to-b from-transparent via-neutral-800 to-transparent w-[1px]" />
          <div className="md:hidden bg-neutral-800 h-[1px] w-full" />

          <div className="p-8 bg-neutral-900/30 flex flex-col justify-center">
            
            <div className="max-w-xs mx-auto w-full space-y-6">
                <div className="text-center space-y-2">
                    <div className="mx-auto w-12 h-12 bg-neutral-800 rounded-2xl flex items-center justify-center mb-4 transition-all duration-500">
                        {step === "enter-code" ? (
                            <Search className="w-6 h-6 text-neutral-400" />
                        ) : (
                            <Lock className="w-6 h-6 text-amber-500 animate-pulse" />
                        )}
                    </div>
                    <h2 className="text-xl font-semibold transition-all">
                        {step === "enter-code" ? "Open Document" : "Enter Password"}
                    </h2>
                    <p className="text-sm text-neutral-400 transition-all">
                        {step === "enter-code" 
                            ? "Enter code or link to access." 
                            : "This note is protected."}
                    </p>
                </div>

                <div className="space-y-3">
                    {step === "enter-code" ? (
                        <div className="space-y-3 animate-in fade-in slide-in-from-right-4 duration-300">
                             <Input 
                                placeholder="e.g. qWertY" 
                                className="bg-neutral-950 border-neutral-700 text-center text-lg tracking-widest font-mono h-12 focus-visible:ring-blue-600"
                                value={inputCode}
                                onChange={(e) => setInputCode(e.target.value)}
                                onPaste={(e) => {
                                    e.preventDefault();
                                    const text = e.clipboardData.getData('text');
                                    const parts = text.split('/');
                                    const code = parts[parts.length - 1];
                                    setInputCode(code);
                                }}
                                onKeyDown={(e) => e.key === 'Enter' && handleCheckCode()}
                            />
                            <Button 
                                className="w-full bg-neutral-800 hover:bg-neutral-700 h-12 transition-all"
                                onClick={handleCheckCode}
                                disabled={loading || !inputCode}
                            >
                                {loading ? <Loader2 className="animate-spin" /> : "Find Note"}
                            </Button>
                        </div>
                    ) : (
                        <div className="space-y-3 animate-in fade-in slide-in-from-right-4 duration-300">
                             <Input 
                                type="password"
                                placeholder="••••••" 
                                className="bg-neutral-950 border-amber-900/50 text-center text-lg h-12 focus-visible:ring-amber-500"
                                value={inputPassword}
                                onChange={(e) => setInputPassword(e.target.value)}
                                autoFocus
                                onKeyDown={(e) => e.key === 'Enter' && handleVerifyPassword()}
                            />
                            <div className="grid grid-cols-2 gap-3">
                                <Button 
                                    variant="ghost" 
                                    className="h-12 hover:bg-neutral-800"
                                    onClick={() => {
                                        setStep("enter-code");
                                        setInputPassword("");
                                    }}
                                >
                                    Back
                                </Button>
                                <Button 
                                    className="bg-amber-600 hover:bg-amber-700 h-12"
                                    onClick={handleVerifyPassword}
                                    disabled={loading}
                                >
                                    {loading ? <Loader2 className="animate-spin" /> : "Unlock"}
                                </Button>
                            </div>
                        </div>
                    )}
                </div>
            </div>

          </div>
        </div>
      </div>
    </main>
  );
}