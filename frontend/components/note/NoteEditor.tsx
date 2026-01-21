"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { NoteHeader } from "@/components/note/NoteHeader";
import { NoteSettings } from "@/components/note/NoteSettings";
import RichEditor from "@/components/note/rich-editor";
import { createText, deleteDocument, getText, updateText, verifyPassword } from "@/lib/api";
import PasswordGate from "@/components/PasswordGate";
import { Loader2 } from "lucide-react"; 

import { useEditor } from "@tiptap/react";
import StarterKit from "@tiptap/starter-kit";
import Placeholder from "@tiptap/extension-placeholder";

import { addToHistory, checkIsOwner, removeFromHistory } from "@/lib/history";

interface NoteEditorProps {
  initialCode?: string;
}

export function NoteEditor({ initialCode }: NoteEditorProps) {
  const router = useRouter();

  const [code, setCode] = useState<string | null>(initialCode || null);
  const [content, setContent] = useState("");
  const [ttl, setTtl] = useState("600");
  const [password, setPassword] = useState("");
  const [summary, setSummary] = useState("");
  const [burnAfterRead, setBurnAfterRead] = useState(false);
  
  const [isNew, setIsNew] = useState(!initialCode);
  const [isLoading, setLoading] = useState(!!initialCode);
  const [isSaving, setSaving] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [isLocked, setIsLocked] = useState(false);

  const [canEdit, setCanEdit] = useState(!initialCode);
  const [isOwner, setIsOwner] = useState(false);
  const [unlockError, setUnlockError] = useState("");

  const editor = useEditor({
    extensions: [
      StarterKit,
      Placeholder.configure({
        placeholder: "Start writing your story...",
        emptyEditorClass: 
          "before:content-[attr(data-placeholder)] before:text-neutral-500 before:absolute before:top-0 before:left-0 before:pointer-events-none relative",
      }),
    ],
    content: content,
    editable: canEdit,
    editorProps: {
      attributes: {
        class: "prose prose-invert max-w-none w-full focus:outline-none leading-relaxed text-lg prose-p:text-neutral-300 prose-p:my-2 prose-headings:text-white prose-headings:mb-3 prose-headings:font-bold prose-strong:text-white prose-ul:my-2 prose-ol:my-2 prose-li:text-neutral-300 marker:text-neutral-500 prose-blockquote:border-l-amber-500 prose-blockquote:text-neutral-400 prose-blockquote:bg-neutral-900/50 prose-blockquote:py-1 prose-blockquote:px-4 prose-code:text-amber-400 prose-code:bg-neutral-900 prose-code:px-1 prose-code:rounded prose-code:before:content-none prose-code:after:content-none",
      },
    },
    onUpdate: ({ editor }) => {
      if (editor.isEditable) {
        setContent(editor.getHTML());
      }
    },
    immediatelyRender: false,
  });

  useEffect(() => {
    if (editor && editor.isEditable !== canEdit) {
      editor.setEditable(canEdit);
    }
  }, [canEdit, editor]);

  useEffect(() => {
    if (!initialCode) return;

    const load = async () => {
      try {
        const doc = await getText(initialCode);

        if (doc.password_required) {
          const cached = sessionStorage.getItem(`pwd_${initialCode}`);
          if (cached) {
            try {
              const unlocked = await verifyPassword(initialCode, cached);
              applyDocData(unlocked);
              return;
            } catch {
              sessionStorage.removeItem(`pwd_${initialCode}`);
            }
          }
          setIsLocked(true);
          return;
        }

        applyDocData(doc);
      } catch (e) {
        toast.error("Document not found");
        router.push("/");
      } finally {
        setLoading(false);
      }
    };

    load();
  }, [initialCode, router]);

  useEffect(() => {
    if (editor && content && editor.getHTML() !== content) {
      if (editor.getText() === "") { 
         editor.commands.setContent(content);
      }
    }
  }, [content, editor]);

  const applyDocData = (doc: any) => {
    setContent(doc.text || "");
    setSummary(doc.summary || "");
    
    const owner = checkIsOwner(initialCode!);
    
    setIsOwner(owner);
    setCanEdit(owner);
    
    setIsNew(false);
    addToHistory(initialCode!, doc.summary || "Viewed", owner);
  };

  const handleUnlock = async (candidatePassword: string) => {
    if (!candidatePassword || !initialCode) return;
    setLoading(true);
    setUnlockError("");

    try {
      const doc = await verifyPassword(initialCode, candidatePassword);
      applyDocData(doc); 
      setIsLocked(false);
      sessionStorage.setItem(`pwd_${initialCode}`, candidatePassword);
      toast.success("Access granted");
    } catch (err) {
      setUnlockError("Invalid password");
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    if (!canEdit && !isNew) return;

    setSaving(true);
    const currentContent = editor ? editor.getHTML() : content;
    
    try {
      const options = {
        text: currentContent,
        ttl: Number(ttl),
        only_one_read: burnAfterRead,
        password: password.trim() === "" ? undefined : password, 
        summary: summary.trim() === "" ? undefined : summary,
      };

      if (isNew) {
         const res = await createText(options);
         
         addToHistory(res.key, summary || "New Note", true, Number(ttl)); 

         if (password) sessionStorage.setItem(`pwd_${res.key}`, password);
         
         setCode(res.key);
         setIsNew(false);
         setIsOwner(true); 
         setCanEdit(true); 
         
         router.push(`/${res.key}`); 
         toast.success("Created successfully!");
      } else {
         if(code) {
            await updateText(code, options);
            addToHistory(code, summary || "Updated", isOwner, Number(ttl));
         }
         
         if (password && code) sessionStorage.setItem(`pwd_${code}`, password);
         toast.success("Changes saved!");
      }

      setShowSettings(false);
    } catch (e: any) {
      const msg = e.response?.data?.detail || "Save failed";
      toast.error(typeof msg === 'string' ? msg : "Save failed");
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async () => {
    if (!code || !confirm("Delete this document?")) return;
    setSaving(true);
    try {
      const ok = await deleteDocument(code);
      if (ok) {
        removeFromHistory(code);
        router.push("/");
      } else {
        toast.error("Delete failed");
      }
    } catch {
      toast.error("Delete error");
    } finally {
      setSaving(false);
    }
  };

  if (isLoading && isLocked) {
     return <div className="flex h-screen items-center justify-center bg-neutral-950 text-white"><Loader2 className="animate-spin w-10 h-10 text-blue-500" /></div>;
  } else if (isLoading) {
    return (
      <div className="flex h-screen items-center justify-center bg-neutral-950 text-white">
        <Loader2 className="animate-spin w-10 h-10 text-blue-500" />
      </div>
    );
  }

  if (isLocked) {
    return (
      <div className="min-h-screen bg-neutral-950 flex items-center justify-center">
        <PasswordGate
          isLoading={isLoading}
          onSubmit={handleUnlock}
          error={unlockError}
        />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-neutral-950 text-white flex flex-col relative">      
      <NoteHeader
       editor={editor}
        isNew={isNew}
        onSave={handleSave}
        saving={isSaving}
        code={code || undefined}
        onOpenSettings={() => setShowSettings(!showSettings)}
        canEdit={canEdit} 
      />

      {showSettings && canEdit && (
        <NoteSettings
           ttl={ttl} setTtl={setTtl}
           password={password} setPassword={setPassword}
           summary={summary} setSummary={setSummary}
           burnAfterRead={burnAfterRead} setBurnAfterRead={setBurnAfterRead}
           isNew={isNew}
           onDelete={handleDelete}
           onClose={() => setShowSettings(false)}
        />
      )}

      <main className="flex-1 flex flex-col w-full h-full overflow-hidden">
        <RichEditor editor={editor} />
      </main>
    </div>
  );
}