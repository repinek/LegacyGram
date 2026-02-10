from base_plugin import BasePlugin, MethodHook, MethodReplacement
from ui.settings import Header, Input, Divider, Switch, Selector, Text, EditText
from android_utils import log
from typing import List, Any, Optional
from hook_utils import find_class, set_private_field, get_private_field
from ui.bulletin import BulletinHelper
from java import jint, jfloat, jboolean
from android.view import View

__name__ = "LegacyGram"
__description__ = "A highly customizable plugin to remove paid and bloated features from Telegram"
__version__ = "0.0.9"
__id__ = "legacygram"
__author__ = "@wepinek"
__icon__ = "LegacyGram/0"
__min_version__ = "12.2.10" # TODO: i sure about 12.1.1 (need support for icon packs and other), but not sure for adding support lower

"""
TODO:
remove premium emoji in nickname
remove profile colors in Profile (already implemented in replies via Extera)
remove some bulletins? 
localization (normal eng and ru)
take etg icon from current icon pack if exist

project stuff TODO:
configure ruff and toml file
do normal import instead this (building)
android and java typings? I don't see any
"""