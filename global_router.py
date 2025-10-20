from typing import List, Callable, Dict, Any
import logging
from .router import AsyncRouter

logger = logging.getLogger(__name__)

class AsyncGlobalRouter:
    """
    Global AsyncTeleBot router - for all async bots
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.router = AsyncRouter("global_async")
            self.registered_bots = set()
            self._initialized = True
            logger.info("🌍 AsyncGlobalRouter launched")
    
    def message_handler(self, commands=None, func=None, content_types=None, **kwargs):
        """Global async message handler decorator"""
        def decorator(handler: Callable):
            self.router.message_handler(
                commands=commands, func=func, content_types=content_types, **kwargs
            )(handler)
            logger.info(f"🌍 Added global async message handler: {handler.__name__}")
            return handler
        return decorator
    
    def callback_query_handler(self, func=None, **kwargs):
        """Global async callback handler decorator"""
        def decorator(handler: Callable):
            self.router.callback_query_handler(func=func, **kwargs)(handler)
            logger.info(f"🌍 Added global async callback handler: {handler.__name__}")
            return handler
        return decorator
    
    def include_router(self, router: AsyncRouter):
        """Adding another async router to the global"""
        self.router.include_router(router)
        logger.info(f"📥 AsyncRouter '{router.name}' added to global")
    
    def register_bot(self, bot):
        """Registering async bot global router"""
        bot_id = id(bot)
        if bot_id in self.registered_bots:
            logger.warning(f"⚠️ Async Bot {bot_id} allaqachon ro'yxatdan o'tgan")
            return
        
        self.router.register(bot)
        self.registered_bots.add(bot_id)
        logger.info(f"🤖 Async bot registered global router")
    
    def get_stats(self):
        """Global async router statistikasi"""
        handler_stats = self.router.get_handler_count()
        return {
            'total_bots': len(self.registered_bots),
            'handlers': handler_stats,
            'global_handlers': {
                'message_handlers': len(self.router.message_handlers),
                'callback_handlers': len(self.router.callback_handlers)
            }
        }

# Global async router instance
_async_global_router = AsyncGlobalRouter()

# Global decoratorlar
def async_message_handler(commands=None, func=None, content_types=None, **kwargs):
    """Global async message handler decorator"""
    return _async_global_router.message_handler(
        commands=commands, func=func, content_types=content_types, **kwargs
    )

def async_callback_handler(func=None, **kwargs):
    """Global async callback handler decorator"""
    return _async_global_router.callback_query_handler(func=func, **kwargs)

# Bot registration
def register_async_bot(bot):
    """Registering async bot global router"""
    return _async_global_router.register_bot(bot)

# Getting statistics
def get_async_global_stats():
    """Get global async statistics"""
    return _async_global_router.get_stats()

# Add a router
def include_async_router(router: AsyncRouter):
    """Add an async router"""
    return _async_global_router.include_router(router)