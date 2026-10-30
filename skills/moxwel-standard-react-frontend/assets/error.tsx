/*
 * TEMPLATE for app/(app)/error.tsx: error boundary of the segment. It never shows the error itself, only a retry.
 */

"use client";

import { mdiRefresh } from "@mdi/js";
import { Button } from "@/components/base-ui/button";
import { Card } from "@/components/ui/card";

type Props = { reset: () => void };

export default function ErrorPage({ reset }: Props) {
  return (
    <div className="flex flex-1 items-start justify-center pt-8 md:items-center md:pt-0">
      <Card className="max-w-md">
        <h2>The items could not be loaded</h2>
        <p>Check your connection and try again.</p>
        <Button icon={mdiRefresh} onClick={reset}>
          Try again
        </Button>
      </Card>
    </div>
  );
}
