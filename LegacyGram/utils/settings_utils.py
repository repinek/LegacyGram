from collections.abc import Callable

from android.view import View
from ui.settings import Switch as BaseSwitch


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
