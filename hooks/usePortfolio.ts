import { useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "../services/api";


export function useDeleteHolding() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: api.deleteHolding,

        onMutate: async (id: string) => {
            await queryClient.cancelQueries({
                queryKey: ["portfolio"],
            });

            const previousPortfolio = queryClient.getQueryData<any[]>([
                "portfolio",
            ]);

            queryClient.setQueryData<any[]>(
                ["portfolio"],
                (old = []) =>
                    old.filter((holding) => holding.id !== id)
            );

            return { previousPortfolio };
        },

        onError: (
            _error: unknown,
            _variables: string,
            context: { previousPortfolio?: any[] } | undefined
        ) => {
            if (context?.previousPortfolio) {
                queryClient.setQueryData(
                    ["portfolio"],
                    context.previousPortfolio
                );
            }
        },

        onSettled: () => {
            queryClient.invalidateQueries({
                queryKey: ["portfolio"],
            });

            queryClient.invalidateQueries({
                queryKey: ["portfolio-summary"],
            });

            queryClient.invalidateQueries({
                queryKey: ["allocation"],
            });

            queryClient.invalidateQueries({
                queryKey: ["performance"],
            });
        },
    });
}