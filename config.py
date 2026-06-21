"""
Configuration module for Discord Ticket Bot
"""
import os
from pathlib import Path
from functools import lru_cache

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    """Main settings for the bot"""
    
    # Discord
    discord_token: str = os.getenv("DISCORD_TOKEN", "")
    discord_prefix: str = os.getenv("DISCORD_PREFIX", "!")
    discord_sync_commands: bool = os.getenv("DISCORD_SYNC_COMMANDS", "true").lower() == "true"
    
    # Database
    database_url: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost:5432/ticket_bot")
    database_pool_size: int = int(os.getenv("DATABASE_POOL_SIZE", "20"))
    database_max_overflow: int = int(os.getenv("DATABASE_MAX_OVERFLOW", "10"))
    
    # Bot Configuration
    bot_name: str = os.getenv("BOT_NAME", "Ticket Bot")
    bot_version: str = os.getenv("BOT_VERSION", "1.0.0")
    
    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    log_file: str = os.getenv("LOG_FILE", "logs/bot.log")
    
    # Features
    enable_transcripts: bool = os.getenv("ENABLE_TRANSCRIPTS", "true").lower() == "true"
    max_open_tickets_per_user: int = int(os.getenv("MAX_OPEN_TICKETS_PER_USER", "1"))
    ticket_timeout_hours: int = int(os.getenv("TICKET_TIMEOUT_HOURS", "72"))
    
    # Role IDs
    support_role_id: int = int(os.getenv("SUPPORT_ROLE_ID", "0"))
    moderator_role_id: int = int(os.getenv("MODERATOR_ROLE_ID", "0"))
    curator_role_id: int = int(os.getenv("CURATOR_ROLE_ID", "0"))
    administrator_role_id: int = int(os.getenv("ADMINISTRATOR_ROLE_ID", "0"))
    
    # Channel IDs
    log_channel_id: int = int(os.getenv("LOG_CHANNEL_ID", "0"))
    transcript_channel_id: int = int(os.getenv("TRANSCRIPT_CHANNEL_ID", "0"))
    
    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()

# Ensure logs directory exists
Path("logs").mkdir(exist_ok=True)
