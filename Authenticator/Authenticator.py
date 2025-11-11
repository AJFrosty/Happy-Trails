from DataManagement import DataManagement
from UserManagement.Administrator import Administrator
from UserManagement.Staff import Staff
from UserManagement.Parent import Parent
from UserManagement.User import User
import datetime
import hashlib
import getpass


class Authenticator:
    def __init__(self, fileManager: DataManagement):
        self.fileManager = fileManager

    def hashPassword(self, password: str) -> str:
        """Return SHA-256 hash of a password."""
        return hashlib.sha256(password.encode()).hexdigest()

    def logAction(self, action: str):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        record = f"{self.getID()}:{self.getName()}:{action}:{timestamp}\n"
        success = self.fileManager.write("session.txt", record, append=True)
        if not success:
            print("⚠️ Failed to log session.")

    def validateCredentials(self, username: str, password: str):
        users = self.fileManager.read("users.txt")
        hashedPw = self.hashPassword(password)

        for line in users:
            parts = line.strip().split(":")
            if len(parts) != 4:
                continue

            userId, role, uname, storedHash = parts
            if uname == username and storedHash == hashedPw:
                return userId, role, uname, storedHash

        return None
    
    def authenticate(self):
        users = self.fileManager.read("users.txt")
        username = input("Username: ").strip()
        password = getpass.getpass("Password: ").strip()
        hashedPw = hashlib.sha256(password.encode()).hexdigest()

        for line in users:
            parts = line.strip().split(":")
            if len(parts) != 4:
                continue

            userId, role, uname, storedHash = parts
            if uname == username and storedHash == hashedPw:
                print(f"✅ Login successful! Welcome, {uname} ({role})")

                if role == "Admin":
                    return Administrator(userId, uname, storedHash, role, self.fileManager, True)
                elif role == "Staff":
                    return Staff(userId, uname, storedHash, role, self.fileManager, True)
                elif role == "Parent":
                    return Parent(userId, uname, storedHash, role, self.fileManager, True)
                else:
                    print(f"⚠️ Unknown role '{role}', returning base User.")
                    return User(userId, uname, storedHash, role, self.fileManager, True)

        print("❌ Invalid username or password.")
        return None

    def login(self):
        print("\n--- LOGIN ---")
        username = input("Username: ").strip()
        password = getpass.getpass("Password: ").strip()

        result = self.validateCredentials(username, password)
        if not result:
            print("❌ Invalid username or password.")
            return None

        userId, role, uname, hashedPw = result
        print(f"✅ Login successful! Welcome, {uname} ({role})")

        #Return instance of appropriate subclass
        if role == "Admin":
            user = Administrator(userId, uname, hashedPw, role, self.fileManager)
            self.logAction(f"Admin logged In: '{uname}'")
        elif role == "Staff":
            user = Staff(userId, uname, hashedPw, role, self.fileManager)
            self.logAction(f"Staff logged In: '{uname}'")
        elif role == "Parent":
            user = Parent(userId, uname, hashedPw, role, self.fileManager)
            self.logAction(f"Parent logged In: '{uname}'")
        else:
            print(f"⚠️ Unknown role '{role}', returning base User.")
            user = User(userId, uname, hashedPw, role, self.fileManager)

        user.__authenticated = True
        return user
