from hook_utils import find_class

from LegacyGram.data.constants import Keys
from LegacyGram.utils.xposed_utils import BaseHook

gift_premium = 38


class ProfileActionBarHook(BaseHook):
    def before_hooked_method(self, param):
        # private final static int gift_premium = 38; in ProfileActivity, which call this method
        if self.is_enabled() and param.args[0] == gift_premium:
            param.setResult(None)


def register_action_bar(plugin) -> None:
    ActionBarMenuItem = find_class("org.telegram.ui.ActionBar.ActionBarMenuItem")
    if ActionBarMenuItem:
        plugin.hook_all_methods(ActionBarMenuItem, "addSubItem", ProfileActionBarHook(plugin, Keys.Gifts.hide_action_bar_send_gift))
