import re
import hashlib
import getpass
import datetime
from DataManagement.DataManagement import DataManagement

class User:

    def __init__(self, id: str, name: str, password: str, role: str, fileManager: DataManagement, authenticated: bool):
        self.__id = id
        self.__name = name
        self.__password = password
        self.__role = role
        self.__fileManager = fileManager
        self.__authenticated = authenticated
        self.rolePrefix = {"Admin": "ADM_", "Staff": "STF_", "Parent": "PRT_"}
        self.roleHeirachy = {"Admin": ["Staff"], "Staff": ["Parent"], "Parent": ["Camper"]}
    
    #Password Management
    def encryptPassword(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def validatePassword(self, password: str) -> bool:
        if (len(password) < 8 or
            not re.search(r"[A-Z]", password) or
            not re.search(r"[a-z]", password) or
            not re.search(r"\d", password) or
            not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)):
            print("❌ Password must include uppercase, lowercase, number, and special character (min 8 chars).")
            return False
        return True
    
    def generateId(self, role: str) -> str:
        prefix = self.rolePrefix.get(role, role[:3].upper() + "_")
        users = self.__fileManager.read("users.txt")
        ids = [int(line.split(":")[0].split("_")[1]) for line in users if len(line.split(":")) >= 2 and line.split(":")[1] == role]
        nextNum = max(ids) + 1 if ids else 0
        return f"{prefix}{nextNum}"
    
    #REGISTRATION
    def register(self):
        if not self.__authenticated:
            print("❌ You must be logged in to create another user.")
            return

        roleToCreate = input("Enter role to create: ").capitalize()
        if not self.canCreate(roleToCreate):
            print(f"❌ A {self.__role} cannot create a {roleToCreate}.")
            return

        users = self.__fileManager.read("users.txt")
        username = input("Enter new username: ").strip()

        if any(line.split(":")[2] == username for line in users if len(line.split(":")) >= 3):
            print("❌ Username already exists.")
            return

        password = getpass.getpass("Enter password: ").strip()
        while not self.validatePassword(password):
            password = getpass.getpass("Re-enter valid password: ").strip()

        hashedPw = self.encryptPassword(password)
        newId = self.generateId(roleToCreate)
        newRecord = f"{newId}:{roleToCreate}:{username}:{hashedPw}\n"
        success = self.__fileManager.write("users.txt", newRecord, append=True)

        if success:
            print(f"✅ {roleToCreate} '{username}' created successfully with ID {newId}.")
            self.logAction(f"Registered camper '{username}'")      
        else:
            print("❌ Failed to create user. Check file permissions.")

    #Functions For Inheritance
    def canCreate(self, roleToCreate: str) -> bool:
        return False

    def canEdit(self, targetRole: str) -> bool:
        return False

    def canDelete(self, targetRole: str) -> bool:
        return False

    def showDashboard(self):
        print(f"Logged in as {self.__role}. No dashboard implemented.")
    

    #ALL THE GETTERS FOR ATTRIBUTES
    def getID(self): return self.__id
    def getName(self): return self.__name
    def getPassword(self): return self.__password
    def getRole(self): return self.__role
    def getFileManager(self): return self.__fileManager
    def isAuthenticated(self): return self.__authenticated

    #LOGGING
    def logAction(self, action: str):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        record = f"{self.getID()}:{self.getName()}:{action}:{timestamp}\n"
        success = self.getFileManager().write("session.txt", record, append=True)
        if not success:
            print("⚠️ Failed to log session.")