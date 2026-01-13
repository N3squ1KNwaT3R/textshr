const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

export interface DocumentData {
  id: string;
  content: string;
  updatedAt: Date;
}

export const getDocument = async (id: string): Promise<DocumentData | null> => {
  await delay(600);
  
  const data = localStorage.getItem(`doc_${id}`);
  if (!data) return null;
  
  return JSON.parse(data);
};

export const saveDocument = async (id: string, content: string): Promise<void> => {
  await delay(400);
  
  const payload: DocumentData = {
    id,
    content,
    updatedAt: new Date(),
  };
  
  localStorage.setItem(`doc_${id}`, JSON.stringify(payload));
};