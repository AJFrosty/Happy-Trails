import csv
from datetime import datetime, date

PASSCODE = "111"
DB_FILE = "campers.csv"
FIELDS = ["id","first_name","last_name","dob","gender","medical_notes","em_contact_name","em_contact_phone"]
SESSIONS = [
    {"name": "Junior (6-8)", "min_age": 6, "max_age": 8},
    {"name": "Intermediate (9-11)", "min_age": 9, "max_age": 11},
    {"name": "Senior (12-15)", "min_age": 12, "max_age": 15},
]
MIN_REG_AGE = 6
MAX_REG_AGE = 15

class CamperRegistry:
    def __init__(self, filename=DB_FILE):
        self.filename = filename
        self.campers = []
        self._load()

    def _load(self):
        try:
            with open(self.filename, newline="", encoding="utf-8") as f:
                rdr = csv.DictReader(f)
                for r in rdr:
                    self.campers.append(r)
        except Exception:
            self.campers = []

    def _save(self):
        with open(self.filename, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS)
            w.writeheader()
            for c in self.campers:
                w.writerow(c)

    def _next_id(self):
        if not self.campers:
            return "1"
        ids = []
        for c in self.campers:
            try: ids.append(int(c.get("id","0")))
            except: ids.append(0)
        return str(max(ids)+1)

    def calculate_age(self, dob_str):
        try:
            d = datetime.strptime(dob_str, "%Y-%m-%d").date()
        except:
            return None
        today = date.today()
        age = today.year - d.year - ((today.month, today.day) < (d.month, d.day))
        return age

    def validate(self, c):
        errs = []
        fn = c.get("first_name","").strip()
        ln = c.get("last_name","").strip()
        dob = c.get("dob","").strip()
        emn = c.get("em_contact_name","").strip()
        emp = c.get("em_contact_phone","").strip()
        if not fn or not ln:
            errs.append("First and last name required")
        if not dob:
            errs.append("Date of birth required")
        else:
            age = self.calculate_age(dob)
            if age is None:
                errs.append("Invalid DOB format (use YYYY-MM-DD)")
            elif age < MIN_REG_AGE or age > MAX_REG_AGE:
                errs.append(f"Age {age} out of range ({MIN_REG_AGE}-{MAX_REG_AGE})")
        if not emn or not emp:
            errs.append("Emergency contact info required")
        if "medical_notes" not in c:
            errs.append("Medical notes required (use 'None' if none)")
        for ex in self.campers:
            if ex["first_name"].lower()==fn.lower() and ex["last_name"].lower()==ln.lower() and ex["dob"]==dob:
                errs.append("Duplicate camper already exists")
        return errs

    def add_camper(self, first, last, dob, gender, med, emn, emp):
        cam = {
            "id": self._next_id(),
            "first_name": first.strip(),
            "last_name": last.strip(),
            "dob": dob.strip(),
            "gender": gender.strip(),
            "medical_notes": med.strip(),
            "em_contact_name": emn.strip(),
            "em_contact_phone": emp.strip()
        }
        errs = self.validate(cam)
        if errs: return False, errs
        self.campers.append(cam)
        self._save()
        return True, cam

    def find_by_id(self, cid):
        for c in self.campers:
            if c["id"] == str(cid): return c
        return None

    def find_by_name(self, term):
        t = term.lower()
        return [c for c in self.campers if t in (c["first_name"]+" "+c["last_name"]).lower()]

    def eligible_sessions(self, dob):
        a = self.calculate_age(dob)
        if a is None: return []
        return [s["name"] for s in SESSIONS if s["min_age"]<=a<=s["max_age"]]

    def filter_by_eligibility(self, session_name):
        res=[]
        for c in self.campers:
            a=self.calculate_age(c["dob"])
            if a is None: continue
            for s in SESSIONS:
                if s["name"].lower()==session_name.lower() and s["min_age"]<=a<=s["max_age"]:
                    res.append(c)
        return res

    def update(self, cid, **kwargs):
        c = self.find_by_id(cid)
        if not c: return False, ["Camper not found"]
        for k,v in kwargs.items():
            if k in FIELDS and k!="id" and v.strip()!="":
                c[k] = v.strip()
        errs = self.validate(c)
        if errs: return False, errs
        self._save()
        return True, c

    def delete(self, cid):
        c = self.find_by_id(cid)
        if not c: return False
        self.campers.remove(c)
        self._save()
        return True

