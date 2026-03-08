from app.message.context import AbstractBotMessageContext


class BotMessageBuilder:
    def build(self, context: AbstractBotMessageContext):
        fabric = context.fabric
        return fabric(context)


message_builder = BotMessageBuilder()