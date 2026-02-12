from collections.abc import Callable
from typing import Any

from android.view import View
from ui.settings import Divider, Header, Text

from LegacyGram.data.constants import GITHUB_URL, Keys
from LegacyGram.i18n.i18n import t
from LegacyGram.main import LegacyGramPlugin
from LegacyGram.utils.extera_utils import open_extera_setting
from LegacyGram.utils.java_utils import get_client_version, open_url
from LegacyGram.utils.settings_utils import Switch


def get_general_sub_page() -> list[Any]:
    return [
        Header(text=t("settings_options")),
        Text(text=t("switch_all"), link_alias=Keys.General.switch_all, on_click=switch_rows),
        Switch(text=t("hide_premium_row"), key=Keys.General.hide_premium_row),
        Switch(text=t("hide_stars_row"), key=Keys.General.hide_stars_row),
        Switch(text=t("hide_ton_row"), key=Keys.General.hide_ton_row),
        Switch(text=t("hide_business_row"), key=Keys.General.hide_business_row),
        Switch(text=t("hide_send_a_gift_row"), key=Keys.General.hide_send_a_gift_row),
        Header(text=t("drawer_options")),
        Text(
            text=t("manage_drawer_options"), link_alias=Keys.General.drawer_options, on_click=open_extera_tab(Keys.General.drawer_options), icon="etg_settings"
        ),
    ]


def get_premium_sub_page() -> list[Any]:
    return [
        Header(text=t("profile_color")),
        Text(
            text=t("manage_reply_elements"), link_alias=Keys.Premium.reply_elements, on_click=open_extera_tab(Keys.Premium.reply_elements), icon="etg_settings"
        ),
        Header(text=t("chat_list")),
        Text(text=t("hide_stories"), link_alias=Keys.Premium.hide_stories, on_click=open_extera_tab(Keys.Premium.hide_stories), icon="etg_settings"),
        Text(
            text=t("hide_action_bar_status"),
            link_alias=Keys.Premium.hide_action_bar_status,
            on_click=open_extera_tab(Keys.Premium.hide_action_bar_status),
            icon="etg_settings",
        ),
        Header(text=t("profile_tabs")),
        Switch(text=t("hide_stories_tab"), key=Keys.Premium.hide_stories_tab),
    ]


def get_gifts_sub_page() -> list[Any]:
    return [
        Header(text=t("gifts_header")),
        Switch(text=t("hide_bottom_gift_button"), key=Keys.Gifts.hide_bottom_gift_button),
        Switch(text=t("hide_gifts_tab"), key=Keys.Gifts.hide_gifts_tab),
        Switch(text=t("hide_stars_rating"), key=Keys.Gifts.hide_stars_rating),
        Switch(text=t("hide_action_bar_send_gift"), key=Keys.Gifts.hide_action_bar_send_gift),
    ]


def get_about_sub_page() -> list[Any]:
    return [
        Text(text=t("client_version", get_client_version()), icon="msg_help"),
        Text(text=t("github_repository"), icon="msg_link", on_click=open_url_view(GITHUB_URL)),
        Divider(text=t("github_info")),
    ]


def get_main_settings_list() -> list[Any]:
    return [
        Header(text=t("settings_related_to")),
        Text(text=t("general"), link_alias="general_sub_page_link", create_sub_fragment=get_general_sub_page, icon="msg_settings"),
        Text(text=t("premium"), link_alias="premium_sub_page_link", create_sub_fragment=get_premium_sub_page, icon="menu_premium_main"),
        Text(text=t("gifts"), link_alias="gifts_sub_page_link", create_sub_fragment=get_gifts_sub_page, icon="msg_input_gift"),
        Divider(),
        Text(text=t("about"), link_alias="about_plugin", create_sub_fragment=get_about_sub_page, icon="msg_info"),
    ]


# helper functions
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


# lambda works too, but It's better
def open_extera_tab(tab_name: str) -> Callable[[View], None]:
    def callback(view: View):
        open_extera_setting(tab_name)

    return callback


def open_url_view(url: str) -> Callable[[View], None]:
    def callback(view: View):
        open_url(url)

    return callback
