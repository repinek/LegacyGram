from base_plugin import MethodHook, MethodReplacement
from android_utils import log

class BaseHook(MethodHook):
    def __init__(self, plugin, setting_key: str = None):
        self.plugin = plugin
        self.setting_key = setting_key

    def is_enabled(self) -> bool:
        if not self.setting_key:
            return True
        return self.plugin.get_setting(self.setting_key, False)

class ReadArgsHook(MethodHook):
    def before_hooked_method(self, param):
        log(param.args)

# class ReturnTrueHook(MethodHook):
#     def __init__(self, plugin):
#         self.plugin = plugin
#
#     def after_hooked_method(self, param):
#         param.setResult(True)
#
# class ReturnFalseHook(MethodHook):
#     def __init__(self, plugin):
#         self.plugin = plugin
#
#     def after_hooked_method(self, param):
#         param.setResult(False)
#
# class ReturnFalseReplacement(MethodReplacement):
#     def replace_hooked_method(self, param):
#         return False
#
# class ReturnTrueReplacement(MethodReplacement):
#     def replace_hooked_method(self, param):
#         return True

