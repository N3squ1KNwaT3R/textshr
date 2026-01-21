import { ensureSession } from "./session-api";

const TEXT_API = "/api/text";

export type TextDocument = {
  text: string;
  size?: number;
  summary?: string;
  password_required?: boolean;
};

export type SaveTextOptions = {
  text: string;
  ttl?: number;
  only_one_read?: boolean;
  password?: string;
  summary?: string;
};


export async function createText(options: SaveTextOptions): Promise<{ key: string }> {
  await ensureSession();

  const backendBody = {
    text: options.text,
    ttl: options.ttl || 3600,
    only_one_read: options.only_one_read ?? false, 
    password: options.password || "",
    summary: options.summary || ""
  };

  const res = await fetch(`${TEXT_API}/`, {
    method: "POST",
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(backendBody),
  });

  if (!res.ok) {
    const err = await res.text();
    console.error("Create Text Error:", err);
    throw new Error("Failed to create text");
  }

  return res.json();
}

export async function updateText(
  key: string,
  options: SaveTextOptions
): Promise<{ key: string }> {
  await ensureSession();

  const backendBody = {
    text: options.text,
    ttl: options.ttl || 3600,
    only_one_read: options.only_one_read ?? false,
    password: options.password || "",
    summary: options.summary || ""
  };

  const res = await fetch(`${TEXT_API}/?key=${key}`, {
    method: "PUT",
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(backendBody),
  });

  if (!res.ok) {
    throw new Error("Failed to update text");
  }

  return { key };
}

export async function getText(key: string): Promise<TextDocument> {
  await ensureSession();

  const res = await fetch(`${TEXT_API}/?key=${key}`, {
    method: "GET",
    credentials: "include",
  });

  if (res.status === 404) {
    throw new Error("Text not found");
  }

  if (!res.ok) {
    throw new Error("Failed to fetch text");
  }

  return res.json();
}


export async function verifyPassword(
  key: string,
  password: string
): Promise<TextDocument> {
  await ensureSession();

  const res = await fetch(`/api/text/verify?key=${key}`, {
    method: "POST",
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ password }),
  });

  if (res.status === 403 || res.status === 401) {
    throw new Error("Wrong password");
  }

  if (!res.ok) {
    throw new Error("Verification failed");
  }

  return res.json();
}

export async function deleteDocument(key: string): Promise<boolean> {
  await ensureSession();

  const res = await fetch(`${TEXT_API}/?key=${key}`, {
    method: "DELETE",
    credentials: "include",
  });

  return res.status === 204;
}