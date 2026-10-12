import html
from html.parser import HTMLParser
import os
import posixpath
import re
import shutil
from urllib.parse import urlsplit, urlunsplit


LATEST_POSTS_LIMIT = 4
LATEST_POSTS_PLACEHOLDER = re.compile(
    r'<div(?=[^>]*\bclass="latest-posts")(?=[^>]*\bdata-latest-posts(?:="")?)[^>]*>\s*</div>'
)
COMMENTS_PLACEHOLDER = re.compile(
    r'<section(?=[^>]*\bclass="blog-comments")(?=[^>]*\bdata-comments(?:="")?)[^>]*>\s*</section>'
)
CUSDIS_APP_ID = os.environ.get("CUSDIS_APP_ID", "73a29664-ef73-4158-a3a9-3850647de254").strip()
CUSDIS_HOST = os.environ.get("CUSDIS_HOST", "https://cusdis.com").rstrip("/")
SITE_URL = os.environ.get("BLOG_SITE_URL", "https://blog.jesse-anderson.net").rstrip("/")
CANONICAL_LINK = re.compile(r'<link rel="canonical" href="[^"]*">')
SITEMAP_LOC = re.compile(r"<loc>([^<]*)</loc>")


class ArchiveListingParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.posts = []
        self._in_listing_body = False
        self._current = None
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = attrs.get("class", "").split()

        if tag == "tbody" and "list" in classes:
            self._in_listing_body = True
            return

        if not self._in_listing_body:
            return

        if tag == "tr":
            self._current = {"title": [], "href": "", "image": ""}
            return

        if not self._current:
            return

        if tag == "img" and not self._current["image"]:
            self._current["image"] = attrs.get("src", "")
            return

        if tag == "a" and "listing-title" in classes:
            self._current["href"] = attrs.get("href", "")
            self._in_title = True

    def handle_data(self, data):
        if self._current and self._in_title:
            self._current["title"].append(data)

    def handle_endtag(self, tag):
        if tag == "a" and self._in_title:
            self._in_title = False
            return

        if tag == "tr" and self._current:
            title = " ".join("".join(self._current["title"]).split())
            href = self._current["href"]
            if title and href:
                self.posts.append({
                    "title": title,
                    "href": href,
                    "image": self._current["image"],
                })
            self._current = None
            self._in_title = False
            return

        if tag == "tbody":
            self._in_listing_body = False


def site_relative_url(raw_url, target_html, site_root):
    if not raw_url:
        return ""

    parsed = urlsplit(raw_url)
    if parsed.scheme or parsed.netloc or raw_url.startswith(("#", "mailto:", "tel:")):
        return raw_url

    site_path = parsed.path
    if site_path.startswith("/"):
        site_path = site_path.lstrip("/")
    else:
        site_path = posixpath.normpath(site_path)
        if site_path.startswith("./"):
            site_path = site_path[2:]

    target_rel = os.path.relpath(target_html, site_root).replace(os.sep, "/")
    target_dir = posixpath.dirname(target_rel) or "."
    rel_path = posixpath.relpath(site_path, target_dir)
    return urlunsplit(("", "", rel_path, parsed.query, parsed.fragment))


def read_latest_posts(site_root):
    archive_path = os.path.join(site_root, "archive.html")
    if not os.path.exists(archive_path):
        print(f"Latest posts skipped: archive not found at {archive_path}")
        return []

    with open(archive_path, "r", encoding="utf-8") as archive_file:
        parser = ArchiveListingParser()
        parser.feed(archive_file.read())

    return parser.posts[:LATEST_POSTS_LIMIT]


