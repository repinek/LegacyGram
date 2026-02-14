from typing import Any

from hook_utils import find_class, get_private_field, set_private_field
from java import jint

from LegacyGram.data.constants import Keys
from LegacyGram.utils.xposed_utils import BaseHook

"""
EXPLANATION
code from updateTabs, but it's looks same in SharedMediaLayout constructor
boolean hasGifts = giftsContainer != null && (userInfo != null && userInfo.stargifts_count > 0 || info != null && info.stargifts_count > 0);
hasGifts = giftsContainer NOT null AND (userInfo NOT null AND userInfo.stargifts_count > 0 OR info not null AND info.stargifts_count > 0)
hasGifts = true AND (true AND false OR false) -> true AND (false) -> false -> tab won't be appeared

Similar to gifts, we change 'stories_pinned_available' and 'stories' collection to prevent appearing tab.
also we hook setChatInfo and setUserInfo which move you to stories tab sometimes
... .setInitialTabId(... ? TAB_ARCHIVED_STORIES : TAB_STORIES);
for weird StoriesCollections logic we just set visibility to false (I'm lazy a little to check they logic, it's working fine)
"""

TL_profileTabGifts = find_class("org.telegram.tgnet.TLRPC$TL_profileTabGifts")
TL_profileTabPosts = find_class("org.telegram.tgnet.TLRPC$TL_profileTabPosts")


class SharedMediaLayoutHook(BaseHook):
    def before_hooked_method(self, param) -> None:
        hide_gifts = self.plugin.get_setting(Keys.Gifts.hide_gifts_tab, False)
        hide_stories = self.plugin.get_setting(Keys.Premium.hide_stories_tab, False)
        if not hide_gifts and not hide_stories:
            return

        chat_info = param.args[5]  # TLRPC.ChatFull chatInfo
        user_info = param.args[6]  # TLRPC.UserFull userInfo

        # log(user_info)
        possible_targets = [chat_info, user_info]

        for target in possible_targets:
            if hide_gifts:
                remove_gifts(target)
            if hide_stories:
                remove_stories(target)


class UpdateTabsHook(BaseHook):
    def before_hooked_method(self, param) -> None:
        hide_gifts = self.plugin.get_setting(Keys.Gifts.hide_gifts_tab, False)
        hide_stories = self.plugin.get_setting(Keys.Premium.hide_stories_tab, False)
        if not hide_gifts and not hide_stories:
            return

        layout = param.thisObject
        user_info = get_private_field(layout, "userInfo")  # org.telegram.tgnet.TLRPC$TL_userFull
        chat_info = get_private_field(layout, "info")  # not a user (channel, chats..)

        possible_targets = [chat_info, user_info]

        for target in possible_targets:
            if hide_gifts:
                remove_gifts(target)
            if hide_stories:
                remove_stories(target)


class SetInfoHook(BaseHook):
    def before_hooked_method(self, param):
        if not self.is_enabled():
            return

        info_obj = param.args[0]
        remove_stories(info_obj)


# not the best how you can do it, but still fine
class SetVisibilityHook(BaseHook):
    def before_hooked_method(self, param):
        if not self.is_enabled():
            return
        # boolean visibility
        if param.args[0] is True:
            param.args[0] = False


def remove_gifts(obj: Any):
    if obj:
        set_private_field(obj, "stargifts_count", jint(0))
        main_tab = get_private_field(obj, "main_tab")
        if isinstance(main_tab, TL_profileTabGifts):
            set_private_field(obj, "main_tab", None)


def remove_stories(obj: Any):
    if obj:
        set_private_field(obj, "stories_pinned_available", False)
        set_private_field(obj, "stories", None)
        main_tab = get_private_field(obj, "main_tab")
        if isinstance(main_tab, TL_profileTabPosts):
            set_private_field(obj, "main_tab", None)


# TODO: fix my profile (remove posts and archived posts)
def register_media_layout(plugin) -> None:
    SharedMediaLayout = find_class("org.telegram.ui.Components.SharedMediaLayout")
    if SharedMediaLayout:
        plugin.hook_all_constructors(SharedMediaLayout, SharedMediaLayoutHook(plugin))
        plugin.hook_all_methods(SharedMediaLayout, "updateTabs", UpdateTabsHook(plugin))
        info_hook = SetInfoHook(plugin, Keys.Premium.hide_stories_tab)
        plugin.hook_all_methods(SharedMediaLayout, "setChatInfo", info_hook)
        plugin.hook_all_methods(SharedMediaLayout, "setUserInfo", info_hook)

    ProfileStoriesCollectionTabs = find_class("org.telegram.ui.ProfileStoriesCollectionTabs")
    if ProfileStoriesCollectionTabs:
        plugin.hook_all_methods(ProfileStoriesCollectionTabs, "setVisibility", SetVisibilityHook(plugin, Keys.Premium.hide_stories_tab))
