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
            self.__fileManager.logAction(f"Registered camper '{username}'")      
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
    
    #Camper Searching
    def viewCamperInfo(self):
        lines = self.getFileManager().read("camper.txt")

        if not lines:
            print("No camper records found.")
            return

        print("\nView Camper Information")
        print("1. Search by Camper ID")
        print("2. Search by Name")
        print("3. View All (Admins/Staff only)")

        choice = input("Choose an option: ").strip()

        def parse(line):
            parts = line.split(":")
            return {
                "camperID": parts[0],
                "name": parts[1],
                "age": parts[2],
                "dob": parts[3],
                "parentID": parts[4],
                "medical": parts[5] if len(parts) > 5 else "N/A"
            }

        def allowed(camper):
            role = self.getRole().lower()
            if role in ["admin", "staff"]:
                return True
            return camper["parentID"] == self.getID()

        def display(camper):
            print("\n---------------------------")
            print(f"Camper ID: {camper['camperID']}")
            print(f"Name: {camper['name']}")
            print(f"Age: {camper['age']}")
            print(f"DOB: {camper['dob']}")
            print(f"Parent ID: {camper['parentID']}")
            print(f"Medical Info: {camper['medical']}")
            print("---------------------------")

        #Search By ID
        if choice == "1":
            cid = input("Enter Camper ID (e.g., CMP0001): ").strip()
            found = []

            for line in lines:
                camper = parse(line)
                if camper["camperID"] == cid and allowed(camper):
                    found.append(camper)

            if not found:
                print("Camper not found or access denied.")
                return

            for c in found:
                display(c)

            self.__fileManager.logAction(f"Viewed camper by ID ({cid})")
            return

        #Search by name/partial name
        elif choice == "2":
            name = input("Enter full or partial name: ").strip().lower()
            found = []

            for line in lines:
                camper = parse(line)
                if name in camper["name"].lower() and allowed(camper):
                    found.append(camper)

            if not found:
                print("No campers matched that name (or not authorized).")
                return

            for c in found:
                display(c)

            self.logAction(f"Viewed camper by name ({name})")
            return

        #View All
        elif choice == "3":
            if self.getRole().lower() not in ["admin", "staff"]:
                print("Only Admin or Staff can view all campers.")
                return

            for line in lines:
                display(parse(line))

            self.logAction("Viewed all campers")
            return

        else:
            print("Invalid option.")
    
    #ALL THE GETTERS FOR ATTRIBUTES
    def getID(self): return self.__id
    def getName(self): return self.__name
    def getPassword(self): return self.__password
    def getRole(self): return self.__role
    def getFileManager(self): return self.__fileManager
    def isAuthenticated(self): return self.__authenticated
    
    