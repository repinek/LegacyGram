from hook_utils import find_class, get_private_field, set_private_field
from java import jint
from ui.bulletin import BulletinHelper

from LegacyGram.data.constants import Keys
from LegacyGram.utils.xposed_utils import BaseHook

"""
EXPLANATION
1. Get list of row field names to hide
2. For each row to hide:
    Set its index to -1
    Decrement all row indices that come after it
3. Update total row count
"""

# from ProfileActivity Class
ROW_FIELDS = [
    "premiumRow",
    "starsRow",
    "tonRow",
    "businessRow",
    "premiumGiftingRow",
]

# when all rows hidden, there's are invisible "header"
PREMIUM_SECTIONS_ROW = "premiumSectionsRow"


class ProfileActivityUpdateRowsIdsHook(BaseHook):
    def get_rows_to_remove(self) -> list[str]:
        rows_to_remove = []

        setting_keys = [
            Keys.hide_premium_row,
            Keys.hide_stars_row,
            Keys.hide_ton_row,
            Keys.hide_business_row,
            Keys.hide_send_a_gift_row,
        ]

        for key in setting_keys:
            if self.plugin.get_setting(key, False):
                rows_to_remove.append(ROW_FIELDS[setting_keys.index(key)])

        # if all is hide -> also remove header
        if len(rows_to_remove) == len(ROW_FIELDS):
            rows_to_remove.append(PREMIUM_SECTIONS_ROW)

        return rows_to_remove

    def after_hooked_method(self, param):
        activity = param.thisObject
        rows_to_remove = self.get_rows_to_remove()

        if not rows_to_remove:
            return

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

                            if field.getModifiers() & 8:  # skip statics
                                continue

                            try:
                                current_val = field.getInt(activity)

                                if target_index < current_val < row_count:
                                    field.setInt(activity, jint(current_val - 1))
                            except Exception:
                                pass
                    row_count -= 1

            if rows_removed > 0:
                set_private_field(activity, "rowCount", jint(row_count))

        except Exception as e:
            BulletinHelper.show_error(f"Error in settings menu cleanup: {e}")


def register_settings_menu(plugin) -> None:
    ProfileActivityClass = find_class("org.telegram.ui.ProfileActivity")
    if ProfileActivityClass:
        plugin.hook_all_methods(ProfileActivityClass, "updateRowsIds", ProfileActivityUpdateRowsIdsHook(plugin))
