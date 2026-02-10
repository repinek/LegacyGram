from LegacyGram.utils.xposed_utils import BaseHook
from hook_utils import find_class, set_private_field, get_private_field
from java import jint, jboolean

# it's looks so bad :cry:
class ProfileTabsHook(BaseHook):
    def __init__(self, plugin, gifts_key: str, stories_key: str):
        super().__init__(plugin)
        self.gifts_key = gifts_key
        self.stories_key = stories_key

    def before_hooked_method(self, param) -> None:
        layout = param.thisObject
        user_info = get_private_field(layout, "userInfo") # org.telegram.tgnet.TLRPC$TL_userFull
        chat_info = get_private_field(layout, "info") # not a user (channel, chats..)

        # boolean hasGifts = giftsContainer != null && (userInfo != null && userInfo.stargifts_count > 0 || info != null && info.stargifts_count > 0);
        if self.plugin.get_setting(self.gifts_key, False):
            if user_info: set_private_field(user_info, "stargifts_count", jint(0))
            if chat_info: set_private_field(chat_info, "stargifts_count", jint(0))

        # # boolean hasStories in SharedMediaLayout (it's too big to paste it here, refer source)
        # if self.plugin.get_setting(self.stories_key, False):
        #     if user_info: set_private_field(user_info, "stories_pinned_available", jint(0))

# class StoriesViewBypass(BaseHook):
#     def before_hooked_method(self, param):
#         if self.is_enabled():
#             param.setResult(jboolean(False))

def register_media_layout(plugin) -> None:
    SharedMediaLayout = find_class("org.telegram.ui.Components.SharedMediaLayout")
    if SharedMediaLayout:
        plugin.hook_all_methods(SharedMediaLayout, "updateTabs",
                                ProfileTabsHook(plugin,
                                                "gifts_tab_in_profile",
                                                "stories_tab_in_profile"
                                                )
                                )

        # bypass_hook = StoriesViewBypass(plugin, "stories_tab_in_profile")
        #
        # plugin.hook_all_methods(SharedMediaLayout, "isStoriesView", bypass_hook)
        # plugin.hook_all_methods(SharedMediaLayout, "includeStories", bypass_hook)