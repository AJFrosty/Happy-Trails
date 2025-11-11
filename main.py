from DataManagement.DataManagement import DataManagement
from Authenticator.Authenticator import Authenticator

def main():
    while True:
        fileManager = DataManagement('Data/')
        auth = Authenticator(fileManager)
        
        currentUser = auth.authenticate()
        
        if not currentUser:
            print("Exiting program.")
            return
        
        while True:
            currentUser.showDashboard()
            
            choice = input("Enter your choice: ").strip()
            
            if currentUser.getRole() == "Admin":
                if choice == "1":
                    currentUser.register()
                elif choice == "2":
                    print("Edit/Delete Users (feature to implement)")
                elif choice == "3":
                    print("Generate Reports (feature to implement)")
                elif choice == "4":
                    print("Backup/Restore Data (feature to implement)")
                elif choice == "5":
                    print("Logging out...")
                    currentUser = None
                    break
                else:
                    print("Invalid choice.")
            
            elif currentUser.getRole() == "Staff":
                if choice == "1":
                    print("View Camper Info (feature to implement)")
                elif choice == "2":
                    print("Record Attendance (feature to implement)")
                elif choice == "3":
                    print("View Attendance Logs (feature to implement)")
                elif choice == "4":
                    currentUser.register()
                elif choice == "5":
                    print("Logging out...")
                    break
                else:
                    print("Invalid choice.")
            
            elif currentUser.getRole() == "Parent":
                if choice == "1":
                    currentUser.registerCamper()
                elif choice == "2":
                    print("Update Camper Info (feature to implement)")
                elif choice == "3":
                    print("Enroll Camper in Session (feature to implement)")
                elif choice == "4":
                    print("Logging out...")
                    break
                else:
                    print("Invalid choice.")
            
            else:
                print("Unknown role. Exiting.")
                break

main()