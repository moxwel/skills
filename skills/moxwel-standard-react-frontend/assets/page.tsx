/*
 * TEMPLATE for a page in app/(app)/<route>/page.tsx: server component that gates access, loads data from lib/ and
 * mounts the features. Tailwind only (if layout is needed); no CSS of its own.
 */

import { PageTitle } from "@/components/ui/pageTitle";
import { ItemManager } from "@/features/items/itemManager";
import { requireUser } from "@/lib/auth/requireUser";
import { PAGES } from "@/lib/const/pages";
import * as itemsDb from "@/lib/db/items";

export default async function ItemsPage() {
  await requireUser();
  const items = itemsDb.listItems();

  return (
    <>
      <PageTitle icon={PAGES.items.icon}>{PAGES.items.label}</PageTitle>
      <ItemManager items={items} />
    </>
  );
}
