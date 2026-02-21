from typing import Any

from ui.settings import Divider, Header, Text

from LegacyGram.data.constants import GITHUB_URL, Keys
from LegacyGram.i18n.i18n import t
from LegacyGram.utils.settings_utils import Switch, check_version, open_extera_tab, open_url_view, open_version_info, switch_rows
from LegacyGram.utils.utils import get_client_version


def get_main_settings_list() -> list[Any]:
    is_version_text_red = check_version(get_client_version())

    return [
        Header(text=t("settings_options")),
        Text(text=t("switch_all"), link_alias=Keys.switch_all, on_click=switch_rows),
        Switch(text=t("hide_premium_row"), key=Keys.hide_premium_row),
        Switch(text=t("hide_stars_row"), key=Keys.hide_stars_row),
        Switch(text=t("hide_ton_row"), key=Keys.hide_ton_row),
        Switch(text=t("hide_business_row"), key=Keys.hide_business_row),
        Switch(text=t("hide_send_a_gift_row"), key=Keys.hide_send_a_gift_row),
        #
        Header(text=t("drawer_options")),
        Text(text=t("manage_drawer_options"), link_alias=Keys.drawer_options, on_click=open_extera_tab(Keys.drawer_options), icon="etg_settings"),
        #
        Header(text=t("chat_list")),
        Text(text=t("hide_stories"), link_alias=Keys.hide_stories, on_click=open_extera_tab(Keys.hide_stories), icon="etg_settings"),
        Text(
            text=t("hide_action_bar_status"),
            link_alias=Keys.hide_action_bar_status,
            on_click=open_extera_tab(Keys.hide_action_bar_status),
            icon="etg_settings",
        ),
        #
        Header(text=t("profile_buttons")),
        Switch(text=t("hide_profile_actions_stories_button"), key=Keys.hide_profile_actions_stories_button),
        Switch(text=t("hide_profile_actions_gift_button"), key=Keys.hide_profile_actions_gift_button),
        Switch(text=t("hide_profile_actions_stream_button"), key=Keys.hide_profile_actions_stream_button),
        #
        Header(text=t("profile_tabs")),
        Switch(text=t("hide_stories_tab"), subtext=t("hide_stories_tab_sub"), key=Keys.hide_stories_tab),
        Switch(text=t("hide_gifts_tab"), key=Keys.hide_gifts_tab),
        #
        Header(text=t("profile_appearance")),
        Text(text=t("manage_reply_elements"), link_alias=Keys.reply_elements, on_click=open_extera_tab(Keys.reply_elements), icon="etg_settings"),
        #
        Header(text=t("action_bar")),
        Switch(text=t("hide_action_bar_live_stream"), key=Keys.hide_action_bar_live_stream),
        Switch(text=t("hide_action_bar_archived_stories"), key=Keys.hide_action_bar_archived_stories),
        Switch(text=t("hide_action_bar_send_gift"), key=Keys.hide_action_bar_send_gift),
        Switch(text=t("hide_action_bar_boost_group"), key=Keys.hide_action_bar_boost_group),
        Switch(text=t("hide_action_bar_add_shortcut"), key=Keys.hide_action_bar_add_shortcut),
        #
        Header(text=t("gifts")),
        Switch(text=t("hide_bottom_gift_button"), key=Keys.hide_bottom_gift_button),
        Switch(text=t("hide_stars_rating"), key=Keys.hide_stars_rating),
        #
        Header(text=t("about_plugin")),
        Text(text=t("client_version", get_client_version()), on_click=open_version_info(get_client_version()), red=is_version_text_red, icon="msg_help"),
        Text(text=t("github_repository"), icon="msg_link", on_click=open_url_view(GITHUB_URL)),
        Divider(text=t("github_sub")),
    ]
