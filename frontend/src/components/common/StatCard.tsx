import { cn } from "@/lib/utils";
import { motion } from "framer-motion";
import type { ReactNode } from "react";

type Props = {
  label: string;
  value: ReactNode;
  hint?: ReactNode;
  icon?: ReactNode;
  changePct?: number;
  accent?: "primary" | "accent" | "success" | "warning" | "destructive";
  className?: string;
};

const accentBg: Record<NonNullable<Props["accent"]>, string> = {
  primary: "from-primary/25 to-primary/0",
  accent: "from-accent/25 to-accent/0",
  success: "from-success/25 to-success/0",
  warning: "from-warning/25 to-warning/0",
  destructive: "from-destructive/25 to-destructive/0",
};

export function StatCard({ label, value, hint, icon, changePct, accent = "primary", className }: Props) {
  const up = (changePct ?? 0) >= 0;
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ y: -3 }}
      transition={{ duration: 0.35, ease: [0.2, 0.7, 0.2, 1] }}
      className={cn(
        "glass relative overflow-hidden rounded-2xl p-5 shadow-elegant",
        className,
      )}
    >
      <div className={cn("pointer-events-none absolute -top-16 -right-16 h-48 w-48 rounded-full bg-gradient-to-br blur-2xl opacity-70", accentBg[accent])} />
      <div className="relative flex items-start justify-between gap-3">
        <div className="min-w-0">
          <div className="text-xs font-medium uppercase tracking-wider text-muted-foreground">{label}</div>
          <div className="mt-2 truncate text-2xl font-semibold tracking-tight text-foreground">{value}</div>
          {hint ? <div className="mt-1 text-xs text-muted-foreground">{hint}</div> : null}
        </div>
        {icon ? (
          <div className="grid h-10 w-10 shrink-0 place-items-center rounded-xl bg-white/5 text-foreground/90 ring-1 ring-white/10">
            {icon}
          </div>
        ) : null}
      </div>
      {typeof changePct === "number" ? (
        <div className="relative mt-4 inline-flex items-center gap-1 rounded-full bg-white/5 px-2 py-1 text-xs">
          <span className={up ? "text-success" : "text-destructive"}>
            {up ? "▲" : "▼"} {Math.abs(changePct).toFixed(2)}%
          </span>
          <span className="text-muted-foreground">vs last month</span>
        </div>
      ) : null}
    </motion.div>
  );
}
