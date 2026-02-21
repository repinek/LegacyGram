from hook_utils import find_class

from LegacyGram.data.constants import Keys
from LegacyGram.utils.xposed_utils import BaseHook

"""
A LITTLE EXPLANATION
There's a separate code paths for addSubItem and lazilyAddSubItems
addSubItem() -> creates ActionBarMenuSubItem view immediately -> adds to popupLayout
lazilyAddSubItem() -> stores item in lazyList (deferred) -> Later: layoutLazyItems() is called ->
                item.add(parent) → creates ActionBarMenuSubItem view → adds to popupLayout

That's why we need both hooks
"""

# from ProfileActivity class
CALL_ITEM = 15  # Start Live Stream / Video Chat | NOT CALLS IN DM!
GIFT_PREMIUM = 38
CHANNEL_STORIES = 39  # Archived Stories
ADD_SHORTCUT_PROFILE = 14  # Add to home screen

# from ChatActivity class
ADD_SHORTCUT_CHAT = 24
BOOST_GROUP = 29


class ActionBarMenuItemAddSubItemHook(BaseHook):
    def before_hooked_method(self, param):
        item_id = param.args[0]  # int id

        hide_live_stream = self.plugin.get_setting(Keys.hide_action_bar_live_stream, False)
        hide_send_gift = self.plugin.get_setting(Keys.hide_action_bar_send_gift, False)
        hide_archived_stories = self.plugin.get_setting(Keys.hide_action_bar_archived_stories, False)
        hide_add_shortcut = self.plugin.get_setting(Keys.hide_action_bar_add_shortcut, False)

        if (
            (hide_live_stream and item_id == CALL_ITEM)
            or (hide_send_gift and item_id == GIFT_PREMIUM)
            or (hide_archived_stories and item_id == CHANNEL_STORIES)
            or (hide_add_shortcut and item_id == ADD_SHORTCUT_PROFILE)
        ):
            param.setResult(None)


class ActionBarMenuItemLazilyAddSubItemHook(BaseHook):
    def before_hooked_method(self, param):
        item_id = param.args[0]  # int id

        hide_add_shortcut = self.plugin.get_setting(Keys.hide_action_bar_add_shortcut, False)
        hide_boost_group = self.plugin.get_setting(Keys.hide_action_bar_boost_group, False)

        if (hide_add_shortcut and item_id == ADD_SHORTCUT_CHAT) or (hide_boost_group and item_id == BOOST_GROUP):
            param.setResult(None)


def register_action_bar(plugin) -> None:
    ActionBarMenuItem = find_class("org.telegram.ui.ActionBar.ActionBarMenuItem")
    if ActionBarMenuItem:
        plugin.hook_all_methods(ActionBarMenuItem, "addSubItem", ActionBarMenuItemAddSubItemHook(plugin))
        plugin.hook_all_methods(ActionBarMenuItem, "lazilyAddSubItem", ActionBarMenuItemLazilyAddSubItemHook(plugin))