def clear(): print("\n"*3)
def pause(): input("Press Enter to continue...")
def prompt(t): return input(t).strip()

def print_table(rows, heads):
    if not rows:
        print("No records.")
        return
    widths = [len(h) for h in heads]
    for r in rows:
        for i,h in enumerate(heads):
            widths[i] = max(widths[i], len(str(r.get(h,""))))
    line = " | ".join(h.ljust(widths[i]) for i,h in enumerate(heads))
    print(line)
    print("-"*len(line))
    for r in rows:
        print(" | ".join(str(r.get(h,"")).ljust(widths[i]) for i,h in enumerate(heads)))

def authorize():
    code = prompt("Enter passcode: ")
    return code == PASSCODE

def main():
    reg = CamperRegistry()
    while True:
        clear()
        print("Camper Registry and Eligibility Management")
        print("1) Register new camper")
        print("2) View all campers (passcode required)")
        print("3) Search campers by name")
        print("4) Filter campers by eligibility or ID")
        print("5) Update camper information (passcode required)")
        print("6) Delete camper (passcode required)")
        print("7) Exit")
        choice = prompt("Select option: ")
        if choice=="1":
            f=prompt("First name: ")
            l=prompt("Last name: ")
            d=prompt("Date of birth (YYYY-MM-DD): ")
            g=prompt("Gender: ")
            m=prompt("Medical notes (None if none): ")
            en=prompt("Emergency contact name: ")
            ep=prompt("Emergency contact phone: ")
            ok,res=reg.add_camper(f,l,d,g,m,en,ep)
            if ok: print("Registered successfully with ID:",res["id"])
            else:
                print("Errors:")
                for e in res: print("-",e)
            pause()
        elif choice=="2":
            if not authorize():
                print("Unauthorized access.")
                pause()
                continue
            rows=reg.campers
            print_table(rows,["id","first_name","last_name","dob","gender"])
            pause()
        elif choice=="3":
            n=prompt("Enter name or part of name: ")
            res=reg.find_by_name(n)
            print_table(res,["id","first_name","last_name","dob","gender"])
            pause()
        elif choice=="4":
            print("1) Filter by eligibility")
            print("2) Filter by ID")
            s=prompt("Choose: ")
            if s=="1":
                sn=prompt("Enter session name: ")
                res=reg.filter_by_eligibility(sn)
                print_table(res,["id","first_name","last_name","dob"])
            elif s=="2":
                cid=prompt("Enter ID: ")
                c=reg.find_by_id(cid)
                if not c: print("Not found.")
                else:
                    print_table([c],["id","first_name","last_name","dob","gender","medical_notes"])
            pause()
        elif choice=="5":
            if not authorize():
                print("Unauthorized access.")
                pause()
                continue
            cid=prompt("Enter ID: ")
            c=reg.find_by_id(cid)
            if not c:
                print("Camper not found.")
                pause()
                continue
            print("Leave blank to keep current.")
            f=prompt(f"First name [{c['first_name']}]: ") or c["first_name"]
            l=prompt(f"Last name [{c['last_name']}]: ") or c["last_name"]
            d=prompt(f"DOB [{c['dob']}]: ") or c["dob"]
            g=prompt(f"Gender [{c['gender']}]: ") or c["gender"]
            m=prompt(f"Medical notes [{c['medical_notes']}]: ") or c["medical_notes"]
            en=prompt(f"Emergency contact name [{c['em_contact_name']}]: ") or c["em_contact_name"]
            ep=prompt(f"Emergency contact phone [{c['em_contact_phone']}]: ") or c["em_contact_phone"]
            ok,res=reg.update(cid,first_name=f,last_name=l,dob=d,gender=g,medical_notes=m,em_contact_name=en,em_contact_phone=ep)
            if ok: print("Updated successfully.")
            else:
                print("Errors:")
                for e in res: print("-",e)
            pause()
        elif choice=="6":
            if not authorize():
                print("Unauthorized access.")
                pause()
                continue
            cid=prompt("Enter ID to delete: ")
            if reg.delete(cid): print("Deleted.")
            else: print("Not found.")
            pause()
        elif choice=="7":
            break
        else:
            print("Invalid option.")
            pause()

if __name__=="__main__":
    main()
