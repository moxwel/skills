/*
 * useFormAction: useActionState for forms that do NOT lose what was typed when the action fails. With the form's
 * `action` prop, React 19 clears the form after every submit (success or failure); here the submit goes through
 * onSubmit + startTransition and the form is cleared by hand only on `ok`. On `errors`, the Base UI Form focuses and
 * selects the first invalid field. Client only. Usage:
 * `<Form ref={formRef} onSubmit={handleSubmit} errors={state.errors}>`.
 */

import { startTransition, useActionState, useEffect, useRef } from "react";
import type { FormEvent } from "react";
import type { ActionState } from "@/actions/types";

type FormAction = (prevState: ActionState, formData: FormData) => Promise<ActionState>;

/**
 * Connects a server action to a Form without clearing it when it fails.
 * @param action - Server action with the useActionState signature.
 * @returns `state` (last ActionState), `isPending`, `formRef` (for the Form) and `handleSubmit`.
 */
export function useFormAction(action: FormAction) {
  const [state, dispatch, isPending] = useActionState(action, {} as ActionState);
  const formRef = useRef<HTMLFormElement>(null);

  // On error it is not cleared: the user fixes it without retyping everything
  useEffect(() => {
    const wasSaved = Boolean(state.ok);
    if (wasSaved) formRef.current?.reset();
  }, [state]);

  /**
   * Sends the form values to the action without letting React or the browser clear it.
   * @param event - Form submit event.
   */
  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    startTransition(() => dispatch(formData));
  };

  return { state, isPending, formRef, handleSubmit };
}
