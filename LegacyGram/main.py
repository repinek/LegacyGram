from typing import Any, Optional

from base_plugin import BasePlugin
from ui.bulletin import BulletinHelper

from LegacyGram.features.action_bar import register_action_bar
from LegacyGram.features.gift_button import register_gift_button
from LegacyGram.features.media_layout import register_media_layout
from LegacyGram.features.settings_menu import register_settings_menu
from LegacyGram.features.star_rating import register_star_rating
from LegacyGram.ui.settings import get_main_settings_list


class LegacyGramPlugin(BasePlugin):
    _instance: Optional["LegacyGramPlugin"] = None

    def on_plugin_load(self) -> None:
        LegacyGramPlugin._instance = self
        self.register_hooks()
        BulletinHelper.show_info("LegacyGram loaded!")  # debug

    def create_settings(self) -> list[Any]:
        return get_main_settings_list()

    def register_hooks(self) -> None:
        register_action_bar(self)
        register_star_rating(self)
        register_media_layout(self)
        register_settings_menu(self)
        register_gift_button(self)

    @classmethod
    def get_instance(cls) -> "LegacyGramPlugin":
        if cls._instance is None:
            BulletinHelper.show_error("Error while getting LegacyGramPlugin Instance!")
        return cls._instance
