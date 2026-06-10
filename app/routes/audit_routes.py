"""
Audit log routes
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.models import AuditAction
from app.repositories.audit_repository import AuditRepository
from app.middleware.auth_middleware import get_current_user, get_current_admin_user
from database.connection import get_db
from app.utils.logger import get_logger
from datetime import datetime

logger = get_logger(__name__)

router = APIRouter(prefix="/audit", tags=["Audit Logs"])


class AuditLogResponse(BaseModel):
    """Audit log response"""
    id: int
    user_id: int
    action: str
    resource_type: str
    resource_id: int
    details: str
    ip_address: str
    status_code: int
    timestamp: datetime
    
    class Config:
        from_attributes = True


@router.get("/logs/user/{user_id}", response_model=List[AuditLogResponse])
async def get_user_audit_logs(
    user_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Get audit logs for a specific user (Admin only)
    
    - **user_id**: ID of user to audit
    - **skip**: Number of records to skip
    - **limit**: Maximum records to return
    """
    try:
        repo = AuditRepository(db)
        logs = repo.get_by_user(user_id, skip, limit)
        logger.info(f"Retrieved {len(logs)} audit logs for user {user_id}")
        return logs
        
    except Exception as e:
        logger.error(f"Error getting audit logs: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting audit logs"
        )


@router.get("/logs/action/{action}", response_model=List[AuditLogResponse])
async def get_action_audit_logs(
    action: AuditAction,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Get audit logs for a specific action (Admin only)
    
    - **action**: Action type (CREATE, READ, UPDATE, DELETE, SALE, LOGIN, LOGOUT)
    - **skip**: Number of records to skip
    - **limit**: Maximum records to return
    """
    try:
        repo = AuditRepository(db)
        logs = repo.get_by_action(action, skip, limit)
        logger.info(f"Retrieved {len(logs)} audit logs for action {action}")
        return logs
        
    except Exception as e:
        logger.error(f"Error getting audit logs: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting audit logs"
        )


@router.get("/logs/resource/{resource_type}/{resource_id}", response_model=List[AuditLogResponse])
async def get_resource_audit_logs(
    resource_type: str,
    resource_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Get audit logs for a specific resource (Admin only)
    
    - **resource_type**: Type of resource (User, Medication, Sale, Stock)
    - **resource_id**: ID of resource
    - **skip**: Number of records to skip
    - **limit**: Maximum records to return
    """
    try:
        repo = AuditRepository(db)
        logs = repo.get_by_resource(resource_type, resource_id, skip, limit)
        logger.info(
            f"Retrieved {len(logs)} audit logs for {resource_type} {resource_id}"
        )
        return logs
        
    except Exception as e:
        logger.error(f"Error getting audit logs: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting audit logs"
        )


@router.get("/logs/recent", response_model=List[AuditLogResponse])
async def get_recent_audit_logs(
    hours: int = Query(24, ge=1, le=7*24),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Get recent audit logs (Admin only)
    
    - **hours**: Number of hours to look back (max 7 days)
    - **skip**: Number of records to skip
    - **limit**: Maximum records to return
    """
    try:
        repo = AuditRepository(db)
        logs = repo.get_recent_logs(hours, skip, limit)
        logger.info(f"Retrieved {len(logs)} recent audit logs (last {hours} hours)")
        return logs
        
    except Exception as e:
        logger.error(f"Error getting recent audit logs: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting audit logs"
        )
