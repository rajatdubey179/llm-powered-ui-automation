import os
import json
from dotenv import load_dotenv

load_dotenv()


def get_config() -> dict:
    env = os.getenv("TEST_ENV", "staging")
    config_map = {
        "base_url": os.getenv("BASE_URL", "https://phptravels.net"),
        "env": env,
        "headless": os.getenv("HEADLESS", "false").lower() == "true",
        "slow_mo": int(os.getenv("SLOW_MO", "500")),
        "timeout": int(os.getenv("DEFAULT_TIMEOUT", "30000")),
    }

    users_path = os.path.join(os.path.dirname(__file__), "../testdata/users.json")
    with open(users_path) as f:
        users = json.load(f)

    user = users.get(env, users.get("staging", {}))
    config_map.update(user)
    return config_map