def render_latest_posts(posts, target_html, site_root):
    if not posts:
        return '<div class="latest-posts" data-latest-posts></div>'

    items = []
    for post in posts:
        title = html.escape(post["title"])
        href = html.escape(site_relative_url(post["href"], target_html, site_root), quote=True)
        image_src = site_relative_url(post["image"], target_html, site_root)
        image_html = ""
        if image_src:
            image_html = (
                f'<img src="{html.escape(image_src, quote=True)}" alt="" '
                'class="latest-post-thumbnail" width="56" height="42" '
                'loading="lazy" decoding="async">'
            )
        items.append(f'        <li><a href="{href}">{image_html}<span>{title}</span></a></li>')

    return "\n".join([
        '<div class="latest-posts" data-latest-posts>',
        "    <h3>Latest Posts</h3>",
        '    <ul id="latest-posts-list">',
        *items,
        "    </ul>",
        "</div>",
    ])


def page_site_path(html_path, site_root):
    site_path = os.path.relpath(html_path, site_root).replace(os.sep, "/")
    if site_path.endswith("/index.html"):
        return site_path[:-len("index.html")]
    return site_path


def page_title(page):
    match = re.search(r"<title>(.*?)</title>", page, re.IGNORECASE | re.DOTALL)
    if not match:
        return ""
    title = re.sub(r"\s+", " ", match.group(1)).strip()
    return html.unescape(title)


def render_comments(page, html_path, site_root):
    site_path = page_site_path(html_path, site_root)
    page_url = f"{SITE_URL}/{site_path}"
    title = page_title(page) or site_path

    return "\n".join([
        '<section class="blog-comments" data-comments>',
        "    <h3>Comments</h3>",
        '    <div id="cusdis_thread"',
        f'         data-host="{html.escape(CUSDIS_HOST, quote=True)}"',
        f'         data-app-id="{html.escape(CUSDIS_APP_ID, quote=True)}"',
        f'         data-page-id="/{html.escape(site_path, quote=True)}"',
        f'         data-page-url="{html.escape(page_url, quote=True)}"',
        f'         data-page-title="{html.escape(title, quote=True)}"',
        '         data-theme="auto"></div>',
        f'    <script async defer src="{html.escape(CUSDIS_HOST, quote=True)}/js/cusdis.es.js"></script>',
        "</section>",
    ])


def inject_latest_posts(site_root):
    posts = read_latest_posts(site_root)
    if not posts:
        return

    latest_posts_updated = 0
    comments_updated = 0
    for root, _, files in os.walk(site_root):
        for filename in files:
            if not filename.endswith(".html"):
                continue

            html_path = os.path.join(root, filename)
            with open(html_path, "r", encoding="utf-8") as html_file:
                page = html_file.read()

            if not LATEST_POSTS_PLACEHOLDER.search(page):
                has_latest_posts = False
            else:
                has_latest_posts = True

            has_comments = bool(COMMENTS_PLACEHOLDER.search(page))
            if not has_latest_posts and not has_comments:
                continue

            if has_latest_posts:
                latest_posts = render_latest_posts(posts, html_path, site_root)
                page = LATEST_POSTS_PLACEHOLDER.sub(latest_posts, page)
                latest_posts_updated += 1

            if has_comments and CUSDIS_APP_ID:
                comments = render_comments(page, html_path, site_root)
                page = COMMENTS_PLACEHOLDER.sub(comments, page)
                comments_updated += 1

            with open(html_path, "w", encoding="utf-8", newline="") as html_file:
                html_file.write(page)

    print(f"Latest posts injected into {latest_posts_updated} page(s)")
    if CUSDIS_APP_ID:
        print(f"Cusdis comments injected into {comments_updated} page(s)")
    else:
        print("Cusdis comments skipped: set CUSDIS_APP_ID to enable anonymous comments")


def clean_url(url):
    # Cloudflare Pages serves /dir/ and /page; the index.html and .html forms 308 to them
    if url == "index.html" or url.endswith("/index.html"):
        return url[:-len("index.html")]
    if url.endswith(".html"):
        return url[:-len(".html")]
    return url


