"""
Sale repository for database operations
"""

from typing import List
from sqlalchemy.orm import Session
from datetime import datetime
from app.models import Sale
from app.repositories.base_repository import BaseRepository
from app.utils.logger import get_logger

logger = get_logger(__name__)


class SaleRepository(BaseRepository[Sale]):
    """Repository for sale operations"""

    def __init__(self, db: Session):
        super().__init__(db, Sale)

    def get_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Sale]:
        """Get all sales by a user"""
        return (
            self.db.query(Sale)
            .filter(Sale.user_id == user_id)
            .order_by(Sale.sale_date.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_receipt_number(self, receipt_number: str) -> Sale:
        """Get sale by receipt number"""
        return self.db.query(Sale).filter(Sale.receipt_number == receipt_number).first()

    def get_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Sale]:
        """Get sales within date range"""
        return (
            self.db.query(Sale)
            .filter(Sale.sale_date >= start_date, Sale.sale_date <= end_date)
            .order_by(Sale.sale_date.desc())
            .all()
        )

    def get_daily_total(self, date: datetime) -> float:
        """Get total sales for a day"""
        from sqlalchemy import func, and_
        from datetime import timedelta
        
        start = datetime(date.year, date.month, date.day)
        end = start + timedelta(days=1)
        
        result = (
            self.db.query(func.sum(Sale.total_price))
            .filter(and_(Sale.sale_date >= start, Sale.sale_date < end))
            .scalar()
        )
        return result or 0.0

    def get_best_selling_medications(self, limit: int = 10) -> List[dict]:
        """Get best-selling medications"""
        from sqlalchemy import func
        
        results = (
            self.db.query(Sale.medication_id, func.sum(Sale.quantity).label("total_qty"))
            .group_by(Sale.medication_id)
            .order_by(func.sum(Sale.quantity).desc())
            .limit(limit)
            .all()
        )
        return results
