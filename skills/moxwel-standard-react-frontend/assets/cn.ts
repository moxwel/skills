/*
 * cn(): joins CSS classes and resolves conflicts between Tailwind utilities with tailwind-merge. Needed because
 * component layout is Tailwind in the JSX: if a feature passes `className="flex-row gap-4"` to a component that already
 * has `flex-col gap-3`, both are utilities of the same layer and whichever Tailwind generates later would win, not the
 * one requested.
 */

import { twMerge } from "tailwind-merge";

/**
 * Joins classes; among conflicting Tailwind utilities the last one wins.
 * @param classes - Classes in order (falsy ones ignored); the caller's className goes last to override.
 * @returns The joined classes, without conflicting utilities.
 */
export function cn(...classes: (string | false | null | undefined)[]): string {
  return twMerge(classes.filter(Boolean).join(" "));
}
