import { createFileRoute } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { AnimatePresence, motion } from "framer-motion";
import { useEffect, useMemo, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import {
  Plus, Search, Pin, MoreHorizontal, Trash2, Edit3, Copy, Check,
  Mic, Paperclip, Send, StopCircle, RotateCcw, Sparkles, ChevronDown, ChevronRight, MessageSquareText, Loader2, X,
} from "lucide-react";
import { api } from "@/services/api";
import type { ChatMessage, ChatSession } from "@/data/mock";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger, DropdownMenuSeparator } from "@/components/ui/dropdown-menu";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { toast } from "sonner";
import { cn } from "@/lib/utils";
import { useAuth } from "@/context/AuthContext";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import DocumentUpload from "@/components/ocument-upload";
import DocumentList from "../../components/document-list";
import { Progress } from "@/components/ui/progress";
import { uploadDocument, type UploadedDocument } from "@/lib/document-api";
export const Route = createFileRoute("/_app/assistant")({
  component: AssistantPage,
  head: () => ({ meta: [{ title: "AI Assistant — Finara" }] }),
});

const MODELS = [
  { id: "finara-1", name: "Finara Advisor", desc: "Best balance of speed and depth" },
  { id: "finara-pro", name: "Finara Pro", desc: "Deep portfolio & tax reasoning" },
  { id: "finara-lite", name: "Finara Lite", desc: "Fastest, ideal for quick answers" },
];

