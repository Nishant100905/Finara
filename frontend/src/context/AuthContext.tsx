import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import { mockAuth, type MockUser } from "@/lib/mock-auth";

type AuthCtx = {
  user: MockUser | null;
  ready: boolean;
  login: (email: string, password: string) => Promise<MockUser>;
  register: (name: string, email: string, password: string) => Promise<MockUser>;
  logout: () => void;
};

const Ctx = createContext<AuthCtx | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<MockUser | null>(null);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    setUser(mockAuth.getUser());
    setReady(true);
  }, []);

  const value: AuthCtx = {
    user,
    ready,
    login: async (e, p) => {
      const u = await mockAuth.login(e, p);
      setUser(u);
      return u;
    },
    register: async (n, e, p) => {
      const u = await mockAuth.register(n, e, p);
      setUser(u);
      return u;
    },
    logout: () => {
      mockAuth.logout();
      setUser(null);
    },
  };

  return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
}

export function useAuth() {
  const ctx = useContext(Ctx);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
