/*
 * Badge: short status label (TEMPLATE for a component in components/ui/). Minimal, generic component: knows nothing
 * about the domain, only receives data and className. Layout with Tailwind in the JSX (via cn, so the caller's
 * className overrides it); appearance in badge.css (plain CSS, classes prefixed "badge"); state goes in data-*.
 */

import { cn } from "@/lib/ui/cn";
import type { ReactNode } from "react";
import "./badge.css";

type Props = { tone?: "neutral" | "success" | "danger"; className?: string; children: ReactNode };

/**
 * Short status label.
 * @param props - Badge props.
 * @param [props.tone=neutral] - Color by state; exposed as data-tone for the CSS.
 * @param [props.className] - Caller's Tailwind classes; override the default layout via cn.
 * @param props.children - Label text.
 * @returns The label (<span>).
 */
export function Badge({ tone = "neutral", className, children }: Props) {
  const rootClassName = cn("badge inline-flex items-center gap-1 px-2 py-0.5", className);
  return (
    <span className={rootClassName} data-tone={tone}>
      {children}
    </span>
  );
}
