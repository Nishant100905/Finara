import { useRef, useState } from "react";
import { Upload, FileText, Loader2, CheckCircle2 } from "lucide-react";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { uploadDocument } from "@/lib/document-api";

type UploadStatus =
    | "idle"
    | "uploading"
    | "processing"
    | "completed";

interface Props {
    onSuccess?: () => void;
}

export default function DocumentUpload({
    onSuccess,
}: Props) {
    const inputRef = useRef<HTMLInputElement>(null);

    const [dragging, setDragging] = useState(false);

    const [progress, setProgress] = useState(0);

    const [status, setStatus] =
        useState<UploadStatus>("idle");

    const [fileName, setFileName] =
        useState("");

    const allowed = [
        "application/pdf",

        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",

        "text/plain",

        "text/csv",
    ];

    const validate = (file: File) => {
        if (!allowed.includes(file.type)) {
            toast.error("Unsupported file type");
            return false;
        }

        if (file.size > 20 * 1024 * 1024) {
            toast.error("Maximum file size is 20 MB");
            return false;
        }

        return true;
    };

    const upload = async (file: File) => {
        if (!validate(file)) return;

        setFileName(file.name);

        setStatus("uploading");

        setProgress(0);

        try {
            await uploadDocument(
                file,
                (p) => {
                    setProgress(p);
                }
            );

            setStatus("processing");

            setProgress(100);

            toast.success(
                "Document uploaded successfully"
            );

            setTimeout(() => {
                setStatus("completed");

                onSuccess?.();
            }, 1000);
        } catch (e) {
            console.error(e);

            toast.error(
                "Upload failed"
            );

            setStatus("idle");

            setProgress(0);
        }
    };

    const chooseFile = () => {
        inputRef.current?.click();
    };

    const onChange = (
        e: React.ChangeEvent<HTMLInputElement>
    ) => {
        const file = e.target.files?.[0];

        if (!file) return;

        upload(file);
    };
    const onDrop = async (
        e: React.DragEvent<HTMLDivElement>
    ) => {
        e.preventDefault();

        setDragging(false);

        const file = e.dataTransfer.files?.[0];

        if (!file) return;

        await upload(file);
    };

    return (
        <>
            <input
                ref={inputRef}
                hidden
                type="file"
                accept=".pdf,.doc,.docx,.txt,.csv"
                onChange={onChange}
            />

            <div
                onClick={chooseFile}
                onDragOver={(e) => {
                    e.preventDefault();
                    setDragging(true);
                }}
                onDragLeave={() => setDragging(false)}
                onDrop={onDrop}
                className={[
                    "cursor-pointer rounded-2xl border-2 border-dashed transition-all",
                    "p-6 text-center",
                    dragging
                        ? "border-primary bg-primary/10"
                        : "border-white/10 bg-white/[0.03] hover:bg-white/[0.05]",
                ].join(" ")}
            >
                {status === "idle" && (
                    <>
                        <Upload className="mx-auto mb-3 h-10 w-10 text-primary" />

                        <h3 className="font-semibold">
                            Upload Document
                        </h3>

                        <p className="mt-1 text-sm text-muted-foreground">
                            Drag & Drop PDF, DOCX, TXT or CSV
                        </p>

                        <Button
                            className="mt-4"
                            type="button"
                        >
                            Choose File
                        </Button>
                    </>
                )}

                {status === "uploading" && (
                    <>
                        <Loader2 className="mx-auto mb-3 h-10 w-10 animate-spin text-primary" />

                        <h3 className="font-semibold">
                            Uploading...
                        </h3>

                        <p className="mb-4 text-sm text-muted-foreground">
                            {fileName}
                        </p>

                        <Progress value={progress} />

                        <div className="mt-2 text-xs text-muted-foreground">
                            {progress}%
                        </div>
                    </>
                )}

                {status === "processing" && (
                    <>
                        <Loader2 className="mx-auto mb-3 h-10 w-10 animate-spin text-primary" />

                        <h3 className="font-semibold">
                            Processing Document
                        </h3>

                        <p className="text-sm text-muted-foreground">
                            Creating embeddings...
                        </p>
                    </>
                )}

                {status === "completed" && (
                    <>
                        <CheckCircle2 className="mx-auto mb-3 h-10 w-10 text-green-500" />

                        <h3 className="font-semibold">
                            Upload Complete
                        </h3>

                        <div className="mt-2 flex items-center justify-center gap-2">
                            <FileText className="h-4 w-4" />

                            <span className="text-sm">
                                {fileName}
                            </span>
                        </div>
                    </>
                )}
            </div>
        </>
    );
}