/*
 * useActionState for forms that keep what was typed when the action fails: React 19 clears the form after every
 * submit with the `action` prop, so the submit goes through onSubmit + startTransition and resets only on `ok`.
 */

import { startTransition, useActionState, useEffect, useRef } from "react";
import type { FormEvent } from "react";
import type { ActionState } from "@/actions/types";

type FormAction = (prevState: ActionState, formData: FormData) => Promise<ActionState>;

export function useFormAction(action: FormAction) {
  const [state, dispatch, isPending] = useActionState(action, {} as ActionState);
  const formRef = useRef<HTMLFormElement>(null);

  // On error it is not cleared: the user fixes it without retyping everything
  useEffect(() => {
    const wasSaved = Boolean(state.ok);
    if (wasSaved) formRef.current?.reset();
  }, [state]);

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    startTransition(() => dispatch(formData));
  };

  return { state, isPending, formRef, handleSubmit };
}
