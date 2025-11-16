"""
Database Schemas for Fine Arts Club

Each Pydantic model represents a collection in MongoDB. The collection name
is the lowercase of the class name.

Collections:
- Artwork -> "artwork"
- Event -> "event"
- Member -> "member"
- Message -> "message"
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime


class Artwork(BaseModel):
    """
    Artworks submitted by members or displayed by the club
    """
    title: str = Field(..., description="Artwork title")
    artist: str = Field(..., description="Artist name")
    image_url: str = Field(..., description="Public URL to the artwork image")
    medium: Optional[str] = Field(None, description="Medium used e.g., Oil on canvas")
    year: Optional[str] = Field(None, description="Year created")
    description: Optional[str] = Field(None, description="Short description of the work")
    featured: bool = Field(False, description="Whether featured on homepage")
    tags: List[str] = Field(default_factory=list, description="Tags for filtering")


class Event(BaseModel):
    """
    Club events (exhibitions, workshops, meetups)
    """
    name: str = Field(..., description="Event name")
    date: datetime = Field(..., description="Event date and time")
    location: str = Field(..., description="Where the event takes place")
    description: Optional[str] = Field(None, description="Event details")
    cover_image: Optional[str] = Field(None, description="Cover image URL")
    rsvp_link: Optional[str] = Field(None, description="External RSVP link if any")


class Member(BaseModel):
    """
    Club members (applications stored here)
    """
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Contact email")
    art_focus: Optional[str] = Field(None, description="Primary art focus e.g., Painting, Sculpture")
    bio: Optional[str] = Field(None, description="Short bio")
    portfolio_link: Optional[str] = Field(None, description="Portfolio URL")


class Message(BaseModel):
    """
    Contact form messages sent to the club
    """
    name: str = Field(...)
    email: EmailStr = Field(...)
    subject: str = Field(...)
    body: str = Field(...)
