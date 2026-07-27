import { backend } from "@/lib/backend";

export type MockUser = {
  id: string;
  name: string;
  email: string;
  avatarUrl?: string;
  createdAt: string;
};

const KEY = "finara.session.v1";

export const mockAuth = {
  getUser(): MockUser | null {
    if (typeof window === "undefined") return null;

    try {
      const raw = localStorage.getItem(KEY);
      return raw ? (JSON.parse(raw) as MockUser) : null;
    } catch {
      return null;
    }
  },

  async login(email: string, password: string): Promise<MockUser> {
    const data = await backend.login(email, password);

    const user: MockUser = {
      id: data.user.id,
      name: data.user.email.split("@")[0],
      email: data.user.email,
      createdAt: new Date().toISOString(),
    };

    localStorage.setItem(KEY, JSON.stringify(user));

    return user;
  },

  async register(
    name: string,
    email: string,
    password: string
  ): Promise<MockUser> {
    await backend.register(email, password);

    // Automatically log in after successful registration
    return this.login(email, password);
  },

  async logout() {
    try {
      await backend.logout();
    } catch {
      // Ignore logout errors
    }

    localStorage.removeItem(KEY);
  },
};