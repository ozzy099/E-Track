from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from ..base import db


class ItemCategory(db.Model):
    __tablename__ = 'ItemCategory'

    itemCategoryID: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True, nullable = False, unique = True)
    itemCategoryName:  Mapped[str] = mapped_column(String(50), nullable = False, unique=True)
    isDeleted: Mapped[bool] = mapped_column(Boolean, default=False,  nullable=True)

    #one to many relationship with item
    items = relationship("Item", back_populates="itemCategory")
    
    def __str__(self):
        return str(self.itemCategoryName)
    
    def get_id(self):
        return str(self.itemCategoryID)
   