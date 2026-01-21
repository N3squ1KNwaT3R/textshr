"use client";

import { Button } from "@/components/ui/button";
import { ChevronLeft, Copy, Save, Loader2, MoreVertical, Eye } from "lucide-react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { type Editor } from "@tiptap/react"; 
import { AiMenu } from "./AiMenu";

interface NoteHeaderProps {
  isNew: boolean;
  onSave: () => void;
  saving: boolean;
  code?: string;
  onOpenSettings: () => void;
  canEdit: boolean;
  editor: Editor | null;
}

export function NoteHeader({
  isNew,
  onSave,
  saving,
  code,
  onOpenSettings,
  canEdit,
  editor
}: NoteHeaderProps) {
  const router = useRouter();

  const handleCopy = () => {
    if (!code) return;
    navigator.clipboard.writeText(`${window.location.origin}/${code}`);
    toast.success("Link copied");
  };

  return (
    <header className="h-16 border-b border-neutral-800 bg-neutral-950 flex items-center justify-between px-4 sticky top-0 z-50">
      <div className="flex items-center gap-4">
        <Button 
          variant="ghost" 
          size="icon" 
          onClick={() => router.push("/")} 
          className="text-neutral-400 hover:bg-white hover:text-black transition-colors"
        >
          <ChevronLeft className="w-5 h-5" />
        </Button>
        
        <h1 className="font-semibold text-white hidden md:block">
          {isNew ? "New Note" : "Edit Note"}
        </h1>
      </div>

      <div className="flex items-center gap-2">
        {canEdit && editor && (
            <AiMenu editor={editor} />
        )}

        {!isNew && (
          <Button 
            variant="outline" 
            size="sm" 
            onClick={handleCopy} 
            className="hidden sm:flex border-neutral-800 bg-neutral-900 text-neutral-300 hover:bg-white hover:text-black transition-colors"
          >
            <Copy className="w-4 h-4 mr-2" /> Copy Link
          </Button>
        )}
        
        {canEdit && (
          <Button 
            onClick={onOpenSettings} 
            variant="ghost" 
            size="icon" 
            className="text-neutral-400 hover:bg-white hover:text-black transition-colors"
          >
              <MoreVertical className="w-5 h-5" />
          </Button>
        )}

        {(canEdit || isNew) ? (
          <Button onClick={onSave} disabled={saving} className="bg-blue-600 hover:bg-blue-700 text-white min-w-[100px]">
            {saving ? <Loader2 className="w-4 h-4 mr-2 animate-spin" /> : <Save className="w-4 h-4 mr-2" />}
            {isNew ? "Create" : "Save"}
          </Button>
        ) : (
          <div className="flex items-center gap-2 px-3 py-2 rounded-md bg-neutral-900 border border-neutral-800 text-neutral-500 select-none cursor-default">
            <Eye className="w-4 h-4" />
            <span className="text-sm font-medium">Read Only</span>
          </div>
        )}
      </div>
    </header>
  );
}