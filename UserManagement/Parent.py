from UserManagement.User import User
import DataManagement
import datetime

class Camper:

    def __init__(self, camperID,name, age, dob, parentId, medicalInfo="N/A"):
        self.__camperID = camperID
        self.__name = name
        self.__age = age
        self.__dob = dob
        self.__parentId = parentId
        self.__medicalInfo = medicalInfo

    def getCamperID(self):
        return self.__camperID
    
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
    
    def getNewCamperID(self) -> str:
        records = self.getFileManager().read("camper.txt")

        max_id = 0
        for line in records:
            parts = line.split(":")
            if len(parts) >= 6:
                cid = parts[0]
                if cid.startswith("CMP"):
                    try:
                        num = int(cid[3:])
                        max_id = max(max_id, num)
                    except ValueError:
                        continue

        new_id = f"CMP{max_id + 1:04d}"
        return new_id

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

        camper_id = self.getNewCamperID()
        camper = Camper(camper_id, name, age, dob_input, self.getID(), medicalInfo)

        record = f"{camper.getCamperID()}:{camper.getName()}:{camper.getAge()}:{camper.getDob()}:{camper.getParentId()}:{camper.getMedicalInfo()}\n"

        success = self.getFileManager().write("camper.txt", record, append=True)

        if success:
            print(f"✅ Camper '{name}' registered successfully with ID {camper_id}.")
            self.logAction(f"Registered camper '{name}' (ID {camper_id})")
        else:
            print("❌ Failed to register camper. Check file permissions.")

    def updateCamper(self):
        if not self.isAuthenticated():
            print("❌ You must be logged in.")
            return

        fm = self.getFileManager()
        campers = fm.read("camper.txt")

        camper_id = input("Enter Camper ID to update: ").strip()

        #Find camper
        found = None
        for line in campers:
            parts = line.split(":")
            if len(parts) >= 5 and parts[3] == self.getID() and parts[0] == camper_id:
                found = parts
                break

        if not found:
            print("❌ Camper not found or you do not have permission to update this camper.")
            return

        old_name, old_age, old_dob, parent_id, old_medical = found

        print("\n--- Leave field empty to keep current value ---")
        new_name = input(f"Name ({old_name}): ").strip() or old_name
        new_medical = input(f"Medical Info ({old_medical}): ").strip() or old_medical

        # Eligibility Check (6–17)
        while True:
            new_age_input = input(f"Age ({old_age}): ").strip()
            if new_age_input == "":
                new_age = int(old_age)
                break
            try:
                new_age = int(new_age_input)
                if 6 <= new_age <= 17:
                    break
                print("❌ Age must be between 6 and 17 for eligibility.")
            except:
                print("❌ Invalid age.")

        # Rewrite file
        new_lines = []
        for line in campers:
            parts = line.split(":")
            if len(parts) >= 5 and parts[0] == camper_id:
                newline = f"{camper_id}:{new_name}:{new_age}:{old_dob}:{parent_id}:{new_medical}"
                new_lines.append(newline)
            else:
                new_lines.append(line)

        fm.write("camper.txt", new_lines, append=False)

        fm.logAction(self.getID(), self.getUsername(), f"Updated camper {camper_id}")

        print("✅ Camper updated successfully.")
        
    def showDashboard(self):
        print("\n--- PARENT DASHBOARD ---")
        print("1. Register New Camper")
        print("2. Update Camper Details")
        print("3. Enroll Camper in Session")
        print("4. Logout")