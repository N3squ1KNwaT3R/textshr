"use client";

import { useEffect, useState, useCallback } from "react";
import { useParams } from "next/navigation";
import { getDocument, saveDocument } from "@/lib/api";
import { CodeEditor } from "@/components/code-editor";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import { Loader2, Save, Copy, Check } from "lucide-react";

export default function DocPage() {
  const params = useParams();
  const id = params.code as string;

  const [content, setContent] = useState("");
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [lastSaved, setLastSaved] = useState<Date | null>(null);
  
  useEffect(() => {
    const loadData = async () => {
      try {
        const doc = await getDocument(id);
        if (doc) {
          setContent(doc.content);
          setLastSaved(new Date(doc.updatedAt));
        } else {
          setContent("# New document\n");
        }
      } catch (error) {
        toast.error("Upload error");
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, [id]);

  
  const handleSave = async () => {
    setSaving(true);
    await saveDocument(id, content);
    setLastSaved(new Date());
    setSaving(false);
    toast.success("Saved!");
  };

  
  useEffect(() => {
    const timer = setTimeout(() => {
        if (!loading && content) {
            
            // tutaj autosave nahui handleSave(); 
        }
    }, 2000);
    return () => clearTimeout(timer);
  }, [content, loading]);

  if (loading) {
    return (
      <div className="h-screen w-full flex items-center justify-center bg-neutral-950 text-neutral-400 gap-2">
        <Loader2 className="animate-spin" />
        Loading docs...
      </div>
    );
  }

  return (
    <div className="flex flex-col h-screen bg-neutral-950 text-neutral-200">
      <header className="h-14 border-b border-neutral-800 px-4 flex items-center justify-between bg-neutral-900/50 backdrop-blur">
        <div className="flex items-center gap-4">
            <div className="font-bold text-lg tracking-tight">TextShare</div>
            <div className="h-4 w-[1px] bg-neutral-700 mx-2"></div>
            <div className="text-xs text-neutral-500 font-mono bg-neutral-800/50 px-2 py-1 rounded">
                /{id}
            </div>
            {lastSaved && (
                <span className="text-xs text-neutral-500 hidden sm:inline-block">
                    Saved: {lastSaved.toLocaleTimeString('uk-UA', { hour: '2-digit', minute: '2-digit', second: '2-digit' })}
                </span>
            )}
        </div>

        <div className="flex gap-2">
          <Button variant="ghost" size="sm" onClick={() => {
            navigator.clipboard.writeText(window.location.href);
            toast("Link copied!");
          }}>
            <Copy className="w-4 h-4 mr-2" /> Share
          </Button>
          
          <Button 
            size="sm" 
            onClick={handleSave} 
            disabled={saving}
            className={saving ? "opacity-80" : "bg-emerald-600 hover:bg-emerald-700 text-white"}
          >
            {saving ? <Loader2 className="w-4 h-4 animate-spin mr-2" /> : <Save className="w-4 h-4 mr-2" />}
            {saving ? "Saving..." : "Save"}
          </Button>
        </div>
      </header>
      <div className="flex-1 p-4 overflow-hidden">
        <CodeEditor 
            initialContent={content} 
            onChange={(val) => setContent(val)} 
        />
      </div>
    </div>
  );
}