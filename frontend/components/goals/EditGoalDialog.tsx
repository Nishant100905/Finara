"use client";

import { useEffect } from "react";
import { useForm } from "react-hook-form";

import { zodResolver } from "@hookform/resolvers/zod";

import {
    goalSchema,
    GoalFormValues,
} from "@/lib/validations/goals";

import { Goal } from "@/types/goals";
import { useUpdateGoal } from "@/hooks/useGoals";

import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
} from "@/components/ui/dialog";

import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

interface Props {
    goal: Goal | null;

    open: boolean;

    onOpenChange: (value: boolean) => void;
}

export default function EditGoalDialog({
    goal,
    open,
    onOpenChange,
}: Props) {
    const updateGoal = useUpdateGoal();

    const form = useForm<GoalFormValues>({
        resolver: zodResolver(goalSchema),
    });

    useEffect(() => {
        if (!goal) return;

        form.reset({
            title: goal.title,
            description: goal.description,
            category: goal.category,
            targetAmount: goal.targetAmount,
            monthlyContribution:
                goal.monthlyContribution,
            targetDate: goal.targetDate.slice(
                0,
                10
            ),
        });
    }, [goal, form]);

    async function submit(
        values: GoalFormValues
    ) {
        if (!goal) return;

        await updateGoal.mutateAsync({
            id: goal.id,
            payload: values,
        });

        onOpenChange(false);
    }

    return (
        <Dialog
            open={open}
            onOpenChange={onOpenChange}
        >
            <DialogContent className="max-w-lg rounded-3xl">
                <DialogHeader>
                    <DialogTitle>Edit Goal</DialogTitle>
                </DialogHeader>

                <form
                    className="space-y-4"
                    onSubmit={form.handleSubmit(submit)}
                >
                    <Input
                        {...form.register("title")}
                    />

                    <Input
                        {...form.register(
                            "description"
                        )}
                    />

                    <Input
                        type="number"
                        {...form.register(
                            "targetAmount",
                            {
                                valueAsNumber: true,
                            }
                        )}
                    />

                    <Input
                        type="number"
                        {...form.register(
                            "monthlyContribution",
                            {
                                valueAsNumber: true,
                            }
                        )}
                    />

                    <Input
                        type="date"
                        {...form.register(
                            "targetDate"
                        )}
                    />

                    <Button
                        className="w-full"
                        disabled={updateGoal.isPending}
                    >
                        Save Changes
                    </Button>
                </form>
            </DialogContent>
        </Dialog>
    );
}