from typing import List, Any
from ui.bulletin import BulletinHelper
from base_plugin import BasePlugin
from settings import get_main_settings_list
from features.remove_gift_button import register_remove_gift_button
from features.settings_menu_cleanup import register_settings_menu_cleanup
from features.remove_gifts_tab import register_remove_gifts_tab
from features.action_bar import register_remove_gift_button
from features.star_rating_view import register_star_rating_hook
from typing import Optional

class LegacyGramPlugin(BasePlugin):
    _instance: Optional['LegacyGramPlugin'] = None

    def on_plugin_load(self) -> None:
        LegacyGramPlugin._instance = self
        self.register_hooks()
        BulletinHelper.show_info("Plugin loaded!")


    def create_settings(self) -> List[Any]:
        return get_main_settings_list()

    def register_hooks(self) -> None:
        register_remove_gift_button(self)
        register_remove_gifts_tab(self)
        register_settings_menu_cleanup(self)
        register_remove_gift_button(self)
        register_star_rating_hook(self)

    @classmethod
    def get_instance(cls) -> 'LegacyGramPlugin':
        if cls._instance is None:
            raise RuntimeError("LegacyGramPlugin is not loaded yet!")
        return cls._instance

