from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from app.utils.auth import JWTManager
from app.repositories.user_repository import UserRepository
from app.models.user import User

security = HTTPBearer()

class AuthMiddleware:
    """Authentication middleware for JWT token validation."""
    
    @staticmethod
    async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
        """
        Get current authenticated user from JWT token.
        This dependency can be used in route handlers to require authentication.
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            # Verify the token
            payload = JWTManager.verify_token(credentials.credentials, token_type="access")
            if payload is None:
                raise credentials_exception
            
            # Extract user ID from token
            user_id: str = payload.get("sub")
            if user_id is None:
                raise credentials_exception
            
            # Get user from database
            user = await UserRepository.get_by_id(user_id)
            if user is None:
                raise credentials_exception
            
            # Check if user is active
            if not user.is_active:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Inactive user",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            return user
            
        except Exception:
            raise credentials_exception
    
    @staticmethod
    async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
        """
        Get current active user.
        Additional layer to ensure user is active.
        """
        if not current_user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )
        return current_user
    
    @staticmethod
    async def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
        """
        Get current user and verify admin privileges.
        This dependency requires the user to be an admin.
        """
        if not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return current_user
    
    @staticmethod
    async def get_optional_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> Optional[User]:
        """
        Get current user if token is provided, otherwise return None.
        This dependency is for optional authentication.
        """
        if credentials is None:
            return None
        
        try:
            # Verify the token
            payload = JWTManager.verify_token(credentials.credentials, token_type="access")
            if payload is None:
                return None
            
            # Extract user ID from token
            user_id: str = payload.get("sub")
            if user_id is None:
                return None
            
            # Get user from database
            user = await UserRepository.get_by_id(user_id)
            if user is None or not user.is_active:
                return None
            
            return user
            
        except Exception:
            return None

# Convenience functions for dependency injection
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Get current authenticated user."""
    return await AuthMiddleware.get_current_user(credentials)

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current active user."""
    return await AuthMiddleware.get_current_active_user(current_user)

async def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current admin user."""
    return await AuthMiddleware.get_current_admin_user(current_user)

async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(
        HTTPBearer(auto_error=False)
    )
) -> Optional[User]:
    """Get current user if authenticated, otherwise None."""
    return await AuthMiddleware.get_optional_user(credentials)
