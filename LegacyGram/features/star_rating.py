from hook_utils import find_class

from LegacyGram.data.constants import Keys
from LegacyGram.utils.xposed_utils import BaseHook


# public void set(TL_stars.Tl_starsRating starsRating)
# just saying that user don't have any starsRating
class StarRatingViewSetHook(BaseHook):
    def before_hooked_method(self, param) -> None:
        if self.is_enabled():
            param.args[0] = None


def register_star_rating(plugin):
    StarRatingView = find_class("org.telegram.ui.Components.StarRatingView")
    if StarRatingView:
        plugin.hook_all_methods(StarRatingView, "set", StarRatingViewSetHook(plugin, Keys.Gifts.hide_stars_rating))
