import { ReactNode } from "react";

interface DialogProps {
  open: boolean;
  onClose: () => void;
  title: string;
  children: ReactNode;
  tone?: "success" | "error";
}

export default function Dialog({ open, onClose, title, children, tone = "success" }: DialogProps) {
  if (!open) return null;

  const toneClasses =
    tone === "success"
      ? "border-emerald-400 bg-emerald-50 text-emerald-800"
      : "border-red-400 bg-red-50 text-red-800";

  const iconClasses =
    tone === "success" ? "bg-emerald-500" : "bg-red-500";

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 px-4">
      <div className="bg-white rounded-xl shadow-xl w-full max-w-md overflow-hidden border border-slate-200">
        <div className={`px-5 py-4 border-b flex items-center gap-3 ${toneClasses}`}>
          <span className={`h-7 w-7 rounded-full ${iconClasses} text-white flex items-center justify-center text-sm font-bold`}>
            {tone === "success" ? "✓" : "!"}
          </span>
          <h3 className="font-semibold">{title}</h3>
        </div>
        <div className="px-5 py-4 text-sm text-slate-700">{children}</div>
        <div className="px-5 py-3 bg-slate-50 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 text-sm font-medium rounded-md bg-govblue-700 text-white hover:bg-govblue-800 transition"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
