"use client";

import { EditorContent, type Editor } from "@tiptap/react";

interface RichEditorProps {
  editor: Editor | null;
}

export default function RichEditor({ editor }: RichEditorProps) {
  if (!editor) return null;

  return (
    <div className="flex flex-col h-full w-full bg-neutral-950 relative">
      <div 
        className={`flex-1 w-full px-4 md:px-20 py-8 overflow-y-auto ${
          editor.isEditable ? "cursor-text" : "cursor-default"
        }`} 
        onClick={() => {
          if (editor.isEditable) {
            editor.commands.focus();
          }
        }}
      >
        <EditorContent editor={editor} />
      </div>
    </div>
  );
}