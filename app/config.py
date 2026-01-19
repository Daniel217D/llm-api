import os


def validate_environment_variables() -> None:
    """
    Validate that all required environment variables are set.

    Raises:
            ValueError: If any required environment variable is missing
    """
    required_vars = {
        "GIGACHAT_AUTH_KEY": "GigaChat authentication key",
        "APP_API_KEY": "Application API key for endpoint authorization",
    }

    missing_vars = []
    for var_name, description in required_vars.items():
        value = os.getenv(var_name, "").strip()
        if not value:
            missing_vars.append(f"{var_name} ({description})")

    if missing_vars:
        error_msg = "Missing required environment variables:\n" + "\n".join(
            f"  - {var}" for var in missing_vars
        )
        raise ValueError(error_msg)
