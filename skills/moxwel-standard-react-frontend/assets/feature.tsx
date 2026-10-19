/*
 * Item manager (TEMPLATE for a feature in features/<feature>/). Form to create items and a list with Delete (with
 * confirmation, soft delete). Uses actions/items; the action only lets the owner or an admin delete. Layout with
 * Tailwind utilities in the JSX; its own visual styles go in itemManager.css.
 */

"use client";

import { mdiDeleteOutline, mdiPlus } from "@mdi/js";
import { useEffect, useState, useTransition } from "react";
import { createItem } from "@/actions/items/createItem";
import { deleteItem } from "@/actions/items/deleteItem";
import { AlertDialog } from "@/components/base-ui/alertDialog";
import { Button } from "@/components/base-ui/button";
import { Field, Form, Input } from "@/components/base-ui/form";
import { useActionToast } from "@/components/base-ui/toast";
import { Card } from "@/components/ui/card";
import { FORM_ACTIONS_LAYOUT } from "@/lib/const/layout";
import { MAX_NAME_LENGTH } from "@/lib/const/limits";
import { NAME_RULES } from "@/lib/const/messages";
import { formatDateTime } from "@/lib/format/formatDateTime";
import { sqliteDateToIso } from "@/lib/format/sqliteDateToIso";
import { useFormAction } from "@/lib/ui/useFormAction";
import type { ItemRow } from "@/lib/db/types";
import "@/features/shared.css";
import "./itemManager.css";

type Props = { items: ItemRow[] };

/**
 * Item manager: create and delete.
 * @param props - ItemManager props.
 * @param props.items - Active items, already loaded by the page.
 * @returns The section with the form and the list.
 */
export function ItemManager({ items }: Props) {
  const { state, isPending: isCreating, formRef, handleSubmit } = useFormAction(createItem);
  const [isDeleting, startTransition] = useTransition();
  const [deletingId, setDeletingId] = useState<number | null>(null);
  const toast = useActionToast();
  // Braces: the effect must not return whatever toast() returns
  useEffect(() => {
    toast(state);
  }, [state, toast]);

  const isEmpty = items.length === 0;

  /**
   * List item: name, date and Delete button with confirmation.
   * @param item - Item to show.
   * @returns The item's <li>.
   */
  const renderItem = (item: ItemRow) => {
    const deleteTitle = `Delete ${item.name}?`;
    const isDeletingThis = isDeleting && deletingId === item.id;
    /** Deletes the item and reports the result with a toast. */
    const confirmDelete = () => {
      setDeletingId(item.id);
      startTransition(async () => {
        toast(await deleteItem(item.id));
      });
    };
    return (
      <li key={item.id} className="itemManager-item flex items-center gap-3 py-2">
        <b className="flex-1">{item.name}</b>
        <time className="feature-muted feature-sm" dateTime={sqliteDateToIso(item.created_at)}>
          {formatDateTime(item.created_at)}
        </time>
        <AlertDialog
          triggerAriaLabel="Delete"
          triggerIcon={mdiDeleteOutline}
          confirmIcon={mdiDeleteOutline}
          title={deleteTitle}
          confirmLabel="Delete"
          disabled={isDeleting}
          isLoading={isDeletingThis}
          onConfirm={confirmDelete}
        />
      </li>
    );
  };

  const createForm = (
    <Card className="max-w-md">
      <h2>New item</h2>
      <Form ref={formRef} onSubmit={handleSubmit} errors={state.errors}>
        <Field name="name" label="Name" description={NAME_RULES}>
          <Input name="name" required maxLength={MAX_NAME_LENGTH} />
        </Field>
        <div className={FORM_ACTIONS_LAYOUT}>
          <Button type="submit" icon={mdiPlus} isLoading={isCreating}>
            Create
          </Button>
        </div>
      </Form>
    </Card>
  );

  const emptyMessage = <p className="feature-empty">No items yet.</p>;

  const itemList = (
    <Card>
      <h2>Items</h2>
      <ul className="flex flex-col">{items.map((item) => renderItem(item))}</ul>
    </Card>
  );

  return (
    <section className="flex flex-col gap-5">
      {createForm}
      {isEmpty ? emptyMessage : itemList}
    </section>
  );
}
