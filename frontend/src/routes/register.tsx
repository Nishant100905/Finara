import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { motion } from "framer-motion";
import { useMemo, useState } from "react";
import { toast } from "sonner";
import { Eye, EyeOff, Loader2, Mail, Lock, User } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { BrandMark } from "@/components/common/BrandMark";
import { useAuth } from "@/context/AuthContext";
import { cn } from "@/lib/utils";

export const Route = createFileRoute("/register")({
  component: RegisterPage,
  head: () => ({
    meta: [{ title: "Create your account — Finara" }, { name: "description", content: "Create your free Finara account." }],
  }),
});

function scorePassword(p: string) {
  let score = 0;
  if (p.length >= 8) score++;
  if (/[A-Z]/.test(p)) score++;
  if (/[0-9]/.test(p)) score++;
  if (/[^A-Za-z0-9]/.test(p)) score++;
  return score; // 0..4
}

function RegisterPage() {
  const navigate = useNavigate();
  const { register } = useAuth();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [show, setShow] = useState(false);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState<string | null>(null);

  const strength = useMemo(() => scorePassword(password), [password]);
  const strengthLabel = ["Very weak", "Weak", "Okay", "Strong", "Excellent"][strength];
  const strengthColor = ["bg-destructive", "bg-destructive", "bg-warning", "bg-primary", "bg-success"][strength];

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErr(null);
    if (name.trim().length < 2) return setErr("Please enter your name");
    if (!/^\S+@\S+\.\S+$/.test(email)) return setErr("Enter a valid email address");
    if (strength < 2) return setErr("Choose a stronger password");
    if (password !== confirm) return setErr("Passwords don't match");
    setLoading(true);
    try {
      await register(name.trim(), email, password);
      toast.success("Welcome to Finara!");
      navigate({ to: "/dashboard" });
    } catch {
      setErr("Something went wrong. Try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid min-h-dvh lg:grid-cols-2">
      <div className="flex items-center justify-center p-6 sm:p-10">
        <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.35 }} className="w-full max-w-md">
          <div className="mb-8"><BrandMark /></div>
          <h2 className="text-2xl font-semibold tracking-tight">Create your account</h2>
          <p className="mt-1 text-sm text-muted-foreground">A minute to sign up. A lifetime of financial clarity.</p>

          <form onSubmit={submit} className="mt-8 space-y-4">
            <div className="space-y-1.5">
              <Label htmlFor="name">Full name</Label>
              <div className="relative">
                <User className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                <Input id="name" autoComplete="name" value={name} onChange={(e) => setName(e.target.value)} className="h-11 pl-9" placeholder="Riya Sharma" />
              </div>
            </div>
            <div className="space-y-1.5">
              <Label htmlFor="email">Email</Label>
              <div className="relative">
                <Mail className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                <Input id="email" autoComplete="email" value={email} onChange={(e) => setEmail(e.target.value)} className="h-11 pl-9" placeholder="you@example.com" />
              </div>
            </div>
            <div className="space-y-1.5">
              <Label htmlFor="password">Password</Label>
              <div className="relative">
                <Lock className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                <Input id="password" type={show ? "text" : "password"} autoComplete="new-password" value={password} onChange={(e) => setPassword(e.target.value)} className="h-11 pl-9 pr-10" />
                <button type="button" aria-label={show ? "Hide password" : "Show password"} onClick={() => setShow((s) => !s)} className="absolute right-2 top-1/2 -translate-y-1/2 rounded-md p-1.5 text-muted-foreground hover:bg-white/5">
                  {show ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </button>
              </div>
              {password && (
                <div className="pt-1">
                  <div className="flex h-1.5 gap-1">
                    {[0,1,2,3].map((i) => (
                      <div key={i} className={cn("flex-1 rounded-full transition", i < strength ? strengthColor : "bg-white/10")} />
                    ))}
                  </div>
                  <div className="mt-1 text-xs text-muted-foreground">{strengthLabel}</div>
                </div>
              )}
            </div>
            <div className="space-y-1.5">
              <Label htmlFor="confirm">Confirm password</Label>
              <Input id="confirm" type={show ? "text" : "password"} value={confirm} onChange={(e) => setConfirm(e.target.value)} className="h-11" />
            </div>

            {err && <div className="rounded-lg border border-destructive/30 bg-destructive/10 px-3 py-2 text-sm text-destructive">{err}</div>}

            <Button type="submit" disabled={loading} className="h-11 w-full gradient-brand text-primary-foreground hover:opacity-95">
              {loading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : null}
              Create account
            </Button>

            <p className="pt-4 text-center text-sm text-muted-foreground">
              Already have an account?{" "}
              <Link to="/login" className="text-primary hover:underline">Sign in</Link>
            </p>
          </form>
        </motion.div>
      </div>

      <div className="relative hidden overflow-hidden lg:block">
        <div className="absolute inset-0 bg-gradient-to-tl from-accent/25 via-primary/20 to-transparent" />
        <div className="relative flex h-full flex-col justify-center p-10">
          <h1 className="max-w-lg text-4xl font-semibold tracking-tight">
            Built for people who take their <span className="gradient-text">money seriously</span>.
          </h1>
          <ul className="mt-8 space-y-4 text-muted-foreground">
            {[
              "Bank-grade encryption. Your data never leaves your control.",
              "AI-powered insights across stocks, mutual funds, crypto & real estate.",
              "Goal tracking with monthly contribution planning.",
              "A private assistant that actually understands your finances.",
            ].map((f) => (
              <li key={f} className="flex items-start gap-3">
                <span className="mt-1 grid h-5 w-5 place-items-center rounded-full gradient-brand text-primary-foreground text-[10px]">✓</span>
                <span className="text-foreground/80">{f}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