function AssistantPage() {
  const { data: seed } = useQuery({ queryKey: ["chats"], queryFn: api.getChats });
  const { data: suggested } = useQuery({ queryKey: ["prompts"], queryFn: api.getSuggestedPrompts });

  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [activeId, setActiveId] = useState<string | null>(null);
  const [q, setQ] = useState("");
  const [model, setModel] = useState(MODELS[0].id);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [refreshDocuments, setRefreshDocuments] = useState(0);
  const [documentsOpen, setDocumentsOpen] = useState(true);
  const [selectedDocId, setSelectedDocId] = useState<string | null>(null);
  const [selectedDocName, setSelectedDocName] = useState<string | null>(null);

  const refreshDocumentList = () => {
    setRefreshDocuments((prev) => prev + 1);
  };

  const handleDocumentSelect = (docId: string, filename: string) => {
    if (selectedDocId === docId) {
      setSelectedDocId(null);
      setSelectedDocName(null);
    } else {
      setSelectedDocId(docId);
      setSelectedDocName(filename);
    }
  };

  useEffect(() => {
    if (seed && sessions.length === 0) {
      setSessions(seed);
      setActiveId(seed[0]?.id ?? null);
    }
  }, [seed, sessions.length]);

  const active = useMemo(() => sessions.find((s) => s.id === activeId) ?? null, [sessions, activeId]);
  const filtered = useMemo(() => {
    const list = q ? sessions.filter((s) => s.title.toLowerCase().includes(q.toLowerCase())) : sessions;
    return [...list].sort((a, b) => Number(b.pinned || 0) - Number(a.pinned || 0));
  }, [sessions, q]);

  const newChat = () => {
    const id = "c_" + Math.random().toString(36).slice(2, 10);
    const s: ChatSession = { id, title: "New chat", updatedAt: new Date().toISOString(), messages: [] };
    setSessions((prev) => [s, ...prev]);
    setActiveId(id);
    setSidebarOpen(false);
  };

  const renameChat = (id: string) => {
    const title = window.prompt("Rename chat", sessions.find((s) => s.id === id)?.title ?? "");
    if (!title) return;
    setSessions((p) => p.map((s) => (s.id === id ? { ...s, title } : s)));
  };
  const deleteChat = (id: string) => {
    setSessions((p) => p.filter((s) => s.id !== id));
    if (activeId === id) setActiveId(sessions.find((s) => s.id !== id)?.id ?? null);
  };
  const pinChat = (id: string) =>
    setSessions((p) => p.map((s) => (s.id === id ? { ...s, pinned: !s.pinned } : s)));

  const updateActive = (fn: (s: ChatSession) => ChatSession) => {
    setSessions((prev) => prev.map((s) => (s.id === activeId ? fn(s) : s)));
  };

  return (
    <div className="h-[calc(100dvh-8rem)] lg:h-[calc(100dvh-6rem)]">
      <div className="grid h-full gap-4 lg:grid-cols-[300px_1fr]">
        {/* Sidebar */}
        <aside className={cn(
          "glass hidden flex-col overflow-hidden rounded-2xl lg:flex",
          sidebarOpen && "!flex fixed inset-4 z-40 lg:relative lg:inset-auto",
        )}>
          <div className="p-3">
            <Button onClick={newChat} className="w-full gradient-brand text-primary-foreground">
              <Plus className="mr-2 h-4 w-4" />New chat
            </Button>
          </div>
          <div className="px-3 pb-2">
            <div className="relative">
              <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <Input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Search chats" className="h-9 pl-9 bg-white/[0.03] border-white/10" />
            </div>
          </div>
          <ScrollArea className="flex-1">
            <div className="px-3 pb-2">

              <button
                onClick={() =>
                  setDocumentsOpen(!documentsOpen)
                }
                className="flex w-full items-center justify-between rounded-xl px-2 py-2 text-sm font-medium transition hover:bg-white/5"
              >
                <span>Documents</span>

                {documentsOpen ? (
                  <ChevronDown className="h-4 w-4" />
                ) : (
                  <ChevronRight className="h-4 w-4" />
                )}
              </button>

            </div>

            {documentsOpen && (

              <>

                <div className="px-3 pb-3">

                  <DocumentUpload
                    onSuccess={refreshDocumentList}
                  />

                </div>

                <div className="px-3 pb-3">

                  <DocumentList
                    refreshTrigger={refreshDocuments}
                    selectedDocId={selectedDocId}
                    onSelectDocument={handleDocumentSelect}
                  />

                </div>

              </>

            )}
            <ul className="space-y-1 p-2">
              {filtered.map((s) => (
                <li key={s.id}>
                  <div className={cn(
                    "group flex items-center gap-2 rounded-xl px-2 py-2 text-sm transition",
                    s.id === activeId ? "bg-white/[0.06]" : "hover:bg-white/[0.04]",
                  )}>
                    <button className="min-w-0 flex-1 text-left" onClick={() => { setActiveId(s.id); setSidebarOpen(false); }}>
                      <div className="flex items-center gap-2">
                        {s.pinned && <Pin className="h-3 w-3 shrink-0 text-primary" />}
                        <span className="truncate">{s.title}</span>
                      </div>
                      <div className="mt-0.5 text-[11px] text-muted-foreground">
                        {new Date(s.updatedAt).toLocaleDateString()}
                      </div>
                    </button>
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <button className="rounded-md p-1 opacity-0 transition group-hover:opacity-100 hover:bg-white/10" aria-label="Actions">
                          <MoreHorizontal className="h-4 w-4" />
                        </button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        <DropdownMenuItem onClick={() => pinChat(s.id)}><Pin className="mr-2 h-4 w-4" />{s.pinned ? "Unpin" : "Pin"}</DropdownMenuItem>
                        <DropdownMenuItem onClick={() => renameChat(s.id)}><Edit3 className="mr-2 h-4 w-4" />Rename</DropdownMenuItem>
                        <DropdownMenuSeparator />
                        <DropdownMenuItem onClick={() => deleteChat(s.id)} className="text-destructive"><Trash2 className="mr-2 h-4 w-4" />Delete</DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </div>
                </li>
              ))}
              {filtered.length === 0 && (
                <div className="p-6 text-center text-sm text-muted-foreground">No chats found</div>
              )}
            </ul>
          </ScrollArea>
        </aside>

        {/* Chat window */}
        <ChatWindow
          active={active}
          model={model}
          setModel={setModel}
          updateActive={updateActive}
          onOpenSidebar={() => setSidebarOpen(true)}
          onNewChat={newChat}
          suggested={suggested ?? []}
          onDocumentUploaded={refreshDocumentList}
          sidebarSelectedDocId={selectedDocId}
          sidebarSelectedDocName={selectedDocName}
        />
      </div>
    </div >
  );
}

