from sqlalchemy import Integer, String, ForeignKey, Date, Enum, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import date
import enum
from ..base import db

class StatusEnum(enum.Enum):
    Active = 1
    DroppedOff = 2
    InRepair = 3
    Recycled = 4
    Donated = 5

    def __str__(self):
        return str(self.name)

class Item(db.Model):
    __tablename__ = 'Item'

    itemID: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True, nullable = False, unique = True)
    vendorID: Mapped[int] = mapped_column(Integer, ForeignKey('Vendor.vendorID'))
    userID: Mapped[int] = mapped_column(Integer, ForeignKey('User.userID' ))
    itemCategoryID: Mapped[int] = mapped_column(Integer, ForeignKey('ItemCategory.itemCategoryID'))
    expiryDate: Mapped[date] = mapped_column(Date, nullable = False)
    status: Mapped[StatusEnum] = mapped_column(Enum(StatusEnum))
    userNotes: Mapped[str] = mapped_column(String(50), nullable = True)
    isDeleted: Mapped[bool] = mapped_column(Boolean, default=False,  nullable=True)
    
    #Relationships back to User, Vendor, and ItemCategory
    user = relationship("User", back_populates = "items", passive_deletes=True)
    vendor = relationship("Vendor", back_populates = "items", passive_deletes=True)
    itemCategory = relationship("ItemCategory", back_populates = "items", passive_deletes=True)

    def __int__(self):
        return self.itemID