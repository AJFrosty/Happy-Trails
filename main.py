from DataManagement.DataManagement import DataManagement
from Authenticator.Authenticator import Authenticator
from SessionManagement.Sessions import SessionManager

def main():
    while True:
        fileManager = DataManagement('Data/')
        auth = Authenticator(fileManager)
        SessMgmr = SessionManager(fileManager)
        
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
                    while True:
                        print("\n====== SESSION MANAGEMENT DASHBOARD ======")
                        print("1. Create Session")
                        print("2. Edit Session")
                        print("3. Delete Session")
                        print("4. View Sessions")
                        print("5. Add Camper to Session")
                        print("6. Return to Admin Menu")
                        print("==========================================")

                        choice = input("Choose an option: ").strip()

                        if choice == "1":
                            SessMgmr.createSession(currentUser)

                        elif choice == "2":
                            SessMgmr.editSession(currentUser)

                        elif choice == "3":
                            SessMgmr.deleteSession(currentUser)

                        elif choice == "4":
                            SessMgmr.displaySessions()

                        elif choice == "5":
                            SessMgmr.addCamperToSessionInteractive()

                        elif choice == "6":
                            print("⬅ Returning to Admin Menu...")
                            return
                        else:
                            print("Invalid option. Please try again.")
                            
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