"use client";

import {
    FileText,
    FileSpreadsheet,
    Image,
} from "lucide-react";

const files = [
    {
        name: "Portfolio.pdf",
        icon: FileText,
    },
    {
        name: "Budget.xlsx",
        icon: FileSpreadsheet,
    },
    {
        name: "Salary.png",
        icon: Image,
    },
];

export default function RecentFiles() {
    return (
        <div className="rounded-2xl border border-white/10 bg-white/5 p-5">

            <h3 className="mb-4 font-semibold text-white">
                Recent Files
            </h3>

            <div className="space-y-3">

                {files.map((file) => (
                    <button
                        key={file.name}
                        className="flex w-full items-center gap-3 rounded-xl p-3 transition hover:bg-white/5"
                    >
                        <file.icon
                            size={18}
                            className="text-cyan-400"
                        />

                        <span className="text-sm text-white">
                            {file.name}
                        </span>

                    </button>
                ))}

            </div>

        </div>
    );
}
