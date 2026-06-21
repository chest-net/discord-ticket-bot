"""
Database models for the ticket system
"""
from datetime import datetime
from typing import Optional
from enum import Enum

from sqlalchemy import (
    BigInteger,
    String,
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    Text,
    Integer,
    Boolean,
    Index,
)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()


class TicketStatus(str, Enum):
    """Ticket status enumeration"""
    OPEN = "open"
    ASSIGNED = "assigned"
    CLOSED = "closed"
    ARCHIVED = "archived"


class TicketCategory(str, Enum):
    """Ticket category enumeration"""
    COMPLAINT = "complaint"
    TECHNICAL = "technical"
    QUESTION = "question"
    APPEAL = "appeal"
    OTHER = "other"


class Guild(Base):
    """Guild (Server) configuration"""
    __tablename__ = "guilds"
    
    id = BigInteger().with_variant(BigInteger(), "postgresql").primary_key = True
    support_channel_id = BigInteger()
    support_role_id = BigInteger()
    moderator_role_id = BigInteger()
    curator_role_id = BigInteger()
    administrator_role_id = BigInteger()
    log_channel_id = BigInteger()
    transcript_channel_id = BigInteger()
    max_open_tickets_per_user = Integer(default=1)
    created_at = DateTime(timezone=True, server_default=func.now())
    updated_at = DateTime(timezone=True, server_default=func.now(), onupdate=func.now())
    
    tickets = relationship("Ticket", back_populates="guild", cascade="all, delete-orphan")
    settings = relationship("TicketSetting", back_populates="guild", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index("idx_guild_support_channel", "support_channel_id"),
    )


class Ticket(Base):
    """Main ticket model"""
    __tablename__ = "tickets"
    
    id = BigInteger().with_variant(BigInteger(), "postgresql").primary_key = True
    guild_id = BigInteger(ForeignKey("guilds.id", ondelete="CASCADE"))
    thread_id = BigInteger(unique=True, nullable=False)
    user_id = BigInteger(nullable=False)
    responsible_staff_id = BigInteger(nullable=True)
    category = SQLEnum(TicketCategory)
    status = SQLEnum(TicketStatus, default=TicketStatus.OPEN)
    created_at = DateTime(timezone=True, server_default=func.now())
    closed_at = DateTime(timezone=True, nullable=True)
    deleted_at = DateTime(timezone=True, nullable=True)
    
    guild = relationship("Guild", back_populates="tickets")
    messages = relationship("TicketMessage", back_populates="ticket", cascade="all, delete-orphan")
    transfers = relationship("TicketTransfer", back_populates="ticket", cascade="all, delete-orphan")
    actions = relationship("TicketAction", back_populates="ticket", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index("idx_ticket_guild_user", "guild_id", "user_id"),
        Index("idx_ticket_thread", "thread_id"),
        Index("idx_ticket_status", "status"),
        Index("idx_ticket_responsible", "responsible_staff_id"),
    )


class TicketMessage(Base):
    """Messages in tickets for transcript generation"""
    __tablename__ = "ticket_messages"
    
    id = BigInteger().with_variant(BigInteger(), "postgresql").primary_key = True
    ticket_id = BigInteger(ForeignKey("tickets.id", ondelete="CASCADE"))
    message_id = BigInteger(unique=True, nullable=False)
    user_id = BigInteger(nullable=False)
    content = Text()
    attachments = Text()  # JSON array of attachment URLs
    created_at = DateTime(timezone=True, server_default=func.now())
    
    ticket = relationship("Ticket", back_populates="messages")
    
    __table_args__ = (
        Index("idx_ticket_message_ticket", "ticket_id"),
        Index("idx_ticket_message_user", "user_id"),
    )


class TicketTransfer(Base):
    """Transfer history of tickets"""
    __tablename__ = "ticket_transfers"
    
    id = BigInteger().with_variant(BigInteger(), "postgresql").primary_key = True
    ticket_id = BigInteger(ForeignKey("tickets.id", ondelete="CASCADE"))
    from_staff_id = BigInteger(nullable=False)
    to_staff_id = BigInteger(nullable=False)
    transferred_by = BigInteger(nullable=False)  # Admin/Curator who transferred
    reason = String(256, nullable=True)
    created_at = DateTime(timezone=True, server_default=func.now())
    
    ticket = relationship("Ticket", back_populates="transfers")
    
    __table_args__ = (
        Index("idx_transfer_ticket", "ticket_id"),
        Index("idx_transfer_from", "from_staff_id"),
        Index("idx_transfer_to", "to_staff_id"),
    )


class TicketAction(Base):
    """Action log for tickets"""
    __tablename__ = "ticket_actions"
    
    id = BigInteger().with_variant(BigInteger(), "postgresql").primary_key = True
    ticket_id = BigInteger(ForeignKey("tickets.id", ondelete="CASCADE"))
    action_type = String(50)  # claim, transfer, close, reopen, delete
    performed_by = BigInteger(nullable=False)
    details = Text()  # JSON with additional info
    created_at = DateTime(timezone=True, server_default=func.now())
    
    ticket = relationship("Ticket", back_populates="actions")
    
    __table_args__ = (
        Index("idx_action_ticket", "ticket_id"),
        Index("idx_action_type", "action_type"),
        Index("idx_action_performer", "performed_by"),
    )


class TicketSetting(Base):
    """Per-guild ticket settings"""
    __tablename__ = "ticket_settings"
    
    id = BigInteger().with_variant(BigInteger(), "postgresql").primary_key = True
    guild_id = BigInteger(ForeignKey("guilds.id", ondelete="CASCADE"))
    setting_key = String(100)
    setting_value = String(500)
    created_at = DateTime(timezone=True, server_default=func.now())
    updated_at = DateTime(timezone=True, server_default=func.now(), onupdate=func.now())
    
    guild = relationship("Guild", back_populates="settings")
    
    __table_args__ = (
        Index("idx_setting_guild_key", "guild_id", "setting_key"),
    )
