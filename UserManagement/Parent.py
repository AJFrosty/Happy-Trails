from UserManagement.User import User
import DataManagement

class Camper:
    def __init__(self, name, age, dob, parentID, medicalInfo="N/A"):
        self.name = name
        self.age = age
        self.dob = dob
        self.parentID = parentID
        self.medicalInfo = medicalInfo

    def getName(self):
        return self.__name

    def getAge(self):
        return self.__age

    def getDOB(self):
        return self.__dob

    def getParentID(self):
        return self.__parentID

    def getMedicalInfo(self):
        return self.__medicalInfo

    def setName(self, name):
        self.__name = name

    def setAge(self, age):
        if not isinstance(age, int) or age <= 0:
            print("❌ Invalid age. Age must be a positive integer.")
            return
        self.__age = age

    def setDOB(self, dob):
        self.__dob = dob

    def setParentID(self, parentID):
        self.__parentID = parentID

    def setMedicalInfo(self, medicalInfo):
        self.__medicalInfo = medicalInfo

class Parent(User):
    def __init__(self, id: str, name: str, password: str, role: str, fileManager: DataManagement, authenticated: bool):
        super().__init__(id,name,password,role,fileManager, authenticated)
        
    def canCreate(self, roleToCreate: str) -> bool:
        return roleToCreate == "Camper"

    def canEdit(self, targetRole: str) -> bool:
        return targetRole == "Camper"

    def canDelete(self, targetRole: str) -> bool:
        return targetRole == "Camper"

    def registerCamper(self):
        if not self.isAuthenticated():
            print("❌ You must be logged in to register a camper.")
            return

        # Collect camper details
        name = input("Enter Camper Name: ").strip()
        age = input("Enter Age: ").strip()
        dob = input("Enter Date of Birth (YYYY-MM-DD): ").strip()
        medicalInfo = input("Enter Medical Info (optional, press Enter to skip): ").strip() or "N/A"

        camper = Camper(name, age, dob, self.getID(), medicalInfo)
        # Save to camper.txt
        record = f"{camper.getName()}:{camper.getAge()}:{camper.getDob()}:{camper.getParentID()}:{camper.getMedicalInfo()}\n"

        success = self.getFileManager().write("camper.txt", record, append=True)
        if success:
            print(f"✅ Camper '{name}' registered successfully.")
            self.logAction(f"Registered camper '{name}'")
        else:
            print("❌ Failed to register camper. Check file permissions.")


    def showDashboard(self):
        print("\n--- PARENT DASHBOARD ---")
        print("1. Register New Camper")
        print("2. Update Camper Details")
        print("3. Enroll Camper in Session")
        print("4. Logout")