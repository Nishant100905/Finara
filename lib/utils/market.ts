export function formatPrice(
    value: number
) {
    return new Intl.NumberFormat(
        "en-IN",
        {
            style: "currency",
            currency: "INR",
            maximumFractionDigits: 2,
        }
    ).format(value);
}

export function formatPercent(
    value: number
) {
    return `${value >= 0 ? "+" : ""}${value.toFixed(
        2
    )}%`;
}

export function getChangeColor(
    value: number
) {
    if (value > 0)
        return "text-green-500";

    if (value < 0)
        return "text-red-500";

    return "text-gray-500";
}

export function getFearGreedColor(
    value: number
) {
    if (value <= 20)
        return "text-red-600";

    if (value <= 40)
        return "text-orange-500";

    if (value <= 60)
        return "text-yellow-500";

    if (value <= 80)
        return "text-green-500";

    return "text-emerald-500";
}