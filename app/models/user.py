from beanie import Document
from pydantic import Field, EmailStr
from typing import Optional
from datetime import datetime

class User(Document):
    """
    User model for MongoDB using Beanie ODM.
    This follows the MVC pattern as the Model layer.
    """
    email: EmailStr = Field(..., unique=True, description="User's email address")
    username: str = Field(..., unique=True, min_length=3, max_length=50, description="Unique username")
    first_name: str = Field(..., min_length=1, max_length=100, description="User's first name")
    last_name: str = Field(..., min_length=1, max_length=100, description="User's last name")
    hashed_password: str = Field(..., description="Hashed password")
    is_active: bool = Field(default=True, description="Whether user is active")
    is_admin: bool = Field(default=False, description="Whether user has admin privileges")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
    
    class Settings:
        name = "users"  # MongoDB collection name
        indexes = [
            "email",
            "username",
            "created_at"
        ]
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', username='{self.username}')>"
    
    @property
    def full_name(self) -> str:
        """Get user's full name."""
        return f"{self.first_name} {self.last_name}"
