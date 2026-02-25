from hook_utils import find_class, get_private_field

from LegacyGram.data.constants import Keys
from LegacyGram.utils.xposed_utils import BaseHook

"""
setMessageObjectInternal(MessageObject) -> read MessageObject.messageOwner.from_boosts_applied
if boosts > 0: create BoostCounter
just hook it and set to 0
"""


class ChatMessageCellSetMessageObjectInternalHook(BaseHook):
    def before_hooked_method(self, param):
        if not self.is_enabled():
            return

        message_obj = param.args[0]
        if message_obj is None:
            return

        message_owner = get_private_field(message_obj, "messageOwner")

        if message_owner is not None:
            message_owner.from_boosts_applied = 0


def register_boost_badge(plugin) -> None:
    ChatMessageCell = find_class("org.telegram.ui.Cells.ChatMessageCell")
    if ChatMessageCell:
        plugin.hook_all_methods(ChatMessageCell, "setMessageObjectInternal", ChatMessageCellSetMessageObjectInternalHook(plugin, Keys.hide_boost_badge))
