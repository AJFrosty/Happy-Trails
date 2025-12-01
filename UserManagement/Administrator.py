from UserManagement.User import User
import DataManagement

class Administrator(User):
    def __init__(self, id: str, name: str, password: str, role: str, fileManager: DataManagement, authenticated: bool):
        super().__init__(id,name,password,role,fileManager, authenticated)

    def canCreate(self, roleToCreate: str) -> bool:
        return roleToCreate == "Staff" or roleToCreate == "Parent" or roleToCreate == "Camper"

    def canEdit(self, targetRole: str) -> bool:
        return True

    def canDelete(self, targetRole: str) -> bool:
        return True


     #REPORTS
    def generateReports(self):
        print("\n=== REPORT GENERATION ===")
        print("1. Users Report")
        print("2. Camper Report")
        print("3. Session Report")
        print("4. Log Activity Report")
        print("5. Back")

        choice = input("Select report type: ").strip()

        if choice == "1":
            self.generateUserReport()

        elif choice == "2":
            self.generateCamperReport()

        elif choice == "3":
            self.generateSessionReport()

        elif choice == "4":
            self.generateLogReport()

        elif choice == "5":
            return

        else:
            print("❌ Invalid option.")

    def generateUserReport(self):
        lines = self.getFileManager().read("users.txt")

        print("\nFilter Users by:")
        print("1. Role")
        print("2. Username")
        print("3. Show All")

        c = input("Choose filter: ")

        if c == "1":
            role = input("Enter role (Admin/Staff/Parent): ").strip().title()

            if role not in ["Admin", "Staff", "Parent"]:
                print("❌ Invalid role entered.")
                return

            data = [l for l in lines if f":{role}:" in l]

            if not data:
                print(f"⚠️ No users found with role '{role}'. Report canceled.")
                return

            action = f"Generated User Report (role={role})"

        elif c == "2":
            name = input("Enter username: ").strip()

            #check username exists at all
            if not any(f":{name}:" in l for l in lines):
                print("❌ Username not found in system.")
                return

            data = [l for l in lines if f":{name}:" in l]

            action = f"Generated User Report (username={name})"

        else:
            data = lines
            action = "Generated User Report (all users)"

        self.getFileManager().createReport("users.txt", data)
        self.logAction(action)

    def generateCamperReport(self):
        lines = self.getFileManager().read("camper.txt")

        print("\nFilter Campers by:")
        print("1. Parent ID")
        print("2. Age")
        print("3. Show All")

        c = input("Select option: ").strip()

        if c == "1":
            pid = input("Parent ID: ").strip()

            #Validate parent ID exists
            if not any(pid == l.split(":")[3] for l in lines):
                print("❌ No campers found for that Parent ID.")
                return

            data = [l for l in lines if pid == l.split(":")[3]]
            action = f"Generated Camper Report (parentID={pid})"

        elif c == "2":
            age = input("Age: ").strip()

            if not age.isdigit():
                print("❌ Age must be a number.")
                return

            if not any(age == l.split(":")[1] for l in lines):
                print("❌ No campers found with that age.")
                return

            data = [l for l in lines if age == l.split(":")[1]]
            action = f"Generated Camper Report (age={age})"

        else:
            data = lines
            action = "Generated Camper Report (all campers)"

        self.getFileManager().createReport("camper.txt", data)
        self.logAction(action)
    
    def generateSessionReport(self):
        lines = self.getFileManager().read("sessions.txt")

        print("\nFilter Sessions by:")
        print("1. Instructor")
        print("2. Age Group Label")
        print("3. Show All")

        c = input("Choose: ")

        if c == "1":
            instructor = input("Instructor Name: ").strip()
            data = [l for l in lines if l.endswith(f":{instructor}")]
            action = f"Generated Session Report (instructor={instructor})"

        elif c == "2":
            label = input("Age Group (e.g. 6-9): ").strip()
            data = [l for l in lines if f":{label}:" in l]
            action = f"Generated Session Report (ageGroup={label})"

        else:
            data = lines
            action = "Generated Session Report (all sessions)"

        self.getFileManager().createReport("sessions.txt", data)
        self.logAction(action)
    
    def generateLogReport(self):
        lines = self.getFileManager().read("log.txt")

        print("\nFilter Logs by:")
        print("1. User ID")
        print("2. Action Type")
        print("3. Show All")

        c = input("Choose: ")

        if c == "1":
            uid = input("User ID: ").strip()
            data = [l for l in lines if l.startswith(uid + ":")]
            action = f"Generated Log Report (userID={uid})"

        elif c == "2":
            action = input("Action (keyword): ").strip()
            data = [l for l in lines if action.lower() in l.lower()]

        else:
            data = lines
            action = "Generated Log Report (all logs)"

        self.getFileManager().createReport("log.txt", data)
        self.logAction(action)

    def deleteUserByID(self):
        lines = self.__fileManager.read("users.txt")

        print("\nDelete User Account")
        uid = input("Enter User ID to delete: ").strip()

        if uid == self.getID():
            print("You cannot delete your own admin account.")
            return

        updated = []
        deleted_user = None

        #Find the user by ID
        for line in lines:
            parts = line.split(":")
            userID = parts[0]

            if userID == uid:
                deleted_user = line
            else:
                updated.append(line)

        if not deleted_user:
            print("User ID not found.")
            return

        print(f"\nFound User: {deleted_user}")
        confirm = input("Are you SURE you want to delete this user? (y/n): ").lower()

        if confirm != "y":
            print("Deletion cancelled.")
            return

        #Write updated list back
        self.__fileManager.write("users.txt", updated, overwrite=True)

        print("User deleted successfully.")
        self.logAction(f"Deleted user with ID {uid}")

    def editUser(self):
        lines = self.__fileManager.read("users.txt")

        print("\nEdit User Account")
        uid = input("Enter User ID to edit: ").strip()

        #Validation: cannot change your own role
        editing_self = (uid == self.getID())

        target_line = None
        updated = []

        #Find target user
        for line in lines:
            parts = line.strip().split(":")
            if parts[0] == uid:
                target_line = parts
            else:
                updated.append(line)

        if not target_line:
            print("❌ User ID not found.")
            return

        userID, username, password, role = target_line

        print(f"\nCurrent Info:")
        print(f"Username: {username}")
        print(f"Role: {role}")

        print("\nWhat would you like to edit?")
        print("1. Username")
        print("2. Password")
        print("3. Role")
        print("4. Cancel")

        choice = input("Option: ").strip()

        if choice == "4":
            print("Edit cancelled.")
            return

        #Edit username
        if choice == "1":
            newUsername = input("Enter new username: ").strip()
            if not newUsername:
                print("❌ Username cannot be empty.")
                return
            username = newUsername
            action = f"Edited Username (ID={uid})"

        #Edit password
        elif choice == "2":
            newPassword = input("Enter new password: ").strip()
            if not newPassword:
                print("❌ Password cannot be empty.")
                return
            password = newPassword
            action = f"Edited Password (ID={uid})"

        # dit role
        elif choice == "3":
            if editing_self:
                print("❌ You cannot change your own role.")
                return

            print("\nAvailable Roles: Staff / Parent")
            newRole = input("Enter new role: ").strip()

            if newRole not in ["Staff", "Parent"]:
                print("❌ Invalid role.")
                return

            role = newRole
            action = f"Edited Role (ID={uid})"

        else:
            print("❌ Invalid choice.")
            return

        #Rebuild updated line
        newLine = f"{userID}:{username}:{password}:{role}\n"
        updated.append(newLine)

        #Save file
        self.__fileManager.write("users.txt", updated, overwrite=True)

        print("User updated successfully.")
        self.logAction(action)

    def showDashboard(self):
        print("\n--- ADMIN DASHBOARD ---")
        print("1. Register an Account")
        print("2. Delete A User")
        print("3. Edit A User")
        print("4. Generate Reports")
        print("5. Backup/Restore Data")
        print("6. Session Management Dashboard")
        print("7. View Camper Info")
        print("8. Logout")
    