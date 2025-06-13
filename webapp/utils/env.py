import os


def load_plain_env_variables() -> None:
    """Load environment variables prefixed with 'FLASK_' from the environment,
    and update the environment with the plain variables.
    """
    flask_env_vars = {}
    for k, v in os.environ.items():
        # Filter for variables that exist and start with 'FLASK_'
        if k.startswith("FLASK_") and v:
            # Remove the 'FLASK_' prefix and update the environment
            flask_env_vars[k[6:]] = v

    # Update the environment with the plain variables
    os.environ.update(flask_env_vars)
