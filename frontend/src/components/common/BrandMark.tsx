import { Link } from "@tanstack/react-router";
import { motion } from "framer-motion";
import { Sparkles } from "lucide-react";

export function BrandMark({ className = "" }: { className?: string }) {
  return (
    <Link to="/dashboard" className={`group inline-flex items-center gap-2 ${className}`}>
      <motion.span
        initial={{ rotate: -12, scale: 0.95 }}
        animate={{ rotate: 0, scale: 1 }}
        transition={{ type: "spring", stiffness: 220, damping: 18 }}
        className="grid h-9 w-9 place-items-center rounded-xl gradient-brand text-primary-foreground shadow-glow"
      >
        <Sparkles className="h-4 w-4" />
      </motion.span>
      <span className="text-lg font-semibold tracking-tight">
        Fin<span className="gradient-text">ara</span>
      </span>
    </Link>
  );
}
