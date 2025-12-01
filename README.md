# 🏕️ **Happy Trails Summer Camp Registration System**

### **User Guide (Console Version)**

Welcome to **Happy Trails**, a console-based summer camp administration and registration system.
This guide provides step-by-step instructions for **Admins**, **Parents**, and **Staff** on how to use the system through **main.py**.

---

# 📌 **1. Getting Started**

### ▶️ **Launching the System**

Run the program using:

```bash
python main.py
```

You will be presented with the **Login Screen**.

---

# 🔐 **2. Logging In**

At startup, the system asks for:

```
Enter username:
Enter password:
```

### ⭐ Default Admin Login

Use the built-in credentials:

| Role  | Username | Password         |
| ----- | -------- | ---------------- |
| Admin | `admin`  | `mypassword123!` |

If login is successful, you will be taken to your **role-specific dashboard**.

---

# 👪 **3. Parent User Guide**

When a Parent logs in, they see:

```
--- PARENT DASHBOARD ---
1. Register New Camper
2. Update Camper Details
3. Enroll Camper in Session
4. Logout
```

---

## **3.1 Register New Camper**

Parents can register their children (ages **6–17**).

You will be asked to enter:

* First & Last Name
* Age
* Date of Birth (YYYY-MM-DD)
* Medical Info (optional)

The system validates:

✔ Age is 6–17
✔ Name contains first and last
✔ Date of birth matches entered age
✔ Camper is not a duplicate

If successful, the camper is added to **camper.txt**.

---

## **3.2 Update Camper Details**

Parents may update:

* Name
* Age
* DOB
* Medical Info

⚠ **Parents can only update their own campers.**

If the camper ID does not belong to the logged-in parent:

```
❌ Camper not found or you do not have permission to update this camper.
```

---

## **3.3 Enroll Camper in a Session**

Parents can select from available sessions.
The system checks:

✔ Camper fits age range
✔ Session has remaining capacity
✔ Session exists

If successful:

```
Camper added to session S100001. Spots remaining: 4.
```

---

## **3.4 Logout**

Ends parent session and returns to login screen.

---

# 🛠️ **4. Admin User Guide**

Admin Dashboard:

```
--- ADMIN DASHBOARD ---
1. Register an Account
2. Delete A User
3. Edit A User
4. Generate Reports
5. Backup/Restore Data
6. Session Management Dashboard
7. View Camper Info
8. Logout
```

Admins have **full system privileges**.

---

## **4.1 Register an Account**

Admins can create:

* Admin
* Staff
* Parent

Inputs:

* Role
* Username
* Password (validated: length, special characters, case)

Passwords are saved hashed in users.txt.

---

## **4.2 Delete a User**

Admins can delete any Staff or Parent (not campers).

Input the **User ID**:

```
Enter User ID to delete:
```

If the ID does not exist:

```
❌ User not found.
```

---

## **4.3 Edit a User**

Admins may change:

* Username
* Password
* Role (assigning new ID when role changes)

Password validation is enforced.

---

## **4.4 Generate Reports**

Admins can generate:

### ✔ User Reports

Filter by role or username.

### ✔ Camper Reports

Filter by parent ID or age.

### ✔ Session Reports

Filter by instructor or age range.

Reports are exported as:

```
users-12.01.25.txt
sessions-12.01.25.txt
camper-12.01.25.txt
```

---

## **4.5 Backup / Restore Data**

Creates `.bak.txt` versions of:

* users
* camper
* log
* session
* summary

If backup exists, it is replaced.

---

## **4.6 Session Management Dashboard**

Takes Admin to:

```
--- SESSION MANAGEMENT ---
1. Create Session
2. Edit Session
3. Delete Session
4. View Sessions
5. Return
```

Admin can create, edit, delete, and view sessions.

---

## **4.7 View Camper Info**

Admins can view **all campers** and their details.

---

## **4.8 Logout**

Returns to login menu.

---

# 👷 **5. Staff User Guide**

Staff Dashboard:

```
--- STAFF DASHBOARD ---
1. View Camper Info
2. Log Attendance for Assigned Sessions
3. View Attendance Records
4. Register Members
5. Logout
```

---

## **5.1 View Camper Info**

Staff can view **all registered campers**.

---

## **5.2 Log Attendance (Release #2 Feature)**

Staff can record:

* Present (P)
* Absent (A)

Attendance is saved to **attendance.txt**:

```
CMP0004, Sarah Jones, Present, 2025-01-14 09:30
```

---

## **5.3 View Attendance Records**

Lists all entries in attendance.txt.

If empty:

```
No attendance records found.
```

---

## **5.4 Register Members**

Staff may register **Parents** only.

They cannot create Admins or Staff.

---

## **5.5 Logout**

Ends staff session.

---

# 📤 **6. File Structure Overview**

| File           | Purpose             |
| -------------- | ------------------- |
| users.txt      | All system users    |
| camper.txt     | Camper records      |
| sessions.txt   | Session listings    |
| log.txt        | Audit logs          |
| attendance.txt | Attendance logs     |
| summary.txt    | Data summary export |
| Data-Bak/      | Backups directory   |

---
