from typing import Optional
from fastapi import HTTPException, status
from app.repositories.user_repository import UserRepository
from app.schemas.auth_schema import UserLogin, UserRegister, Token, RefreshToken, PasswordChange
from app.schemas.user_schema import UserResponse
from app.utils.auth import JWTManager, PasswordManager
from app.models.user import User

class AuthService:
    """Authentication service for user registration, login, and token management."""
    
    @staticmethod
    async def register_user(user_data: UserRegister) -> UserResponse:
        """
        Register a new user.
        """
        # Check if email already exists
        if await UserRepository.email_exists(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Check if username already exists
        if await UserRepository.username_exists(user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        
        # Hash the password
        hashed_password = PasswordManager.hash_password(user_data.password)
        
        # Create user data for repository
        from app.schemas.user_schema import UserCreate
        user_create_data = UserCreate(
            email=user_data.email,
            username=user_data.username,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            password=user_data.password,  # This will be ignored in favor of hashed_password
            is_admin=False
        )
        
        # Create the user
        user = await UserRepository.create(user_create_data, hashed_password)
        
        return UserResponse.from_orm(user)
    
    @staticmethod
    async def login_user(login_data: UserLogin) -> Token:
        """
        Authenticate user and return JWT tokens.
        """
        # Get user by email or username
        user = await UserRepository.get_by_email_or_username(login_data.identifier)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email/username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Verify password
        if not PasswordManager.verify_password(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email/username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Check if user is active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Account is deactivated",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create token pair
        token_data = JWTManager.create_token_pair(
            user_id=str(user.id),
            username=user.username,
            email=user.email
        )
        
        return Token(**token_data)
    
    @staticmethod
    async def refresh_token(refresh_data: RefreshToken) -> Token:
        """
        Refresh access token using refresh token.
        """
        # Verify refresh token
        payload = JWTManager.verify_token(refresh_data.refresh_token, token_type="refresh")
        
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Get user ID from token
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Get user from database
        user = await UserRepository.get_by_id(user_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create new token pair
        token_data = JWTManager.create_token_pair(
            user_id=str(user.id),
            username=user.username,
            email=user.email
        )
        
        return Token(**token_data)
    
    @staticmethod
    async def change_password(user_id: str, password_data: PasswordChange) -> bool:
        """
        Change user password with old password verification.
        """
        # Get user
        user = await UserRepository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Verify old password
        if not PasswordManager.verify_password(password_data.old_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect old password"
            )
        
        # Hash new password
        new_hashed_password = PasswordManager.hash_password(password_data.new_password)
        
        # Update password in database
        from app.schemas.user_schema import UserUpdate
        update_data = UserUpdate()
        update_data_dict = {"hashed_password": new_hashed_password}
        
        # Manually update the user
        user.hashed_password = new_hashed_password
        await user.save()
        
        return True
    
    @staticmethod
    async def get_current_user_profile(user: User) -> UserResponse:
        """
        Get current authenticated user's profile.
        """
        return UserResponse.from_orm(user)
    
    @staticmethod
    async def verify_user_token(token: str) -> Optional[User]:
        """
        Verify token and return user if valid.
        """
        payload = JWTManager.verify_token(token, token_type="access")
        if not payload:
            return None
        
        user_id = payload.get("sub")
        if not user_id:
            return None
        
        user = await UserRepository.get_by_id(user_id)
        if not user or not user.is_active:
            return None
        
        return user
    
    @staticmethod
    async def logout_user(user: User) -> bool:
        """
        Logout user (in this implementation, we just return success).
        In a real application, you might want to invalidate the token
        by maintaining a blacklist of tokens.
        """
        # For JWT, logout is typically handled on the client side
        # by removing the token from storage.
        # Server-side logout would require token blacklisting.
        return True
