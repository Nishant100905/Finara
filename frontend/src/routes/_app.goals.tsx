import { createFileRoute } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { motion } from "framer-motion";
import { Plus, Pencil, Trash2, Calendar, Wallet } from "lucide-react";
import { api } from "@/services/api";
import type { Goal } from "@/data/mock";
import { GlassCard } from "@/components/common/GlassCard";
import { SectionHeader } from "@/components/common/SectionHeader";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Skeleton } from "@/components/ui/skeleton";
import { formatCurrency, formatDate } from "@/lib/format";
import { toast } from "sonner";

export const Route = createFileRoute("/_app/goals")({
  component: GoalsPage,
  head: () => ({ meta: [{ title: "Goals — Finara" }] }),
});

const EMOJIS = ["🏡","🚗","🌴","🎓","🛟","💍","🗾","🏝️","🚀","👶"];

function GoalsPage() {
  const { data, isLoading } = useQuery({ queryKey: ["goals"], queryFn: api.getGoals });
  const [goals, setGoals] = useState<Goal[]>([]);
  const [open, setOpen] = useState(false);
  const [editing, setEditing] = useState<Goal | null>(null);

  // Sync from query once loaded
  if (data && goals.length === 0) queueMicrotask(() => setGoals(data));

  const totalTarget = goals.reduce((s, g) => s + g.target, 0);
  const totalCurrent = goals.reduce((s, g) => s + g.current, 0);
  const overallPct = totalTarget ? Math.round((totalCurrent / totalTarget) * 100) : 0;

  const upsert = (g: Goal) => {
    setGoals((prev) => {
      const exists = prev.some((x) => x.id === g.id);
      return exists ? prev.map((x) => (x.id === g.id ? g : x)) : [g, ...prev];
    });
    toast.success(editing ? "Goal updated" : "Goal created");
    setEditing(null); setOpen(false);
  };

  const remove = (id: string) => {
    setGoals((prev) => prev.filter((g) => g.id !== id));
    toast.success("Goal deleted");
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h1 className="text-3xl font-semibold tracking-tight sm:text-4xl">Financial goals</h1>
          <p className="mt-1 text-sm text-muted-foreground">Plan, track, and hit every milestone.</p>
        </div>
        <Dialog open={open} onOpenChange={(v) => { setOpen(v); if (!v) setEditing(null); }}>
          <DialogTrigger asChild>
            <Button className="gradient-brand text-primary-foreground"><Plus className="mr-2 h-4 w-4" />New goal</Button>
          </DialogTrigger>
          <GoalDialog goal={editing} onSave={upsert} />
        </Dialog>
      </div>

      <GlassCard>
        <div className="grid gap-6 sm:grid-cols-3">
          <ProgressRing value={overallPct} label="Overall progress" />
          <div className="space-y-1">
            <div className="text-xs uppercase tracking-wider text-muted-foreground">Saved so far</div>
            <div className="text-2xl font-semibold">{formatCurrency(totalCurrent)}</div>
            <div className="text-sm text-muted-foreground">of {formatCurrency(totalTarget)}</div>
          </div>
          <div className="space-y-1">
            <div className="text-xs uppercase tracking-wider text-muted-foreground">Monthly contributions</div>
            <div className="text-2xl font-semibold">
              {formatCurrency(goals.reduce((s, g) => s + g.monthlyContribution, 0))}
            </div>
            <div className="text-sm text-muted-foreground">Across {goals.length} goals</div>
          </div>
        </div>
      </GlassCard>

      <SectionHeader title="Your goals" description="Tap a goal to edit contributions or deadlines." />
      {isLoading ? (
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {Array.from({ length: 3 }).map((_, i) => <Skeleton key={i} className="h-52 rounded-2xl" />)}
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {goals.map((g, i) => (
            <motion.div key={g.id} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.04 }}>
              <GoalCard goal={g} onEdit={() => { setEditing(g); setOpen(true); }} onDelete={() => remove(g.id)} />
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
}

function GoalCard({ goal, onEdit, onDelete }: { goal: Goal; onEdit: () => void; onDelete: () => void }) {
  const pct = Math.min(100, Math.round((goal.current / goal.target) * 100));
  const remaining = Math.max(0, goal.target - goal.current);
  const monthsLeft = Math.max(1, Math.ceil((new Date(goal.deadline).getTime() - Date.now()) / (1000 * 60 * 60 * 24 * 30)));
  const projectedTotal = goal.current + goal.monthlyContribution * monthsLeft;
  const onTrack = projectedTotal >= goal.target;

  return (
    <div className="glass hover-lift group relative overflow-hidden rounded-2xl p-5">
      <div className="pointer-events-none absolute -right-10 -top-10 h-32 w-32 rounded-full bg-primary/20 blur-2xl" />
      <div className="relative flex items-start justify-between">
        <div className="flex items-center gap-3">
          <div className="grid h-12 w-12 place-items-center rounded-2xl bg-white/5 text-2xl">{goal.emoji}</div>
          <div>
            <div className="text-base font-semibold">{goal.title}</div>
            <div className="text-xs text-muted-foreground">{goal.category}</div>
          </div>
        </div>
        <div className="flex gap-1 opacity-0 transition group-hover:opacity-100">
          <Button size="icon" variant="ghost" onClick={onEdit} aria-label="Edit"><Pencil className="h-4 w-4" /></Button>
          <Button size="icon" variant="ghost" onClick={onDelete} aria-label="Delete"><Trash2 className="h-4 w-4" /></Button>
        </div>
      </div>

      <div className="relative mt-5 flex items-center gap-4">
        <ProgressRing value={pct} size={80} stroke={7} />
        <div className="min-w-0 flex-1">
          <div className="text-lg font-semibold">{formatCurrency(goal.current)}</div>
          <div className="text-xs text-muted-foreground">of {formatCurrency(goal.target)}</div>
          <div className="mt-1 text-xs">
            <span className={onTrack ? "text-success" : "text-warning"}>
              {onTrack ? "On track" : "Needs boost"}
            </span>
            <span className="text-muted-foreground"> · {formatCurrency(remaining, { compact: true })} to go</span>
          </div>
        </div>
      </div>

      <div className="relative mt-4 grid grid-cols-2 gap-2 text-xs text-muted-foreground">
        <div className="flex items-center gap-1.5"><Calendar className="h-3.5 w-3.5" />{formatDate(goal.deadline)}</div>
        <div className="flex items-center gap-1.5"><Wallet className="h-3.5 w-3.5" />{formatCurrency(goal.monthlyContribution, { compact: true })}/mo</div>
      </div>
    </div>
  );
}

function ProgressRing({
  value, size = 128, stroke = 10, label,
}: { value: number; size?: number; stroke?: number; label?: string }) {
  const r = (size - stroke) / 2;
  const c = 2 * Math.PI * r;
  const off = c - (value / 100) * c;
  return (
    <div className="relative" style={{ width: size, height: size }}>
      <svg width={size} height={size}>
        <circle cx={size/2} cy={size/2} r={r} stroke="rgba(255,255,255,0.08)" strokeWidth={stroke} fill="none" />
        <motion.circle
          cx={size/2} cy={size/2} r={r}
          stroke="url(#ringG)" strokeWidth={stroke} strokeLinecap="round" fill="none"
          strokeDasharray={c}
          initial={{ strokeDashoffset: c }}
          animate={{ strokeDashoffset: off }}
          transition={{ duration: 1, ease: [0.2, 0.7, 0.2, 1] }}
          transform={`rotate(-90 ${size/2} ${size/2})`}
        />
        <defs>
          <linearGradient id="ringG" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stopColor="var(--color-primary)" />
            <stop offset="100%" stopColor="var(--color-accent)" />
          </linearGradient>
        </defs>
      </svg>
      <div className="absolute inset-0 grid place-items-center">
        <div className="text-center">
          <div className="text-2xl font-semibold">{value}%</div>
          {label && <div className="text-[10px] uppercase tracking-wider text-muted-foreground">{label}</div>}
        </div>
      </div>
    </div>
  );
}

function GoalDialog({ goal, onSave }: { goal: Goal | null; onSave: (g: Goal) => void }) {
  const [title, setTitle] = useState(goal?.title ?? "");
  const [emoji, setEmoji] = useState(goal?.emoji ?? EMOJIS[0]);
  const [target, setTarget] = useState(goal?.target ?? 100000);
  const [current, setCurrent] = useState(goal?.current ?? 0);
  const [monthly, setMonthly] = useState(goal?.monthlyContribution ?? 5000);
  const [deadline, setDeadline] = useState(goal?.deadline ?? new Date(Date.now() + 365 * 86400000).toISOString().slice(0, 10));
  const [category, setCategory] = useState<Goal["category"]>(goal?.category ?? "Travel");

  const submit = () => {
    if (!title.trim() || target <= 0) return toast.error("Please fill title and target");
    onSave({
      id: goal?.id ?? "g_" + Math.random().toString(36).slice(2, 8),
      title: title.trim(), emoji, target, current, deadline, monthlyContribution: monthly, category,
    });
  };

  return (
    <DialogContent className="max-w-lg">
      <DialogHeader>
        <DialogTitle>{goal ? "Edit goal" : "Create a new goal"}</DialogTitle>
      </DialogHeader>
      <div className="grid gap-4 py-2">
        <div className="grid grid-cols-[auto_1fr] gap-3">
          <div>
            <Label>Icon</Label>
            <div className="mt-1.5 flex flex-wrap gap-1">
              {EMOJIS.map((e) => (
                <button key={e} onClick={() => setEmoji(e)}
                  className={`grid h-9 w-9 place-items-center rounded-xl border ${emoji === e ? "border-primary/40 bg-primary/10" : "border-white/10 bg-white/[0.03]"}`}>
                  <span className="text-lg">{e}</span>
                </button>
              ))}
            </div>
          </div>
          <div>
            <Label>Title</Label>
            <Input value={title} onChange={(e) => setTitle(e.target.value)} className="mt-1.5" placeholder="Down payment" />
          </div>
        </div>
        <div className="grid grid-cols-2 gap-3">
          <div>
            <Label>Target amount</Label>
            <Input type="number" value={target} onChange={(e) => setTarget(Number(e.target.value))} className="mt-1.5" />
          </div>
          <div>
            <Label>Saved so far</Label>
            <Input type="number" value={current} onChange={(e) => setCurrent(Number(e.target.value))} className="mt-1.5" />
          </div>
          <div>
            <Label>Monthly contribution</Label>
            <Input type="number" value={monthly} onChange={(e) => setMonthly(Number(e.target.value))} className="mt-1.5" />
          </div>
          <div>
            <Label>Deadline</Label>
            <Input type="date" value={deadline} onChange={(e) => setDeadline(e.target.value)} className="mt-1.5" />
          </div>
        </div>
        <div>
          <Label>Category</Label>
          <Select value={category} onValueChange={(v) => setCategory(v as Goal["category"])}>
            <SelectTrigger className="mt-1.5"><SelectValue /></SelectTrigger>
            <SelectContent>
              {["Retirement","Home","Travel","Education","Emergency","Vehicle"].map((c) => <SelectItem key={c} value={c}>{c}</SelectItem>)}
            </SelectContent>
          </Select>
        </div>
      </div>
      <DialogFooter>
        <Button onClick={submit} className="gradient-brand text-primary-foreground">{goal ? "Save changes" : "Create goal"}</Button>
      </DialogFooter>
    </DialogContent>
  );
}
