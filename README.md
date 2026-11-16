# Sequire Consulting website

Static site (plain HTML, CSS and a small JS file). No build step. Hosted on GitHub Pages.

## Structure

```
index.html                 Home page
nsikan-efo/index.html      Lead Consultant page  => /nsikan-efo/
services/*/index.html      One page per service  => /services/<name>/
privacy/index.html         Privacy notice        => /privacy/
terms/index.html           Terms and conditions  => /terms/
404.html                   Not-found page (GitHub Pages uses it automatically)
assets/css/styles.css      All styles; brand colours are variables at the top
assets/js/main.js          Mobile menu, "See our approach" cards, footer year
assets/fonts/              Self-hosted fonts (Cormorant Garamond, Manjari)
assets/img/                Photos, share images, touch icon
scripts/update_insights.py Refreshes Insights from the Substack feed
data/                      Saved article summaries
.github/workflows/         Daily Insights update
favicon.svg
robots.txt  sitemap.xml  llms.txt   Search and AI-search files
CNAME                      Custom domain for GitHub Pages
.nojekyll                  Tells GitHub Pages to serve files as-is
```

## Deploy on GitHub Pages

1. Create a repository (e.g. `sequire-consulting`) and upload everything in this folder to the root, including the hidden `.nojekyll` file.
2. Repository => **Settings => Pages** => Source: *Deploy from a branch* => Branch: `main`, folder `/ (root)` => Save.
3. Check `CNAME` contains the exact domain (currently `sequireconsulting.com`). Change it if the site will live on `www.` or another domain, and update every `https://www.sequireconsulting.com` URL in the HTML, `sitemap.xml`, `robots.txt` and `llms.txt` to match.
4. At the domain registrar, add DNS records:
   - Apex domain: four `A` records => `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - `www`: `CNAME` => `<github-username>.github.io`
5. Back in Settings => Pages, wait for the DNS check to pass, then tick **Enforce HTTPS**.

## After launch (search visibility)

1. **Google Search Console**: add the domain, verify it (DNS TXT record), then submit `https://www.sequireconsulting.com/sitemap.xml`.
2. **Bing Webmaster Tools**: import from Search Console. Bing also feeds ChatGPT and Copilot search.
3. **Google Business Profile**: create one for Sequire Consulting if there is a public business address or service area.
4. Test structured data at https://search.google.com/test/rich-results and https://validator.schema.org.
5. Keep the LinkedIn, Instagram and Substack bios pointing back to the website, using the same description, so search engines and AI assistants connect them.

## Insights: automatic updates from Substack

The Insights section on the home page updates itself from the Sequire Substack.

- `.github/workflows/update-insights.yml` runs every day at 07:17 Lagos time. It runs `scripts/update_insights.py`, which reads https://sequireconsulting.substack.com/feed, takes the three newest posts and rewrites only the block between `<!-- INSIGHTS:START -->` and `<!-- INSIGHTS:END -->` in `index.html`. If anything changed it commits, and GitHub Pages republishes the site.
- To update straight after publishing a post: GitHub repository, **Actions**, **Update Insights from Substack**, **Run workflow**.
- Each card shows the post's Substack subtitle. To use a different summary on the website, add the post URL and summary to `data/insight-summaries.json`.
- Thumbnails are generated from the article title in the brand colours, so no images are needed.
- One-time setup: repository **Settings**, **Actions**, **General**, **Workflow permissions**: choose **Read and write permissions**.
- GitHub pauses scheduled workflows in repositories with no activity for 60 days. The daily commits keep it active while posts are being published; if it pauses, re-enable it on the Actions tab.
- Test locally with a saved feed: `python3 scripts/update_insights.py --feed path/to/feed.xml`.

## Editing notes

- **Fonts:** the display serif (Cormorant Garamond) is used only for each page's main headline (`.display`). All other headings and body text use Manjari, a sans serif.
- **Logo:** `assets/img/sequire-consulting-logo.png` (green, header) and `sequire-consulting-logo-light.png` (cream, footer), each with a `.webp` copy. Both were cut out from the supplied JPG logo. If a vector (SVG) logo becomes available, swap it in for sharper edges.
- **Booking:** discovery-call buttons link to Calendly (https://calendly.com/nsikan-sequireconsulting/discovery-call).
- **FAQ and process:** the FAQ and "How an engagement works" structured data in `index.html` were generated from the visible text. If you edit either, update the matching JSON-LD in the `<head>`.
- **Service pages:** each service has its own page under `/services/`, written around the phrases clients in Lagos and Nigeria search with (CAC registration, SOPs, market entry, company secretarial and so on). Each has its own FAQ and structured data; if you edit a FAQ answer, update the matching JSON-LD in that page's `<head>` too.
- **Privacy notice and terms:** these are the founder's own documents, embedded word for word with their original clause numbering. Do not edit the wording on the site. If she issues a new version, replace the page content from her document.
- When content changes, update `<lastmod>` dates in `sitemap.xml`.
