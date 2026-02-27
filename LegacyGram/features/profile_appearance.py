from hook_utils import find_class, get_private_field

from LegacyGram.data.constants import Keys
from LegacyGram.utils.xposed_utils import BaseHook


class StarGiftPatternsDrawProfileAnimatedPatternHook(BaseHook):
    """
    We just skip drawing method lol
    """

    def before_hooked_method(self, param):
        if not self.is_enabled():
            return
        param.setResult(None)


class ProfileGiftsViewUpdateHook(BaseHook):
    """
    ProfileGiftsView.update()
        -> StarsController.getProfileGiftsList()
        -> Creates Gift objects and adds to gifts ArrayList
        -> dispatchDraw() renders them around avatar

    so we just clear a array with gifts and redraw View
    """

    def after_hooked_method(self, param):
        if not self.is_enabled():
            return

        instance = param.thisObject
        if instance is None:
            return

        try:
            gifts = get_private_field(instance, "gifts")
            if gifts is not None:
                gifts.clear()

                # redraw the view
                instance.invalidate()
        except Exception:
            pass


class ChatMessageCellSetMessageObjectInternalHook(BaseHook):
    """
    setMessageObjectInternal(MessageObject) -> read MessageObject.messageOwner.from_boosts_applied
    if boosts > 0: create BoostCounter
    just hook it and set to 0
    """

    def before_hooked_method(self, param):
        if not self.is_enabled():
            return

        message_obj = param.args[0]
        if message_obj is None:
            return

        message_owner = get_private_field(message_obj, "messageOwner")

        if message_owner is not None:
            message_owner.from_boosts_applied = 0


def register_profile_appearance(plugin) -> None:
    # Profile Background Emoji
    StarGiftPatterns = find_class("org.telegram.ui.Stars.StarGiftPatterns")
    if StarGiftPatterns:
        plugin.hook_all_methods(
            StarGiftPatterns, "drawProfileAnimatedPattern", StarGiftPatternsDrawProfileAnimatedPatternHook(plugin, Keys.hide_profile_background_emoji)
        )

    # Profile Pinned Gifts
    ProfileGiftsView = find_class("org.telegram.ui.Stars.ProfileGiftsView")
    if ProfileGiftsView:
        plugin.hook_all_methods(ProfileGiftsView, "update", ProfileGiftsViewUpdateHook(plugin, Keys.hide_profile_pinned_gifts))

    # Boost Badge
    ChatMessageCell = find_class("org.telegram.ui.Cells.ChatMessageCell")
    if ChatMessageCell:
        plugin.hook_all_methods(ChatMessageCell, "setMessageObjectInternal", ChatMessageCellSetMessageObjectInternalHook(plugin, Keys.hide_boost_badge))