function ChatWindow({
  active, model, setModel, updateActive, onOpenSidebar, onNewChat, suggested, onDocumentUploaded, sidebarSelectedDocId, sidebarSelectedDocName,
}: {
  active: ChatSession | null;
  model: string;
  setModel: (v: string) => void;
  updateActive: (fn: (s: ChatSession) => ChatSession) => void;
  onOpenSidebar: () => void;
  onNewChat: () => void;
  suggested: string[];
  onDocumentUploaded: () => void;
  sidebarSelectedDocId?: string | null;
  sidebarSelectedDocName?: string | null;
}) {
  const { user } = useAuth();
  const [input, setInput] = useState("");
  const [streaming, setStreaming] = useState(false);
  const [streamText, setStreamText] = useState("");
  const [isThinking, setIsThinking] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [uploading, setUploading] = useState(false);

  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadFileName, setUploadFileName] = useState("");
  const [attachedDocument, setAttachedDocument] = useState<UploadedDocument | null>(null);
  const scrollRef = useRef<HTMLDivElement | null>(null);
  const abortRef = useRef<AbortController | null>(null);
  const textareaRef = useRef<HTMLTextAreaElement | null>(null);

  useEffect(() => { textareaRef.current?.focus(); }, [active?.id]);
  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [active?.messages.length, streamText]);

  const send = async (text: string, options: { skipUserMessage?: boolean } = {}) => {
    if (!text.trim() || !active) return;

    // Only add user message if not skipping
    if (!options.skipUserMessage) {
      const userMsg: ChatMessage = { id: "m_" + Date.now(), role: "user", content: text, createdAt: new Date().toISOString() };
      // Title from first message
      updateActive((s) => ({
        ...s,
        title: s.messages.length === 0 ? text.slice(0, 40) : s.title,
        updatedAt: new Date().toISOString(),
        messages: [...s.messages, userMsg],
      }));
    }

    setInput("");
    setStreaming(true);
    setStreamText("");

    const controller = new AbortController();
    abortRef.current = controller;
    try {
      let buffer = "";
      // Collect document_ids: prefer attachedDocument (paperclip), fall back to sidebar selection
      const docIds: string[] = [];
      if (attachedDocument) {
        docIds.push(attachedDocument.document_id);
      } else if (sidebarSelectedDocId) {
        docIds.push(sidebarSelectedDocId);
      }
      const final = await api.streamAssistantReply(text, (chunk) => {
        buffer += chunk;
        setStreamText(buffer);
      }, controller.signal, docIds.length > 0 ? docIds : undefined);
      updateActive((s) => ({ ...s, messages: [...s.messages, final], updatedAt: new Date().toISOString() }));
    } finally {
      setStreaming(false);
      setStreamText("");
      abortRef.current = null;
    }
  };

  const stop = () => abortRef.current?.abort();
  const regenerate = async () => {
    if (!active) return;
    const last = [...active.messages].reverse().find((m) => m.role === "user");
    if (!last) return;
    updateActive((s) => ({ ...s, messages: s.messages.filter((m) => !(m.role === "assistant" && m === s.messages.at(-1))) }));
    await send(last.content, { skipUserMessage: true });
  };

  const onKey = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); if (!uploading) void send(input); }
  };

  const validateUpload = (file: File): boolean => {
    const extension = file.name.split(".").pop()?.toLowerCase();
    if (!extension || !["pdf", "docx", "txt", "csv"].includes(extension)) {
      toast.error("Unsupported file type. Please select a PDF, DOCX, TXT, or CSV file.");
      return false;
    }
    if (file.size > 20 * 1024 * 1024) {
      toast.error("This file is too large. The maximum upload size is 20 MB.");
      return false;
    }
    return true;
  };

  const uploadErrorMessage = (error: unknown): string => {
    const response = (error as { response?: { status?: number; data?: { detail?: unknown } } }).response;
    const status = response?.status;
    const detail = response?.data?.detail;
    if (status === 413) return "This file is too large for the server. Please choose a file under 20 MB.";
    if (status === 415) return "This file format is not supported. Please choose a PDF, DOCX, TXT, or CSV file.";
    if (status === 500) return "The document could not be processed. Please try again shortly.";
    if (!status) return "We couldn't reach the server. Check your connection and try again.";
    if (typeof detail === "string") return detail;
    return "The document upload failed. Please try again.";
  };

  const uploadFile = async (file: File) => {
    if (uploading || !validateUpload(file)) return;

    setUploading(true);
    setUploadFileName(file.name);
    setUploadProgress(0);
    try {
      const document = await uploadDocument(file, setUploadProgress);
      setAttachedDocument(document);
      onDocumentUploaded();
      toast.success(`${document.filename} uploaded successfully`);
    } catch (error: unknown) {
      toast.error(uploadErrorMessage(error));
    } finally {
      setUploading(false);
      setUploadProgress(0);
      setUploadFileName("");
      if (fileInputRef.current) fileInputRef.current.value = "";
    }
  };

  const onFileInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) void uploadFile(file);
  };

  const onDrop = (event: React.DragEvent<HTMLElement>) => {
    event.preventDefault();
    const file = event.dataTransfer.files?.[0];
    if (file) void uploadFile(file);
  };

  return (
    <section className="glass flex min-h-0 flex-col overflow-hidden rounded-2xl" onDragOver={(e) => e.preventDefault()} onDrop={onDrop}>
      {/* Header */}
      <header className="flex items-center gap-2 border-b border-white/5 px-4 py-3">
        <Button variant="ghost" size="icon" onClick={onOpenSidebar} className="lg:hidden" aria-label="Open chats">
          <MessageSquareText className="h-5 w-5" />
        </Button>
        <div className="min-w-0">
          <div className="truncate text-sm font-medium">{active?.title ?? "New chat"}</div>
          <div className="text-[11px] text-muted-foreground">Personalized to your financial profile</div>
        </div>
        <div className="ml-auto flex items-center gap-2">
          <Select value={model} onValueChange={setModel}>
            <SelectTrigger className="h-9 gap-2 border-white/10 bg-white/[0.03] text-sm">
              <Sparkles className="h-3.5 w-3.5 text-primary" />
              <SelectValue />
              <ChevronDown className="h-3.5 w-3.5 opacity-60" />
            </SelectTrigger>
            <SelectContent>
              {MODELS.map((m) => (
                <SelectItem key={m.id} value={m.id}>
                  <div>
                    <div className="text-sm font-medium">{m.name}</div>
                    <div className="text-xs text-muted-foreground">{m.desc}</div>
                  </div>
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          <Button variant="outline" size="sm" className="border-white/10 bg-white/[0.03]" onClick={onNewChat}>
            <Plus className="mr-1 h-4 w-4" /> New
          </Button>
        </div>
      </header>

      {/* Messages */}
      <div ref={scrollRef} className="min-h-0 flex-1 overflow-y-auto px-4 py-6 sm:px-8">
        {(!active || active.messages.length === 0) ? (
          <EmptyChat onPick={(p) => void send(p)} suggested={suggested} />
        ) : (
          <div className="mx-auto max-w-3xl space-y-6">
            {active.messages.map((m) => <MessageBubble key={m.id} msg={m} userInitial={user?.name?.[0]} />)}
            <AnimatePresence>
              {streaming && (
                <motion.div
                  key="streaming"
                  initial={{ opacity: 0, y: 6 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -6 }}
                >
                  <AssistantBubble animated={false}>
                    <StreamingContent text={streamText} />
                  </AssistantBubble>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        )}
      </div>

      {/* Composer */}
      <footer className="border-t border-white/5 p-3 sm:p-4">
        <div className="mx-auto max-w-3xl">
          {active?.messages.length ? (
            <div className="mb-2 flex items-center justify-center gap-2">
              {streaming ? (
                <Button size="sm" variant="outline" className="border-white/10 bg-white/[0.03]" onClick={stop}>
                  <StopCircle className="mr-2 h-3.5 w-3.5" />Stop generating
                </Button>
              ) : null}
            </div>
          ) : null}
          {uploading && (
            <div className="mb-2 space-y-1.5 px-1">
              <div className="flex justify-between text-xs text-muted-foreground">
                <span className="truncate">Uploading {uploadFileName}</span>
                <span>{uploadProgress}%</span>
              </div>
              <Progress value={uploadProgress} />
            </div>
          )}
          <div className="relative rounded-2xl border border-white/10 bg-white/[0.03] focus-within:border-primary/40 focus-within:shadow-glow">
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf,.docx,.txt,.csv"
              className="hidden"
              onChange={onFileInputChange}
            />
            {attachedDocument && (
              <div className="flex items-center px-4 pt-3">
                <Badge variant="secondary" className="max-w-full gap-1.5 pr-1.5">
                  <span aria-hidden="true">📄</span>
                  <span className="truncate">{attachedDocument.filename}</span>
                  <button
                    type="button"
                    onClick={() => setAttachedDocument(null)}
                    className="rounded-sm p-0.5 hover:bg-white/10"
                    aria-label={`Remove ${attachedDocument.filename}`}
                  >
                    <X className="h-3 w-3" />
                  </button>
                </Badge>
              </div>
            )}
            <Textarea
              ref={textareaRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={onKey}
              rows={2}
              placeholder="Ask about your money, portfolio, or the market…"
              className="min-h-[64px] resize-none border-0 bg-transparent px-4 pb-12 pt-3 focus-visible:ring-0"
            />
            <div className="absolute inset-x-2 bottom-2 flex items-center gap-1">
              <Button variant="ghost" size="icon" aria-label="Attach" disabled={uploading} onClick={() => fileInputRef.current?.click()}>
                {uploading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Paperclip className="h-4 w-4" />}
              </Button>
              <Button variant="ghost" size="icon" aria-label="Voice" onClick={() => toast.info("Voice input (demo)")}>
                <Mic className="h-4 w-4" />
              </Button>
              <div className="ml-auto flex items-center gap-2">
                <span className="hidden text-[10px] text-muted-foreground sm:inline">Shift ↵ for newline</span>
                <Button
                  size="icon"
                  disabled={!input.trim() || streaming || uploading}
                  onClick={() => void send(input)}
                  className="h-9 w-9 gradient-brand text-primary-foreground"
                  aria-label="Send"
                >
                  <Send className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </div>
        </div>
      </footer>
    </section>
  );
}

function EmptyChat({ onPick, suggested }: { onPick: (p: string) => void; suggested: string[] }) {
  return (
    <div className="mx-auto flex max-w-2xl flex-col items-center justify-center gap-6 pt-6 text-center sm:pt-16">
      <div className="grid h-16 w-16 place-items-center rounded-2xl gradient-brand text-primary-foreground shadow-glow">
        <Sparkles className="h-7 w-7" />
      </div>
      <div>
        <h2 className="text-2xl font-semibold tracking-tight">How can I help with your money today?</h2>
        <p className="mt-1 text-sm text-muted-foreground">Ask about your portfolio, goals, or spending.</p>
      </div>
      <div className="grid w-full gap-2 sm:grid-cols-2">
        {suggested.map((p) => (
          <button
            key={p} onClick={() => onPick(p)}
            className="rounded-2xl border border-white/10 bg-white/[0.03] p-4 text-left text-sm transition hover:bg-white/[0.06] hover-lift"
          >
            <div className="flex items-start gap-3">
              <Sparkles className="mt-0.5 h-4 w-4 shrink-0 text-primary" />
              <span className="text-foreground/90">{p}</span>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}

function MessageBubble({ msg, userInitial }: { msg: ChatMessage; userInitial?: string }) {
  if (msg.role === "user") {
    return (
      <div className="flex justify-end">
        <div className="flex max-w-[85%] items-start gap-3">
          <div className="rounded-2xl rounded-tr-md gradient-brand px-4 py-2.5 text-sm text-primary-foreground shadow-elegant">
            {msg.content}
          </div>
          <Avatar className="h-8 w-8"><AvatarFallback className="bg-white/10 text-xs">{userInitial ?? "U"}</AvatarFallback></Avatar>
        </div>
      </div>
    );
  }
  return <AssistantBubble animated={false}><Markdown content={msg.content} /></AssistantBubble>;
}

function AssistantBubble({ children, animated = true }: { children: React.ReactNode; animated?: boolean }) {
  if (!animated) {
    return (
      <div className="flex items-start gap-3">
        <div className="grid h-8 w-8 shrink-0 place-items-center rounded-xl gradient-brand text-primary-foreground">
          <Sparkles className="h-4 w-4" />
        </div>
        <div className="min-w-0 flex-1">
          <div className="text-sm leading-relaxed text-foreground/95">
            {children}
          </div>
        </div>
      </div>
    );
  }
  return (
    <motion.div initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} className="flex items-start gap-3">
      <div className="grid h-8 w-8 shrink-0 place-items-center rounded-xl gradient-brand text-primary-foreground">
        <Sparkles className="h-4 w-4" />
      </div>
      <div className="min-w-0 flex-1">
        <div className="text-sm leading-relaxed text-foreground/95">
          {children}
        </div>
      </div>
    </motion.div>
  );
}

function StreamingContent({ text }: { text: string }) {
  if (!text) {
    return (
      <div className="flex items-center gap-2 text-sm text-muted-foreground">
        <div className="flex gap-1">
          {[0, 1, 2].map(i => (
            <motion.span key={i}
              className="block h-1.5 w-1.5 rounded-full bg-primary"
              animate={{ opacity: [0.3, 1, 0.3], y: [0, -2, 0] }}
              transition={{ duration: 1.1, repeat: Infinity, delay: i * 0.15 }}
            />
          ))}
        </div>
      </div>
    );
  }
  return (
    <div>
      <Markdown content={text} />
      <span className="ml-0.5 inline-block h-4 w-1.5 translate-y-0.5 animate-pulse bg-primary" />
    </div>
  );
}

function Markdown({ content }: { content: string }) {
  return (
    <div className="prose prose-invert prose-sm max-w-none prose-headings:font-semibold prose-p:my-2 prose-ul:my-2 prose-li:my-0.5 prose-code:rounded prose-code:bg-white/10 prose-code:px-1 prose-code:py-0.5 prose-code:text-[0.85em] prose-code:text-primary prose-code:before:content-none prose-code:after:content-none">
      <ReactMarkdown
        components={{
          pre: (props) => <CodeBlock {...props} />,
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}

function CodeBlock({ children }: React.HTMLAttributes<HTMLElement>) {
  const [copied, setCopied] = useState(false);
  const ref = useRef<HTMLPreElement | null>(null);
  const copy = async () => {
    try {
      const t = ref.current?.innerText ?? "";
      await navigator.clipboard.writeText(t);
      setCopied(true); setTimeout(() => setCopied(false), 1500);
    } catch { /* noop */ }
  };
  return (
    <div className="not-prose relative my-3 overflow-hidden rounded-xl border border-white/10 bg-black/40">
      <button onClick={copy} className="absolute right-2 top-2 rounded-md border border-white/10 bg-white/5 px-2 py-1 text-[10px] text-muted-foreground transition hover:text-foreground">
        {copied ? <Check className="h-3 w-3" /> : <Copy className="h-3 w-3" />}
      </button>
      <pre ref={ref} className="overflow-x-auto p-4 text-xs leading-relaxed">{children}</pre>
    </div>
  );
}
