import { z } from "zod";

export const goalSchema = z.object({
    title: z
        .string()
        .trim()
        .min(3, "Title is required"),

    description: z
        .string()
        .trim()
        .min(5, "Description is required"),

    category: z.enum([
        "Emergency Fund",
        "Retirement",
        "Vacation",
        "House",
        "Vehicle",
        "Education",
        "Investment",
        "Custom",
    ]),

    targetAmount: z
        .number({
            invalid_type_error:
                "Target amount is required",
        })
        .positive(),

    monthlyContribution: z
        .number({
            invalid_type_error:
                "Monthly contribution is required",
        })
        .positive(),

    targetDate: z.string().min(1),
});

export type GoalFormValues =
    z.infer<typeof goalSchema>;