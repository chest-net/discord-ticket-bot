"""
Validation utilities
"""
from typing import Optional
from datetime import datetime
import disnake

from utils.logger import logger


def validate_discord_id(value: int) -> bool:
    """Validate Discord ID format"""
    return isinstance(value, int) and value > 0


def validate_ticket_category(category: str) -> bool:
    """Validate ticket category"""
    valid_categories = ["complaint", "technical", "question", "appeal", "other"]
    return category in valid_categories


def validate_ticket_status(status: str) -> bool:
    """Validate ticket status"""
    valid_statuses = ["open", "assigned", "closed", "archived"]
    return status in valid_statuses


def validate_role_exists(guild: disnake.Guild, role_id: int) -> bool:
    """Check if role exists in guild"""
    try:
        role = guild.get_role(role_id)
        return role is not None
    except Exception as e:
        logger.error(f"Error validating role {role_id}: {str(e)}")
        return False


def validate_channel_exists(guild: disnake.Guild, channel_id: int) -> bool:
    """Check if channel exists in guild"""
    try:
        channel = guild.get_channel(channel_id)
        return channel is not None
    except Exception as e:
        logger.error(f"Error validating channel {channel_id}: {str(e)}")
        return False


def validate_user_exists(guild: disnake.Guild, user_id: int) -> bool:
    """Check if user exists in guild"""
    try:
        member = guild.get_member(user_id)
        return member is not None
    except Exception as e:
        logger.error(f"Error validating user {user_id}: {str(e)}")
        return False


def validate_thread_exists(guild: disnake.Guild, thread_id: int) -> bool:
    """Check if thread exists in guild"""
    try:
        thread = guild.get_thread(thread_id)
        return thread is not None
    except Exception as e:
        logger.error(f"Error validating thread {thread_id}: {str(e)}")
        return False


def validate_ticket_permissions(
    member: disnake.Member,
    required_role_ids: Optional[list] = None
) -> bool:
    """Validate if member has permission to manage tickets"""
    if member.guild_permissions.administrator:
        return True
    
    if required_role_ids:
        return any(role.id in required_role_ids for role in member.roles)
    
    return False


def is_valid_email(email: str) -> bool:
    """Simple email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def is_valid_url(url: str) -> bool:
    """Simple URL validation"""
    import re
    pattern = r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)'
    return re.match(pattern, url) is not None


def sanitize_input(text: str, max_length: int = 1000) -> str:
    """Sanitize user input"""
    if not isinstance(text, str):
        return ""
    
    # Remove potentially harmful characters
    text = text.strip()
    
    # Limit length
    if len(text) > max_length:
        text = text[:max_length]
    
    return text


def validate_guild_config(
    support_role_id: int,
    log_channel_id: int,
    guild: disnake.Guild
) -> tuple[bool, str]:
    """Validate guild configuration"""
    errors = []
    
    if not validate_role_exists(guild, support_role_id):
        errors.append("Support role не найдена")
    
    if not validate_channel_exists(guild, log_channel_id):
        errors.append("Log channel не найден")
    
    if errors:
        return False, "; ".join(errors)
    
    return True, ""
