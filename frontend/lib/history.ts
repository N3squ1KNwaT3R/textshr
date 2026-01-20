export interface HistoryItem {
  key: string;
  date: string;
  summary?: string;
  isOwner?: boolean; 
}

const STORAGE_KEY = "textshare_history";

export function addToHistory(key: string, summary?: string, isOwner?: boolean) {
  if (typeof window === "undefined") return;

  const currentRaw = localStorage.getItem(STORAGE_KEY);
  let history: HistoryItem[] = currentRaw ? JSON.parse(currentRaw) : [];

  const existingItem = history.find((item) => item.key === key);
  
  const finalIsOwner = isOwner !== undefined ? isOwner : (existingItem?.isOwner || false);

  history = history.filter((item) => item.key !== key);

  history.unshift({
    key,
    date: new Date().toISOString(),
    summary: summary || "",
    isOwner: finalIsOwner,
  });

  if (history.length > 10) history = history.slice(0, 10);

  localStorage.setItem(STORAGE_KEY, JSON.stringify(history));
}

export function getHistory(): HistoryItem[] {
  if (typeof window === "undefined") return [];
  const currentRaw = localStorage.getItem(STORAGE_KEY);
  return currentRaw ? JSON.parse(currentRaw) : [];
}

export function checkIsOwner(key: string): boolean {
  if (typeof window === "undefined") return false;
  const history = getHistory();
  const item = history.find((i) => i.key === key);
  return item?.isOwner || false;
}

export function removeFromHistory(key: string) {
    if (typeof window === "undefined") return;
    const currentRaw = localStorage.getItem(STORAGE_KEY);
    if (!currentRaw) return;
    
    let history: HistoryItem[] = JSON.parse(currentRaw);
    history = history.filter((item) => item.key !== key);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(history));
    return history;
}