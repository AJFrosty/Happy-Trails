from UserManagement.User import User
import DataManagement
import datetime

class Staff(User):
    def __init__(self, id: str, name: str, password: str, role: str, fileManager: DataManagement, authenticated: bool):
        super().__init__(id,name,password,role,fileManager, authenticated)

    def canCreate(self, roleToCreate: str) -> bool:
        return roleToCreate == "Parent" or roleToCreate == "Camper"

    def canEdit(self, targetRole: str) -> bool:
        return targetRole == "Parent" or targetRole == "Camper"

    def canDelete(self, targetRole: str) -> bool:
        return False

    def recordAttendance(self):

        campers = self.__fileManager.read("camper.txt")
        if not campers:
            print("❌ No campers found.")
            return

        camper_id = input("Enter Camper ID to record attendance: ").strip().upper()

        #Find camper
        camper_line = None
        for line in campers:
            parts = line.strip().split(":")
            if parts[0] == camper_id:
                camper_line = parts
                break

        if not camper_line:
            print("❌ Camper not found!")
            return

        camper_name = camper_line[1]

        print(f"📘 Recording attendance for: {camper_name}")

        status = input("Enter attendance (P = Present / A = Absent): ").strip().upper()

        if status == "P":
            status_text = "Present"
        elif status == "A":
            status_text = "Absent"
        else:
            print("❌ Invalid input. Use P or A.")
            return

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        record = f"{camper_id}:{camper_name}:{status_text}:{timestamp}\n"
        self.__fileManager.write("attendance.txt", record, append=True)

        print("✔ Attendance recorded successfully!")
        self.__fileManager.logAction(f"Recorded attendance for {camper_id} ({status_text})")

    def viewAttendanceLogs(self):
        fileManager = self.getFileManager()

        logs = fileManager.read("attendance.txt")

        if not logs:
            print("📭 No attendance records found.")
            return

        print("\n========== ATTENDANCE LOGS ==========")

        for line in logs:
            camper_id, camper_name, status, timestamp = line.strip().split(":")
            print(f"{camper_id} | {camper_name} | {status} | {timestamp}")

        print("======================================\n")

        self.logAction("Viewed attendance logs")


    def showDashboard(self):
        print("\n--- STAFF DASHBOARD ---")
        print("1. View Camper Info")
        print("2. Log Attendance for Assigned Sessions")
        print("3. View Attendance Records")
        print("4. Register Members")
        print("5. Logout")
