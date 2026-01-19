"use client";

import { useEffect, useRef } from "react";
import { initSession } from "@/lib/session-api";
import { toast } from "sonner";

export function SessionProvider({ children }: { children: React.ReactNode }) {
  const initialized = useRef(false);

  useEffect(() => {
    if (!initialized.current) {
      initialized.current = true;
      initSession().then((success) => {
        if (!success) {
           console.warn("Could not establish session cookie");
        }
      });
    }
  }, []);

  return <>{children}</>;
}