from UserManagement.User import User
import DataManagement

class Staff(User):
    def __init__(self, id: str, name: str, password: str, role: str, fileManager: DataManagement, authenticated: bool):
        super().__init__(id,name,password,role,fileManager, authenticated)

    def canCreate(self, roleToCreate: str) -> bool:
        return roleToCreate == "Parent" or roleToCreate == "Camper"

    def canEdit(self, targetRole: str) -> bool:
        return targetRole == "Parent" or targetRole == "Camper"

    def canDelete(self, targetRole: str) -> bool:
        return False

    def showDashboard(self):
        print("\n--- STAFF DASHBOARD ---")
        print("1. View Camper Info")
        print("2. Log Attendance for Assigned Sessions")
        print("3. View Attendance Records")
        print("4. Register a Camper")
        print("5. Logout")
