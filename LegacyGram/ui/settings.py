from collections.abc import Callable
from typing import Any

from android.view import View
from ui.settings import Divider, Header, Text

from LegacyGram.data.constants import GITHUB_URL
from LegacyGram.main import LegacyGramPlugin
from LegacyGram.utils.extera_utils import open_extera_setting
from LegacyGram.utils.java_utils import get_client_version, open_url
from LegacyGram.utils.settings_utils import Switch


def get_general_sub_page() -> list[Any]:
    return [
        Header(text="Settings Options"),
        Text(text="Switch All", on_click=switch_rows, link_alias="switch_rows"),
        Switch(key="hide_premium_row", text="Hide Telegram Premium"),
        Switch(key="hide_stars_row", text="Hide My stars"),
        Switch(key="hide_ton_row", text="Hide My TON"),
        Switch(key="hide_business_row", text="Hide Telegram Business"),
        Switch(key="hide_send_gift_row", text="Hide Send a Gift"),
        Header(text="Drawer Options"),
        Text(text="Manage Drawer Options", icon="etg_settings", on_click=open_extera_tab("drawerSettings")),
    ]


def get_premium_sub_page() -> list[Any]:
    return [
        # Header(text="This is a Sub-Page with functions related to Premium"),
        Header(text="Profile Color"),
        Text(text="Manage Reply Elements", icon="etg_settings", on_click=open_extera_tab("replyElements")),
        Header(text="Chat List"),
        Text(text="Hide Stories", icon="etg_settings", on_click=open_extera_tab("hideStories")),
        Text(text="Hide Status", icon="etg_settings", on_click=open_extera_tab("hideActionBarStatus")),
        Header(text="Profile Tabs"),
        Switch(key="stories_tab_in_profile", text="Disable Stories Tab in Profile"),
    ]


def get_gifts_sub_page() -> list[Any]:
    return [
        # Header(text="This is a Sub-Page with functions related to Gifts"),
        Header(text="Gifts Tabs, Buttons and etc..."),
        Switch(
            key="gift_button_in_chats",
            text="Disable Gift Button in Chats",
        ),
        Switch(
            key="gifts_tab_in_profile",
            text="Disable Gifts Tab in Profile",
        ),
        Switch(
            key="stars_rating_in_profile",
            text="Disable Stars Rating in Profile",
        ),
        Switch(
            key="send_gift_action_bar_in_profile",
            text="Disable Send Gift button from Action Bar",
        ),
    ]


def get_about_sub_page() -> list[Any]:
    return [Text(text=get_client_version()), Text(text="Github Repository", on_click=open_url_view(GITHUB_URL))]


def get_main_settings_list() -> list[Any]:
    return [
        Header(text="Setting related to..."),
        Text(text="General", icon="msg_settings", create_sub_fragment=get_general_sub_page, link_alias="general_sub_page_link"),
        Text(text="Premium", icon="menu_premium_main", create_sub_fragment=get_premium_sub_page, link_alias="premium_sub_page_link"),
        Text(text="Gifts, Stars and TON", icon="msg_input_gift", create_sub_fragment=get_gifts_sub_page, link_alias="gifts_sub_page_link"),
        Divider(),
        Text(
            text="About Plugin",
            icon="",  # TODO
            create_sub_fragment=get_about_sub_page,
            link_alias="about_plugin",
        ),
    ]


# helper functions
def switch_rows(view: View) -> None:
    plugin_instance = LegacyGramPlugin.get_instance()
    row_keys = ["hide_premium_row", "hide_stars_row", "hide_ton_row", "hide_business_row", "hide_send_gift_row"]

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
