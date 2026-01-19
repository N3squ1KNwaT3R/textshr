const SESSION_API = "/api/session"; 

export async function initSession() {
  try {
    const res = await fetch(`${SESSION_API}/create`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({}), 
    });

    if (res.ok) {
      console.log("Session created successfully!");
      return true;
    }
    
    if (res.status === 409) {
      console.log("Session already exists (it's ok)");
      return true;
    }

    console.error("- Session init failed:", res.status);
    return false;
  } catch (error) {
    console.error("- Session network error:", error);
    return false;
  }
}