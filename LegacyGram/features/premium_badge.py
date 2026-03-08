from hook_utils import find_class, get_private_field

from LegacyGram.data.constants import Keys
from LegacyGram.utils.xposed_utils import BaseHook

'''
EXPLANATION
MessageCell.GetAuthorStatus() # Works only in chats!
    -> if user not null -> call UserObject.GetEmojiStatusDocumentId & exteraBadge
        -> if EmojiStatusDocumentId not null -> return it
        -> if exteraBadge not null -> return badge
        -> if user.premium -> return msg_premium_liststar
    else logic for chat / channels (or idk)
    not checked for exteraBadge

UserObject.GetEmojiStatusDocumentIdHook()  # Only 5 calls
    called in ChatMessageCell, DrawerUserCell, DrawerProfileCell
    so it's removes emoji status from (you will see msg_premium_liststar):
        messages in chats, drawer menu, chat list, title in chat list (search is not effected)

DialogObject.GetEmojiStatusDocumentIdHook() has over than 52 calls

Some Solution: instead remove premium badge in all places, just hook isPremiumUser

If you want to go without isPremiumUser hook:
class ProfileActivityGetEmojiStatusDrawableHook(BaseHook):
    """Hide premium badge in Profile"""

    def before_hooked_method(self, param):
        if not self.is_enabled():
            return

        param.setResult(None)


class ChatAvatarContainerSetTitleHook(BaseHook):
    """Hide premium badge in chat header"""

    def before_hooked_method(self, param):
        if not self.is_enabled():
            return

        param.args[4] = False  # boolean premium
'''


class ProfileActivitySetCollectibleGiftStatusHook(BaseHook):
    def before_hooked_method(self, param):
        if not self.is_enabled():
            return
        param.setResult(None)


class UserObjectGetEmojiStatusDocumentIdHook(BaseHook):
    def before_hooked_method(self, param):
        if not self.is_enabled():
            return
        param.setResult(None)


class DialogObjectGetEmojiStatusDocumentIdHook(BaseHook):
    """
    Also fixes the issue when you click on badge in chat, you got wrong logic
    ref: see didPressUserStatus in ChatActivity using JADX
    if (!user.premium || DialogObject.getEmojiStatusDocumentId(user.emoji_status) == 0) {
        BadgesController badgesController = BadgesController.INSTANCE;
        BadgeDTO badge = badgesController.getBadge(user);
        if (badge != null) {
            // We are showing here stuff
            return;
        }
        return;
    }
    """

    def before_hooked_method(self, param):
        if not self.is_enabled():
            return
        param.setResult(0)


class ChatMessageCellGetAuthorStatusHook(BaseHook):
    """
    This hook remain only exteraGram badge in messages in chats
    ref: see original method using JADX

    java:
        private Object getAuthorStatus() {
        MessageObject messageObject;
        TLRPC.User user = this.currentUser;
        if (user != null) {
            BadgeDTO badge = BadgesController.INSTANCE.getBadge(this.currentUser);
            if (badge != null) {
                return badge
            }
            return null
        }
        return null
    """

    _BadgesController = None

    def before_hooked_method(self, param):
        if not self.is_enabled():
            return

        current_user = get_private_field(param.thisObject, "currentUser")

        if current_user:
            if self._BadgesController is None:
                self._BadgesController = find_class("com.exteragram.messenger.badges.BadgesController")
            badge = self._BadgesController.INSTANCE.getBadge(current_user)
            param.setResult(badge)
        else:
            param.setResult(None)


class MessagesControllerIsPremiumUserHook(BaseHook):
    def after_hooked_method(self, param):
        if not self.is_enabled():
            return
        param.setResult(False)


def register_premium_badge(plugin) -> None:
    ProfileActivity = find_class("org.telegram.ui.ProfileActivity")
    if ProfileActivity:
        plugin.hook_all_methods(ProfileActivity, "setCollectibleGiftStatus", ProfileActivitySetCollectibleGiftStatusHook(plugin, Keys.hide_gift_hint))

    ChatMessageCell = find_class("org.telegram.ui.Cells.ChatMessageCell")
    if ChatMessageCell:
        plugin.hook_all_methods(ChatMessageCell, "getAuthorStatus", ChatMessageCellGetAuthorStatusHook(plugin, Keys.hide_premium_badge))

    DialogObject = find_class("org.telegram.messenger.DialogObject")
    UserObject = find_class("org.telegram.messenger.UserObject")
    if DialogObject:
        plugin.hook_all_methods(DialogObject, "getEmojiStatusDocumentId", DialogObjectGetEmojiStatusDocumentIdHook(plugin, Keys.hide_premium_badge))
    if UserObject:
        plugin.hook_all_methods(UserObject, "getEmojiStatusDocumentId", UserObjectGetEmojiStatusDocumentIdHook(plugin, Keys.hide_premium_badge))

    MessagesController = find_class("org.telegram.messenger.MessagesController")
    if MessagesController:
        plugin.hook_all_methods(MessagesController, "isPremiumUser", MessagesControllerIsPremiumUserHook(plugin, Keys.hide_premium_badge))
