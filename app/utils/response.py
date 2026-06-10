"""
Response wrapper for consistent API responses
"""

from typing import Any, Optional, Dict
from pydantic import BaseModel


class APIResponse(BaseModel):
    """Standard API response wrapper"""
    success: bool
    data: Optional[Any] = None
    message: str = "Success"
    errors: Optional[Dict[str, Any]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "data": {"id": 1, "name": "Example"},
                "message": "Operation completed successfully",
                "errors": None
            }
        }
