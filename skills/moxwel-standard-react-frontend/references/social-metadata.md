# Page metadata and link previews

Covers the metadata a page exposes to browsers, search engines and social platforms: title, description, Open Graph, video and image embeds, theme color and locale. Authority: the Open Graph protocol, https://ogp.me/, and the Next.js Metadata API (`node_modules/next/dist/docs/` when it exists, since it matches the installed version).

## Rules

1. **Metadata comes from the page's own `metadata` or `generateMetadata` export** (App Router), never from hand-written `<head>` tags. The root layout sets the defaults: `metadataBase` and the title template.
2. **`metadataBase` is an absolute URL from one validated source** (an env variable checked at startup). Every relative URL in metadata resolves against it. Without it, the tags contain paths that crawlers cannot use.
3. **Every page that can be shared has `title`, and `openGraph` with `title`, `type`, `url` and `siteName`.** `og:url` is absolute. The four properties ogp.me requires are `og:title`, `og:type`, `og:image` and `og:url`.
4. **`og:type` comes from the ogp.me vocabulary.** A page that is not one of the specific types uses the general one (`website`), or a video type when the page is about a video (`video.other` for a video that is not a movie or an episode).
5. **Video embeds need the exact playable file:** an absolute `og:video` URL to a file the platform can play inline, `og:video:type` with its exact MIME type, and `og:video:width` and `og:video:height` measured from the file. Add `og:video:secure_url` when the site is served over HTTPS. The media URL must support HTTP `Range` requests (206), because platforms and Safari seek with them.
6. **Image metadata describes that image.** Never reuse the dimensions of another resource (a video's width and height for a thumbnail). Set `og:image:width` and `og:image:height` only when they are known for that exact file; otherwise send `og:image:type` alone.
7. **`og:locale` matches the UI language** in the `ll_CC` form (`es_CL`, `en_US`), and `<html lang>` matches it too.
8. **Descriptions are real text or absent.** Use the content's own summary. Never invent one, and never fill it with a generic sentence (the same honesty rule as R-38 in the antislop core).
9. **Private and hidden content emits no Open Graph tags.** Return a neutral title for a not-found or hidden resource (`{ title: "Not found" }`), with the same response as a missing one, so the metadata does not reveal that it exists. Mark non-public pages `robots: { index: false }`.
10. **`theme-color` belongs to the `viewport` export**, not to `metadata`. Next reads it from there.
11. **Crawlers do not run JavaScript.** The tags must be in the server-rendered HTML of the response. Metadata set only after hydration is invisible to them.
12. **Previews are cached by the platforms.** Changing or hiding a page does not clear what a platform already cached. Say so where the feature is described, so nobody assumes a hide is instant.

## Details

### Tags and what they need

| Tag | ogp.me | Rule |
|---|---|---|
| `og:title` | required | Plain text, the resource's own name. |
| `og:type` | required | `website`, `article`, `video.other`, `video.movie`, `video.episode`, ... Pick the closest. |
| `og:image` | required | Absolute URL. Large images give large cards: a width of at least 1200 px is common practice. |
| `og:url` | required | Absolute, canonical URL of the page. |
| `og:site_name` | optional | The product name. |
| `og:description` | optional | Only when there is a real summary (rule 8). |
| `og:locale` | optional | UI locale in `ll_CC` form (rule 7). |
| `og:video` | optional | Absolute URL of the playable file (rule 5). |
| `og:video:secure_url` | optional | Same URL over HTTPS; only when the site is HTTPS. |
| `og:video:type` | optional | Exact MIME type of the file, for example `video/mp4`. |
| `og:video:width`, `og:video:height` | optional | Measured from the file (rule 5). |
| `og:image:type`, `og:image:width`, `og:image:height` | optional | Describe that image only (rule 6). |

### Next.js mapping

- `openGraph.videos` becomes `og:video` (plus the `secure_url`, `type`, `width` and `height` fields of each entry). It is emitted for every `openGraph.type`, because the video fields belong to the basic set, not only to the `video.movie` and `video.episode` types.
- `openGraph.images` becomes `og:image`; each entry takes `url`, `secureUrl`, `type`, `width`, `height` and `alt`.
- `openGraph.locale` becomes `og:locale`; `openGraph.siteName` becomes `og:site_name`.
- A relative `openGraph.url` or image `url` resolves against `metadataBase`.
- `twitter` metadata is optional. Use `summary_large_image` for an image card. A `player` card needs a real player page at its own URL; do not add it without one.

### Testing

- Read the HTML the server sends, not the browser's DOM after hydration: `curl -s <url> | grep 'property="og:'`.
- Use the platform's own debugger when there is one, for example the Facebook Sharing Debugger (https://developers.facebook.com/tools/debug/). Platforms differ: one may play a video inline where another shows only a card.
- Check the media URL separately: it must answer with the right MIME type, and a `Range` request must return 206.

## Gotchas

- **Relative URLs with no `metadataBase`** silently produce relative tags. Nothing throws.
- **Wrong dimensions are accepted silently.** A thumbnail given the video's size looks valid in the markup and is wrong for the crawler.
- **`metadata` is not the place for `themeColor`.** It moved to `viewport`.
- **A private resource that throws in `generateMetadata`** leaks its existence through the error. Return the neutral title instead.
- **Cached previews outlive the content** (rule 12). A test that hides a page and checks the card immediately will show the old one.

## Checklist

- [ ] Every shareable page has `title` and `openGraph` with absolute `url`, a valid `type`, `siteName` and `locale`.
- [ ] `metadataBase` comes from one validated source; no relative URL reaches a tag.
- [ ] Video embeds use an absolute playable file with its exact MIME type and measured dimensions; the media answers `Range` requests.
- [ ] Image dimensions describe that image, or are absent.
- [ ] Descriptions are real text or absent; no invented summaries.
- [ ] Private, hidden and missing resources return the same neutral response and no Open Graph tags.
- [ ] `theme-color` is in `viewport`; `<html lang>` matches `og:locale`.
- [ ] The tags are in the server-rendered HTML, checked with `curl`.
