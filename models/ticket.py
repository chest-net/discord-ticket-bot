"""
Pydantic models for API/service layer
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum


class TicketStatus(str, Enum):
    """Ticket status"""
    OPEN = "open"
    ASSIGNED = "assigned"
    CLOSED = "closed"
    ARCHIVED = "archived"


class TicketCategory(str, Enum):
    """Ticket category"""
    COMPLAINT = "complaint"
    TECHNICAL = "technical"
    QUESTION = "question"
    APPEAL = "appeal"
    OTHER = "other"


class UserBase(BaseModel):
    """Base user model"""
    user_id: int
    username: str
    avatar_url: Optional[str] = None


class TicketCreate(BaseModel):
    """Model for creating a ticket"""
    guild_id: int
    user_id: int
    thread_id: int
    category: TicketCategory
    
    class Config:
        json_schema_extra = {
            "example": {
                "guild_id": 123456789,
                "user_id": 987654321,
                "thread_id": 111222333,
                "category": "technical"
            }
        }


class TicketUpdate(BaseModel):
    """Model for updating a ticket"""
    status: Optional[TicketStatus] = None
    responsible_staff_id: Optional[int] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "assigned",
                "responsible_staff_id": 123456789
            }
        }


class TicketResponse(BaseModel):
    """Ticket response model"""
    id: int
    guild_id: int
    thread_id: int
    user_id: int
    responsible_staff_id: Optional[int] = None
    category: TicketCategory
    status: TicketStatus
    created_at: datetime
    closed_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class TicketMessageCreate(BaseModel):
    """Model for creating ticket message"""
    ticket_id: int
    message_id: int
    user_id: int
    content: str
    attachments: Optional[str] = None


class TicketMessageResponse(BaseModel):
    """Ticket message response"""
    id: int
    ticket_id: int
    message_id: int
    user_id: int
    content: str
    attachments: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class TicketTransferCreate(BaseModel):
    """Model for creating ticket transfer"""
    ticket_id: int
    from_staff_id: int
    to_staff_id: int
    transferred_by: int
    reason: Optional[str] = None


class TicketTransferResponse(BaseModel):
    """Ticket transfer response"""
    id: int
    ticket_id: int
    from_staff_id: int
    to_staff_id: int
    transferred_by: int
    reason: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class TicketActionCreate(BaseModel):
    """Model for creating ticket action"""
    ticket_id: int
    action_type: str  # claim, transfer, close, reopen, delete
    performed_by: int
    details: Optional[str] = None


class TicketActionResponse(BaseModel):
    """Ticket action response"""
    id: int
    ticket_id: int
    action_type: str
    performed_by: int
    details: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class GuildConfigUpdate(BaseModel):
    """Model for updating guild configuration"""
    support_channel_id: Optional[int] = None
    support_role_id: Optional[int] = None
    moderator_role_id: Optional[int] = None
    curator_role_id: Optional[int] = None
    administrator_role_id: Optional[int] = None
    log_channel_id: Optional[int] = None
    transcript_channel_id: Optional[int] = None
    max_open_tickets_per_user: Optional[int] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "support_channel_id": 123456789,
                "support_role_id": 987654321,
                "log_channel_id": 555666777
            }
        }


class GuildResponse(BaseModel):
    """Guild configuration response"""
    id: int
    support_channel_id: int
    support_role_id: int
    log_channel_id: int
    transcript_channel_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class TranscriptData(BaseModel):
    """Data for transcript generation"""
    ticket_id: int
    thread_id: int
    user_id: int
    username: str
    category: TicketCategory
    status: TicketStatus
    created_at: datetime
    closed_at: Optional[datetime] = None
    responsible_staff_id: Optional[int] = None
    responsible_staff_name: Optional[str] = None
    messages: List[TicketMessageResponse]
    transfers: List[TicketTransferResponse]
    
    class Config:
        from_attributes = True
