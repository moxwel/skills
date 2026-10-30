# Copy

Covers the text a person reads inside a product: UI strings, button labels, errors, toasts, empty and loading messages, and any other user-facing string in code.

## Rules

1. **ASCII punctuation and symbols only** in user-facing text: straight quotes, no em or en dash (use a comma, a period, a colon or parentheses), no ellipsis character (three periods, `...`, are fine), no arrow characters, no bullets or other typographic symbols. Letters keep their full orthography (accents, n with tilde).
2. **Buttons and links name the action,** never "Get Started", "Learn More", "Try Now", "Explore" or "Discover": `Create account`, `Download report`.
3. **No buzzwords:** "AI Powered", "Seamless", "Revolutionary", "Cutting Edge", "Next Generation", "Powerful", "Effortless", "Intelligent", "Ultimate". Say the concrete benefit instead.
4. **Never invent facts:** no numbers, statistics, testimonials, names, dates, security or performance claims without a real source. A missing value stays empty or is a labeled placeholder (`[REAL DATA]`).
5. **No emoji** in UI text, unless the user explicitly asks for them.
6. **Messages say what happened and what to do next:** an error names what failed and the next step, an empty state says why it is empty and gives the action that fills it, a loading state says what is loading.
7. **Write like a person:** name who acts when it is known (`We updated the page`, not `The page was updated`), and cut filler (`in order to`, `it is important to note that`) and chatbot closers (`I hope this helps`).

## Details

- **Before and after:**

| Before | After |
|---|---|
| `Unlock seamless collaboration` | `Work with your team in one shared space` |
| `Get Started` | `Create account` |
| `No data available` | `No jobs yet. Run a sync to see results here` |
| `Something went wrong` | `The upload failed. Check your connection and try again` |
| `The password was updated` | `Password updated` |

- **Placeholders** in fields and cells say what goes there (`Your name`, `email@example.com`) instead of fake but plausible data (`John Doe`, `johndoe@example.com`).
- **Quotation marks and capitals:** quotes only for real quotations, titles and dialogue; no sentence in ALL CAPS for emphasis.
- **Unfinished text:** a loading message is `Loading items...` with three periods, never the single ellipsis character. A truncated value is cut by the layout (`text-overflow`), not by typing an ellipsis.
- **The project's own voice wins:** a project `CLAUDE.md`/`AGENTS.md` or a writing sample from the user sets the tone. If that voice uses an em dash or a generic label on purpose, name the rule and ask before keeping or cutting it.

## Gotchas

- **Comments and docs are not copy.** The ASCII rule covers text a person reads in the product, not code comments or these reference files.
- **A real number is fine.** Rule 4 bans invented facts, not facts that come from the data or a named source.

## Checklist

- [ ] Only ASCII punctuation and symbols (no dashes, ellipsis character, arrows or bullets), no emoji unless asked, no buzzword or generic button label.
- [ ] Every number, name, date or claim comes from real data or is a labeled placeholder.
- [ ] Errors, empty states and loading messages say what happened and what to do next.
- [ ] Placeholders say what goes in the field instead of faking a value.
