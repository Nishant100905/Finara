"use client";

import { useState } from "react";

import type {
    ChatMessage,
    ChatResponse,
} from "@/lib/types/chat";

import { sendMessage } from "@/lib/api/chat";

export function useChat() {
    const [messages, setMessages] = useState<ChatMessage[]>([]);

    const [loading, setLoading] = useState(false);

    const [threadId, setThreadId] = useState<string>();

    async function send(text: string) {
        if (!text.trim()) return;

        const userMessage: ChatMessage = {
            id: crypto.randomUUID(),
            role: "user",
            content: text,
        };

        setMessages((prev) => [...prev, userMessage]);

        setLoading(true);

        try {
            const response: ChatResponse =
                await sendMessage(text, threadId);

            setThreadId(response.thread_id);

            setMessages((prev) => [
                ...prev,
                response.message,
            ]);
        } finally {
            setLoading(false);
        }
    }

    return {
        messages,
        loading,
        send,
    };
}