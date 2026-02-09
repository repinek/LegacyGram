from base_plugin import BasePlugin, MethodHook, MethodReplacement
from ui.settings import Header, Input, Divider, Switch, Selector, Text, EditText
from android_utils import log
from typing import List, Any
from hook_utils import find_class, set_private_field, get_private_field
from ui.bulletin import BulletinHelper
from java import jint
from android.view import View

__name__ = "LegacyGram"
__description__ = "A highly customizable plugin to remove paid and bloated features from Telegram"
__version__ = "0.0.6"
__id__ = "legacygram"
__author__ = "@wepinek"
__icon__ = "exteraPlugins/1"
__min_version__ = "12.1.1"

"""
TODO:
remove send gift button from dropdown menu in Profile
remove star levels
remove premium emoji in nickname
remove profile colors in Profile (already implemented in replies via Extera)
remove some bulletins? 
localization (normal eng and ru)

project stuff TODO:
configure ruff and toml file
do normal import instead this
"""