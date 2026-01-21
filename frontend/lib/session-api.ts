export async function ensureSession() {
  const res = await fetch("/api/session/create", {
    method: "POST",
    credentials: "include",
  });

  if (res.status === 409) {
    return true;
  }

  if (!res.ok) {
    throw new Error("Session init failed");
  }

  return true;
}
