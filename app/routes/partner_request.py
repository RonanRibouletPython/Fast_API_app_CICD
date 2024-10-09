from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.utils.utility import get_db
from app.db.models.partner_request import PartnerRequest as PartnerRequestModel
from app.schemas.partner_request import PartnerRequest, PartnerRequestCreate
from app.schemas.user import User as UserSchema
from app.utils.user import get_current_user
from app.db.models.user import User as UserModel
from app.utils.logger import logger
from datetime import datetime

router = APIRouter()

@router.post("/partner/request/{requested_user_id}", response_model=PartnerRequest)
async def send_partner_request(
    requested_user_id: int,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user)
):
    """Send a partner request to another user."""
    requested_user = db.query(UserModel).filter(UserModel.id == requested_user_id).first()
    
    # check if the requested user exists
    if not requested_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # check if the current user is sending a partner request to themselves
    if current_user.id == requested_user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot send a partner request to yourself.")
    
    # check if the current user or requested user is already in a relationship
    if current_user.partner_id or requested_user.partner_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="One of the users is already in a relationship.")
    
    # check if a request is already pending for either user
    existing_request = db.query(PartnerRequestModel).filter(
        ((PartnerRequestModel.requester_id == current_user.id) & (PartnerRequestModel.requested_id == requested_user_id)) |
        ((PartnerRequestModel.requester_id == requested_user_id) & (PartnerRequestModel.requested_id == current_user.id))
    ).filter(PartnerRequestModel.status == 'pending').first()
    
    if existing_request:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A partner request is already pending between these users.")
    
    # create a new partner request
    new_partner_request = PartnerRequestModel(
        requester_id=current_user.id,
        requested_id=requested_user_id,
    )
    db.add(new_partner_request)
    db.commit()
    db.refresh(new_partner_request)
    
    logger.info(f"Partner request sent from user {current_user.id} to user {requested_user_id}.")
    
    return new_partner_request

@router.post("/partner/response/{request_id}", response_model=PartnerRequest)
async def respond_to_partner_request(
    request_id: int,
    response: str,  # 'accepted' or 'declined'
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user)
):
    """Respond to a partner request."""
    partner_request = db.query(PartnerRequestModel).filter_by(
        id=request_id,
        requested_id=current_user.id,
        status='pending'
    ).first()

    if not partner_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Partner request not found.")
    
    if response not in ['accepted', 'declined']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid response.")
    
    if partner_request.requester_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot respond to your own partner request.")
    
    if response == 'declined':
        partner_request.status = 'declined'
        partner_request.updated_at = datetime.now()
        db.commit()
        return partner_request

    if response == 'accepted':
        # Fetch the requester user from the UserModel
        requester = db.query(UserModel).filter(
            UserModel.id == partner_request.requester_id
        ).first()

        if not requester:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requester not found.")
        
        if requester.partner_id or current_user.partner_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="One of the users is already in a relationship.")
        
        # Update partner IDs for both users
        requester.partner_id = current_user.id
        current_user.partner_id = requester.id
        partner_request.updated_at = datetime.now()
        
        # modify the updated_at field in the user database
        requester.updated_at = datetime.now()
        current_user.updated_at = datetime.now()
        
        # Update the partner request status
        partner_request.status = 'accepted'

        db.commit()
        return partner_request
    
@router.post("/partner/cancel")
async def cancel_partner_request(
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user)
):
    """Cancel the partner relationship."""
    if not current_user.partner_id:
        raise HTTPException(status_code=400, detail="You are not in a relationship")

    partner = db.query(UserModel).filter(UserModel.id == current_user.partner_id).first()

    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found")

    # Break the mutual relationship
    current_user.partner_id = None
    partner.partner_id = None
    partner.updated_at = datetime.now()
    current_user.updated_at = datetime.now()
    db.commit()
    
    return {"message": "Partner relationship canceled"}

