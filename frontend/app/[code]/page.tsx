"use client";

import { useEffect, useState, use } from "react";
import { useRouter } from "next/navigation";
import { getDocument, saveDocument, verifyPassword, deleteDocument, TextDocument } from "@/lib/api";
import { addToHistory, removeFromHistory } from "@/lib/history";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Checkbox } from "@/components/ui/checkbox";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { toast } from "sonner";
import { 
  Loader2, Save, Copy, ArrowLeft, Lock, Unlock, 
  Settings, Trash2, Clock, EyeOff, FileText 
} from "lucide-react";

export default function DocPage({ params }: { params: Promise<{ code: string }> }) {
  const { code } = use(params);
  const router = useRouter();

  const [content, setContent] = useState("");
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [isNew, setIsNew] = useState(false);
  const [isLocked, setIsLocked] = useState(false);
  const [passwordInput, setPasswordInput] = useState("");

  const [showSettings, setShowSettings] = useState(false);
  
  const [ttl, setTtl] = useState("86400");
  const [password, setPassword] = useState("");
  const [burnAfterRead, setBurnAfterRead] = useState(false);
  const [summary, setSummary] = useState("");

  useEffect(() => {
    const loadData = async () => {
      try {
        const doc = await getDocument(code);
        
        if (doc) {
          if (doc.password_required) {
            setIsLocked(true);
            setLoading(false);
            return;
          }
          setContent(doc.text || "");
          setSummary(doc.summary || "");
          addToHistory(code, doc.summary || "Watched");
        } else {
          setIsNew(true);
        }
      } catch (error) {
        toast.error("Error loading");
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, [code]);

  const handleUnlock = async () => {
    if (!passwordInput) return;
    setLoading(true);
    try {
        const doc = await verifyPassword(code, passwordInput);
        setContent(doc.text || "");
        setSummary(doc.summary || "");
        setIsLocked(false);
        addToHistory(code, "Unlocked");
        toast.success("Access granted");
    } catch (e) {
        toast.error("Invalid password");
    } finally {
        setLoading(false);
    }
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      const savedKey = await saveDocument({
        text: content,
        ttl: parseInt(ttl),
        only_one_read: burnAfterRead,
        password: password,
        summary: summary
      }, code, isNew);
      
      toast.success(isNew ? "Created!" : "Updated!");

      if (isNew && savedKey !== code) {
        removeFromHistory(code);
        addToHistory(savedKey, summary || "Saved");
        router.replace(`/${savedKey}`);
      } else {
        addToHistory(code, summary || "Saved");
      }
      
      setIsNew(false);
      setShowSettings(false);
      
    } catch (e) {
      toast.error("Error saving");
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async () => {
    if (!confirm("Are you sure you want to delete this document? This action cannot be undone.")) return;
    
    setSaving(true);
    try {
      const success = await deleteDocument(code);
      if (success) {
        toast.success("Deleted");
        removeFromHistory(code);
        router.push("/");
      } else {
        toast.error("Failed to delete (you are not the owner?)");
      }
    } catch (e) {
      toast.error("Error deleting");
    } finally {
      setSaving(false);
    }
  };

  if (loading) return (
    <div className="flex h-screen items-center justify-center bg-neutral-950 text-white">
      <Loader2 className="animate-spin w-10 h-10 text-blue-500" />
    </div>
  );

  if (isLocked) {
    return (
        <div className="flex h-screen items-center justify-center bg-neutral-950 text-white p-4">
            <div className="max-w-md w-full bg-neutral-900 border border-neutral-800 rounded-2xl p-8 text-center space-y-6 shadow-2xl">
                <div className="mx-auto w-16 h-16 bg-neutral-800 rounded-full flex items-center justify-center">
                    <Lock className="w-8 h-8 text-amber-500" />
                </div>
                <div>
                    <h1 className="text-2xl font-bold">Access restricted</h1>
                    <p className="text-neutral-400 mt-2">Enter the password to view.</p>
                </div>
                <div className="space-y-3">
                    <Input 
                        type="password" 
                        placeholder="Password..." 
                        className="bg-neutral-950 border-neutral-700 text-center h-12 text-lg"
                        value={passwordInput}
                        onChange={(e) => setPasswordInput(e.target.value)}
                        onKeyDown={(e) => e.key === 'Enter' && handleUnlock()}
                    />
                    <Button onClick={handleUnlock} className="w-full h-12 bg-amber-600 hover:bg-amber-700 text-lg">
                        <Unlock className="w-5 h-5 mr-2" /> Unlock
                    </Button>
                </div>
                <Button variant="ghost" onClick={() => router.push("/")}>To main page</Button>
            </div>
        </div>
    );
  }

  return (
    <div className="min-h-screen bg-neutral-950 text-white flex flex-col relative">
      <header className="border-b border-neutral-800 p-4 flex items-center justify-between bg-neutral-900/50 backdrop-blur z-20">
        <div className="flex items-center gap-3">
          <Button variant="ghost" size="icon" onClick={() => router.push("/")}>
            <ArrowLeft className="w-5 h-5" />
          </Button>
          <div className="flex flex-col">
            <span className="font-mono text-blue-400 font-bold tracking-wider">{code}</span>
            {summary && <span className="text-xs text-neutral-500 max-w-[150px] truncate">{summary}</span>}
          </div>
        </div>
        
        <div className="flex items-center gap-2">
            <Button 
                variant={showSettings ? "secondary" : "ghost"} 
                size="icon" 
                onClick={() => setShowSettings(!showSettings)}
                className={isNew ? "animate-pulse text-blue-400 bg-blue-900/20" : ""}
            >
                <Settings className="w-5 h-5" />
            </Button>

            <Button variant="secondary" onClick={() => {
                navigator.clipboard.writeText(window.location.href);
                toast.success("Link copied");
            }}>
                <Copy className="w-4 h-4 mr-2" /> <span className="hidden sm:inline">Copy Link</span>
            </Button>
            
            <Button onClick={handleSave} disabled={saving} className="bg-blue-600 hover:bg-blue-700 min-w-[110px]">
                {saving ? <Loader2 className="animate-spin w-4 h-4 mr-2" /> : <Save className="w-4 h-4 mr-2" />}
                {isNew ? "Create" : "Save"}
            </Button>
        </div>
      </header>

      {showSettings && (
        <div className="absolute top-[70px] right-4 w-full max-w-sm bg-neutral-900 border border-neutral-800 rounded-xl shadow-2xl p-5 z-30 animate-in slide-in-from-top-2 fade-in duration-200">
            <div className="flex items-center justify-between mb-4">
                <h3 className="font-semibold text-lg">Settings</h3>
                <Button variant="ghost" size="sm" onClick={() => setShowSettings(false)} className="h-6 w-6 p-0">✕</Button>
            </div>
            
            <div className="space-y-4">
                <div className="space-y-2">
                    <label className="text-sm text-neutral-400 flex items-center gap-2">
                        <Clock className="w-4 h-4" /> Time to live (TTL)
                    </label>
                    
                    <Select value={ttl} onValueChange={setTtl}>
                      <SelectTrigger className="w-full bg-neutral-950 border-neutral-800">
                        <SelectValue placeholder="Select TTL" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="3600">1 hour</SelectItem>
                        <SelectItem value="86400">1 day</SelectItem>
                        <SelectItem value="604800">1 week</SelectItem>
                        <SelectItem value="2592000">1 month</SelectItem>
                      </SelectContent>
                    </Select>

                </div>

                <div className="space-y-2">
                    <label className="text-sm text-neutral-400 flex items-center gap-2">
                        <Lock className="w-4 h-4" /> Password (optional)
                    </label>
                    <Input 
                        type="password" 
                        placeholder="Enter for protection..." 
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        className="bg-neutral-950 border-neutral-800"
                    />
                </div>

                <div className="space-y-2">
                    <label className="text-sm text-neutral-400 flex items-center gap-2">
                        <FileText className="w-4 h-4" /> Short description
                    </label>
                    <Input 
                        placeholder="Note title..." 
                        value={summary}
                        onChange={(e) => setSummary(e.target.value)}
                        className="bg-neutral-950 border-neutral-800"
                    />
                </div>

                <div className="flex items-center justify-between p-3 bg-neutral-950 rounded-lg border border-neutral-800">
                    <div className="space-y-0.5">
                        <label className="text-sm font-medium flex items-center gap-2 text-red-400">
                            <EyeOff className="w-4 h-4" /> One-time read
                        </label>
                    </div>
                    <Checkbox 
                      checked={burnAfterRead} 
                      onCheckedChange={(checked) => setBurnAfterRead(checked as boolean)} 
                      id="terms" 
                  />
                </div>

                {!isNew && (
                    <Button 
                        variant="destructive" 
                        className="w-full bg-red-950/50 hover:bg-red-900 text-red-500 border border-red-900/50"
                        onClick={handleDelete}
                    >
                        <Trash2 className="w-4 h-4 mr-2" /> Delete document
                    </Button>
                )}
            </div>
        </div>
      )}

      <main className="flex-1 p-4 md:p-8 max-w-5xl mx-auto w-full">
        <textarea
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder="Write your text here..."
          className="w-full h-[80vh] bg-transparent border-none resize-none focus:outline-none text-lg font-mono text-neutral-200 placeholder:text-neutral-700 leading-relaxed"
          spellCheck={false}
        />
      </main>
    </div>
  );
}