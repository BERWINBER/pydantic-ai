# 04_config_settings: Secure Configuration with `BaseSettings`

In production AI/ML systems, you **must not** hardcode sensitive data like API keys. These values must be loaded securely from **environment variables** (e.g., `OPENAI_API_KEY`).

The **`BaseSettings`** class (from `pydantic-settings`) automates this process:

1.  **Automation:** It searches `os.environ` for variables matching your field names.
2.  **Validation:** It ensures required keys are present and handles type conversion.

This is the standard, secure, and reliable way to manage configuration.

Run `python 04_settings_loader.py` (which simulates setting the environment variables for testing).