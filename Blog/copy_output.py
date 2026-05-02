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


def copy_site(source_dir, destination_dir):
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    for item in os.listdir(source_dir):
        source_item = os.path.join(source_dir, item)
        destination_item = os.path.join(destination_dir, item)

        if os.path.isdir(source_item):
            shutil.copytree(source_item, destination_item, dirs_exist_ok=True)
        else:
            shutil.copy2(source_item, destination_item)


def main():
    source_dir = os.path.join(os.getcwd(), "_site")
    destination_dir = os.path.abspath(os.path.join(os.getcwd(), "../../Blog"))

    print(source_dir)
    print(destination_dir)

    inject_latest_posts(source_dir)
    copy_site(source_dir, destination_dir)


if __name__ == "__main__":
    main()
