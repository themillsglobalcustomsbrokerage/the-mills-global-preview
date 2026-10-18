# Adding and editing articles and news

1. Go to `/admin/` on the site (not linked anywhere public) and choose **Sign in with GitHub**.
   Only people with write access to the repo can sign in (currently the two org owners).
2. Pick **Articles** or **News**, then **New Article / New News item**.
3. Fill in title, date, category, summary, cover image and body. Tick **Draft** to keep it unpublished.
4. Press **Publish**. This saves a commit; about a minute later the page is rebuilt and live.

Editing or unticking Draft on an existing post works the same way. Deleting a post removes its page.

## Under the hood
- Posts are Markdown files: `content/posts/articles/*.md` and `content/posts/news/*.md`.
- The automatic rebuild will be set up as part of the team's own GitHub workflow (a sample is in `docs/build-content.workflow.yml`). Until then, run `tools/build-content.py` after each change, and commit
  the generated `articles/`, `news/`, `blog.html`, `learning-pavilion.html` and `content/posts.json`.
- Cover images upload to `assets/images/blog/`. If none is set, a category default image is used.
- To rebuild locally: `python3 tools/build-content.py`.
- When the repo moves or is renamed, update `repo:` in `admin/config.yml`.
