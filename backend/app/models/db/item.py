from sqlalchemy import Column,  Integer, String, ForeignKey, DECIMAL, Date
from sqlalchemy.orm import relationship, declarative_base
import uuid
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()


# Account Table
class Account(Base):
    __tablename__ = "accounts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    external_id = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    type = Column(Integer, nullable=False)
    module_id = Column(UUID(as_uuid=True), ForeignKey("module.id"), nullable=False)
    
    # Relationships
    module = relationship("Module", back_populates="accounts")
    account_histories = relationship("AccountHistory", back_populates="account")
    account_investments_histories = relationship("InvestmentsHistory", back_populates="account")


# History Table
class AccountHistory(Base):
    __tablename__ = "account_history"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False)
    amount = Column(DECIMAL(15, 2), nullable=False)
    pru = Column(DECIMAL(15, 2))
    capital_gain = Column(DECIMAL(15, 2))
    date = Column(Date, nullable=False)
    
    # Relationships
    account = relationship("Account", back_populates="account_histories")

class InvestmentsHistory(Base):
    __tablename__ = "investments_history"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    date = Column(Date, nullable=False)
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False)
    label = Column(String(255), nullable=False)
    quantity = Column(DECIMAL(15, 2), nullable=True)
    unitprice = Column(DECIMAL(15, 2), nullable=True)
    unitvalue = Column(DECIMAL(15, 2), nullable=True)
    valuation = Column(DECIMAL(15, 2), nullable=False)
    diff = Column(DECIMAL(15, 2), nullable=True)
    diff_ratio = Column(DECIMAL(15, 2), nullable=True)
    
    # Relationships
    account = relationship("Account", back_populates="account_investments_histories")




# Module Table
class Module(Base):
    __tablename__ = "module"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    type = Column(String(100), nullable=False)
    
    # Relationships
    accounts = relationship("Account", back_populates="module")

