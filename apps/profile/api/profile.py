from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging
from datetime import datetime

from core.db import get_db
from apps.auth.deps import get_current_user , role_required # Based on your project structure
from ..schemas.profile import ProfileCreate, ProfileUpdate, ProfileOut
from ..crud import profile as crud_profile
from apps.auth.models.user import User  # From auth app crud
from apps.profile.models.profile import Profile  # Your profile model
from apps.auth.crud import auth as crud_user 

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router_profile = APIRouter(prefix="/profiles", tags=["profiles"])

# Helper function to log platform statistics
def log_platform_stats(db: Session, action: str, user_id: int):
    """Log platform statistics for monitoring"""
    try:
        # Get basic statistics
        total_users = crud_user.get_user_count(db)
        total_profiles = crud_profile.get_profile_count(db)
        active_users_today = crud_user.get_active_users_count(db)  # Users active today
        
        logger.info(f"PLATFORM_STATS | Action: {action} | User: {user_id} | "
                   f"Total Users: {total_users} | Total Profiles: {total_profiles} | "
                   f"Active Users Today: {active_users_today} | Timestamp: {datetime.utcnow()}")
    except Exception as e:
        logger.error(f"Failed to log platform stats: {str(e)}")

# Validation helper
def validate_profile_ownership(db: Session, profile_id: int, current_user_id: int):
    """Validate that the current user owns the profile or is admin"""
    profile = crud_profile.get_profile(db, profile_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    # Check if user owns the profile or is admin
    if profile.user_id != current_user_id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this profile"
        )
    
    return profile

# Create profile
@router_profile.post("/", response_model=ProfileOut)
def create_profile(
    profile_in: ProfileCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new profile for the current user"""
    try:
        # Check if user already has a profile (if business logic requires one profile per user)
        existing_profile = crud_profile.get_profile_by_user_id(db, current_user.id)
        if existing_profile:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already has a profile"
            )
        
        # Create profile with current user's ID
        new_profile = crud_profile.create_profile(db, profile_in, user_id=current_user.id)
        
        # Log platform statistics
        log_platform_stats(db, "CREATE_PROFILE", current_user.id)
        
        logger.info(f"Profile created for user {current_user.id}")
        return new_profile
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating profile for user {current_user.id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create profile"
        )

# Read specific profile
@router_profile.get("/{profile_id}", response_model=ProfileOut)
def read_profile(
    profile_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific profile (only owner or admin can access)"""
    try:
        # Validate ownership and get profile
        profile = validate_profile_ownership(db, profile_id, current_user.id)
        
        # Log platform statistics
        log_platform_stats(db, "READ_PROFILE", current_user.id)
        
        return profile
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error reading profile {profile_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve profile"
        )

# Read current user's profile
@router_profile.get("/me/profile", response_model=ProfileOut)
def read_my_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current user's profile"""
    try:
        profile = crud_profile.get_profile_by_user_id(db, current_user.id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found"
            )
        
        # Log platform statistics
        log_platform_stats(db, "READ_MY_PROFILE", current_user.id)
        
        return profile
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error reading profile for user {current_user.id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve profile"
        )

# List profiles (admin only)
@router_profile.get("/", response_model=List[ProfileOut])
def list_profiles(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all profiles (admin only)"""
    try:
        # Check if user is admin
        if not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required"
            )
        
        profiles = crud_profile.get_profiles(db, skip=skip, limit=limit)
        
        # Log platform statistics
        log_platform_stats(db, "LIST_PROFILES", current_user.id)
        
        return profiles
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error listing profiles: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve profiles"
        )

# Update profile
@router_profile.put("/{profile_id}", response_model=ProfileOut)
def update_profile(
    profile_id: int, 
    profile_in: ProfileUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a profile (only owner or admin can update)"""
    try:
        # Validate ownership
        validate_profile_ownership(db, profile_id, current_user.id)
        
        # Update profile
        updated_profile = crud_profile.update_profile(db, profile_id, profile_in)
        if not updated_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found"
            )
        
        # Log platform statistics
        log_platform_stats(db, "UPDATE_PROFILE", current_user.id)
        
        logger.info(f"Profile {profile_id} updated by user {current_user.id}")
        return updated_profile
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating profile {profile_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update profile"
        )

# Delete profile
@router_profile.delete("/{profile_id}")
def delete_profile(
    profile_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a profile (only owner or admin can delete)"""
    try:
        # Validate ownership
        validate_profile_ownership(db, profile_id, current_user.id)
        
        # Delete profile
        deleted_profile = crud_profile.delete_profile(db, profile_id)
        if not deleted_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found"
            )
        
        # Log platform statistics
        log_platform_stats(db, "DELETE_PROFILE", current_user.id)
        
        logger.info(f"Profile {profile_id} deleted by user {current_user.id}")
        return {"ok": True, "message": "Profile deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting profile {profile_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete profile"
        )

# Platform statistics endpoint (admin only)
@router_profile.get("/admin/stats")
def get_platform_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(["admin"])) 
):
    """Get platform statistics (admin only)"""
    try:
        stats = {
            "total_users": crud_user.get_user_count(db),
            "total_profiles": crud_profile.get_profile_count(db),
            "active_users_today": crud_user.get_active_users_count(db),
            "active_users_this_week": crud_user.get_active_users_count(db, days=7),
            "active_users_this_month": crud_user.get_active_users_count(db, days=30),
            "timestamp": datetime.utcnow()
        }
        
        logger.info(f"Platform statistics accessed by admin user {current_user.id}")
        return stats
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving platform statistics: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve statistics"
        )