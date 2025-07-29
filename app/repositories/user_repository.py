from typing import List, Optional
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserUpdate
from beanie import PydanticObjectId
from datetime import datetime

class UserRepository:
    """
    Repository class for User model with MongoDB.
    Handles all database operations for users following the Repository pattern.
    """
    
    @staticmethod
    async def create(user_data: UserCreate, hashed_password: str) -> User:
        """Create a new user in MongoDB."""
        user_dict = user_data.dict()
        user_dict['hashed_password'] = hashed_password
        user_dict['is_admin'] = user_data.is_admin or False
        
        user = User(**user_dict)
        await user.insert()
        return user
    
    @staticmethod
    async def get_by_id(user_id: str) -> Optional[User]:
        """Get user by ID."""
        try:
            return await User.get(PydanticObjectId(user_id))
        except:
            return None
    
    @staticmethod
    async def get_by_email(email: str) -> Optional[User]:
        """Get user by email."""
        return await User.find_one(User.email == email)
    
    @staticmethod
    async def get_by_username(username: str) -> Optional[User]:
        """Get user by username."""
        return await User.find_one(User.username == username)
    
    @staticmethod
    async def get_by_email_or_username(identifier: str) -> Optional[User]:
        """Get user by email or username."""
        return await User.find_one(
            {"$or": [
                {"email": identifier},
                {"username": identifier}
            ]}
        )
    
    @staticmethod
    async def get_all(skip: int = 0, limit: int = 100, active_only: bool = True) -> List[User]:
        """Get all users with pagination."""
        query = User.find()
        if active_only:
            query = User.find(User.is_active == True)
        return await query.skip(skip).limit(limit).to_list()
    
    @staticmethod
    async def count(active_only: bool = True) -> int:
        """Count total users."""
        if active_only:
            return await User.find(User.is_active == True).count()
        return await User.count()
    
    @staticmethod
    async def update(user_id: str, user_data: UserUpdate) -> Optional[User]:
        """Update user information."""
        try:
            user = await User.get(PydanticObjectId(user_id))
            if not user:
                return None
            
            update_data = user_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                if hasattr(user, field):
                    setattr(user, field, value)
            
            user.updated_at = datetime.utcnow()
            await user.save()
            return user
        except:
            return None
    
    @staticmethod
    async def delete(user_id: str) -> bool:
        """Delete user (soft delete by setting is_active=False)."""
        try:
            user = await User.get(PydanticObjectId(user_id))
            if not user:
                return False
            
            user.is_active = False
            user.updated_at = datetime.utcnow()
            await user.save()
            return True
        except:
            return False
    
    @staticmethod
    async def hard_delete(user_id: str) -> bool:
        """Permanently delete user from database."""
        try:
            user = await User.get(PydanticObjectId(user_id))
            if not user:
                return False
            
            await user.delete()
            return True
        except:
            return False
    
    @staticmethod
    async def search(query: str, skip: int = 0, limit: int = 100) -> List[User]:
        """Search users by name, email, or username."""
        return await User.find(
            {"$and": [
                {"is_active": True},
                {"$or": [
                    {"first_name": {"$regex": query, "$options": "i"}},
                    {"last_name": {"$regex": query, "$options": "i"}},
                    {"email": {"$regex": query, "$options": "i"}},
                    {"username": {"$regex": query, "$options": "i"}}
                ]}
            ]}
        ).skip(skip).limit(limit).to_list()
    
    @staticmethod
    async def email_exists(email: str, exclude_user_id: Optional[str] = None) -> bool:
        """Check if email already exists."""
        query = {"email": email}
        if exclude_user_id:
            query["_id"] = {"$ne": PydanticObjectId(exclude_user_id)}
        
        user = await User.find_one(query)
        return user is not None
    
    @staticmethod
    async def username_exists(username: str, exclude_user_id: Optional[str] = None) -> bool:
        """Check if username already exists."""
        query = {"username": username}
        if exclude_user_id:
            query["_id"] = {"$ne": PydanticObjectId(exclude_user_id)}
        
        user = await User.find_one(query)
        return user is not None
