import { saveAs } from "file-saver";
import { Holding } from "@/types/portfolio";

export function exportPortfolioCSV(
    holdings: Holding[]
) {
    const rows = holdings.map(
        (holding) => ({
            Symbol: holding.symbol,
            Name: holding.name,
            Type: holding.assetType,
            Quantity: holding.quantity,
            AvgPrice:
                holding.averagePrice,
            CurrentPrice:
                holding.currentPrice,
            CurrentValue:
                holding.currentValue,
            ProfitLoss:
                holding.profitLoss,
        })
    );

    const csv = [
        Object.keys(rows[0]).join(","),

        ...rows.map((row) =>
            Object.values(row).join(",")
        ),
    ].join("\n");

    const blob = new Blob([csv], {
        type: "text/csv;charset=utf-8;",
    });

    saveAs(blob, "portfolio.csv");
}