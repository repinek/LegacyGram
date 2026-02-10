from hook_utils import find_class
from ui.bulletin import BulletinHelper


def get_client_version() -> str:
    try:
        BuildVars = find_class("org.telegram.messenger.BuildVars")
        if BuildVars:
            return str(BuildVars.BUILD_VERSION_STRING)
    except Exception as e:
        BulletinHelper.show_error(f"Failed to get client version: {e}")

    return "Unknown"