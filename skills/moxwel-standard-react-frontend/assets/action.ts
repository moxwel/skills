/*
 * TEMPLATE for a server action (actions/<domain>/<action>.ts): creates an item for the logged-in user. Follows the 5
 * security steps in order: authorization, sanitize, object access, lib/, response.
 */

"use server";

import { refresh } from "next/cache";
import { requireUser } from "@/lib/auth/requireUser";
import { NAME_RULES } from "@/lib/const/messages";
import * as itemsDb from "@/lib/db/items";
import { cleanSlug, formText } from "@/lib/validation/validate";
import type { ActionState } from "@/actions/types";

/**
 * Creates the user's item; returns `errors.name` if the name is invalid or already exists.
 * @throws If the DB fails for a reason other than the UNIQUE constraint (insertItem rethrows it).
 */
export async function createItem(_previousState: ActionState, formData: FormData): Promise<ActionState> {
  // any client can call an action, so validate here
  const session = await requireUser();

  const name = cleanSlug(formText(formData.get("name")));
  if (!name) return { errors: { name: NAME_RULES } };

  // no owner check on create, update and delete do it
  const itemId      = itemsDb.insertItem(name, session.userId);
  const isDuplicate = itemId === null;
  if (isDuplicate) return { errors: { name: "That item already exists." } };

  refresh();
  return { ok: `Item ${name} created.` };
}
