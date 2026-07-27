export type GoalCategory =
    | "Emergency Fund"
    | "Retirement"
    | "Vacation"
    | "House"
    | "Vehicle"
    | "Education"
    | "Investment"
    | "Custom";

export type GoalStatus =
    | "Not Started"
    | "In Progress"
    | "Completed"
    | "Paused";

export interface Goal {
    id: string;

    title: string;

    description: string;

    category: GoalCategory;

    targetAmount: number;

    currentAmount: number;

    monthlyContribution: number;

    progress: number;

    targetDate: string;

    status: GoalStatus;

    createdAt: string;

    updatedAt: string;
}

export interface GoalAnalytics {
    totalGoals: number;

    activeGoals: number;

    completedGoals: number;

    totalSaved: number;

    targetAmount: number;

    completionRate: number;

    monthlyContribution: number;
}

export interface GoalInsight {
    title: string;

    description: string;

    priority: "low" | "medium" | "high";
}

export interface CreateGoalRequest {
    title: string;

    description: string;

    category: GoalCategory;

    targetAmount: number;

    monthlyContribution: number;

    targetDate: string;
}

export interface UpdateGoalRequest
    extends CreateGoalRequest { }