/*
 * Returns the session or redirects to /login. Route handlers use getSession instead and respond 401/403.
 */

import { redirect } from "next/navigation";
import { PAGES } from "@/lib/const/pages";
import { getSession } from "./session";
import type { Session } from "./types";

export async function requireUser(): Promise<Session> {
  const session = await getSession();
  if (!session) redirect(PAGES.login.href);
  return session;
}
