import { useNavigate } from "@tanstack/react-router";
import {
  CommandDialog, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList, CommandSeparator,
} from "@/components/ui/command";
import {
  LayoutDashboard, MessageSquareText, Wallet, Target, HeartPulse, LineChart, Settings, Plus, LogOut,
} from "lucide-react";
import { useAuth } from "@/context/AuthContext";

export function CommandPalette({ open, onOpenChange }: { open: boolean; onOpenChange: (v: boolean) => void }) {
  const navigate = useNavigate();
  const { logout } = useAuth();

  const go = (to: string) => {
    onOpenChange(false);
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    navigate({ to: to as any });
  };

  return (
    <CommandDialog open={open} onOpenChange={onOpenChange}>
      <CommandInput placeholder="Search or jump to…" />
      <CommandList>
        <CommandEmpty>No results found.</CommandEmpty>
        <CommandGroup heading="Navigate">
          <CommandItem onSelect={() => go("/dashboard")}><LayoutDashboard className="mr-2 h-4 w-4" />Dashboard</CommandItem>
          <CommandItem onSelect={() => go("/assistant")}><MessageSquareText className="mr-2 h-4 w-4" />AI Assistant</CommandItem>
          <CommandItem onSelect={() => go("/portfolio")}><Wallet className="mr-2 h-4 w-4" />Portfolio</CommandItem>
          <CommandItem onSelect={() => go("/goals")}><Target className="mr-2 h-4 w-4" />Goals</CommandItem>
          <CommandItem onSelect={() => go("/financial-health")}><HeartPulse className="mr-2 h-4 w-4" />Financial Health</CommandItem>
          <CommandItem onSelect={() => go("/market")}><LineChart className="mr-2 h-4 w-4" />Market</CommandItem>
          <CommandItem onSelect={() => go("/settings")}><Settings className="mr-2 h-4 w-4" />Settings</CommandItem>
        </CommandGroup>
        <CommandSeparator />
        <CommandGroup heading="Actions">
          <CommandItem onSelect={() => go("/goals")}><Plus className="mr-2 h-4 w-4" />New goal</CommandItem>
          <CommandItem onSelect={() => go("/assistant")}><Plus className="mr-2 h-4 w-4" />New chat</CommandItem>
          <CommandItem onSelect={() => { logout(); go("/login"); }}><LogOut className="mr-2 h-4 w-4" />Sign out</CommandItem>
        </CommandGroup>
      </CommandList>
    </CommandDialog>
  );
}
