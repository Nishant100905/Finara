"use client";

import {
    useMutation,
    useQuery,
    useQueryClient,
} from "@tanstack/react-query";

import {
    createGoal,
    deleteGoal,
    getGoalAnalytics,
    getGoalInsights,
    getGoals,
    updateGoal,
} from "@/lib/api/goals";

import {
    CreateGoalRequest,
    UpdateGoalRequest,
} from "@/types/goals";

function invalidateGoals(
    queryClient: ReturnType<
        typeof useQueryClient
    >
) {
    return Promise.all([
        queryClient.invalidateQueries({
            queryKey: ["goals"],
        }),

        queryClient.invalidateQueries({
            queryKey: [
                "goal-analytics",
            ],
        }),

        queryClient.invalidateQueries({
            queryKey: [
                "goal-insights",
            ],
        }),
    ]);
}

export function useGoals() {
    return useQuery({
        queryKey: ["goals"],

        queryFn: getGoals,
    });
}

export function useGoalAnalytics() {
    return useQuery({
        queryKey: [
            "goal-analytics",
        ],

        queryFn:
            getGoalAnalytics,
    });
}

export function useGoalInsights() {
    return useQuery({
        queryKey: [
            "goal-insights",
        ],

        queryFn:
            getGoalInsights,
    });
}

export function useCreateGoal() {
    const queryClient =
        useQueryClient();

    return useMutation({
        mutationFn: (
            payload: CreateGoalRequest
        ) => createGoal(payload),

        onSuccess: () =>
            invalidateGoals(
                queryClient
            ),
    });
}

export function useUpdateGoal() {
    const queryClient =
        useQueryClient();

    return useMutation({
        mutationFn: ({
            id,
            payload,
        }: {
            id: string;

            payload: UpdateGoalRequest;
        }) =>
            updateGoal(
                id,
                payload
            ),

        onSuccess: () =>
            invalidateGoals(
                queryClient
            ),
    });
}

export function useDeleteGoal() {
    const queryClient =
        useQueryClient();

    return useMutation({
        mutationFn: deleteGoal,

        onSuccess: () =>
            invalidateGoals(
                queryClient
            ),
    });
}