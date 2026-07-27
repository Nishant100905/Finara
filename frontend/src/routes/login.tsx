import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { motion } from "framer-motion";
import { useEffect, useState } from "react";
import { toast } from "sonner";
import { Eye, EyeOff, Loader2, Mail, Lock } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import { Separator } from "@/components/ui/separator";
import { BrandMark } from "@/components/common/BrandMark";
import { useAuth } from "@/context/AuthContext";

export const Route = createFileRoute("/login")({
  component: LoginPage,
  head: () => ({
    meta: [{ title: "Sign in — Finara" }, { name: "description", content: "Sign in to your Finara account." }],
  }),
});

function LoginPage() {
  const navigate = useNavigate();
  const { user, ready, login } = useAuth();
  const [email, setEmail] = useState("demo@finara.ai");
  const [password, setPassword] = useState("demo1234");
  const [show, setShow] = useState(false);
  const [remember, setRemember] = useState(true);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    // Same source of truth as the rest of the app (mockAuth).
    // Using backend.getToken() here caused an infinite redirect loop
    // when the two stores fell out of sync.
    if (ready && user) {
      navigate({ to: "/dashboard" });
    }
  }, [ready, user, navigate]);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErr(null);
    if (!/^\S+@\S+\.\S+$/.test(email)) return setErr("Enter a valid email address");
    if (password.length < 6) return setErr("Password must be at least 6 characters");
    setLoading(true);
    try {
      await login(email, password);
      toast.success("Welcome back to Finara");
      navigate({ to: "/dashboard" });
    } catch {
      setErr("Something went wrong. Try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative grid min-h-dvh lg:grid-cols-2">
      {/* Left: hero */}
      <div className="relative hidden overflow-hidden lg:block">
        <div className="absolute inset-0 bg-gradient-to-br from-primary/25 via-accent/20 to-transparent" />
        <div
          className="absolute inset-0 opacity-40"
          style={{
            backgroundImage:
              "radial-gradient(600px 300px at 20% 30%, oklch(0.72 0.16 165 / .35), transparent), radial-gradient(500px 320px at 80% 70%, oklch(0.68 0.18 285 / .3), transparent)",
          }}
        />
        <div className="relative flex h-full flex-col justify-between p-10">
          <BrandMark />
          <div>
            <motion.h1
              initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}
              className="max-w-md text-4xl font-semibold tracking-tight"
            >
              Your money, <span className="gradient-text">clearer</span> than ever.
            </motion.h1>
            <p className="mt-3 max-w-md text-muted-foreground">
              Finara is the AI financial advisor that watches your accounts, plans your goals, and answers every "what if" — instantly.
            </p>
            <div className="mt-8 grid grid-cols-3 gap-3">
              {[
                { k: "Net Worth", v: "₹14.7L" },
                { k: "Savings Rate", v: "36%" },
                { k: "Goals on track", v: "4 / 5" },
              ].map((s) => (
                <div key={s.k} className="glass rounded-2xl p-4">
                  <div className="text-xs text-muted-foreground">{s.k}</div>
                  <div className="mt-1 text-xl font-semibold">{s.v}</div>
                </div>
              ))}
            </div>
          </div>
          <p className="text-xs text-muted-foreground">© {new Date().getFullYear()} Finara Inc.</p>
        </div>
      </div>

      {/* Right: form */}
      <div className="flex items-center justify-center p-6 sm:p-10">
        <motion.div
          initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.35 }}
          className="w-full max-w-md"
        >
          <div className="mb-8 lg:hidden"><BrandMark /></div>
          <h2 className="text-2xl font-semibold tracking-tight">Sign in to Finara</h2>
          <p className="mt-1 text-sm text-muted-foreground">Welcome back. Enter your details to continue.</p>

          <form onSubmit={submit} className="mt-8 space-y-4">
            <div className="space-y-1.5">
              <Label htmlFor="email">Email</Label>
              <div className="relative">
                <Mail className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                <Input id="email" autoComplete="email" value={email} onChange={(e) => setEmail(e.target.value)} className="h-11 pl-9" placeholder="you@example.com" />
              </div>
            </div>
            <div className="space-y-1.5">
              <div className="flex items-center justify-between">
                <Label htmlFor="password">Password</Label>
                <button type="button" className="text-xs text-primary hover:underline" onClick={() => toast.info("Password reset link sent (demo)")}>
                  Forgot?
                </button>
              </div>
              <div className="relative">
                <Lock className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                <Input id="password" type={show ? "text" : "password"} autoComplete="current-password" value={password} onChange={(e) => setPassword(e.target.value)} className="h-11 pl-9 pr-10" />
                <button type="button" aria-label={show ? "Hide password" : "Show password"} onClick={() => setShow((s) => !s)} className="absolute right-2 top-1/2 -translate-y-1/2 rounded-md p-1.5 text-muted-foreground hover:bg-white/5">
                  {show ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </button>
              </div>
            </div>

            <div className="flex items-center gap-2">
              <Checkbox id="remember" checked={remember} onCheckedChange={(v) => setRemember(v === true)} />
              <Label htmlFor="remember" className="text-sm text-muted-foreground">Remember me for 30 days</Label>
            </div>

            {err && <div className="rounded-lg border border-destructive/30 bg-destructive/10 px-3 py-2 text-sm text-destructive">{err}</div>}

            <Button type="submit" disabled={loading} className="h-11 w-full gradient-brand text-primary-foreground hover:opacity-95">
              {loading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : null}
              Sign in
            </Button>

            <div className="relative py-2">
              <Separator />
              <span className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 bg-background px-3 text-xs text-muted-foreground">or continue with</span>
            </div>

            <div className="grid grid-cols-3 gap-2">
              {["Google", "Apple", "GitHub"].map((p) => (
                <Button key={p} type="button" variant="outline" className="h-11 border-white/10 bg-white/[0.03]" onClick={() => toast.info(`${p} sign-in (UI only)`)}>
                  {p}
                </Button>
              ))}
            </div>

            <p className="pt-4 text-center text-sm text-muted-foreground">
              New here?{" "}
              <Link to="/register" className="text-primary hover:underline">Create an account</Link>
            </p>
          </form>
        </motion.div>
      </div>
    </div>
  );
}
