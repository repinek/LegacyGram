from hook_utils import find_class, get_private_field, set_private_field
from java import jint

from LegacyGram.data.constants import Keys
from LegacyGram.utils.xposed_utils import BaseHook


class ProfileGiftsTabHook(BaseHook):
    def before_hooked_method(self, param) -> None:
        if not self.is_enabled():
            return
        layout = param.thisObject
        user_info = get_private_field(layout, "userInfo")  # org.telegram.tgnet.TLRPC$TL_userFull
        chat_info = get_private_field(layout, "info")  # not a user (channel, chats..)

        # boolean hasGifts = giftsContainer != null && (userInfo != null && userInfo.stargifts_count > 0 || info != null && info.stargifts_count > 0);
        # hasGifts = giftsContainer NOT null AND (userInfo NOT null AND userInfo.stargifts_count > 0 OR info not null AND info.stargifts_count > 0)
        # hasGifts = true AND (true AND false OR false) -> true AND (false) -> false -> tab won't be appeared
        if user_info:
            set_private_field(user_info, "stargifts_count", jint(0))
        if chat_info:
            set_private_field(chat_info, "stargifts_count", jint(0))


# hasStories so big, so refer source for full context
# && includeStories(); so we just hooking that and returning false for not rendering any
class ProfileStoriesTabHook(BaseHook):
    def before_hooked_method(self, param):
        if self.is_enabled():
            param.setResult(False)


# TODO: fix this, sometimes you can see it when open profile (default page is sets to gifts or posts)
def register_media_layout(plugin) -> None:
    SharedMediaLayout = find_class("org.telegram.ui.Components.SharedMediaLayout")
    if SharedMediaLayout:
        plugin.hook_all_methods(SharedMediaLayout, "updateTabs", ProfileGiftsTabHook(plugin, Keys.Gifts.hide_gifts_tab))

        plugin.hook_all_methods(SharedMediaLayout, "includeStories", ProfileStoriesTabHook(plugin, Keys.Premium.hide_stories_tab))
