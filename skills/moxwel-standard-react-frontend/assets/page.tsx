/*
 * /items page (TEMPLATE for a page in app/(app)/<route>/page.tsx), for logged-in users. Server component: controls
 * access, loads data from lib/ and mounts the features. Tailwind only (if layout is needed); no CSS of its own.
 */

import { PageTitle } from "@/components/ui/pageTitle";
import { ItemManager } from "@/features/items/itemManager";
import { requireUser } from "@/lib/auth/requireUser";
import { PAGES } from "@/lib/const/pages";
import * as itemsDb from "@/lib/db/items";

/**
 * /items page (logged-in user).
 * @returns The title and the item manager.
 */
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
