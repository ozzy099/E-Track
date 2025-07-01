from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from ..base import db

class Vendor(db.Model):
    __tablename__ = 'Vendor'

    vendorID: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True, nullable = False, unique = True)
    vendorName: Mapped[str] = mapped_column(String(50), nullable = False)
    sustainabilityCertified: Mapped[bool] = mapped_column(Boolean, nullable = False)
    isDeleted: Mapped[bool] = mapped_column(Boolean, default=False,  nullable=True)

    #one to many relationship with item
    items = relationship("Item", back_populates = "vendor")

    def __str__(self):
        return str(self.vendorName)
    
    def get_id(self):
        return str(self.vendorID)

