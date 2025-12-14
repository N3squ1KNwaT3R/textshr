"use client";

import { useState, useEffect } from "react";
import { Textarea } from "@/components/ui/textarea";
import { ScrollArea } from "@/components/ui/scroll-area";
import ReactMarkdown from "react-markdown";

interface CodeEditorProps {
  initialContent: string;
  readOnly?: boolean;
  onChange: (value: string) => void;
}

export function CodeEditor({ initialContent, readOnly = false, onChange }: CodeEditorProps) {
  const [content, setContent] = useState(initialContent);
  
  useEffect(() => {
    setContent(initialContent);
  }, [initialContent]);

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const newVal = e.target.value;
    setContent(newVal);
    onChange(newVal);
  };

  return (
    <div className="flex flex-col md:flex-row h-full w-full border rounded-md overflow-hidden bg-neutral-900 border-neutral-800">
      <div className={`flex flex-col h-full border-r border-neutral-800 ${readOnly ? 'hidden md:flex md:w-0' : 'w-full md:w-1/2'}`}>
        <div className="bg-neutral-950 px-4 py-2 text-xs text-neutral-500 border-b border-neutral-800 font-mono flex justify-between">
          <span>INPUT (MARKDOWN)</span>
          <span>{content.length} chars</span>
        </div>
        <Textarea 
          value={content}
          onChange={handleChange}
          disabled={readOnly}
          className="flex-1 resize-none rounded-none border-0 bg-neutral-900 text-neutral-200 font-mono focus-visible:ring-0 p-4 leading-relaxed text-sm"
          placeholder="Write something..."
        />
      </div>



      <div className={`flex flex-col h-full bg-neutral-950 ${readOnly ? 'w-full' : 'w-full md:w-1/2'}`}>
        <div className="bg-neutral-950 px-4 py-2 text-xs text-neutral-500 border-b border-neutral-800 font-mono">
          PREVIEW
        </div>
        <div className="flex-1 overflow-auto p-6">
          <article className="prose prose-invert prose-sm max-w-none prose-headings:font-bold prose-h1:text-2xl prose-a:text-blue-400">
             {content ? <ReactMarkdown>{content}</ReactMarkdown> : <span className="text-neutral-600 italic">Preview area...</span>}
          </article>
        </div>
      </div>
    </div>
  );
}