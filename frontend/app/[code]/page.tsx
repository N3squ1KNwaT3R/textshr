import { NoteEditor } from "@/components/note/NoteEditor";

interface PageProps {
  params: Promise<{ code: string }>;
}

export default async function ViewPage({ params }: PageProps) {
  const { code } = await params;
  
  return <NoteEditor initialCode={code} />;
}