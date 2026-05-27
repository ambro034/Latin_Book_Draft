import os
import json
import re
from openai import AzureOpenAI


def _rag_context_block(seed_text: str) -> str:
    """Pull prior-work context from the RAG store.

    ON by default. Disable with BEOPS_RAG_DISABLED=1. Also auto-skips when
    no database URL is configured (NEON_DATABASE_URL / DATABASE_URL), so
    environments without Neon don't break.

    All RAG imports are local so importing this module never pulls in
    sentence-transformers / torch / psycopg — the smoke test enforces
    that invariant.
    """
    if os.getenv("BEOPS_RAG_DISABLED") == "1":
        return ""
    if not (os.getenv("NEON_DATABASE_URL") or os.getenv("DATABASE_URL")
            or os.getenv("BEOPS_TEST_DATABASE_URL")):
        # No DB configured — silently no-op rather than crash.
        return ""
    try:
        from rag.db import connect
        from rag.retriever import context_for
    except Exception as e:  # pragma: no cover - opt-in failure shouldn't crash
        print(f"⚠️ RAG packages not importable, skipping context: {e}")
        return ""
    try:
        with connect() as conn:
            return context_for(conn, seed_text, k=8)
    except Exception as e:  # pragma: no cover - DB hiccup shouldn't crash
        print(f"⚠️ RAG context fetch failed (continuing without it): {e}")
        return ""

def load_4o_config():
    # Get the absolute path to the current file
    current_file_path = os.path.abspath(__file__)
    # To get the directory containing the current file, not the file path itself
    current_dir = os.path.dirname(current_file_path)

    # Look for config file in configs directory first, then fallback to current directory
    config_path = os.path.join(os.path.dirname(current_dir), "configs", "config-o4-mini.json")
    if not os.path.exists(config_path):
        config_path = os.path.join(current_dir, "config-o4-mini.json")
    
    with open(config_path) as config_file:
        config_details = json.load(config_file)
    return config_details


config_details = load_4o_config()

# Initialize Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint=config_details["OPENAI_API_BASE"],
    api_key=config_details["API_KEY"],
    api_version=config_details["API_VERSION"],
)


def detect_language(text):
    """Detect if text is primarily Russian or English"""
    # Simple heuristic: count Cyrillic vs Latin characters
    cyrillic_chars = len(re.findall(r'[а-яё]', text.lower()))
    latin_chars = len(re.findall(r'[a-z]', text.lower()))
    
    if cyrillic_chars > latin_chars:
        return "russian"
    else:
        return "english"





