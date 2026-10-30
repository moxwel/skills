/*
 * Joins CSS classes and resolves Tailwind conflicts with tailwind-merge, so a caller's `className="flex-row gap-4"`
 * beats a component's own `flex-col gap-3` instead of depending on which utility Tailwind generates last.
 */

import { twMerge } from "tailwind-merge";

export function cn(...classes: (string | false | null | undefined)[]): string {
  return twMerge(classes.filter(Boolean).join(" "));
}
