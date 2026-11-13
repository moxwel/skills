# Page metadata and link previews: details

Details and gotchas for the rules in [../social-metadata.md](../social-metadata.md).

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
