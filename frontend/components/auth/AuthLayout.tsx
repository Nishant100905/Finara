"use client";

import { ReactNode } from "react";

import AuthBackground from "./AuthBackground";

interface Props {
    children: ReactNode;
}

export default function AuthLayout({
    children,
}: Props) {
    return (
        <main className="relative flex min-h-screen items-center justify-center overflow-hidden">

            <AuthBackground />

            <div className="relative z-10 w-full px-6">
                <div className="mx-auto flex max-w-7xl items-center justify-center lg:grid lg:grid-cols-2 lg:gap-16">

                    {/* Left Side */}
                    <div className="hidden lg:block">

                        <h1 className="text-6xl font-bold text-white">
                            FinAI
                        </h1>

                        <p className="mt-6 max-w-lg text-xl leading-9 text-white/70">
                            Your AI-powered financial operating system for smarter investing,
                            planning, forecasting, and wealth management.
                        </p>

                        <div className="mt-10 space-y-5">

                            <div className="rounded-2xl border border-white/10 bg-white/5 p-5 backdrop-blur-xl">
                                📈 Live Portfolio Analytics
                            </div>

                            <div className="rounded-2xl border border-white/10 bg-white/5 p-5 backdrop-blur-xl">
                                🤖 AI Financial Assistant
                            </div>

                            <div className="rounded-2xl border border-white/10 bg-white/5 p-5 backdrop-blur-xl">
                                🎯 Goal Tracking & Forecasting
                            </div>

                        </div>

                    </div>

                    {/* Right Side */}
                    <div className="flex justify-center">
                        {children}
                    </div>

                </div>
            </div>

        </main>
    );
}
