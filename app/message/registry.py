from app.message.context import AbstractBotMessageContext, Greeting
from app.message.fabric import greeting

_context_to_fabric = {
    Greeting: greeting
}

class BotMessageRegistry:
    def get_fabric(self, context: AbstractBotMessageContext):
        fabric = _context_to_fabric.get(type(context))
        if not fabric:
            raise Exception(f"Fabric for context {type(context)} were not found")
        return fabric

regirsty = BotMessageRegistry()