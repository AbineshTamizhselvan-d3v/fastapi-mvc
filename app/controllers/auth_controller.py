from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.auth_schema import (
    UserLogin, UserRegister, Token, RefreshToken, 
    PasswordChange
)
from app.schemas.user_schema import UserResponse
from app.services.auth_service import AuthService
from app.middleware.auth import get_current_active_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister):
    """
    Register a new user account.
    
    - **email**: Valid email address
    - **username**: Unique username (3-50 characters)
    - **password**: Strong password (min 8 characters)
    - **first_name**: User's first name
    - **last_name**: User's last name
    """
    return await AuthService.register_user(user_data)

@router.post("/login", response_model=Token)
async def login(login_data: UserLogin):
    """
    Authenticate user and return JWT tokens.
    
    - **identifier**: Email or username
    - **password**: User password
    
    Returns access token, refresh token, and expiration info.
    """
    return await AuthService.login_user(login_data)

@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_data: RefreshToken):
    """
    Refresh access token using refresh token.
    
    - **refresh_token**: Valid refresh token
    
    Returns new access token and refresh token.
    """
    return await AuthService.refresh_token(refresh_data)

@router.post("/logout")
async def logout(current_user: User = Depends(get_current_active_user)):
    """
    Logout current user.
    
    Note: With JWT, logout is typically handled client-side.
    This endpoint serves as a confirmation of successful logout.
    """
    success = await AuthService.logout_user(current_user)
    if success:
        return {"message": "Successfully logged out"}
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Logout failed"
    )

@router.get("/me", response_model=UserResponse)
async def get_current_user(current_user: User = Depends(get_current_active_user)):
    """
    Get current authenticated user's profile information.
    
    Requires valid JWT token in Authorization header.
    """
    return await AuthService.get_current_user_profile(current_user)

@router.put("/change-password")
async def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_active_user)
):
    """
    Change current user's password.
    
    - **old_password**: Current password for verification
    - **new_password**: New password (min 8 characters)
    
    Requires valid JWT token in Authorization header.
    """
    success = await AuthService.change_password(str(current_user.id), password_data)
    if success:
        return {"message": "Password changed successfully"}
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Password change failed"
    )

@router.get("/verify-token")
async def verify_token(current_user: User = Depends(get_current_active_user)):
    """
    Verify if the provided JWT token is valid.
    
    Returns user information if token is valid.
    Useful for checking token validity without full profile data.
    """
    return {
        "valid": True,
        "user_id": str(current_user.id),
        "username": current_user.username,
        "email": current_user.email,
        "is_active": current_user.is_active,
        "is_admin": current_user.is_admin
    }
