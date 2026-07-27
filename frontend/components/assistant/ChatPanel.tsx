"use client";

import { useState } from "react";
import {
    Bot,
    Send,
    Sparkles,
} from "lucide-react";

import GlassCard from "@/components/glass/GlassCard";
import ChatMessage from "./ChatMessage";
interface Message {
    id: number;
    role: "user" | "assistant";
    content: string;
}

const initialMessages: Message[] = [
    {
        id: 1,
        role: "assistant",
        content:
            "Hello! I'm FinAI. I can analyze your portfolio, answer financial questions, forecast trends, and help you achieve your financial goals.",
    },
];

export default function ChatPanel() {
    const [messages] = useState(initialMessages);
    const [isTyping, setIsTyping] = useState(false);
    const [input, setInput] = useState("");

    return (
        <GlassCard className="flex h-[750px] flex-col overflow-hidden">

            {/* Header */}
            <div className="flex items-center justify-between border-b border-white/10 px-6 py-5">

                <div className="flex items-center gap-3">

                    <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br from-violet-500 to-cyan-500">
                        <Bot className="h-6 w-6 text-white" />
                    </div>

                    <div>
                        <h2 className="text-xl font-semibold text-white">
                            FinAI Assistant
                        </h2>

                        <p className="text-sm text-emerald-400">
                            ● Online
                        </p>
                    </div>

                </div>

                <Sparkles className="h-5 w-5 text-cyan-400" />

            </div>

            {/* Messages */}
            <div className="flex-1 space-y-6 overflow-y-auto px-6 py-6">

                <div className="flex-1 space-y-6 overflow-y-auto px-6 py-6">
                    {messages.map((message) => (
                        <ChatMessage
                            key={message.id}
                            role={message.role}
                            content={message.content}
                        />
                    ))}
                </div>

            </div>

            {/* Input */}
            <div className="border-t border-white/10 p-5">

                <div className="flex items-center gap-3 rounded-2xl border border-white/10 bg-white/5 p-3">

                    <input
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Ask FinAI anything..."
                        className="flex-1 bg-transparent text-white outline-none placeholder:text-white/40"
                    />

                    <button
                        className="
              flex
              h-12
              w-12
              items-center
              justify-center
              rounded-xl
              bg-gradient-to-r
              from-violet-600
              to-cyan-500
              transition
              hover:scale-105
            "
                    >
                        <Send className="h-5 w-5 text-white" />
                    </button>

                </div>

            </div>

        </GlassCard>
    );
}