import { cn } from "@/lib/utils";
import type { ReactNode, HTMLAttributes } from "react";

export function GlassCard({
  children,
  className,
  ...rest
}: { children: ReactNode; className?: string } & HTMLAttributes<HTMLDivElement>) {
  return (
    <div className={cn("glass rounded-2xl p-5 shadow-elegant", className)} {...rest}>
      {children}
    </div>
  );
}