def clean_canonical_links(site_root):
    updated = 0
    for root, _, files in os.walk(site_root):
        for filename in files:
            if not filename.endswith(".html"):
                continue

            html_path = os.path.join(root, filename)
            with open(html_path, "r", encoding="utf-8") as html_file:
                page = html_file.read()

            site_path = os.path.relpath(html_path, site_root).replace(os.sep, "/")
            canonical_url = f"{SITE_URL}/{clean_url(site_path)}"
            canonical = f'<link rel="canonical" href="{html.escape(canonical_url, quote=True)}">'
            cleaned = CANONICAL_LINK.sub(lambda _: canonical, page)
            if cleaned == page:
                continue

            with open(html_path, "w", encoding="utf-8", newline="") as html_file:
                html_file.write(cleaned)
            updated += 1

    print(f"Canonical links cleaned on {updated} page(s)")


def clean_sitemap(site_root):
    # Run on the published copy only: Quarto matches entries in _site/sitemap.xml
    # by their original URLs on incremental renders.
    sitemap_path = os.path.join(site_root, "sitemap.xml")
    if not os.path.exists(sitemap_path):
        print(f"Sitemap skipped: not found at {sitemap_path}")
        return

    with open(sitemap_path, "r", encoding="utf-8") as sitemap_file:
        sitemap = sitemap_file.read()

    sitemap = SITEMAP_LOC.sub(lambda match: f"<loc>{clean_url(match.group(1))}</loc>", sitemap)

    with open(sitemap_path, "w", encoding="utf-8", newline="") as sitemap_file:
        sitemap_file.write(sitemap)

    print("Sitemap URLs cleaned")


# Names that are allowed out even though they start with a dot or an underscore.
PUBLISH_ALLOWED_PRIVATE = {".nojekyll"}
DRAFT_FRONT_MATTER = re.compile(r"^draft:\s*true\s*$", re.MULTILINE)


# Reasons a path is kept out, in the order they are reported. Drafts come first because they are
# the one a person most often needs to act on.
REASON_DRAFT = "DRAFT: `draft: true` in the post's front matter"
REASON_SCRATCH = 'scratch folder: name starts with "_"'
REASON_HIDDEN = 'hidden or cache: name starts with "."'
REASON_COMPILED = "compiled Python (.pyc)"
REASON_NOTEBOOK = "notebook (.ipynb)"
REASON_ORDER = [REASON_DRAFT, REASON_SCRATCH, REASON_HIDDEN, REASON_COMPILED, REASON_NOTEBOOK]


def private_reason(name):
    # Scratch folders (_bench, _work), caches (.jupyter_cache, __pycache__) and compiled Python
    # never belong in the published copy, whatever Quarto put in _site. Returns why, or None.
    if name in PUBLISH_ALLOWED_PRIVATE:
        return None
    if name.endswith(".pyc"):
        return REASON_COMPILED
    if name.startswith("_"):
        return REASON_SCRATCH
    if name.startswith("."):
        return REASON_HIDDEN
    return None


def is_private_name(name):
    return private_reason(name) is not None


def draft_post_dirs(project_dir):
    # Quarto still writes a full page for a post marked `draft: true`; it only leaves it out of
    # the listing, sitemap and search. Find those posts so their pages stay out of the copy.
    # Returns {post folder name: source file that carries the flag}.
    posts_dir = os.path.join(project_dir, "posts")
    drafts = {}
    if not os.path.isdir(posts_dir):
        return drafts

    for name in sorted(os.listdir(posts_dir)):
        post_dir = os.path.join(posts_dir, name)
        if not os.path.isdir(post_dir):
            continue
        for filename in sorted(os.listdir(post_dir)):
            if not filename.endswith((".qmd", ".md")):
                continue
            with open(os.path.join(post_dir, filename), "r", encoding="utf-8", errors="replace") as source:
                head = source.read(4000)
            parts = head.split("---", 2)
            if len(parts) >= 3 and DRAFT_FRONT_MATTER.search(parts[1]):
                drafts.setdefault(name, f"posts/{name}/{filename}")
    return drafts


