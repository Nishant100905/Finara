import api from "./api";

export interface UploadedDocument {
    document_id: string;
    filename: string;
    status: string;
}

export const uploadDocument = async (
    file: File,
    onUploadProgress?: (progress: number) => void
): Promise<UploadedDocument> => {
    const formData = new FormData();

    formData.append("file", file);

    const response = await api.post(
        "/api/documents/upload",
        formData,
        {
            headers: {
                "Content-Type": "multipart/form-data",
            },
            onUploadProgress: (event) => {
                if (!event.total) return;

                const progress = Math.round(
                    (event.loaded * 100) / event.total
                );

                onUploadProgress?.(progress);
            },
        }
    );

    return response.data as UploadedDocument;
};

export const getDocuments = async () => {
    const response = await api.get("/api/documents");
    return response.data;
};

export const deleteDocument = async (id: string) => {
    await api.delete(`/api/documents/${id}`);
};
