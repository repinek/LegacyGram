from collections.abc import Callable

from android.view import View
from client_utils import get_last_fragment
from ui.alert import AlertDialogBuilder
from ui.settings import Switch as BaseSwitch

from LegacyGram.data.constants import Keys
from LegacyGram.i18n.i18n import t
from LegacyGram.main import LegacyGramPlugin
from LegacyGram.utils.extera_utils import open_extera_setting
from LegacyGram.utils.utils import open_url, parse_version


def Switch(
    key: str,
    text: str,
    default: bool | None = False,
    subtext: str | None = None,
    icon: str | None = None,
    on_change: Callable[[bool], None] | None = None,
    on_long_click: Callable[[View], None] | None = None,
    link_alias: str | None = None,
) -> BaseSwitch:
    """
    Uses key for link_alias, default is False
    """
    link_alias = key if link_alias is None else link_alias
    return BaseSwitch(key=key, text=text, default=default, subtext=subtext, icon=icon, on_change=on_change, on_long_click=on_long_click, link_alias=link_alias)


def check_version(version: str) -> bool:
    if parse_version(version) == (12, 1, 1):
        return False
    return True


def switch_rows(view: View) -> None:
    plugin_instance = LegacyGramPlugin.get_instance()
    row_keys = [
        Keys.General.hide_premium_row,
        Keys.General.hide_stars_row,
        Keys.General.hide_ton_row,
        Keys.General.hide_business_row,
        Keys.General.hide_send_a_gift_row,
    ]

    any_disabled = any(not plugin_instance.get_setting(key, False) for key in row_keys)
    new_state = True if any_disabled else False

    for key in row_keys:
        plugin_instance.set_setting(key, new_state, reload_settings=True)


def open_version_info(version: str) -> Callable[[View], None]:
    def callback(view: View):
        current_fragment = get_last_fragment()
        activity = current_fragment.getParentActivity() if current_fragment else None
        if not activity:
            return

        builder = AlertDialogBuilder(activity)
        if parse_version(version) == (12, 1, 1):
            builder.set_title(t("version_ok_title"))
            builder.set_message(t("version_ok_message", version))
        else:
            builder.set_title(t("version_warn_title"))
            builder.set_message(t("version_warn_message", version))

        builder.set_positive_button("OK", lambda b, w: b.dismiss())
        builder.show()

    return callback


# lambda works too, but It's better
def open_extera_tab(tab_name: str) -> Callable[[View], None]:
    def callback(view: View):
        open_extera_setting(tab_name)

    return callback


def open_url_view(url: str) -> Callable[[View], None]:
    def callback(view: View):
        open_url(url)

    return callback
