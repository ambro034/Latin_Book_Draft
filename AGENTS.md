# AGENTS.md

## Project Overview

BeOps is a comprehensive documentation site covering DevOps best practices, Kubernetes, and Site Reliability Engineering (SRE) principles. The project includes:

- **Jekyll-based documentation site** with GitHub Pages hosting
- **Python content generation tools** in `posts-generator/` directory
- **AI-powered content creation** using OpenAI and Google Gemini APIs

## Setup Commands

### Jekyll Site Setup
```bash
# Install Ruby dependencies
bundle install

# Start local development server
bundle exec jekyll serve --livereload

# Build for production
bundle exec jekyll build
```

### Python Tools Setup
```bash
# Navigate to posts-generator directory
cd posts-generator

# Create virtual environment
python -m venv py-feedparser

# Activate virtual environment
source py-feedparser/bin/activate  # On macOS/Linux
# or
py-feedparser\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt
```

## Code Style

### Python (posts-generator/)
- Follow PEP 8 style guidelines
- Use meaningful variable names
- Add docstrings for functions and classes
- Use type hints where appropriate
- Keep functions focused and single-purpose

### Jekyll/Markdown
- Use consistent front matter format
- Follow Jekyll naming conventions for posts
- Use descriptive file names with dates
- Maintain consistent heading hierarchy

## Testing Instructions

### Python Tools Testing
```bash
cd posts-generator
python py-feedparser.py --test
python title_generator.py --test
python youtube_processor.py --test
```

### Jekyll Site Testing
```bash
# Test build locally
bundle exec jekyll build

# Check for broken links
bundle exec jekyll build --verbose
```

## Content Generation Workflow

### AI Content Creation
1. **Configuration**: Use config files in `posts-generator/configs/`
2. **Prompts**: Store AI prompts in `posts-generator/prompts.json`
3. **Output**: Generated content goes to `posts-generator/produced_posts/`
4. **Logging**: Check `posts-generator/logs/` for execution logs

### Key Files
- `py-feedparser.py`: Main content generation script
- `title_generator.py`: AI-powered title generation
- `youtube_processor.py`: YouTube content processing
- `openai_worker_4o.py`: OpenAI API integration

## Security Considerations

- **API Keys**: Store in `.env` file (not in version control)
- **Service Accounts**: Use `configs/service-account.json` for Google APIs
- **Configurations**: Keep sensitive configs out of public repos

## File Structure Guidelines

### Posts
- Store in `_posts/` with format: `YYYY-MM-DD-title.md`
- Use consistent front matter (see `tests/site-audit/POST_TEMPLATE.md`)
- Required: `title`, `author`, `date`, `layout: post`, and `category` (one of `devops`, `k8s`, `sre`, `ai`, `job-interviews`)
- Include proper categories and tags

### Assets
- Images go in `assets/`
- Keep file sizes optimized
- Use descriptive filenames

## Deployment

### GitHub Pages
- Site automatically builds on push to main branch
- Check GitHub Actions for build status
- Live site: https://neverthesame.github.io/BeOps/
- All authoring and content changes must be made from the `gh-pages` branch.
- **Site is served under baseurl `/BeOps`.** Every internal link in templates, includes, or hand-written Liquid MUST use the `relative_url` filter (e.g. `{{ '/devops/' | relative_url }}`). Hard-coded absolute paths like `/devops/` will 404 on the live site. See `tests/site-audit/AUTHORING.md`.
- **Supported categories**: `devops`, `k8s`, `sre`, `ai`, `job-interviews`. Single source of truth is `_data/categories.yml`. Each has an index page in `_pages/<slug>.md` with `permalink: /<slug>/` and `is_category: true` in front matter. Adding a new category requires (1) appending to `_data/categories.yml`, (2) creating `_pages/<slug>.md`, and (3) updating `BEOPS_CATEGORIES` in `.github/workflows/site-audit.yml`.
- **Site audit**: `tests/site-audit/` contains a Playwright + lychee audit. It runs in CI on every push to `gh-pages` and nightly; run locally with `cd tests/site-audit && npm run audit`. The audit fails on broken links, missing-baseurl links, unreachable/orphan posts, or category pages that don't list their posts.

### Content Updates
1. Generate new content using Python tools
2. Review and edit generated content
3. Add to `_posts/` directory
4. Commit and push to trigger rebuild

## RAG over own posts (mandatory before drafting)

This repo has a hybrid-retrieval RAG store over every published post
(see `docs/architecture.md`). **Any agent — human or AI — drafting a
new post MUST consult it first** so we cite prior work and stop
repeating ourselves.

### For the CLI agent (Copilot CLI, Claude Code, etc.) — required step

Before writing a new `_posts/*.md`, run:

```bash
cd posts-generator
export NEON_DATABASE_URL='postgres://…'   # the prod DSN; same value as the GH secret
python -m rag.cli context "<one-paragraph description of the post you're about to write>"
```

The command prints a "PRIOR POSTS YOU HAVE ALREADY WRITTEN" block with
clickable URLs and an anti-rehash instruction. Use it to:

1. **Cite** every prior post your draft overlaps with (link to its URL).
2. **Avoid rehashing** angles that are already covered — pick a genuinely
   new angle or explicitly extend / contradict prior coverage.
3. If `python -m rag.cli context` returns empty: the topic is new, proceed.

If `NEON_DATABASE_URL` is unset, ask the user for it before drafting.
Skipping this step is a regression — the whole point of the RAG layer is
to prevent duplicate coverage.

### For the Python generator (`py-feedparser.py` etc.)

The integration in `openai_worker_4o.py` runs RAG **by default** when
`NEON_DATABASE_URL` is in the environment. To opt out for a one-off run:

```bash
BEOPS_RAG_DISABLED=1 python py-feedparser.py --config config-4o.json
```

After publishing a new post, the `rag-index.yml` workflow re-indexes the
corpus automatically on push to `gh-pages`.

## Common Tasks

### Adding New Content
```bash
cd posts-generator
export NEON_DATABASE_URL='postgres://…'   # enables RAG grounding
python py-feedparser.py --config config-4o.json
```

### Updating Dependencies
```bash
# Python
pip freeze > requirements.txt

# Ruby
bundle update
```

### Troubleshooting
- Check logs in `posts-generator/logs/`
- Verify API configurations
- Ensure virtual environment is activated
- Check Jekyll build output for errors

## AI Integration Notes

- **OpenAI**: Use GPT-4o for content generation
- **Google Gemini**: Use for YouTube content processing
- **Prompt Management**: All prompts stored in `prompts.json`
- **Rate Limiting**: Implement proper delays between API calls
- **Error Handling**: Log all API interactions for debugging
