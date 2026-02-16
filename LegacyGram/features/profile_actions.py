from hook_utils import find_class

from LegacyGram.data.constants import Keys
from LegacyGram.utils.xposed_utils import BaseHook

KEY_GIFT = 3  # from ProfileActionsClass


# public void set(int key, boolean enabled)
class ProfileActionsSetHook(BaseHook):
    def before_hooked_method(self, param):
        if self.is_enabled():
            if param.args[0] == KEY_GIFT:
                param.setResult(None)


# calls from Insert if insertIfNotAvailable
# (List<Action> list, int key)
class ProfileActionsGetOrCreateHook(BaseHook):
    def before_hooked_method(self, param):
        if self.is_enabled():
            if param.args[1] == KEY_GIFT:
                param.setResult(None)


def register_profile_actions(plugin) -> None:
    ProfileActionsView = find_class("org.telegram.ui.Components.ProfileActionsView")
    if ProfileActionsView:
        plugin.hook_all_methods(ProfileActionsView, "set", ProfileActionsSetHook(plugin, Keys.Gifts.hide_profile_actions_gift_button))
        plugin.hook_all_methods(ProfileActionsView, "getOrCreate", ProfileActionsGetOrCreateHook(plugin, Keys.Gifts.hide_profile_actions_gift_button))
