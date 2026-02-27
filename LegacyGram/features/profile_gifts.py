from hook_utils import find_class, get_private_field

from LegacyGram.data.constants import Keys
from LegacyGram.utils.xposed_utils import BaseHook

"""
ProfileGiftsView.update()
    -> StarsController.getProfileGiftsList()
    -> Creates Gift objects and adds to gifts ArrayList
    -> dispatchDraw() renders them around avatar

so we just clear a array with gifts and redraw View
"""


class ProfileGiftsViewUpdateHook(BaseHook):
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


def register_profile_gifts(plugin) -> None:
    ProfileGiftsView = find_class("org.telegram.ui.Stars.ProfileGiftsView")
    if ProfileGiftsView:
        plugin.hook_all_methods(ProfileGiftsView, "update", ProfileGiftsViewUpdateHook(plugin, Keys.hide_pinned_gifts))
