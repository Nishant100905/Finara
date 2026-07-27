// Central currency & number formatting. Default INR per project spec.
export const CURRENCY = "INR";

export const formatCurrency = (n: number, opts: { compact?: boolean; currency?: string } = {}) => {
  const { compact = false, currency = CURRENCY } = opts;
  try {
    return new Intl.NumberFormat("en-IN", {
      style: "currency",
      currency,
      maximumFractionDigits: compact ? 1 : 0,
      notation: compact ? "compact" : "standard",
    }).format(n);
  } catch {
    return `₹${n.toLocaleString("en-IN")}`;
  }
};

export const formatNumber = (n: number, compact = false) =>
  new Intl.NumberFormat("en-IN", {
    notation: compact ? "compact" : "standard",
    maximumFractionDigits: 2,
  }).format(n);

export const formatPercent = (n: number, digits = 2) =>
  `${n >= 0 ? "+" : ""}${n.toFixed(digits)}%`;

export const formatDate = (d: string | Date) =>
  new Date(d).toLocaleDateString("en-IN", { day: "2-digit", month: "short", year: "numeric" });

export const formatTime = (d: string | Date) =>
  new Date(d).toLocaleTimeString("en-IN", { hour: "2-digit", minute: "2-digit" });
