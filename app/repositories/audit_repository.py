"""
Audit log repository for database operations
"""

from typing import List
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models import AuditLog, AuditAction
from app.repositories.base_repository import BaseRepository
from app.utils.logger import get_logger

logger = get_logger(__name__)


class AuditRepository(BaseRepository[AuditLog]):
    """Repository for audit log operations"""

    def __init__(self, db: Session):
        super().__init__(db, AuditLog)

    def log_action(
        self,
        user_id: int,
        action: AuditAction,
        resource_type: str,
        resource_id: int = None,
        details: str = None,
        ip_address: str = None,
        status_code: int = None,
        error_message: str = None
    ) -> AuditLog:
        """Create audit log entry"""
        audit = AuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
            ip_address=ip_address,
            status_code=status_code,
            error_message=error_message
        )
        self.db.add(audit)
        self.db.commit()
        self.db.refresh(audit)
        logger.info(f"Audit log: User {user_id} performed {action} on {resource_type} {resource_id}")
        return audit

    def get_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        """Get all audit logs for a specific user"""
        return (
            self.db.query(AuditLog)
            .filter(AuditLog.user_id == user_id)
            .order_by(AuditLog.timestamp.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_action(self, action: AuditAction, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        """Get all audit logs for a specific action"""
        return (
            self.db.query(AuditLog)
            .filter(AuditLog.action == action)
            .order_by(AuditLog.timestamp.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_resource(self, resource_type: str, resource_id: int, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        """Get all audit logs for a specific resource"""
        return (
            self.db.query(AuditLog)
            .filter(AuditLog.resource_type == resource_type, AuditLog.resource_id == resource_id)
            .order_by(AuditLog.timestamp.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_recent_logs(self, hours: int = 24, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        """Get recent audit logs"""
        since = datetime.now() - timedelta(hours=hours)
        return (
            self.db.query(AuditLog)
            .filter(AuditLog.timestamp >= since)
            .order_by(AuditLog.timestamp.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
