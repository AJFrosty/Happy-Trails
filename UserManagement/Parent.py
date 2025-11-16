from UserManagement.User import User
import DataManagement
import datetime

class Camper:

    def __init__(self, name, age, dob, parentId, medicalInfo="N/A"):
        self.__name = name
        self.__age = age
        self.__dob = dob
        self.__parentId = parentId
        self.__medicalInfo = medicalInfo

    def getName(self):
        return self.__name

    def getAge(self):
        return self.__age

    def getDob(self):
        return self.__dob

    def getParentId(self):
        return self.__parentId

    def getMedicalInfo(self):
        return self.__medicalInfo

    def setName(self, name):
        self.__name = name

    def setAge(self, age):
        if not isinstance(age, int) or age <= 0:
            print("❌ Invalid age. Age must be a positive integer.")
            return
        self.__age = age

    def setDob(self, dob):
        self.__dob = dob

    def setParentId(self, parentId):
        self.__parentId = parentId

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

        while True:
            name = input("Enter Camper Name (First and Last): ").strip()
            if len(name.split()) < 2:
                print("❌ Please enter both first and last name.")
            else:
                break

        while True:
            try:
                age = int(input("Enter Age (5-19): ").strip())
                if age < 5 or age > 19:
                    print("❌ Age must be between 5 and 19.")
                else:
                    break
            except ValueError:
                print("❌ Age must be a valid number.")

        while True:
            dob_input = input("Enter Date of Birth (YYYY-MM-DD): ").strip()
            try:
                dob = datetime.datetime.strptime(dob_input, "%Y-%m-%d").date()
                today = datetime.date.today()
                calculated_age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                
                if abs(calculated_age - age) > 1:
                    print(f"⚠️ Age entered ({age}) does not match date of birth ({dob_input}). Please recheck.")
                    continue
                break
            except ValueError:
                print("❌ Invalid date format. Please use YYYY-MM-DD.")

        medicalInfo = input("Enter Medical Info (optional, press Enter to skip): ").strip() or "N/A"

        camper = Camper(name, age, dob_input, self.getID(), medicalInfo)

        record = f"{camper.getName()}:{camper.getAge()}:{camper.getDob()}:{camper.getParentId()}:{camper.getMedicalInfo()}\n"
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