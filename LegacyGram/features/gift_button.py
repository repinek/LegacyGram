from hook_utils import find_class
from LegacyGram.utils.xposed_utils import BaseHook

# public static final int BUTTON_GIFT = 1;
BUTTON_GIFT = 1

class ProfileGiftButton(BaseHook):
    def before_hooked_method(self, param):
        if self.is_enabled():
            param.setResult(None)

class ChannelGiftButton(BaseHook):
    def before_hooked_method(self, param):
        if self.is_enabled():
            # showButton(final int buttonId
            if param.args[0] == BUTTON_GIFT:
                param.setResult(None)

def register_gift_button(plugin) -> None:
    ChatActivityEnterView = find_class("org.telegram.ui.Components.ChatActivityEnterView")
    if ChatActivityEnterView:
        plugin.hook_all_methods(ChatActivityEnterView, "createGiftButton", ProfileGiftButton(plugin, "gift_button_in_chats"))

    ChatActivityChannelButtonsLayout = find_class("org.telegram.ui.Components.chat.layouts.ChatActivityChannelButtonsLayout")
    if ChatActivityChannelButtonsLayout:
        plugin.hook_all_methods(ChatActivityChannelButtonsLayout, "showButton", ChannelGiftButton(plugin, "gift_button_in_chats"))