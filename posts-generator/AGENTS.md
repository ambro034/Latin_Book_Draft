# AGENTS.md - Posts Generator

## Subproject Overview

This directory contains AI-powered content generation tools for the BeOps documentation site. The tools use OpenAI GPT-4o and Google Gemini APIs to create technical blog posts from various sources.

## Quick Start

```bash
# Activate virtual environment
source py-feedparser/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run content generation
python py-feedparser.py --config config-4o.json
```

## Key Files

- `py-feedparser.py`: Main content generation script (1558 lines)
- `title_generator.py`: AI-powered title generation
- `youtube_processor.py`: YouTube content processing
- `openai_worker_4o.py`: OpenAI API integration
- `prompts.json`: AI prompts and instructions
- `logging_config.py`: Logging configuration

## Configuration

### API Configuration
- Use `configs/config-4o.json` for OpenAI GPT-4o
- Use `configs/config-o4-mini.json` for OpenAI GPT-4o-mini
- Use `configs/gemini-config.json` for Google Gemini

### Environment Variables
```bash
# Required for OpenAI
export OPENAI_API_KEY="your-api-key"

# Required for Google Gemini
export GOOGLE_APPLICATION_CREDENTIALS="configs/service-account.json"
```

## Content Generation Workflow

1. **Input Sources**: RSS feeds, YouTube videos, manual prompts
2. **Processing**: AI analysis and content generation
3. **Output**: Markdown files in `produced_posts/` directory
4. **Logging**: Detailed logs in `logs/` directory

## Testing

```bash
# Test content generation
python py-feedparser.py --test

# Test title generation
python title_generator.py --test

# Test YouTube processing
python youtube_processor.py --test
```

## Troubleshooting

- Check `logs/` directory for detailed error information
- Verify API configurations in `configs/` directory
- Ensure virtual environment is activated
- Check API rate limits and quotas

## Output Structure

```
produced_posts/
├── linkedin/     # LinkedIn-optimized posts
├── ru/          # Russian language posts
└── en/          # English language posts
```

## Best Practices

- Always review generated content before publishing
- Monitor API usage and costs
- Keep prompts updated in `prompts.json`
- Use appropriate config files for different use cases
- Check logs regularly for errors and improvements
