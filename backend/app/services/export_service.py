import pandas as pd
import io
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from ..models.transaction import Transaction
from datetime import datetime

class ExportService:
    def __init__(self, db: Session):
        self.db = db
    
    def export_transactions_csv(self, user_id: str, start_date: str = None, end_date: str = None) -> str:
        """
        Export user transactions as CSV
        """
        query = self.db.query(Transaction).filter(Transaction.user_id == user_id)
        
        if start_date:
            query = query.filter(Transaction.date >= start_date)
        if end_date:
            query = query.filter(Transaction.date <= end_date)
        
        transactions = query.order_by(Transaction.date.desc()).all()
        
        # Convert to DataFrame
        data = []
        for t in transactions:
            data.append({
                'Date': t.date.strftime('%Y-%m-%d'),
                'Description': t.description,
                'Amount': float(t.amount),
                'Currency': t.currency,
                'Merchant': t.merchant or '',
                'Category': t.category or '',
                'Business_Expense': 'Yes' if t.is_business_expense else 'No',
                'Confidence_Score': t.confidence_score or 0.0,
                'Manually_Overridden': 'Yes' if t.manually_overridden else 'No',
                'LLM_Reasoning': t.llm_reasoning or ''
            })
        
        df = pd.DataFrame(data)
        
        # Create CSV string
        output = io.StringIO()
        df.to_csv(output, index=False)
        return output.getvalue()
    
    def export_business_expenses_csv(self, user_id: str, start_date: str = None, end_date: str = None) -> str:
        """
        Export only business expenses as CSV
        """
        query = self.db.query(Transaction).filter(
            Transaction.user_id == user_id,
            Transaction.is_business_expense == True
        )
        
        if start_date:
            query = query.filter(Transaction.date >= start_date)
        if end_date:
            query = query.filter(Transaction.date <= end_date)
        
        transactions = query.order_by(Transaction.date.desc()).all()
        
        # Convert to DataFrame
        data = []
        for t in transactions:
            data.append({
                'Date': t.date.strftime('%Y-%m-%d'),
                'Description': t.description,
                'Amount': float(t.amount),
                'Currency': t.currency,
                'Merchant': t.merchant or '',
                'Category': t.category or '',
                'Confidence_Score': t.confidence_score or 0.0,
                'LLM_Reasoning': t.llm_reasoning or ''
            })
        
        df = pd.DataFrame(data)
        
        # Create CSV string
        output = io.StringIO()
        df.to_csv(output, index=False)
        return output.getvalue()
    
    def generate_summary_report(self, user_id: str, start_date: str = None, end_date: str = None) -> Dict[str, Any]:
        """
        Generate a summary report of transactions
        """
        query = self.db.query(Transaction).filter(Transaction.user_id == user_id)
        
        if start_date:
            query = query.filter(Transaction.date >= start_date)
        if end_date:
            query = query.filter(Transaction.date <= end_date)
        
        transactions = query.all()
        
        total_amount = sum(float(t.amount) for t in transactions)
        business_amount = sum(float(t.amount) for t in transactions if t.is_business_expense)
        personal_amount = sum(float(t.amount) for t in transactions if not t.is_business_expense)
        
        # Category breakdown
        category_totals = {}
        for t in transactions:
            if t.is_business_expense and t.category:
                category = t.category
                amount = float(t.amount)
                category_totals[category] = category_totals.get(category, 0) + amount
        
        return {
            "total_transactions": len(transactions),
            "total_amount": round(total_amount, 2),
            "business_amount": round(business_amount, 2),
            "personal_amount": round(personal_amount, 2),
            "business_percentage": round((business_amount / total_amount * 100) if total_amount > 0 else 0, 2),
            "category_breakdown": {k: round(v, 2) for k, v in category_totals.items()},
            "date_range": {
                "start_date": start_date,
                "end_date": end_date
            },
            "generated_at": datetime.utcnow().isoformat()
        }
    
    def export_tax_report(self, user_id: str, tax_year: int) -> str:
        """
        Export tax-ready report for a specific year
        """
        start_date = f"{tax_year}-01-01"
        end_date = f"{tax_year}-12-31"
        
        query = self.db.query(Transaction).filter(
            Transaction.user_id == user_id,
            Transaction.is_business_expense == True,
            Transaction.date >= start_date,
            Transaction.date <= end_date
        )
        
        transactions = query.order_by(Transaction.date).all()
        
        # Convert to DataFrame with tax-friendly format
        data = []
        for t in transactions:
            data.append({
                'Date': t.date.strftime('%m/%d/%Y'),
                'Description': t.description,
                'Amount': float(t.amount),
                'Category': t.category or 'Uncategorized',
                'Merchant': t.merchant or '',
                'Receipt_Required': 'Yes' if float(t.amount) > 75 else 'No'
            })
        
        df = pd.DataFrame(data)
        
        # Create CSV string
        output = io.StringIO()
        df.to_csv(output, index=False)
        return output.getvalue() 