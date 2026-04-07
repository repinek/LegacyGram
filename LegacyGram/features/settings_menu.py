from hook_utils import find_class, get_private_field, set_private_field
from java import jint
from java.lang.reflect import Modifier

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

    def before_hooked_method(self, param):
        """Remove a bot verification description in Profile by nullify bot_verification field"""
        if not self.plugin.get_setting(Keys.hide_bot_verification, False):
            return

        instance = param.thisObject
        user_info = get_private_field(instance, "userInfo")
        chat_info = get_private_field(instance, "chatInfo")
        if user_info:
            user_info.bot_verification = None
        if chat_info:
            chat_info.bot_verification = None

    def after_hooked_method(self, param):
        rows_to_remove = self.get_rows_to_remove()
        if not rows_to_remove:
            return

        instance = param.thisObject

        row_count = get_private_field(instance, "rowCount")
        if not isinstance(row_count, int):
            return

        # Get all fields in ProfileActivity
        fields = instance.getClass().getDeclaredFields()
        valid_row_fields = []
        for field in fields:
            # only int, with "row" in lowercase name and not statics
            if field.getType().toString() == "int" and "row" in field.getName().lower() and not (field.getModifiers() & Modifier.STATIC):
                field.setAccessible(True)  # since all values is private
                valid_row_fields.append(field)

        rows_removed = 0

        for row_name in rows_to_remove:
            target_index = get_private_field(instance, row_name)  # e.g private int premiumRow
            if target_index is not None and target_index != -1:  # -1 not displayed
                rows_removed += 1
                set_private_field(instance, row_name, jint(-1))  # row will not be displayed, cuz set to 0. Instead, will be displayed versionRow

                for field in valid_row_fields:
                    current_val = field.getInt(instance)

                    if target_index < current_val < row_count:
                        field.setInt(instance, jint(current_val - 1))

                row_count -= 1
        if rows_removed > 0:
            set_private_field(instance, "rowCount", jint(row_count))


def register_settings_menu(plugin) -> None:
    ProfileActivityClass = find_class("org.telegram.ui.ProfileActivity")
    if ProfileActivityClass:
        plugin.hook_all_methods(ProfileActivityClass, "updateRowsIds", ProfileActivityUpdateRowsIdsHook(plugin))
