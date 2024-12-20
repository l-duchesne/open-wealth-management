import logging

from app.clients.woob_client import get_accounts
from app.models.db.database import get_db
from app.models.db.item import Module, Account, AccountHistory,InvestmentsHistory
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from datetime import date
from woob.capabilities.base import DecimalField
from decimal import Decimal
from woob.capabilities import bank
from sqlalchemy.exc import NoResultFound
from sqlalchemy.future import select

LOG = logging.getLogger(__name__)


async def refresh(db: AsyncSession = Depends(get_db)):
    try:
        module, accounts = get_accounts()

        module_id=uuid.uuid4()
        db_module = Module(
            id = module_id,
            name=module.name,
            type="bank"
        )
        db.add(db_module)
        
        db_accounts = []
        db_accounts_history = []
        db_investments_history = []
        for account in accounts:
            account_id=await create_or_update_account(db, account, module_id)
            
            investments = module.iter_investment(account)
            total_diff =0
            for investment in investments:
                db_investment = InvestmentsHistory(
                    date= date.today(),
                    account_id = account_id,
                    label = investment.label,
                    quantity  =  investment.quantity if isinstance(investment.quantity, Decimal) else None,
                    unitprice  = investment.unitprice if isinstance(investment.unitprice, Decimal) else None,
                    unitvalue  = investment.unitvalue if isinstance(investment.unitvalue, Decimal) else None,
                    valuation  = investment.valuation,
                    diff  = investment.diff if isinstance(investment.diff, Decimal) else None,
                    diff_ratio  = investment.diff_ratio if isinstance(investment.diff_ratio, Decimal) else None,
                )
                if isinstance(investment.diff, Decimal):
                    total_diff = total_diff +  investment.diff
                db_investments_history.append(db_investment)
                
            db_account_history = AccountHistory(
                account_id = account_id ,
                amount =  account.balance,
                date =  date.today(),
                capital_gain=total_diff
            )
            db_accounts_history.append(db_account_history)
            
            
        db.add_all(db_accounts)
        db.add_all(db_investments_history)    
        db.add_all(db_accounts_history)  
        await db.commit()
    except Exception as e:
        # Handle exceptions and rollback on error
        await db.rollback()
        raise e

async def create_or_update_account(session: AsyncSession, account : bank.Account, module_id: uuid ):
        # Try to fetch the account by external_id
        result = await session.execute( select(Account).filter_by(external_id=account.id))
        account_found = result.scalar_one_or_none()
        if account_found:
            # If found, update the fields
            account_found.name = account.label
            account_found.type = account.type
            LOG.info(f"Updated account with external_id: {account.id}")
            return account.id
        else:
            account_id = uuid.uuid4()
            
            # If not found, create a new account
            db_account = Account(
                id= account_id,
                external_id = account.id ,
                name =  account.label,
                type = account.type  ,
                module_id = module_id 
            )
            session.add(db_account)
            print(f"Created new account with external_id: {account.id}")
            return account_id