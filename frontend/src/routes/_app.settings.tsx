import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { useState } from "react";
import { toast } from "sonner";
import {
  User, Shield, Bell, Palette, Sparkles, Link2, Lock, AlertTriangle, LogOut,
} from "lucide-react";
import { GlassCard } from "@/components/common/GlassCard";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Separator } from "@/components/ui/separator";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { useAuth } from "@/context/AuthContext";

export const Route = createFileRoute("/_app/settings")({
  component: SettingsPage,
  head: () => ({ meta: [{ title: "Settings — Finara" }] }),
});

function SettingsPage() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-semibold tracking-tight sm:text-4xl">Settings</h1>
        <p className="mt-1 text-sm text-muted-foreground">Manage your profile, security, and preferences.</p>
      </div>

      <Tabs defaultValue="profile" className="space-y-6">
        <TabsList className="glass h-auto flex-wrap p-1">
          <TabsTrigger value="profile"><User className="mr-1.5 h-4 w-4" />Profile</TabsTrigger>
          <TabsTrigger value="security"><Shield className="mr-1.5 h-4 w-4" />Security</TabsTrigger>
          <TabsTrigger value="notifications"><Bell className="mr-1.5 h-4 w-4" />Notifications</TabsTrigger>
          <TabsTrigger value="appearance"><Palette className="mr-1.5 h-4 w-4" />Appearance</TabsTrigger>
          <TabsTrigger value="ai"><Sparkles className="mr-1.5 h-4 w-4" />AI</TabsTrigger>
          <TabsTrigger value="accounts"><Link2 className="mr-1.5 h-4 w-4" />Accounts</TabsTrigger>
          <TabsTrigger value="privacy"><Lock className="mr-1.5 h-4 w-4" />Privacy</TabsTrigger>
        </TabsList>

        <TabsContent value="profile">
          <GlassCard>
            <div className="flex flex-col gap-6 sm:flex-row sm:items-center">
              <Avatar className="h-20 w-20">
                <AvatarFallback className="text-2xl bg-gradient-to-br from-primary to-accent text-primary-foreground">
                  {user?.name?.[0]?.toUpperCase() ?? "U"}
                </AvatarFallback>
              </Avatar>
              <div className="flex-1">
                <div className="text-lg font-semibold">{user?.name}</div>
                <div className="text-sm text-muted-foreground">{user?.email}</div>
                <div className="mt-3 flex gap-2">
                  <Button size="sm" className="gradient-brand text-primary-foreground" onClick={() => toast.success("Upload dialog opened (demo)")}>Change photo</Button>
                  <Button size="sm" variant="outline" className="border-white/10 bg-white/[0.03]">Remove</Button>
                </div>
              </div>
            </div>
            <Separator className="my-6 bg-white/5" />
            <div className="grid gap-4 sm:grid-cols-2">
              <Field label="Full name" defaultValue={user?.name} />
              <Field label="Email" defaultValue={user?.email} />
              <Field label="Phone" placeholder="+91 98765 43210" />
              <Field label="Date of birth" type="date" />
            </div>
            <div className="mt-6 flex justify-end">
              <Button className="gradient-brand text-primary-foreground" onClick={() => toast.success("Profile saved")}>Save changes</Button>
            </div>
          </GlassCard>
        </TabsContent>

        <TabsContent value="security">
          <GlassCard>
            <SectionTitle title="Change password" />
            <div className="grid gap-4 sm:grid-cols-3">
              <Field label="Current password" type="password" />
              <Field label="New password" type="password" />
              <Field label="Confirm" type="password" />
            </div>
            <div className="mt-4"><Button className="gradient-brand text-primary-foreground">Update password</Button></div>

            <Separator className="my-6 bg-white/5" />
            <SectionTitle title="Two-factor authentication" />
            <Row title="Authenticator app" desc="Use an app like 1Password or Authy" />
            <Row title="SMS backup" desc="Receive a code via SMS" defaultChecked />

            <Separator className="my-6 bg-white/5" />
            <SectionTitle title="Sessions" />
            <div className="rounded-xl border border-white/10 bg-white/[0.03] p-4 text-sm">
              <div className="flex items-center justify-between">
                <div>
                  <div className="font-medium">Chrome — Mumbai, IN</div>
                  <div className="text-xs text-muted-foreground">Current session · Last active just now</div>
                </div>
                <Badge className="bg-success/15 text-success border-success/30">Active</Badge>
              </div>
            </div>
          </GlassCard>
        </TabsContent>

        <TabsContent value="notifications">
          <GlassCard>
            <SectionTitle title="Email" />
            <Row title="Weekly financial digest" desc="Every Monday morning" defaultChecked />
            <Row title="Goal milestones" desc="Notify when a goal crosses 25 / 50 / 75 / 100%" defaultChecked />
            <Row title="AI insights" desc="Personalized recommendations, twice a month" />
            <Separator className="my-6 bg-white/5" />
            <SectionTitle title="Push" />
            <Row title="Large transactions" desc="Alert for transactions over ₹25,000" defaultChecked />
            <Row title="Market anomalies" desc="Sharp moves in your watchlist" defaultChecked />
            <Row title="Bill reminders" desc="3 days before due date" />
          </GlassCard>
        </TabsContent>

        <TabsContent value="appearance">
          <GlassCard>
            <SectionTitle title="Theme" />
            <div className="grid gap-3 sm:grid-cols-3">
              {[
                { key: "dark",   label: "Dark",   sub: "Default" },
                { key: "midnight", label: "Midnight", sub: "Deeper blacks" },
                { key: "system", label: "System", sub: "Match device" },
              ].map((t) => (
                <button key={t.key}
                  className="glass rounded-2xl p-4 text-left transition hover:ring-1 hover:ring-primary/40">
                  <div className="mb-3 h-16 rounded-lg" style={{ background: "var(--gradient-brand)" }} />
                  <div className="text-sm font-medium">{t.label}</div>
                  <div className="text-xs text-muted-foreground">{t.sub}</div>
                </button>
              ))}
            </div>
            <Separator className="my-6 bg-white/5" />
            <div className="grid gap-4 sm:grid-cols-2">
              <div>
                <Label>Language</Label>
                <Select defaultValue="en-IN">
                  <SelectTrigger className="mt-1.5"><SelectValue /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="en-IN">English (India)</SelectItem>
                    <SelectItem value="en-US">English (US)</SelectItem>
                    <SelectItem value="hi-IN">हिन्दी</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Label>Currency</Label>
                <Select defaultValue="INR">
                  <SelectTrigger className="mt-1.5"><SelectValue /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="INR">Indian Rupee (₹)</SelectItem>
                    <SelectItem value="USD">US Dollar ($)</SelectItem>
                    <SelectItem value="EUR">Euro (€)</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </GlassCard>
        </TabsContent>

        <TabsContent value="ai">
          <GlassCard>
            <SectionTitle title="AI preferences" />
            <Row title="Personalized recommendations" desc="Let Finara use your data to tailor advice" defaultChecked />
            <Row title="Voice input" desc="Enable speech-to-text in the assistant" />
            <Row title="Auto-summarize weekly" desc="Get a Sunday summary of your money" defaultChecked />
            <Separator className="my-6 bg-white/5" />
            <div>
              <Label>Default model</Label>
              <Select defaultValue="finara-1">
                <SelectTrigger className="mt-1.5 max-w-sm"><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="finara-1">Finara Advisor</SelectItem>
                  <SelectItem value="finara-pro">Finara Pro</SelectItem>
                  <SelectItem value="finara-lite">Finara Lite</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </GlassCard>
        </TabsContent>

        <TabsContent value="accounts">
          <GlassCard>
            <SectionTitle title="Connected accounts" />
            <ul className="space-y-3">
              {[
                { name: "HDFC Bank", type: "Bank",       connected: true  },
                { name: "Zerodha",   type: "Brokerage",  connected: true  },
                { name: "CoinDCX",   type: "Crypto",     connected: false },
                { name: "Google",    type: "OAuth",      connected: true  },
              ].map((a) => (
                <li key={a.name} className="flex items-center justify-between rounded-xl border border-white/10 bg-white/[0.03] p-3">
                  <div>
                    <div className="text-sm font-medium">{a.name}</div>
                    <div className="text-xs text-muted-foreground">{a.type}</div>
                  </div>
                  {a.connected
                    ? <Button size="sm" variant="outline" className="border-white/10 bg-white/[0.03]">Disconnect</Button>
                    : <Button size="sm" className="gradient-brand text-primary-foreground">Connect</Button>}
                </li>
              ))}
            </ul>
          </GlassCard>
        </TabsContent>

        <TabsContent value="privacy">
          <GlassCard>
            <SectionTitle title="Data & privacy" />
            <Row title="Personalized ads" desc="We never sell your data. This turns off in-app suggestions." />
            <Row title="Product analytics" desc="Help us improve Finara with anonymous usage data" defaultChecked />
            <Separator className="my-6 bg-white/5" />
            <div className="flex flex-wrap gap-2">
              <Button variant="outline" className="border-white/10 bg-white/[0.03]">Download my data</Button>
              <Button variant="outline" className="border-white/10 bg-white/[0.03]" onClick={() => { logout(); navigate({ to: "/login" }); }}>
                <LogOut className="mr-2 h-4 w-4" />Sign out
              </Button>
            </div>
          </GlassCard>

          <GlassCard className="mt-4 border-destructive/30">
            <div className="flex items-start gap-3">
              <div className="grid h-10 w-10 place-items-center rounded-xl bg-destructive/15 text-destructive">
                <AlertTriangle className="h-5 w-5" />
              </div>
              <div className="flex-1">
                <div className="text-base font-semibold">Danger zone</div>
                <p className="mt-1 text-sm text-muted-foreground">
                  Deleting your account is permanent. All your data, goals, and chat history will be erased.
                </p>
              </div>
              <Button variant="destructive" onClick={() => toast.error("Account deletion requested (demo)")}>Delete account</Button>
            </div>
          </GlassCard>
        </TabsContent>
      </Tabs>
    </div>
  );
}

function Field({ label, ...rest }: React.InputHTMLAttributes<HTMLInputElement> & { label: string }) {
  const id = `f-${label.replace(/\s+/g, "-").toLowerCase()}`;
  return (
    <div>
      <Label htmlFor={id}>{label}</Label>
      <Input id={id} {...rest} className="mt-1.5 border-white/10 bg-white/[0.03]" />
    </div>
  );
}

function SectionTitle({ title }: { title: string }) {
  return <h3 className="mb-4 text-sm font-semibold uppercase tracking-wider text-muted-foreground">{title}</h3>;
}

function Row({ title, desc, defaultChecked }: { title: string; desc: string; defaultChecked?: boolean }) {
  return (
    <div className="flex items-center justify-between border-b border-white/5 py-3 last:border-0">
      <div>
        <div className="text-sm font-medium">{title}</div>
        <div className="text-xs text-muted-foreground">{desc}</div>
      </div>
      <Switch defaultChecked={defaultChecked} />
    </div>
  );
}
