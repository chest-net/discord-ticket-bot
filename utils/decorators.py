"""
Permission and role decorators
"""
from functools import wraps
from typing import Callable, Optional, List
import disnake
from disnake.ext import commands

from utils.logger import logger


def require_role(*role_ids: int):
    """Decorator to require specific roles"""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(interaction: disnake.ApplicationCommandInteraction, *args, **kwargs):
            member = interaction.author
            if not isinstance(member, disnake.Member):
                await interaction.response.send_message(
                    "❌ Эта команда доступна только на серверах",
                    ephemeral=True
                )
                return
            
            has_role = any(role.id in role_ids for role in member.roles)
            
            if not has_role:
                logger.warning(
                    f"User {member.id} tried to use {func.__name__} without required role"
                )
                await interaction.response.send_message(
                    "❌ У вас нет прав для использования этой команды",
                    ephemeral=True
                )
                return
            
            return await func(interaction, *args, **kwargs)
        return wrapper
    return decorator


def require_guild_owner():
    """Decorator to require guild owner"""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(interaction: disnake.ApplicationCommandInteraction, *args, **kwargs):
            if interaction.guild.owner_id != interaction.author.id:
                logger.warning(
                    f"User {interaction.author.id} tried to use {func.__name__} without being guild owner"
                )
                await interaction.response.send_message(
                    "❌ Эта команда доступна только владельцу сервера",
                    ephemeral=True
                )
                return
            
            return await func(interaction, *args, **kwargs)
        return wrapper
    return decorator


def require_permissions(**permissions):
    """Decorator to require specific permissions"""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(interaction: disnake.ApplicationCommandInteraction, *args, **kwargs):
            member = interaction.author
            if not isinstance(member, disnake.Member):
                await interaction.response.send_message(
                    "❌ Эта команда доступна только на серверах",
                    ephemeral=True
                )
                return
            
            member_perms = interaction.author.guild_permissions
            
            for perm_name, required in permissions.items():
                perm_value = getattr(member_perms, perm_name, False)
                if required and not perm_value:
                    logger.warning(
                        f"User {member.id} tried to use {func.__name__} without permission {perm_name}"
                    )
                    await interaction.response.send_message(
                        f"❌ У вас нет прав: {perm_name}",
                        ephemeral=True
                    )
                    return
            
            return await func(interaction, *args, **kwargs)
        return wrapper
    return decorator


def require_bot_permissions(**permissions):
    """Decorator to require bot permissions"""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(interaction: disnake.ApplicationCommandInteraction, *args, **kwargs):
            bot_perms = interaction.guild.me.guild_permissions
            
            for perm_name, required in permissions.items():
                perm_value = getattr(bot_perms, perm_name, False)
                if required and not perm_value:
                    logger.warning(
                        f"Bot missing permission {perm_name} in guild {interaction.guild.id}"
                    )
                    await interaction.response.send_message(
                        f"❌ У бота нет прав: {perm_name}",
                        ephemeral=True
                    )
                    return
            
            return await func(interaction, *args, **kwargs)
        return wrapper
    return decorator


def cooldown(rate: int, per: float):
    """Cooldown decorator"""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(interaction: disnake.ApplicationCommandInteraction, *args, **kwargs):
            # Simple cooldown check can be implemented with discord.py built-in
            return await func(interaction, *args, **kwargs)
        return wrapper
    return decorator


def error_handler(func: Callable):
    """Decorator for error handling"""
    @wraps(func)
    async def wrapper(interaction: disnake.ApplicationCommandInteraction, *args, **kwargs):
        try:
            return await func(interaction, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}", exc_info=True)
            try:
                await interaction.response.send_message(
                    f"❌ Ошибка: {str(e)}",
                    ephemeral=True
                )
            except:
                pass
    return wrapper
