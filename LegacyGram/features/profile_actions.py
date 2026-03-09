from hook_utils import find_class

from LegacyGram.data.constants import Keys
from LegacyGram.utils.xposed_utils import BaseHook

# from ProfileActionsView Class
KEY_GIFT = 3
KEY_VOICE_CHAT = 10
KEY_STREAM = 11
KEY_STORY = 12


# calls from Insert if insertIfNotAvailable
# set(int key, boolean enabled)
# getOrCreate(List<Action> list, int key)
class ProfileActionsViewHook(BaseHook):
    def __init__(self, plugin, key_index: int):
        super().__init__(plugin)
        self.key_index = key_index

    def before_hooked_method(self, param):
        hide_gifts = self.plugin.get_setting(Keys.hide_profile_actions_gift_button, False)
        hide_stories = self.plugin.get_setting(Keys.hide_profile_actions_stories_button, False)
        hide_stream = self.plugin.get_setting(Keys.hide_profile_actions_stream_button, False)

        if not hide_gifts and not hide_stories and not hide_stream:
            return

        current_key = param.args[self.key_index]

        should_hide = (
            (hide_gifts and current_key == KEY_GIFT)
            or (hide_stories and current_key == KEY_STORY)
            or (hide_stream and current_key in (KEY_VOICE_CHAT, KEY_STREAM))
        )

        if should_hide:
            param.setResult(None)


def register_profile_actions(plugin) -> None:
    ProfileActionsView = find_class("org.telegram.ui.Components.ProfileActionsView")
    if ProfileActionsView:
        plugin.hook_all_methods(ProfileActionsView, "set", ProfileActionsViewHook(plugin, 0))
        plugin.hook_all_methods(ProfileActionsView, "getOrCreate", ProfileActionsViewHook(plugin, 1))
