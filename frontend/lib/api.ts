export interface TextDocument {
  text: string;
  size?: number;
  summary?: string;
  password_required?: boolean;
}

interface CreateResponse {
  key: string;
  status: string;
}
export interface SaveOptions {
  text: string;
  ttl: number;
  password?: string;
  only_one_read: boolean; 
  summary?: string;
}

const API_BASE = "/api/text"; 

export async function getDocument(key: string): Promise<TextDocument | null> {
  const params = new URLSearchParams({ key });
  
  const res = await fetch(`${API_BASE}/?${params}`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
    cache: "no-store",
    credentials: "include", 
  });

  if (res.status === 404) return null;
  if (!res.ok) throw new Error("Failed to fetch");

  return res.json();
}

export async function verifyPassword(key: string, password: string): Promise<TextDocument> {
  const params = new URLSearchParams({ key });
  
  const res = await fetch(`${API_BASE}/verify?${params}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify({ password }),
  });

  if (res.status === 403) {
    throw new Error("Wrong password");
  }

  if (!res.ok) {
    throw new Error("Verification error");
  }

  return res.json();
}

export async function deleteDocument(key: string): Promise<boolean> {
  const params = new URLSearchParams({ key });
  
  const res = await fetch(`${API_BASE}/?${params}`, {
    method: "DELETE",
    credentials: "include", 
  });

  return res.status === 204;
}


export async function saveDocument(
  options: SaveOptions,
  currentKey?: string,
  isNew: boolean = true
): Promise<string> {
  const bodyData = JSON.stringify({
    text: options.text,
    ttl: Number(options.ttl),
    only_one_read: options.only_one_read,
    password: options.password || undefined,
    summary: options.summary || undefined
  });

  if (isNew) {
    const res = await fetch(`${API_BASE}/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include", 
      body: bodyData,
    });

    if (!res.ok) {
        throw new Error("Failed to create");
    }
    
    const data = await res.json();
    return data.key;
  } 
  else if (currentKey) {
    const params = new URLSearchParams({ key: currentKey });
    
    await fetch(`${API_BASE}/?${params}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: bodyData,
    });
    
    return currentKey;
  }
  
  throw new Error("Invalid save state");
}