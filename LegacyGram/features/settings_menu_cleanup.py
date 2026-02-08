from base_plugin import MethodHook
from hook_utils import find_class, set_private_field, get_private_field
from java import jint
from android_utils import log
from typing import List, Any
from ui.bulletin import BulletinHelper

# ROWS = [
#     "premiumRow",
#     "starsRow",
#     "tonRow",
#     "businessRow",
#     "premiumGiftingRow",
#     "premiumSectionsRow" # Just a spacing
#     # "botStarsBalanceRow",
#     # "botTonBalanceRow",
# ]

class SettingsMenuCleanupHook(MethodHook):
    def __init__(self, plugin):
        self.plugin = plugin

    def check_settings(self) -> List[Any]:
        rows_to_remove = []
        if self.plugin.get_setting("hide_premium_row", False):
            rows_to_remove.append("premiumRow")
        if self.plugin.get_setting("hide_stars_row", False):
            rows_to_remove.append("starsRow")
        if self.plugin.get_setting("hide_ton_row", False):
            rows_to_remove.append("tonRow")
        if self.plugin.get_setting("hide_business_row", False):
            rows_to_remove.append("businessRow")
        if self.plugin.get_setting("hide_send_gift_row", False):
            rows_to_remove.append("premiumGiftingRow")
        if len(rows_to_remove) == 5:
            rows_to_remove.append("premiumSectionsRow")
        return rows_to_remove

    # TODO comment this
    def after_hooked_method(self, param):
        activity = param.thisObject
        rows_to_remove = self.check_settings()

        try:
            row_count = get_private_field(activity, "rowCount")
            if row_count is None:
                return

            cls = activity.getClass()
            fields = cls.getDeclaredFields()

            rows_removed = 0

            for row_name in rows_to_remove:
                target_index = get_private_field(activity, row_name)

                if target_index is not None and target_index != -1:

                    rows_removed += 1
                    set_private_field(activity, row_name, jint(-1))

                    for field in fields:
                        if field.getType().toString() == "int":
                            field.setAccessible(True)

                            if field.getModifiers() & 8: # skip statics
                                continue

                            try:
                                current_val = field.getInt(activity)

                                if target_index < current_val < row_count:
                                    field.setInt(activity, jint(current_val - 1))
                            except:
                                pass
                    row_count -= 1

            if rows_removed > 0:
                set_private_field(activity, "rowCount", jint(row_count))

        except Exception as e:
            BulletinHelper.show_error(f"Error in settings menu cleanup: {e}")


def register_settings_menu_cleanup(plugin) -> None:
    ProfileActivityClass = find_class("org.telegram.ui.ProfileActivity")
    if ProfileActivityClass:
        plugin.hook_all_methods(ProfileActivityClass, "updateRowsIds", SettingsMenuCleanupHook(plugin))