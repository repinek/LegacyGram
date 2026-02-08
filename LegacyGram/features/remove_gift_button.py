from hook_utils import find_class
from base_plugin import MethodHook


class GiftInChatHook(MethodHook):
    def __init__(self, plugin):
        self.plugin = plugin

    def before_hooked_method(self, param):
        if not self.plugin.get_setting("gift_button_in_chats", False):
            return

class GiftButtonInChannelHook(MethodHook):
    def __init__(self, plugin):
        self.plugin = plugin

    def before_hooked_method(self, param):
        if not self.plugin.get_setting("gift_button_in_chats", False):
            return
        # 0 arg is final int buttonId
        if param.args[0] == 1: # public static final int BUTTON_GIFT = 1; it's id for button
            param.setResult(None)


def register_remove_gift_button(plugin) -> None:
    ChatActivityEnterView = find_class("org.telegram.ui.Components.ChatActivityEnterView")
    if ChatActivityEnterView:
        plugin.hook_all_methods(ChatActivityEnterView, "createGiftButton", GiftInChatHook(plugin))

    ChatActivityChannelButtonsLayout = find_class("org.telegram.ui.Components.chat.layouts.ChatActivityChannelButtonsLayout")
    if ChatActivityChannelButtonsLayout:
        plugin.hook_all_methods(ChatActivityChannelButtonsLayout, "showButton", GiftButtonInChannelHook(plugin))