def print_grouped(heading, entries):
    # entries: (path, reason, note). Printed under one heading, one group per reason.
    if not entries:
        return
    print(f"{heading} ({len(entries)}):")
    reasons = [r for r in REASON_ORDER if any(e[1] == r for e in entries)]
    reasons += sorted({e[1] for e in entries} - set(reasons))
    for reason in reasons:
        group = sorted(e for e in entries if e[1] == reason)
        print(f"  {reason} ({len(group)}):")
        for entry_path, _, note in group:
            print(f"    {entry_path}" + (f"   <- {note}" if note else ""))


def copy_site(source_dir, destination_dir, project_dir=None):
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    drafts = draft_post_dirs(project_dir) if project_dir else {}
    posts_root = os.path.join(source_dir, "posts")
    skipped = []

    def ignore(directory, names):
        ignored = []
        for name in names:
            is_draft = os.path.normcase(directory) == os.path.normcase(posts_root) and name in drafts
            reason = REASON_DRAFT if is_draft else private_reason(name)
            if reason is None:
                continue
            ignored.append(name)
            rel = os.path.relpath(os.path.join(directory, name), source_dir).replace(os.sep, "/")
            note = f"set `draft: false` in {drafts[name]} to publish" if is_draft else ""
            skipped.append((rel, reason, note))
        return ignored

    for item in os.listdir(source_dir):
        if item in ignore(source_dir, [item]):
            continue

        source_item = os.path.join(source_dir, item)
        destination_item = os.path.join(destination_dir, item)

        if os.path.isdir(source_item):
            shutil.copytree(source_item, destination_item, dirs_exist_ok=True, ignore=ignore)
        else:
            shutil.copy2(source_item, destination_item)

    print_grouped("Kept out of the published copy", skipped)
    if not skipped:
        print("Kept out of the published copy (0)")

    report_stale(destination_dir, drafts)


def report_stale(destination_dir, drafts):
    # The copy never deletes, so anything that reached the destination earlier is still there.
    # Report it; removing it is a decision for a person.
    stale = []
    for root, dirs, files in os.walk(destination_dir):
        if os.path.normcase(root) == os.path.normcase(destination_dir):
            # Top-level dot folders (.git, .github) belong to the published repo itself.
            dirs[:] = [d for d in dirs if not d.startswith(".")]
        rel_root = os.path.relpath(root, destination_dir).replace(os.sep, "/")
        prefix = "" if rel_root == "." else rel_root + "/"
        for name in list(dirs):
            is_draft = rel_root == "posts" and name in drafts
            reason = REASON_DRAFT if is_draft else private_reason(name)
            if reason is None:
                continue
            note = f"published earlier; {drafts[name]} is a draft now" if is_draft else ""
            stale.append((f"{prefix}{name}/", reason, note))
            dirs.remove(name)
        for name in files:
            if name.endswith(".pyc"):
                stale.append((f"{prefix}{name}", REASON_COMPILED, ""))
            elif name.endswith(".ipynb"):
                stale.append((f"{prefix}{name}", REASON_NOTEBOOK, ""))

    print_grouped("WARNING: already in the published copy and probably should not be", stale)


def main():
    project_dir = os.getcwd()
    source_dir = os.path.join(project_dir, "_site")
    # BLOG_PUBLISH_DIR lets a test render publish somewhere harmless.
    destination_dir = os.path.abspath(
        os.environ.get("BLOG_PUBLISH_DIR") or os.path.join(project_dir, "../../Blog")
    )

    print(source_dir)
    print(destination_dir)

    inject_latest_posts(source_dir)
    clean_canonical_links(source_dir)
    copy_site(source_dir, destination_dir, project_dir)
    clean_sitemap(destination_dir)


if __name__ == "__main__":
    main()
