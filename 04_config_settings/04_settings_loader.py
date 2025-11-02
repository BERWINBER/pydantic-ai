# 04_config_settings/04_settings_loader.py

import os
from pydantic_settings import BaseSettings
from pydantic import ValidationError


class AIServiceConfig(BaseSettings):
    """Loads configuration from environment variables."""

    # Required key
    openai_api_key: str

    # Defaults if environment variable is missing
    max_tokens: int = 2048

    # Coerces "True"/"False" to bools
    debug: bool = False


# --- Setup: Simulate environment variables being set ---
# In a real environment, you would use 'export OPENAI_API_KEY=...' in your terminal
os.environ["OPENAI_API_KEY"] = "sk-simulated-key"
os.environ["MAX_TOKENS"] = "512"  # Loaded as string, converted to int
os.environ["DEBUG"] = "True"

try:
    # BaseSettings automatically loads and validates here!
    config = AIServiceConfig()

    print("✅ Configuration Loaded Securely.")
    print(f"Key Loaded: {config.openai_api_key[:12]}...")
    print(f"Max Tokens: {config.max_tokens} (Type: {type(config.max_tokens)})")
    print(f"Debug Mode: {config.debug}")

except Exception as e:
    print(f"❌ Configuration Load Error: {e}")

finally:
    # Cleanup environment for safety and repeatable tests
    del os.environ["OPENAI_API_KEY"]
    del os.environ["MAX_TOKENS"]
    del os.environ["DEBUG"]

print("-" * 20)

# --- Failure Case: Missing a Required Key ---
try:
    # Now, this will fail because the required key is missing
    AIServiceConfig()
except ValidationError as e:
    print(
        "❌ Pydantic prevents a crash by alerting us that the required key is missing."
    )
    print(e.errors()[0]["msg"])
