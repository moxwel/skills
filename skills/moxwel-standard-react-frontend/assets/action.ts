/*
 * createItem() (logged-in user) (TEMPLATE for a server action in actions/<domain>/<action>.ts): validates the name and
 * creates the item on behalf of the user. Follows the 5 security steps in order: authorization, sanitize, object
 * access, lib/, response.
 */

"use server";

import { refresh } from "next/cache";
import { requireUser } from "@/lib/auth/requireUser";
import { NAME_RULES } from "@/lib/const/messages";
import * as itemsDb from "@/lib/db/items";
import { cleanSlug, str } from "@/lib/validation/validate";
import type { ActionState } from "@/actions/types";

/**
 * Creates an item with a unique name on behalf of the user.
 * @param _prev - Previous state; required by useActionState, unused.
 * @param formData - Form with the name field.
 * @returns `ok` with the toast message, or `errors.name` if the name is invalid or already exists.
 * @throws If the DB fails for a reason other than the UNIQUE constraint (insertItem rethrows it).
 */
export async function createItem(_prev: ActionState, formData: FormData): Promise<ActionState> {
  // Every action is a public endpoint: validate here even if only a protected page uses it
  const session = await requireUser();

  const name = cleanSlug(str(formData.get("name")));
  if (!name) return { errors: { name: NAME_RULES } };

  // No owner check: on create there is no existing object (update/delete do it here)
  const wasInserted = itemsDb.insertItem(name, session.userId);
  if (!wasInserted) return { errors: { name: "That item already exists." } };

  refresh();
  return { ok: `Item ${name} created.` };
}
