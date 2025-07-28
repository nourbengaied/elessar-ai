from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import Optional
from ..database import get_db
from ..services.export_service import ExportService
from ..utils.security import get_current_user
import io

router = APIRouter(prefix="/export", tags=["export"])

@router.get("/transactions/csv")
async def export_transactions_csv(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Export all transactions as CSV
    """
    try:
        export_service = ExportService(db)
        csv_content = export_service.export_transactions_csv(
            current_user["sub"], start_date, end_date
        )
        
        # Create streaming response
        csv_io = io.StringIO(csv_content)
        
        return StreamingResponse(
            iter([csv_io.getvalue()]),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=transactions_{start_date or 'all'}_{end_date or 'all'}.csv"
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/business-expenses/csv")
async def export_business_expenses_csv(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Export only business expenses as CSV
    """
    try:
        export_service = ExportService(db)
        csv_content = export_service.export_business_expenses_csv(
            current_user["sub"], start_date, end_date
        )
        
        # Create streaming response
        csv_io = io.StringIO(csv_content)
        
        return StreamingResponse(
            iter([csv_io.getvalue()]),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=business_expenses_{start_date or 'all'}_{end_date or 'all'}.csv"
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tax-report/csv")
async def export_tax_report_csv(
    tax_year: int = Query(..., description="Tax year (e.g., 2024)"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Export tax-ready report for a specific year
    """
    try:
        export_service = ExportService(db)
        csv_content = export_service.export_tax_report(
            current_user["sub"], tax_year
        )
        
        # Create streaming response
        csv_io = io.StringIO(csv_content)
        
        return StreamingResponse(
            iter([csv_io.getvalue()]),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=tax_report_{tax_year}.csv"
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/summary-report")
async def get_summary_report(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get a summary report of transactions
    """
    try:
        export_service = ExportService(db)
        summary = export_service.generate_summary_report(
            current_user["sub"], start_date, end_date
        )
        
        return summary
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 