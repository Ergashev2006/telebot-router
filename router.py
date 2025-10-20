import telebot.async_telebot 
from typing import List, Callable, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class AsyncRouter:
    """
    Router for AsyncTeleBot
    """
    
    def __init__(self, name: str = ""):
        self.name = name
        self.message_handlers = []
        self.callback_handlers = []
        logger.info(f"⚡ AsyncRouter '{name}' created")
    
    def message_handler(self, commands=None, func=None, content_types=None, **kwargs):
        """Async message handler decorator"""
        def decorator(handler: Callable):
            self.message_handlers.append({
                'handler': handler,
                'commands': commands,
                'func': func,
                'content_types': content_types or ['text'],
                **kwargs
            })
            logger.debug(f"📨 Added message handler to async router: {handler.__name__}")
            return handler
        return decorator
    
    def callback_query_handler(self, func=None, **kwargs):
        """Async callback handler decorator"""
        def decorator(handler: Callable):
            self.callback_handlers.append({
                'handler': handler,
                'func': func,
                **kwargs
            })
            logger.debug(f"🔄 Added callback handler to async router: {handler.__name__}")
            return handler
        return decorator
    
    def include_router(self, router: 'AsyncRouter'):
        """Adding another async router"""
        self.message_handlers.extend(router.message_handlers)
        self.callback_handlers.extend(router.callback_handlers)
        logger.info(f"📥 AsyncRouter '{router.name}' added")
    
    def register(self, bot: AsyncTeleBot):
        """Connecting handlers to an async bot"""
        self._register_message_handlers(bot)
        self._register_callback_handlers(bot)
        logger.info(f"🤖 Async router {len(self.message_handlers)} message, {len(self.callback_handlers)} callback handler ulandi")
    
    def _register_message_handlers(self, bot: AsyncTeleBot):
        """Registering async message handlers"""
        for handler_data in self.message_handlers:
            handler = handler_data['handler']
            commands = handler_data.get('commands')
            func = handler_data.get('func')
            content_types = handler_data.get('content_types')
            
            wrapper = self._create_async_wrapper(handler, bot, func)
            
            if commands and func:
                bot.message_handler(commands=commands, func=wrapper)(wrapper)
            elif commands:
                bot.message_handler(commands=commands)(wrapper)
            elif func:
                bot.message_handler(func=wrapper)(wrapper)
            else:
                bot.message_handler(content_types=content_types)(wrapper)
    
    def _register_callback_handlers(self, bot: AsyncTeleBot):
        """Registering async callback handlers"""
        for handler_data in self.callback_handlers:
            handler = handler_data['handler']
            func = handler_data.get('func')
            
            wrapper = self._create_async_callback_wrapper(handler, bot, func)
            
            if func:
                bot.callback_query_handler(func=wrapper)(wrapper)
            else:
                bot.callback_query_handler()(wrapper)
    
    def _create_async_wrapper(self, handler: Callable, bot: AsyncTeleBot, filter_func: Optional[Callable]):
        """Async message handler wrapper"""
        has_bot_param = 'bot' in handler.__code__.co_varnames
        
        async def wrapper(message, *args, **kwargs):
            if filter_func and not filter_func(message):
                return
            try:
                if has_bot_param:
                    return await handler(message, bot=bot, *args, **kwargs)
                else:
                    return await handler(message, *args, **kwargs)
            except Exception as e:
                logger.error(f"❌ Error: {handler.__name__} - {e}")
                raise
        
        wrapper.__name__ = f"async_wrapped_{handler.__name__}"
        return wrapper
    
    def _create_async_callback_wrapper(self, handler: Callable, bot: AsyncTeleBot, filter_func: Optional[Callable]):
        """Async callback handler wrapper"""
        has_bot_param = 'bot' in handler.__code__.co_varnames
        
        async def wrapper(call, *args, **kwargs):
            if filter_func and not filter_func(call):
                return
            try:
                if has_bot_param:
                    return await handler(call, bot=bot, *args, **kwargs)
                else:
                    return await handler(call, *args, **kwargs)
            except Exception as e:
                logger.error(f"❌ Error: {handler.__name__} - {e}")
                raise
        
        wrapper.__name__ = f"async_callback_wrapped_{handler.__name__}"
        return wrapper
    
    def get_handler_count(self):
        """Number of Handlers"""
        return {
            'message_handlers': len(self.message_handlers),
            'callback_handNumber of Handlersllback_handlers)
        }
    
    def clear_handlers(self):
        """Cleaning Handlers"""
        self.message_handlers.clear()
        self.callback_handlers.clear()
        logger.info("🧹 Async router handlers cleaned up")