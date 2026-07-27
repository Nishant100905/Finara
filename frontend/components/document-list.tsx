import { useEffect, useState } from "react";
import {
    FileText,
    Trash2,
    RefreshCw,
    Loader2,
    CheckCircle2,
    Clock3,
    AlertCircle,
} from "lucide-react";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";
import {
    Card,
    CardContent,
} from "@/components/ui/card";

import {
    getDocuments,
    deleteDocument,
} from "@/lib/document-api";

export interface DocumentItem {
    id: string;
    filename: string;
    status: "ready" | "processing" | "failed";
    uploaded_at: string;
}

interface Props {
    refreshTrigger?: number;
    selectedDocId?: string | null;
    onSelectDocument?: (docId: string, filename: string) => void;
}

export default function DocumentList({
    refreshTrigger,
    selectedDocId,
    onSelectDocument,
}: Props) {
    const [documents, setDocuments] = useState<DocumentItem[]>([]);

    const [loading, setLoading] = useState(false);

    const loadDocuments = async () => {
        setLoading(true);

        try {
            const data = await getDocuments();

            setDocuments(data);
        } catch (err) {
            console.error(err);

            toast.error("Unable to load documents.");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadDocuments();
    }, [refreshTrigger]);

    const remove = async (id: string) => {
        try {
            await deleteDocument(id);

            toast.success("Document deleted");

            setDocuments((prev) =>
                prev.filter((d) => d.id !== id)
            );
        } catch (err) {
            console.error(err);

            toast.error("Delete failed");
        }
    };

    const StatusBadge = ({
        status,
    }: {
        status: DocumentItem["status"];
    }) => {
        switch (status) {
            case "ready":
                return (
                    <Badge className="bg-green-600">
                        <CheckCircle2 className="mr-1 h-3 w-3" />
                        Ready
                    </Badge>
                );

            case "processing":
                return (
                    <Badge
                        variant="secondary"
                        className="gap-1"
                    >
                        <Loader2 className="h-3 w-3 animate-spin" />
                        Processing
                    </Badge>
                );

            case "failed":
                return (
                    <Badge
                        variant="destructive"
                        className="gap-1"
                    >
                        <AlertCircle className="h-3 w-3" />
                        Failed
                    </Badge>
                );

            default:
                return (
                    <Badge variant="outline">
                        <Clock3 className="mr-1 h-3 w-3" />
                        Unknown
                    </Badge>
                );
        }
    };

    return (
        <Card className="border-white/10 bg-white/[0.03]">
            <CardContent className="p-4">

                <div className="mb-4 flex items-center justify-between">

                    <div>

                        <h3 className="font-semibold">
                            Uploaded Documents
                        </h3>

                        <p className="text-xs text-muted-foreground">
                            Documents available for RAG
                        </p>

                    </div>

                    <Button
                        size="icon"
                        variant="ghost"
                        onClick={loadDocuments}
                    >
                        <RefreshCw className="h-4 w-4" />
                    </Button>

                </div>

                {loading ? (

                    <div className="flex justify-center py-8">

                        <Loader2 className="h-6 w-6 animate-spin" />

                    </div>

                ) : documents.length === 0 ? (

                    <div className="py-8 text-center text-sm text-muted-foreground">

                        No documents uploaded yet.

                    </div>

                ) : (

                    <ScrollArea className="h-[350px]">

                        <div className="space-y-3">

                            {documents.map((doc) => (

                                <div
                                    key={doc.id}
                                    onClick={() => onSelectDocument?.(doc.id, doc.filename)}
                                    className={`flex items-center justify-between rounded-xl border p-3 cursor-pointer transition ${
                                        selectedDocId === doc.id
                                            ? "border-primary bg-primary/10"
                                            : "border-white/10 bg-white/[0.02] hover:border-white/20"
                                    }`}
                                >
                                    <div className="flex items-center gap-3">

                                        <FileText className={`h-8 w-8 ${selectedDocId === doc.id ? "text-primary" : "text-muted-foreground"}`} />

                                        <div>

                                            <div className="max-w-[180px] truncate font-medium">

                                                {doc.filename}

                                            </div>

                                            <div className="text-xs text-muted-foreground">

                                                {new Date(
                                                    doc.uploaded_at
                                                ).toLocaleString()}

                                            </div>

                                        </div>

                                    </div>

                                    <div className="flex items-center gap-2">

                                        {selectedDocId === doc.id && (
                                            <Badge className="bg-primary text-primary-foreground gap-1">
                                                <CheckCircle2 className="h-3 w-3" />
                                                Active
                                            </Badge>
                                        )}

                                        {selectedDocId !== doc.id && (
                                            <StatusBadge
                                                status={doc.status}
                                            />
                                        )}

                                        <Button
                                            size="icon"
                                            variant="ghost"
                                            onClick={(e) => { e.stopPropagation(); remove(doc.id); }}
                                        >
                                            <Trash2 className="h-4 w-4 text-destructive" />
                                        </Button>

                                    </div>
                                </div>

                            ))}

                        </div>

                    </ScrollArea>

                )}

            </CardContent>
        </Card>
    );
}