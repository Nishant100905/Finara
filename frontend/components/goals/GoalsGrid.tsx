"use client";

import { Goal } from "@/types/goals";
import GoalCard from "./GoalCard";

interface Props {
    goals: Goal[];
    onEdit: (goal: Goal) => void;
    onDelete: (goal: Goal) => void;
}

export default function GoalsGrid({
    goals,
    onEdit,
    onDelete,
}: Props) {
    return (
        <div className="grid gap-6 sm:grid-cols-2 xl:grid-cols-3">
            {goals.map((goal) => (
                <GoalCard
                    key={goal.id}
                    goal={goal}
                    onEdit={onEdit}
                    onDelete={onDelete}
                />
            ))}
        </div>
    );
}
