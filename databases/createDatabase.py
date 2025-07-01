from flask import Flask
from .base import db
from .models import *
from .models.user import AccessRoleEnum
from .models.item import StatusEnum
from sqlalchemy.dialects.sqlite import insert
from datetime import date
import bcrypt


def hashPassword(userPassword):
    return bcrypt.hashpw(userPassword.encode('utf-8'), bcrypt.gensalt())


def createDatabase(app: Flask):
   
    db.init_app(app=app)

    with app.app_context():
        db.create_all()

        #Upserting technique referenced from: https://www.slingacademy.com/article/sqlalchemy-upsert-update-if-exists-insert-if-not/ 
        #Upserting test data for Users 
        
        
        users = [
                {"userID": 1, "firstName": "John", "lastName": "Adams", "username": "johnAdams1", "password": hashPassword("password"), "accessRole": AccessRoleEnum.Admin, "isDeleted": False }, 
                {"userID": 2, "firstName": "Emily", "lastName": "Clark", "username": "emilyClark2", "password": hashPassword("Grape77!"), "accessRole": AccessRoleEnum.Admin, "isDeleted": False},
                {"userID": 3, "firstName": "James", "lastName": "Bennett", "username": "jamesBennett3", "password": hashPassword("AquaLion5^"), "accessRole": AccessRoleEnum.User, "isDeleted": False},
                {"userID": 4, "firstName": "Sophia", "lastName": "Turner", "username": "sophiaTurner4", "password": hashPassword("FastDuck6#"), "accessRole": AccessRoleEnum.User, "isDeleted": False},
                {"userID": 5, "firstName": "Liam", "lastName": "Mitchell", "username": "liamMitchell5", "password": hashPassword("LoudBat5%"), "accessRole": AccessRoleEnum.User, "isDeleted": False},
                {"userID": 6, "firstName": "Olivia", "lastName": "Green", "username": "oliviaGreen6", "password": hashPassword("NovaTree2@"), "accessRole": AccessRoleEnum.User, "isDeleted": False},
                {"userID": 7, "firstName": "Daniel", "lastName": "White", "username": "danielWhite7", "password": hashPassword("SwiftDog5%"), "accessRole": AccessRoleEnum.User, "isDeleted": False},
                {"userID": 8, "firstName": "Chloe", "lastName": "Scott", "username": "chloeScott8", "password": hashPassword("SnowDrip8*"), "accessRole": AccessRoleEnum.User, "isDeleted": False},
                {"userID": 9, "firstName": "Ethan", "lastName": "Hall", "username": "ethanHall9", "password": hashPassword("HappyPig4!"), "accessRole": AccessRoleEnum.User, "isDeleted": False},
                {"userID": 10, "firstName": "Grace", "lastName": "King", "username": "graceKing10", "password": hashPassword("TreeFrog0!"), "accessRole": AccessRoleEnum.User, "isDeleted": False}
            ]
        insertUsers = insert(User).values(users)
        upsertUsers = insertUsers.on_conflict_do_update(
            index_elements=["userID"],
            set_={'userID': insertUsers.excluded.userID}
        )
        db.session.execute(upsertUsers)
        db.session.commit()
        
        #Upserting test data for Vendors
      
        vendors = [
                {"vendorID": 1, "vendorName": "Samsung", "sustainabilityCertified": True, "isDeleted": False },
                {"vendorID": 2, "vendorName": "Apple", "sustainabilityCertified": True, "isDeleted": False },
                {"vendorID": 3, "vendorName": "Nvidia", "sustainabilityCertified": False, "isDeleted": False },   
                {"vendorID": 4, "vendorName": "Quantum Byte", "sustainabilityCertified": False, "isDeleted": False},
                {"vendorID": 5, "vendorName": "Zenith Circuits", "sustainabilityCertified": True, "isDeleted": False},
                {"vendorID": 6, "vendorName": "BlueNova Systems", "sustainabilityCertified": False, "isDeleted": False},
                {"vendorID": 7, "vendorName": "Orion Hardware", "sustainabilityCertified": True, "isDeleted": False},
                {"vendorID": 8, "vendorName": "HexaTech Labs", "sustainabilityCertified": False, "isDeleted": False},
                {"vendorID": 9, "vendorName": "SolarEdge Devices", "sustainabilityCertified": True, "isDeleted": False},
                {"vendorID": 10, "vendorName": "PulseGrid Innovations", "sustainabilityCertified": False, "isDeleted": False}
            ]
        insertVendors = insert(Vendor).values(vendors)
        upsertVendors = insertVendors.on_conflict_do_update(
                index_elements=["vendorID"],
                set_={'vendorID': insertVendors.excluded.vendorID}
            )
        db.session.execute(upsertVendors)
        db.session.commit()
        
        #Upserting test data for ItemCategory
        
        categories = [
                {"itemCategoryID": 1, "itemCategoryName": "Monitor", "isDeleted": False }, 
                {"itemCategoryID": 2, "itemCategoryName": "Keyboard", "isDeleted": False},
                {"itemCategoryID": 3, "itemCategoryName": "Mouse", "isDeleted": False},
                {"itemCategoryID": 4, "itemCategoryName": "Laptop", "isDeleted": False},
                {"itemCategoryID": 5, "itemCategoryName": "Printer", "isDeleted": False},
                {"itemCategoryID": 6, "itemCategoryName": "Router", "isDeleted": False},
                {"itemCategoryID": 7, "itemCategoryName": "Smartphone", "isDeleted": False},
                {"itemCategoryID": 8, "itemCategoryName": "Tablet", "isDeleted": False},
                {"itemCategoryID": 9, "itemCategoryName": "Server", "isDeleted": False},
                {"itemCategoryID": 10, "itemCategoryName": "Projector", "isDeleted": False}
            ]
        insertItemCategory = insert(ItemCategory).values(categories)
        upsertItemCategory = insertItemCategory.on_conflict_do_update(
                index_elements=["itemCategoryID"],
                set_={'itemCategoryID': insertItemCategory.excluded.itemCategoryID}
            )
        db.session.execute(upsertItemCategory)
        db.session.commit()
        
        #Upserting test data for Item
        
        items = [
                {"itemID": 1, "vendorID": 3, "userID": 2, "itemCategoryID": 4, "expiryDate": date(2025,6,23), "status": StatusEnum.Donated, "userNotes": "Donated in bin", "isDeleted": False }, 
                {"itemID": 2, "vendorID": 6, "userID": 4, "itemCategoryID": 1, "expiryDate": date(2025,7,15), "status": StatusEnum.Active, "userNotes": "", "isDeleted": False},
                {"itemID": 3, "vendorID": 1, "userID": 7, "itemCategoryID": 9, "expiryDate": date(2025,9,1), "status": StatusEnum.Donated, "userNotes": "", "isDeleted": False},
                {"itemID": 4, "vendorID": 8, "userID": 3, "itemCategoryID": 5, "expiryDate": date(2025,8,20), "status": StatusEnum.InRepair, "userNotes": "Broken charging port", "isDeleted": False},
                {"itemID": 5, "vendorID": 4, "userID": 1, "itemCategoryID": 7, "expiryDate": date(2025,10,10), "status": StatusEnum.Recycled, "userNotes": "", "isDeleted": False},
                {"itemID": 6, "vendorID": 10, "userID": 5, "itemCategoryID": 2, "expiryDate": date(2025,11,5), "status": StatusEnum.Active, "userNotes": "Working fine", "isDeleted": False},
                {"itemID": 7, "vendorID": 2, "userID": 8, "itemCategoryID": 8, "expiryDate": date(2025,6,30), "status": StatusEnum.Active, "userNotes": "", "isDeleted": False},
                {"itemID": 8, "vendorID": 5, "userID": 6, "itemCategoryID": 3, "expiryDate": date(2025,7,25), "status": StatusEnum.InRepair, "userNotes": "Damaged Screen", "isDeleted": False},
                {"itemID": 9, "vendorID": 9, "userID": 10, "itemCategoryID": 10, "expiryDate": date(2025,8,10), "status": StatusEnum.Recycled, "userNotes": "Dropped off anonymously", "isDeleted": False},
                {"itemID": 10, "vendorID": 7, "userID": 2, "itemCategoryID": 5, "expiryDate": date(2025,9,18), "status": StatusEnum.Recycled, "userNotes": "Depositied into basement", "isDeleted": False}
            ]
        insertItem = insert(Item).values(items)
        upsertItem = insertItem.on_conflict_do_update(
                index_elements=["itemID"],
                set_={'itemID': insertItem.excluded.itemID}
            )
        db.session.execute(upsertItem)
        db.session.commit()