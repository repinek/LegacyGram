from hook_utils import find_class

from LegacyGram.data.constants import Keys
from LegacyGram.utils.utils import get_client_version, parse_version
from LegacyGram.utils.xposed_utils import BaseHook

# from ChatActivityChannelButtonsLayout Class
BUTTON_GIFT = 1


class ChatActivityEnterViewCreateGiftButtonHook(BaseHook):
    def before_hooked_method(self, param):
        if self.is_enabled():
            param.setResult(None)


class ChatActivityChannelButtonsLayoutShowButtonHook(BaseHook):
    def before_hooked_method(self, param):
        if self.is_enabled():
            if param.args[0] == BUTTON_GIFT:  # final int buttonId
                param.setResult(None)


def register_gift_button(plugin) -> None:
    client_version = parse_version(get_client_version())

    ChatActivityEnterView = find_class("org.telegram.ui.Components.ChatActivityEnterView")
    if ChatActivityEnterView:
        plugin.hook_all_methods(ChatActivityEnterView, "createGiftButton", ChatActivityEnterViewCreateGiftButtonHook(plugin, Keys.hide_bottom_gift_button))

    if client_version >= (12, 2, 3):  # TODO: check 12.2.3 version
        ChatActivityChannelButtonsLayout = find_class("org.telegram.ui.Components.chat.layouts.ChatActivityChannelButtonsLayout")
        if ChatActivityChannelButtonsLayout:
            plugin.hook_all_methods(
                ChatActivityChannelButtonsLayout, "showButton", ChatActivityChannelButtonsLayoutShowButtonHook(plugin, Keys.hide_bottom_gift_button)
            )
