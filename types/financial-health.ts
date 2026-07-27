export interface HealthScore {
    score: number;
    status: "Excellent" | "Good" | "Fair" | "Poor";
    change: number;
}

export interface NetWorth {
    totalAssets: number;
    totalLiabilities: number;
    netWorth: number;
    changePercent: number;
}

export interface CashFlow {
    month: string;
    income: number;
    expenses: number;
    savings: number;
}

export interface SpendingCategory {
    category: string;
    amount: number;
    percentage: number;
}

export interface FinancialHealthMetrics {
    savingsRate: number;
    debtToIncomeRatio: number;
    emergencyFundProgress: number;
    emergencyFundTarget: number;
    emergencyFundCurrent: number;
}

export interface Recommendation {
    id: string;
    title: string;
    description: string;
    priority: "low" | "medium" | "high";
}

export interface FinancialHealthResponse {
    score: HealthScore;
    netWorth: NetWorth;
    metrics: FinancialHealthMetrics;
    cashFlow: CashFlow[];
    spending: SpendingCategory[];
    recommendations: Recommendation[];
}