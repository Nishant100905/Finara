import { createFileRoute, redirect } from "@tanstack/react-router";
import { mockAuth } from "@/lib/mock-auth";

export const Route = createFileRoute("/")({
  // Runs on the client (mock auth reads localStorage). SSR just falls
  // through to the component fallback below.
  beforeLoad: () => {
    if (typeof window === "undefined") return;
    const user = mockAuth.getUser();
    throw redirect({ to: user ? "/dashboard" : "/login" });
  },
  component: () => null,
});
