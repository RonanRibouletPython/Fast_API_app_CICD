from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.utils.utility import get_db
from app.db.models.activity import Activity as ActivityModel
from app.schemas.activity import ActivityCreate, ActivityResponse
from app.utils.user import get_current_user
from app.db.models.user import User as UserModel
from app.utils.logger import logger
from typing import Optional
import random


router = APIRouter()

@router.post("/activity/", response_model=ActivityResponse)
async def create_activity(
    activity: ActivityCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Create a new activity."""
    logger.info(f"Current user ID: {current_user.id}, attempting to create activity: {activity}")
    
    if not current_user.partner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to create activities without a partner.",
        )
        
    # fetch the partner
    partner = db.query(UserModel).filter(UserModel.id == current_user.partner_id).first()
    
    if not partner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Partner not found.",
        )
        
    # create the activity
    new_activity = ActivityModel(
        activity_name=activity.activity_name,
        activity_type=activity.activity_type,
        budget=activity.budget,
        location=activity.location,
        link_info=activity.link_info,
        description=activity.description,
        user_id=current_user.id,
        partner_id=current_user.partner_id
    )
    
    db.add(new_activity)
    db.commit()
    db.refresh(new_activity)
        
    logger.info(f"Activity {new_activity.id} created successfully.")
    
    # Return the created activity with partner ID
    return ActivityResponse(
        id=new_activity.id,
        activity_name=new_activity.activity_name,
        activity_type=new_activity.activity_type,
        budget=new_activity.budget,
        location=new_activity.location,
        link_info=new_activity.link_info,
        description=new_activity.description,
        user_id=current_user.id,
        partner_id=current_user.partner_id
    )
    
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.utils.utility import get_db
from app.db.models.activity import Activity as ActivityModel
from app.schemas.activity import ActivityResponse
from app.utils.user import get_current_user
from app.db.models.user import User as UserModel
from app.utils.logger import logger
from typing import Optional
import random

router = APIRouter()

@router.get("/activity/", response_model=ActivityResponse)
async def get_activities(
    budget: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Retrieve a random activity created by the user's partner, optionally filtered by budget."""
    logger.info(f"Current user ID: {current_user.id}, attempting to retrieve activities.")

    # Check if the current user has a partner
    if not current_user.partner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to retrieve activities without a partner.",
        )

    # Fetch the partner
    partner = db.query(UserModel).filter(UserModel.id == current_user.partner_id).first()

    if not partner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Partner not found.",
        )

    # Query to get activities created by the partner
    query = db.query(ActivityModel).filter(ActivityModel.user_id == current_user.partner_id)

    # Apply the budget filter if provided
    if budget:
        try:
            query = query.filter(ActivityModel.budget == budget.lower())
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid budget provided.",
            )

    # Fetch the activities
    activities = query.all()

    # If no activities found, return an error
    if not activities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No activities found.",
        )

    # Shuffle the activities and select one randomly
    random.shuffle(activities)
    selected_activity = activities[0]  # Pick the first one after shuffling

    logger.info(f"Random activity (ID: {selected_activity.id}) retrieved successfully.")

    # Return the selected activity
    return ActivityResponse(
        id=selected_activity.id,
        activity_name=selected_activity.activity_name,
        activity_type=selected_activity.activity_type,
        budget=selected_activity.budget,
        location=selected_activity.location,
        link_info=selected_activity.link_info,
        description=selected_activity.description,
        user_id=current_user.partner_id,  # The partner is the creator
        partner_id=current_user.partner_id  # Return the partner_id for reference
    )