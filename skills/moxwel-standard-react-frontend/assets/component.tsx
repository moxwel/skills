/*
 * TEMPLATE for a component in components/ui/: generic, knows nothing about the domain. Layout is Tailwind via cn (the
 * caller's className overrides it); appearance is badge.css (classes prefixed "badge"); state goes in data-*.
 */

import { cn } from "@/lib/ui/cn";
import type { ReactNode } from "react";
import "./badge.css";

type Props = { tone?: "neutral" | "success" | "danger"; className?: string; children: ReactNode };

export function Badge({ tone = "neutral", className, children }: Props) {
  const rootClassName = cn("badge inline-flex items-center gap-1 px-2 py-0.5", className);
  return (
    <span className={rootClassName} data-tone={tone}>
      {children}
    </span>
  );
}
