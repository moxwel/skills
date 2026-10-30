/*
 * TEMPLATE for app/(app)/loading.tsx: server fallback while a page loads its data. Tailwind only, top on mobile and
 * centered from md.
 */

import { Spinner } from "@/components/ui/spinner";

export default function Loading() {
  return (
    <div className="flex flex-1 items-start justify-center pt-8 md:items-center md:pt-0">
      <div className="flex items-center gap-3">
        <Spinner />
        <p>Loading items...</p>
      </div>
    </div>
  );
}
