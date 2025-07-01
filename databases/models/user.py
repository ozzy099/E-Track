from sqlalchemy import Integer, String, Enum, Boolean, LargeBinary
from sqlalchemy.orm import relationship, Mapped, mapped_column
from ..base import db
import enum
from flask_login import UserMixin

class AccessRoleEnum(enum.Enum):
    User = 1
    Admin = 2

    def __str__(self):
        return str(self.name)


class User(UserMixin, db.Model):
    __tablename__ = 'User'

    userID: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True, nullable = False, unique = True)
    firstName: Mapped[str] = mapped_column(String (50), nullable = False)
    lastName: Mapped[str] = mapped_column(String (50), nullable = False)
    username: Mapped[str] = mapped_column(String (25), unique = True, nullable = False)
    password: Mapped[bytes] = mapped_column(LargeBinary(60), nullable = False)
    accessRole:  Mapped[AccessRoleEnum] = mapped_column(Enum(AccessRoleEnum))
    isDeleted: Mapped[bool] = mapped_column(Boolean, default=False,  nullable=True) 

    #Defining one to many relationship with Item
    items = relationship("Item", back_populates="user")
   
    def __str__(self):
        return str(self.userID) + f" ({str(self.firstName)} {str(self.lastName)})"
    
    def get_id(self):
        return str(self.userID)