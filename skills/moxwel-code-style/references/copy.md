# Copy

Covers the text a person reads: inside a product (UI strings, button labels, errors, toasts, empty and loading messages, any other user-facing string in code) and around the code (comments, doc comments, READMEs and other documentation). The goal is text that sounds written by a person.

## Rules

1. **ASCII punctuation and symbols only:** straight quotes, no em or en dash (use a comma, a period, a colon or parentheses), no ellipsis character (three periods, `...`, are fine), no arrow characters, no bullets or other typographic symbols. In UI strings and documentation letters keep their full orthography (accents, n with tilde); code comments drop accents (comments-and-docs.md rule 1).
2. **Buttons and links name the action,** never "Get Started", "Learn More", "Try Now", "Explore" or "Discover": `Create account`, `Download report`. UI text only.
3. **No buzzwords:** "AI Powered", "Seamless", "Revolutionary", "Cutting Edge", "Next Generation", "Powerful", "Effortless", "Intelligent", "Ultimate". Say the concrete benefit instead.
4. **Never invent facts:** no numbers, statistics, testimonials, names, dates, security or performance claims without a real source. A missing value stays empty or is a labeled placeholder (`[REAL DATA]`).
5. **No emoji** in UI text, comments or documentation, unless the user explicitly asks for them.
6. **Messages say what happened and what to do next:** an error names what failed and the next step, an empty state says why it is empty and gives the action that fills it, a loading state says what is loading. UI text only.
7. **Write like a person:** name who acts when it is known (`We updated the page`, not `The page was updated`), and cut filler (`in order to`, `it is important to note that`) and chatbot closers (`I hope this helps`).
8. **Comments and docs follow the same voice,** on top of their own rules: comments-and-docs.md sets the form of comments (short inline comments are lowercase fragments with no final period) and markdown.md the shape of documentation.

Details and gotchas, binding too: [details/copy.md](details/copy.md).

## Checklist

- [ ] Only ASCII punctuation and symbols (no dashes, ellipsis character, arrows or bullets), no emoji unless asked, no buzzword or generic button label.
- [ ] Every number, name, date or claim comes from real data or is a labeled placeholder.
- [ ] Errors, empty states and loading messages say what happened and what to do next.
- [ ] Placeholders say what goes in the field instead of faking a value.
- [ ] Comments and documentation have no buzzwords, no invented facts, no emoji and no filler, and read like a person wrote them.
