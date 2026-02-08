from typing import List, Any
from ui.bulletin import BulletinHelper
from base_plugin import BasePlugin
from settings import get_main_settings_list
from features.remove_gift_button import register_remove_gift_button
from features.settings_menu_cleanup import register_settings_menu_cleanup
from features.remove_gifts_tab import register_remove_gifts_tab

class LegacyGramPlugin(BasePlugin):
    def on_plugin_load(self) -> None:
        BulletinHelper.show_info("Plugin loaded!")
        register_remove_gift_button(self)
        register_remove_gifts_tab(self)
        register_settings_menu_cleanup(self)

    def create_settings(self) -> List[Any]:
        return get_main_settings_list(self)
