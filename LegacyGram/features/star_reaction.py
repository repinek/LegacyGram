from hook_utils import find_class

from LegacyGram.data.constants import Keys
from LegacyGram.utils.xposed_utils import BaseHook

TL_reactionPaid = find_class("org.telegram.tgnet.TLRPC$TL_reactionPaid")


class ReactionsLayoutInBubbleSetMessageHook(BaseHook):
    def before_hooked_method(self, param):
        if not self.is_enabled():
            return

        message_object = param.args[0]  # MessageObject messageObject
        # MessageObject.TL_messageReactions.ArrayList<ReactionCount>
        results = message_object.messageOwner.reactions.results

        to_remove = None

        for i in range(results.size()):
            reaction_count = results.get(i)  # class ReactionCount
            reaction = reaction_count.reaction  # class Reaction
            # org.telegram.tgnet.TLRPC$TL_reactionEmoji, reactionCustomEmoji, reactionEmpty or reactionPaid
            if isinstance(reaction, TL_reactionPaid):  # ty: ignore
                to_remove = reaction_count
                break

        if to_remove:
            results.remove(to_remove)


class ReactionsContainerLayoutSetVisibleReactionsListHook(BaseHook):
    def before_hooked_method(self, param):
        if not self.is_enabled():
            return

        visible_reactions_list = param.args[0]  # List<ReactionsLayoutInBubble.VisibleReaction> visibleReactionsList

        index_to_remove = None

        for i in range(visible_reactions_list.size()):
            reaction = visible_reactions_list.get(i)  # class VisibleReaction

            if reaction.isStar:  # public boolean isStar;
                index_to_remove = i
                break

        if index_to_remove is not None:
            visible_reactions_list.remove(index_to_remove)


def register_star_reaction(plugin) -> None:
    ReactionsLayoutInBubble = find_class("org.telegram.ui.Components.Reactions.ReactionsLayoutInBubble")
    if ReactionsLayoutInBubble:
        plugin.hook_all_methods(ReactionsLayoutInBubble, "setMessage", ReactionsLayoutInBubbleSetMessageHook(plugin, Keys.hide_star_reaction))

    ReactionsContainerLayout = find_class("org.telegram.ui.Components.ReactionsContainerLayout")
    if ReactionsContainerLayout:
        plugin.hook_all_methods(
            ReactionsContainerLayout, "setVisibleReactionsList", ReactionsContainerLayoutSetVisibleReactionsListHook(plugin, Keys.hide_star_reaction)
        )
