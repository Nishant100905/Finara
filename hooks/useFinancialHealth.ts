"use client";

import {
    useMutation,
    useQuery,
    useQueryClient,
} from "@tanstack/react-query";

import {
    getFinancialHealth,
    refreshFinancialHealth,
} from "@/lib/api/financial-health";

export function useFinancialHealth() {
    return useQuery({
        queryKey: ["financial-health"],

        queryFn: getFinancialHealth,

        staleTime: 1000 * 60 * 5,

        refetchOnWindowFocus: false,
    });
}

export function useRefreshFinancialHealth() {
    const queryClient =
        useQueryClient();

    return useMutation({
        mutationFn:
            refreshFinancialHealth,

        onSuccess: () => {
            queryClient.invalidateQueries({
                queryKey: [
                    "financial-health",
                ],
            });
        },
    });
}