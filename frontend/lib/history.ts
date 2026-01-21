export interface HistoryItem {
  key: string;
  date: string;
  summary?: string;
  isOwner?: boolean; 
  ttl?: number;
}

const STORAGE_KEY = "textshare_history";

const notifyHistoryChange = () => {
  if (typeof window !== "undefined") {
    window.dispatchEvent(new Event("history-change"));
  }
};

export function addToHistory(key: string, summary?: string, isOwner?: boolean, ttl?: number) {
  if (typeof window === "undefined") return;

  const currentRaw = localStorage.getItem(STORAGE_KEY);
  let history: HistoryItem[] = currentRaw ? JSON.parse(currentRaw) : [];

  const existingItem = history.find((item) => item.key === key);
  const finalIsOwner = isOwner !== undefined ? isOwner : (existingItem?.isOwner || false);
  
  history = history.filter((item) => item.key !== key);

  history.unshift({
    key,
    date: existingItem ? existingItem.date : new Date().toISOString(),
    summary: summary || "",
    isOwner: finalIsOwner,
    ttl: ttl, 
  });

  if (history.length > 50) history = history.slice(0, 50);

  localStorage.setItem(STORAGE_KEY, JSON.stringify(history));
  
  notifyHistoryChange();
}

export function getHistory(): HistoryItem[] {
  if (typeof window === "undefined") return [];
  const currentRaw = localStorage.getItem(STORAGE_KEY);
  if (!currentRaw) return [];

  let history: HistoryItem[] = JSON.parse(currentRaw);
  const now = Date.now();
  let changed = false;

  const validHistory = history.filter((item) => {
    if (!item.ttl) return true;
    const createdTime = new Date(item.date).getTime();
    const expiryTime = createdTime + (item.ttl * 1000);
    if (now > expiryTime) {
      changed = true;
      return false;
    }
    return true;
  });

  if (changed) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(validHistory));
  }

  return validHistory;
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
    
    notifyHistoryChange();
}