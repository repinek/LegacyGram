from ui.settings import Header, Input, Divider, Switch, Selector, Text, EditText
from typing import List, Any
from base_plugin import BasePlugin
from android.view import View
from utils.extera_utils import open_extera_setting

# TODO: make it class ??
plugin_instance: BasePlugin

def get_general_sub_page() -> List[Any]:
    return [
        Header(text="Settings Menu Rows Cleanup"),
        Text(text="Switch All", on_click=switch_rows, link_alias="switch_rows"),
        Switch(key="hide_premium_row", text="Hide Telegram Premium", default=False, link_alias="hide_premium_row"),
        Switch(key="hide_stars_row", text="Hide My stars", default=False, link_alias="hide_stars_row"),
        Switch(key="hide_ton_row", text="Hide My TON", default=False, link_alias="hide_ton_row"),
        Switch(key="hide_business_row", text="Hide Telegram Business", default=False, link_alias="hide_business_row"),
        Switch(key="hide_send_gift_row", text="Hide Send a Gift", default=False, link_alias="hide_send_gift_row"),
    ]

def get_premium_sub_page() -> List[Any]:
    return [
        # Header(text="This is a Sub-Page with functions related to Premium"),
        Header(text="Profile Color"),
        Text(text="Manage Reply Elements", icon="", on_click=open_reply_tab), # TODO: extera icon
        Divider(text="Powered by exteraGram")
    ]

def get_gifts_sub_page() -> List[Any]:
    return [
        # Header(text="This is a Sub-Page with functions related to Gifts"),
        Switch(
            key="gift_button_in_chats",
            text="Disable gift button in chats",
            default=False,
            link_alias="gift_button_in_chats"
        ),
        Switch(
            key="gifts_tab_in_profile",
            text="Disable gifts tab in profile",
            default=False,
            link_alias="gifts_tab_in_profile"
        ),
        Switch(
            key="stars_rating_in_profile",
            text="Disable stars rating in profile",
            default=False,
            link_alias="stars_rating_in_profile"
        )
    ]

def get_main_settings_list(plugin: BasePlugin) -> List[Any]:
    global plugin_instance
    plugin_instance = plugin
    return [
        Header(text="Setting related to..."),
        Text(
            text="General",
            icon="msg_settings",
            create_sub_fragment=get_general_sub_page,
            link_alias="general_sub_page_link"
        ),
        Text(
            text="Premium",
            icon="menu_premium_main",
            create_sub_fragment=get_premium_sub_page,
            link_alias="premium_sub_page_link"
        ),
        Text(
            text="Gifts, Stars and TON",
            icon="msg_input_gift",
            create_sub_fragment=get_gifts_sub_page,
            link_alias="gifts_sub_page_link"
        )
    ]


def switch_rows(view: View) -> None :
    global plugin_instance
    row_keys = [
        "hide_premium_row",
        "hide_stars_row",
        "hide_ton_row",
        "hide_business_row",
        "hide_send_gift_row"
    ]

    any_disabled = any(not plugin_instance.get_setting(key, False) for key in row_keys)
    new_state = True if any_disabled else False

    for key in row_keys:
         plugin_instance.set_setting(key, new_state, reload_settings=True)

def open_reply_tab(view: View) -> None:
    open_extera_setting("replyElements")