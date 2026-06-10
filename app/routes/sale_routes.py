"""
Sale routes - The showcase of ACID transactions!
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from typing import List
from app.schemas.sale_schema import SaleCreate, SaleResponse
from app.services.sale_service import SaleService
from app.middleware.auth_middleware import get_current_user, get_current_admin_user
from database.connection import get_db
from app.utils.logger import get_logger
from app.utils.exceptions import PharmaCoreException

logger = get_logger(__name__)

router = APIRouter(prefix="/sales", tags=["Sales"])


def get_client_ip(request: Request) -> str:
    """Extract client IP from request"""
    return request.client.host if request.client else "unknown"


@router.post("/", response_model=SaleResponse, status_code=status.HTTP_201_CREATED)
async def create_sale(
    sale_data: SaleCreate,
    request: Request,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a sale transaction with ACID guarantee
    
    This endpoint demonstrates professional-grade transaction handling:
    - Pessimistic locking prevents race conditions
    - Automatic rollback on any failure
    - Complete audit trail of all actions
    - Inventory consistency guaranteed
    
    - **medication_id**: ID of medication to sell
    - **quantity**: Quantity to sell
    - **payment_method**: Payment method (cash, card, etc)
    """
    try:
        service = SaleService(db)
        ip_address = get_client_ip(request)
        
        sale = service.create_sale(
            user_id=current_user.id,
            medication_id=sale_data.medication_id,
            quantity=sale_data.quantity,
            payment_method=sale_data.payment_method,
            ip_address=ip_address
        )
        
        logger.info(
            f"Sale created: {sale.receipt_number} "
            f"(user: {current_user.id}, amount: {sale.total_price})"
        )
        return sale
        
    except PharmaCoreException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Error creating sale: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating sale"
        )


@router.get("/", response_model=List[SaleResponse])
async def list_sales(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List all sales with pagination
    
    - **skip**: Number of records to skip
    - **limit**: Maximum records to return
    """
    try:
        service = SaleService(db)
        sales = service.get_sales_by_user(current_user.id, skip, limit)
        logger.info(f"Listed {len(sales)} sales (user: {current_user.id})")
        return sales
        
    except Exception as e:
        logger.error(f"Error listing sales: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error listing sales"
        )


@router.get("/{sale_id}", response_model=SaleResponse)
async def get_sale(
    sale_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get sale details by ID"""
    try:
        service = SaleService(db)
        sale = service.get_sale_by_id(sale_id)
        
        # Authorization check
        if sale.user_id != current_user.id and current_user.role.value != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this sale"
            )
        
        logger.info(f"Retrieved sale {sale_id} (user: {current_user.id})")
        return sale
        
    except PharmaCoreException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting sale: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting sale"
        )


@router.get("/analytics/daily-total", response_model=dict)
async def get_daily_total(
    current_user = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Get total sales for today (Admin only)
    
    This demonstrates analytics capabilities
    """
    try:
        from datetime import datetime
        service = SaleService(db)
        today = datetime.now()
        total = service.get_daily_sales_total(today)
        
        logger.info(f"Retrieved daily total: {total} (user: {current_user.id})")
        return {
            "date": today.date(),
            "total_sales": total,
            "currency": "USD"
        }
        
    except Exception as e:
        logger.error(f"Error getting daily total: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting daily total"
        )
