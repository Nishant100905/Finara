export function getHealthColor(
    score: number
) {
    if (score >= 80)
        return "text-green-500";

    if (score >= 60)
        return "text-yellow-500";

    if (score >= 40)
        return "text-orange-500";

    return "text-red-500";
}

export function getHealthBadge(
    score: number
) {
    if (score >= 80)
        return "Excellent";

    if (score >= 60)
        return "Good";

    if (score >= 40)
        return "Fair";

    return "Poor";
}

export function formatCurrency(
    value: number
) {
    return new Intl.NumberFormat(
        "en-IN",
        {
            style: "currency",
            currency: "INR",
            maximumFractionDigits: 0,
        }
    ).format(value);
}

export function formatPercent(
    value: number
) {
    return `${value.toFixed(1)}%`;
}