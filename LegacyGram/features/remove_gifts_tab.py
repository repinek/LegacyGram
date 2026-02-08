from base_plugin import MethodHook
from hook_utils import find_class, set_private_field, get_private_field
from java import jint
from android_utils import log


# boolean hasGifts = giftsContainer != null && (userInfo != null && userInfo.stargifts_count > 0 || info != null && info.stargifts_count > 0);
# we are just hooking this and say: user don't have any gifts, skip this tab
class GiftsInProfileHook(MethodHook):
    def __init__(self, plugin):
        self.plugin = plugin

    def before_hooked_method(self, param) -> None:
        gifts_tab_disable = self.plugin.get_setting("gifts_tab_in_profile", False)
        # stars_rating_disable = self.plugin.get_setting("stars_rating_in_profile", False)
        # if not gifts_tab_disable and not stars_rating_disable:
        #     return

        layout = param.thisObject

        user_info = get_private_field(layout, "userInfo") # rg.telegram.tgnet.TLRPC$TL_userFull

        if gifts_tab_disable:
            chat_info = get_private_field(layout, "info") # not a user (channel, chats..)
            if user_info:
                set_private_field(user_info, "stargifts_count", jint(0))
            if chat_info:
                set_private_field(chat_info, "stargifts_count", jint(0))

        # if stars_rating_disable:
        #     set_private_field(user_info, "stars_rating", None)
        #     set_private_field(user_info, "stars_my_pending_rating_date", jint(0))

def register_remove_gifts_tab(plugin) -> None:
    SharedMediaLayout = find_class("org.telegram.ui.Components.SharedMediaLayout")
    if SharedMediaLayout:
        plugin.hook_all_methods(SharedMediaLayout, "updateTabs", GiftsInProfileHook(plugin))
