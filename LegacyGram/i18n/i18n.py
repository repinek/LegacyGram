from hook_utils import find_class
from locales import STRINGS

_cached_lang: str | None = None

def get_system_language() -> str:
    global _cached_lang
    if not _cached_lang:
        try:
            Locale = find_class("java.util.Locale")
            lang = Locale.getDefault().getLanguage()
            _cached_lang = lang if lang in STRINGS else "en"
        except Exception:
            _cached_lang = "en"

    return _cached_lang

def i(key: str) -> str:
    lang = get_system_language()
    target_locale = STRINGS.get(lang, STRINGS.get("en", {}))
    result = target_locale.get(key)
    if result is None:
        result = f"MISSING: {key}"

    return result


