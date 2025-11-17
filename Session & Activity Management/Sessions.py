from datetime import datetime, date
from DataManagement.DataManagement import DataManagement
from UserManagement.User import User

class Session:
    def __init__(self, session_id, name, activity_type, start_date, end_date, age_group_label, min_age, max_age, capacity, spots_available, instructor):
        self.session_id = session_id
        self.name = name
        self.activity_type = activity_type
        self.start_date = start_date
        self.end_date = end_date
        self.age_group_label = age_group_label
        self.min_age = min_age
        self.max_age = max_age
        self.capacity = capacity
        self.spots_available = spots_available
        self.instructor = instructor

    def toRecord(self):
        return f"{self.session_id}:{self.name}:{self.activity_type}:{self.start_date}:{self.end_date}:" \
               f"{self.age_group_label}:{self.min_age}:{self.max_age}:{self.capacity}:" \
               f"{self.spots_available}:{self.instructor}\n"

    @staticmethod
    def fromRecord(line):
        parts = line.strip().split(":")
        if len(parts) != 11:
            return None
        return Session(
            session_id=parts[0],
            name=parts[1],
            activity_type=parts[2],
            start_date=parts[3],
            end_date=parts[4],
            age_group_label=parts[5],
            min_age=int(parts[6]),
            max_age=int(parts[7]),
            capacity=int(parts[8]),
            spots_available=int(parts[9]),
            instructor=parts[10]
        )


class SessionManager:
    def __init__(self, fileManager: DataManagement):
        self.fileManager = fileManager
        self.sessions = {}
        self.loadSessions()
    
    #Load & Save Sessions
    def loadSessions(self):
        lines = self.fileManager.read("sessions.txt")
        if not lines:
            return
        for line in lines:
            s = Session.fromRecord(line)
            if s:
                self.sessions[s.session_id] = s

    def saveSessions(self):
        text = "".join(s.toRecord() for s in self.sessions.values())
        self.fileManager.write("sessions.txt", text, append=False)
    
    #Creating Sessions

    def generateID(self):
        return f"S{1000000 + len(self.sessions)}"
    
    def createSession(self, adminUser: User):
        if adminUser.getRole().lower() != "admin":
            print("❌ You are not authorized to create sessions. (REQ-3.7)")
            return

        print("\n=== Create New Session ===")
        name = input("Session Name: ").strip()
        activity = input("Activity Type: ").strip()
        start = input("Start Date (YYYY-MM-DD): ").strip()
        end = input("End Date (YYYY-MM-DD): ").strip()
        age_label = input("Age Group Label (e.g. 6-9): ").strip()

        try:
            min_age, max_age = map(int, age_label.split("-"))
        except:
            print("❌ Invalid age group format.")
            return

        instructor = input("Assigned Instructor: ").strip()
        capacityStr = input("Capacity: ").strip()

        if not capacityStr.isdigit():
            print("❌ Capacity must be a number.")
            return

        capacity = int(capacityStr)

        if not self.validateSessionDetails(name, activity, start, end, min_age, max_age, instructor, capacity):
            return

        session_id = self.generateID()
        session = Session(
            session_id=session_id,
            name=name,
            activity_type=activity,
            start_date=start,
            end_date=end,
            age_group_label=age_label,
            min_age=min_age,
            max_age=max_age,
            capacity=capacity,
            spots_available=capacity,
            instructor=instructor
        )
        self.sessions[session_id] = session
        self.saveSessions()

        print(f"✅ Session '{name}' created with ID {session_id}.")
    
    def editSession(self, adminUser: User):
        if adminUser.getRole().lower() != "admin":
            print("❌ Unauthorized.")
            return

        sid = input("Enter Session ID to Edit: ").strip().upper()

        if sid not in self.sessions:
            print("❌ Session not found.")
            return

        s = self.sessions[sid]

        print("\n=== Editing Session ===")
        print("Press Enter to keep current value.\n")

        name = input(f"Name ({s.name}): ").strip() or s.name
        activity = input(f"Activity Type ({s.activity_type}): ").strip() or s.activity_type
        start = input(f"Start Date ({s.start_date}): ").strip() or s.start_date
        end = input(f"End Date ({s.end_date}): ").strip() or s.end_date
        age_label = input(f"Age Group ({s.age_group_label}): ").strip() or s.age_group_label
        instructor = input(f"Instructor ({s.instructor}): ").strip() or s.instructor
        capacityStr = input(f"Capacity ({s.capacity}): ").strip() or str(s.capacity)

        try:
            min_age, max_age = map(int, age_label.split("-"))
        except:
            print("❌ Invalid age group format.")
            return

        if not capacityStr.isdigit():
            print("❌ Capacity must be numeric.")
            return

        capacity = int(capacityStr)
        taken = s.capacity - s.spots_available
        newSpots = max(0, capacity - taken)

        if not self.validateSessionDetails(name, activity, start, end, min_age, max_age, instructor, capacity):
            return

        s.name = name
        s.activity_type = activity
        s.start_date = start
        s.end_date = end
        s.age_group_label = age_label
        s.min_age = min_age
        s.max_age = max_age
        s.capacity = capacity
        s.spots_available = newSpots
        s.instructor = instructor

        self.saveSessions()

        print("✅ Session updated successfully.")

    def deleteSession(self, adminUser: User):
        if adminUser.getRole().lower() != "admin":
            print("❌ Unauthorized.")
            return

        sid = input("Enter Session ID to Delete: ").strip().upper()

        if sid not in self.sessions:
            print("❌ No such session.")
            return

        del self.sessions[sid]
        self.saveSessions()

        print("🗑️ Session deleted successfully.")
    
    def displaySessions(self):
        if not self.sessions:
            print("⚠️ No sessions available.")
            return

        print("\n=== Available Sessions ===")
        for s in self.sessions.values():
            print(f"{s.session_id} | {s.name} | {s.activity_type} | {s.start_date}→{s.end_date} | "
                  f"Ages {s.min_age}-{s.max_age} | {s.spots_available}/{s.capacity} spots | Instructor: {s.instructor}")

    def validateSessionDetails(self, name: str, activity: str, start: str, end: str, min_age: int, max_age: int, instructor: str, capacity: int):
        if not name or not activity or not instructor:
            print("❌ Missing required fields.")
            return False

        try:
            startD = datetime.strptime(start, "%Y-%m-%d").date()
            endD = datetime.strptime(end, "%Y-%m-%d").date()
        except:
            print("❌ Invalid date format. Use YYYY-MM-DD. (REQ-3.8)")
            return False

        if endD < startD:
            print("❌ End date cannot be before start date.")
            return False

        if min_age < 0 or max_age < min_age:
            print("❌ Invalid age range.")
            return False

        if capacity <= 0:
            print("❌ Capacity must be greater than zero.")
            return False

        # Overlap check (REQ 3.8)
        for sid, sess in self.sessions.items():
            if sess.instructor.lower() != instructor.lower():
                continue  # different instructor ok

            s1_start = datetime.strptime(sess.start_date, "%Y-%m-%d").date()
            s1_end = datetime.strptime(sess.end_date, "%Y-%m-%d").date()

            if not (endD < s1_start or startD > s1_end):
                print(f"❌ Overlapping schedule for instructor {instructor}. (REQ-3.8)")
                return False

        return True