def create_post_from_blog_post(post_text, prompt_type="basic_post_prompt", language="auto"):
    """
    Create a blog post from provided content with AI detection review.
    
    Args:
        post_text (str): The source content to create a post from
        prompt_type (str): Type of prompt to use (basic_post_prompt, technical_post_prompt, gh_repo_post_prompt)
        language (str): Language for the post ("auto", "russian", "english")
    
    Returns:
        str: The generated blog post
    """
    with open('prompts.json', 'r', encoding='utf-8') as file:
        prompts = json.loads(file.read())

    # Auto-detect language if not specified
    if language == "auto":
        language = detect_language(post_text)
    
    # Get additional guidelines
    additional_guidelines = prompts.get("additional_guidelines", "")
    
    # Select appropriate prompt based on type and language
    if prompt_type == "gh_repo_post_prompt":
        if language == "russian":
            system_message = additional_guidelines + prompts.get("gh_repo_post_prompt", "")
            user_message = "Напиши пост на русском про этот репозиторий:\n\n" + post_text[:(8192*2)]
        else:
            system_message = additional_guidelines + prompts.get("gh_repo_post_prompt_en", "")
            user_message = "Write a post in English about this repository:\n\n" + post_text[:(8192*2)]
    elif prompt_type == "technical_post_prompt":
        if language == "russian":
            system_message = additional_guidelines + prompts.get("technical_post_prompt", "")
            user_message = "Напиши технический пост на русском про эту технологию:\n\n" + post_text[:(8192*2)]
        else:
            system_message = additional_guidelines + prompts.get("technical_post_prompt_en", "")
            user_message = "Write a technical post in English about this technology:\n\n" + post_text[:(8192*2)]
    elif prompt_type == "youtube_post_prompt":
        if language == "russian":
            system_message = additional_guidelines + prompts.get("youtube_post_prompt", "")
            user_message = "Напиши пост на русском про это YouTube видео:\n\n" + post_text[:(8192*2)]
        else:
            system_message = additional_guidelines + prompts.get("youtube_post_prompt_en", "")
            user_message = "Write a post in English about this YouTube video:\n\n" + post_text[:(8192*2)]
    elif prompt_type == "linkedin_post_prompt":
        if language == "russian":
            system_message = additional_guidelines + prompts.get("linkedin_post_prompt", "")
            user_message = "Создай профессиональный пост для LinkedIn на русском языке:\n\n" + post_text[:(8192*2)]
        else:
            system_message = additional_guidelines + prompts.get("linkedin_post_prompt_en", "")
            user_message = "Create a professional LinkedIn post in English:\n\n" + post_text[:(8192*2)]
    else:  # basic_post_prompt
        if language == "russian":
            system_message = additional_guidelines + prompts.get("basic_post_prompt", "")
            user_message = "Напиши пост на русском про эту новость:\n\n" + post_text[:(8192*2)]
        else:
            system_message = additional_guidelines + prompts.get("basic_post_prompt_en", "")
            user_message = "Write a post in English about this news:\n\n" + post_text[:(8192*2)]

    # Create messages for the API
    rag_block = _rag_context_block(post_text[:2000])
    if rag_block:
        system_message = system_message + "\n\n" + rag_block

    messages = [
        {
            "role": "system",
            "content": system_message
        },
        {
            "role": "user",
            "content": user_message
        }
    ]

    try:
        # Generate initial post
        completion = client.chat.completions.create(
            model=config_details["DEPLOYMENT_NAME"],
            messages=messages,
            max_completion_tokens=4096
        )
        
        initial_post = completion.choices[0].message.content
        
        # Check if AI refused to process
        if initial_post and ("sorry" in initial_post.lower() or "can't help" in initial_post.lower() or "cannot" in initial_post.lower() or "i'm not able" in initial_post.lower()):
            print(f"⚠️ AI refused to process with prompt type '{prompt_type}'. Trying fallback approach...")
            
            # Try with a simpler, more direct prompt
            fallback_messages = [
                {
                    "role": "system",
                    "content": "You are a helpful content writer. Create engaging blog posts about technology topics."
                },
                {
                    "role": "user",
                    "content": f"Write a blog post about this content: {post_text[:4000]}"
                }
            ]
            
            try:
                fallback_completion = client.chat.completions.create(
                    model=config_details["DEPLOYMENT_NAME"],
                    messages=fallback_messages,
                    max_completion_tokens=4096
                )
                initial_post = fallback_completion.choices[0].message.content
            except Exception as fallback_error:
                print(f"Fallback also failed: {fallback_error}")
                return f"Failed to generate post. AI refused to process content."
        
        # Now apply AI detection review using human_style_rewriting
        human_style_config = prompts.get("human_style_rewriting", {})
        system_prompt = additional_guidelines + human_style_config.get("system_prompt", "")
        user_prompt = human_style_config.get("user_prompt", "")
        
        if system_prompt and user_prompt:
            # Create review messages
            review_messages = [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt + "\n\n" + initial_post
                }
            ]
            
            try:
                review_completion = client.chat.completions.create(
                    model=config_details["DEPLOYMENT_NAME"],
                    messages=review_messages,
                    max_completion_tokens=4096
                )
                
                final_post = review_completion.choices[0].message.content
                
                return final_post.strip()
                
            except Exception as e:
                print(f"Warning: AI review failed, returning original post. Error: {e}")
                return initial_post.strip()
        else:
            return initial_post.strip()
            
    except Exception as e:
        return f"Failed to generate post. Error: {e}"


def create_post_in_other_language(post_text, prompt_type, original_language):
    """
    Create a post in the opposite language of the original.
    
    Args:
        post_text (str): The source content
        prompt_type (str): Type of prompt to use
        original_language (str): The language of the original post
    
    Returns:
        str: The generated post in the other language
    """
    target_language = "english" if original_language == "russian" else "russian"
    return create_post_from_blog_post(post_text, prompt_type, target_language)
