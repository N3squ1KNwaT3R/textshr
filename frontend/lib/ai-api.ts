import { ensureSession } from "./session-api";

const AI_API = "/api/text"; 

export async function correctText(text: string): Promise<string> {
  await ensureSession();

  const res = await fetch(`${AI_API}/text_correction`, {
    method: "POST",
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });

  if (!res.ok) {
    const err = await res.text();
    console.error("AI Correction Error:", err);
    throw new Error("Failed to correct text");
  }

  const data = await res.json();
  return data.result;
}

export async function summarizeText(text: string): Promise<string> {
  await ensureSession();

  const res = await fetch(`${AI_API}/text_summarization`, {
    method: "POST",
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });

  if (!res.ok) {
    const err = await res.text();
    console.error("AI Summarization Error:", err);
    throw new Error("Failed to summarize text");
  }

  const data = await res.json();
  return data.result;
}