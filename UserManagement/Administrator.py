from UserManagement.User import User
import DataManagement

class Administrator(User):
    def __init__(self, id: str, name: str, password: str, role: str, fileManager: DataManagement, authenticated: bool):
        super().__init__(id,name,password,role,fileManager, authenticated)

    def canCreate(self, roleToCreate: str) -> bool:
        return roleToCreate == "Staff"

    def canEdit(self, targetRole: str) -> bool:
        return True

    def canDelete(self, targetRole: str) -> bool:
        return True

    def showDashboard(self):
        print("\n--- ADMIN DASHBOARD ---")
        print("1. Create Staff Account")
        print("2. Edit/Delete User")
        print("3. Generate Reports")
        print("4. Backup/Restore Data")
        print("5. Logout")