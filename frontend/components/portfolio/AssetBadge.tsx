"use client";

import clsx from "clsx";

interface Props {
    asset: string;
}

export default function AssetBadge({
    asset,
}: Props) {
    return (
        <span
            className={clsx(
                "rounded-full px-3 py-1 text-xs font-semibold",

                asset === "Stock" &&
                "bg-blue-500/15 text-blue-400",

                asset === "ETF" &&
                "bg-purple-500/15 text-purple-400",

                asset === "Crypto" &&
                "bg-yellow-500/15 text-yellow-400",

                asset === "Mutual Fund" &&
                "bg-emerald-500/15 text-emerald-400"
            )}
        >
            {asset}
        </span>
    );
}
