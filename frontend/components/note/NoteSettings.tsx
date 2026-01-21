import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Checkbox } from "@/components/ui/checkbox";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Clock, Lock, FileText, EyeOff, Trash2 } from "lucide-react";

interface NoteSettingsProps {
  ttl: string;
  setTtl: (val: string) => void;
  password: string;
  setPassword: (val: string) => void;
  summary: string;
  setSummary: (val: string) => void;
  burnAfterRead: boolean;
  setBurnAfterRead: (val: boolean) => void;
  isNew: boolean;
  onDelete: () => void;
  onClose: () => void;
}

export function NoteSettings({
  ttl,
  setTtl,
  password,
  setPassword,
  summary,
  setSummary,
  burnAfterRead,
  setBurnAfterRead,
  isNew,
  onDelete,
  onClose,
}: NoteSettingsProps) {
  return (
    <div className="absolute top-[70px] right-4 w-full max-w-sm bg-neutral-900 border border-neutral-800 rounded-xl shadow-2xl p-5 z-30 animate-in slide-in-from-top-2 fade-in duration-200">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-semibold text-lg">Settings</h3>
        <Button variant="ghost" size="sm" onClick={onClose} className="h-6 w-6 p-0">
          ✕
        </Button>
      </div>

      <div className="space-y-4">
        <div className="space-y-2">
          <label className="text-sm text-neutral-400 flex items-center gap-2">
            <Clock className="w-4 h-4" /> Time to live (TTL)
          </label>
          <Select value={ttl} onValueChange={setTtl}>
            <SelectTrigger className="w-full bg-neutral-950 border-neutral-800">
              <SelectValue placeholder="Select TTL" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="600">10 minutes</SelectItem>
              <SelectItem value="3600">1 hour</SelectItem>
              <SelectItem value="28800">8 hours</SelectItem>
              <SelectItem value="86400">24 hours</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-2">
          <label className="text-sm text-neutral-400 flex items-center gap-2">
            <Lock className="w-4 h-4" /> Password (optional)
          </label>
          <Input
            type="password"
            placeholder="Enter for protection..."
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="bg-neutral-950 border-neutral-800"
          />
        </div>


        <div className="flex items-center justify-between p-3 bg-neutral-950 rounded-lg border border-neutral-800">
          <div className="space-y-0.5">
            <label className="text-sm font-medium flex items-center gap-2 text-red-400">
              <EyeOff className="w-4 h-4" /> One-time read
            </label>
          </div>
          <Checkbox
            checked={burnAfterRead}
            onCheckedChange={(checked) => setBurnAfterRead(checked as boolean)}
          />
        </div>

        

        {!isNew && (
          <>
          
          <hr className="border-neutral-800" />
          <Button
            variant="destructive"
            className="w-full bg-red-950/50 hover:bg-red-900 text-red-500 border border-red-900/50"
            onClick={onDelete}
          >
            <Trash2 className="w-4 h-4 mr-2" /> Delete document
          </Button>
          </>
        )}
      </div>
    </div>
  );
}