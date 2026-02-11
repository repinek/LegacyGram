from ui.settings import Switch as BaseSwitch
from android.view import View
from typing import Callable, Any

def Switch(key: str,
           text: str,
           default: bool = False,
           subtext: str = ...,
           icon: str = ...,
           on_change: Callable[[bool], None] = ...,
           on_long_click: Callable[[View], None] = ...,
           link_alias: str = ...
           ) -> BaseSwitch:
    """
    Uses key for link_alias, default is False
    """
    link_alias = key if link_alias is ... else link_alias
    return BaseSwitch(
        key=key,
        text=text,
        default=default,
        subtext=subtext,
        icon=icon,
        on_change=on_change,
        on_long_click=on_long_click,
        link_alias=link_alias
    )