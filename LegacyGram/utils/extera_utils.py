from hook_utils import find_class
from ui.bulletin import BulletinHelper


# thx jadx
def open_extera_setting(alias: str, plugin_id: str | None = None):
    SettingsRegistry = find_class("com.exteragram.messenger.preferences.utils.SettingsRegistry")

    if SettingsRegistry:
        try:
            registry_instance = SettingsRegistry.getInstance()
            registry_instance.handleLink(alias, plugin_id)

        except Exception as e:
            BulletinHelper.show_error(f"Failed to invoke extera handleLink: {e}")
