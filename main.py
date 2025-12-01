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
                    currentUser.deleteUserByID()
                elif choice == "3":
                    currentUser.editUser()
                elif choice == "4":
                    currentUser.generateReports()
                elif choice == "5":
                    fileManager.backupAll()
                elif choice == "6":
                    print("Session Management Dashboard(Create/Edit/Delete)")
                elif choice == "7":
                    currentUser.viewCamperInfo()
                elif choice == "8":
                    print("Logging out...")
                    currentUser = None
                    break
                else:
                    print("Invalid choice.")
            
            elif currentUser.getRole() == "Staff":
                if choice == "1":
                    currentUser.viewCamperInfo()
                elif choice == "2":
                    currentUser.recordAttendance()
                elif choice == "3":
                    currentUser.viewAttendanceLogs()
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
                    currentUser.updateCamper()
                elif choice == "3":
                    currentUser.enrollCamperInSession()
                elif choice == "4":
                    print("Logging out...")
                    break
                else:
                    print("Invalid choice.")
            
            else:
                print("Unknown role. Exiting.")
                break

main()