from session_module import (
    SessionService,
    Session,
    parse_age_label,
    _parse_date,
)

class AdminConsole:
    def __init__(self) -> None:
        self.service = SessionService()
        self.is_admin = False
        self.current_user = "guest"

    def run(self) -> None:
        self._login()
        while True:
            self._show_dashboard()
            choice = input("Select option: ").strip()
            if choice == "1":
                self._manage_sessions()
            elif choice == "2":
                self._generate_reports()
            elif choice.lower() == "q":
                print("Goodbye!")
                return
            else:
                print("Invalid option.")
            print("[Done] Returning to dashboard...\\n")

    def _login(self) -> None:
        print("=== HT Summer Camp - Login ===")
        user = input("Username: ").strip()
        pw = input("Password: ").strip()
        if user.lower() == "admin" and pw == "admin123":
            self.is_admin = True
            self.current_user = "admin"
            print("[Success] Authenticated as ADMIN.")
        else:
            self.is_admin = False
            self.current_user = user or "guest"
            print("[Info] Read-only mode enabled (non-admin).")

    def _show_dashboard(self) -> None:
        print("\\n=== Admin Dashboard ===")
        m = self.service.compute_metrics()
        print(f"Sessions: {m.total_sessions} | Upcoming: {m.upcoming_sessions} | Capacity Used: {m.total_enrolled}/{m.total_capacity}")
        print("1) Manage Sessions")
        print("2) Generate Reports")
        print("Q) Quit")

    def _manage_sessions(self) -> None:
        while True:
            print("\\n=== Manage Sessions ===")
            print("A) List all (real time)")
            print("B) Filter/Sort")
            if self.is_admin:
                print("C) Create session")
                print("D) Edit session")
                print("E) Delete session")
                print("F) Register a camper")
                print("G) Cancel a registration")
            else:
                print("[Read-only] Create/Edit/Delete/Registration disabled.")
            print("X) Back")

            c = input("Choice: ").strip().upper()
            if c == "A":
                self._list_sessions()
            elif c == "B":
                self._filter_sort_flow()
            elif c == "C" and self._require_admin():
                self._create_flow()
            elif c == "D" and self._require_admin():
                self._edit_flow()
            elif c == "E" and self._require_admin():
                self._delete_flow()
            elif c == "F" and self._require_admin():
                self._register_flow()
            elif c == "G" and self._require_admin():
                self._cancel_flow()
            elif c == "X":
                return
            else:
                print("Invalid option.")

    def _require_admin(self) -> bool:
        if not self.is_admin:
            print("[Denied] Read-only mode.")
            return False
        return True

    def _list_sessions(self) -> None:
        items = self.service.list_sessions()
        if not items:
            print("(No sessions)")
            return
        for s in items:
            print(f"[{s.id}] {s.name} | {s.activity_type} | {s.start_date}–{s.end_date} | {s.age_group_label} ({s.min_age}-{s.max_age}) | cap {s.capacity} | spots {s.spots_available} | {s.instructor}")

    def _filter_sort_flow(self) -> None:
        d = input("Filter by date (YYYY-MM-DD or empty): ").strip()
        ag = input("Filter by age group label or empty: ").strip()
        inst = input("Filter by instructor or empty: ").strip()
        act = input("Filter by activity type or empty: ").strip()
        sort = input("Sort by (date|age|instructor|activity|capacity|none): ").strip().lower() or "none"
        items = self.service.filter_and_sort(d, ag, inst, act, sort)
        if not items:
            print("(No results)")
            return
        for s in items:
            print(f"[{s.id}] {s.name} | {s.activity_type} | {s.start_date}–{s.end_date} | {s.age_group_label} ({s.min_age}-{s.max_age}) | cap {s.capacity} | spots {s.spots_available} | {s.instructor}")

    def _create_flow(self) -> None:
        name = input("Name: ").strip()
        act_type = input("Activity Type: ").strip()
        start = input("Start Date (YYYY-MM-DD): ").strip()
        end = input("End Date (YYYY-MM-DD): ").strip()
        age_label = input("Age Group Label (e.g., 8-10): ").strip()
        min_age, max_age = parse_age_label(age_label)
        capacity = int(input("Capacity: ").strip())
        instructor = input("Instructor: ").strip()

        s = Session(
            id="",
            name=name,
            activity_type=act_type,
            start_date=_parse_date(start),
            end_date=_parse_date(end),
            age_group_label=age_label,
            min_age=min_age,
            max_age=max_age,
            capacity=capacity,
            spots_available=capacity,
            instructor=instructor,
        )
        res = self.service.create_session(s, self.current_user)
        print(res.message)

    def _edit_flow(self) -> None:
        sid = input("Enter Session ID to edit: ").strip()
        print("Leave blank to keep existing value.")
        fields = {}
        name = input("Name: ").strip()
        if name: fields["name"] = name
        act = input("Activity Type: ").strip()
        if act: fields["activity_type"] = act
        sd = input("Start Date (YYYY-MM-DD): ").strip()
        if sd: fields["start_date"] = sd
        ed = input("End Date (YYYY-MM-DD): ").strip()
        if ed: fields["end_date"] = ed
        ag = input("Age Group Label (e.g., 8-10): ").strip()
        if ag:
            fields["age_group_label"] = ag
            mn_mx = parse_age_label(ag)
            fields["min_age"] = str(mn_mx[0])
            fields["max_age"] = str(mn_mx[1])
        min_a = input("Min Age: ").strip()
        if min_a: fields["min_age"] = min_a
        max_a = input("Max Age: ").strip()
        if max_a: fields["max_age"] = max_a
        cap = input("Capacity: ").strip()
        if cap: fields["capacity"] = cap
        spots = input("Spots Available: ").strip()
        if spots: fields["spots_available"] = spots
        inst = input("Instructor: ").strip()
        if inst: fields["instructor"] = inst

        res = self.service.edit_session(sid, fields, self.current_user)
        print(res.message)

    def _delete_flow(self) -> None:
        sid = input("Enter Session ID to delete: ").strip()
        res = self.service.delete_session(sid, self.current_user)
        print(res.message)

    def _register_flow(self) -> None:
        sid = input("Session ID: ").strip()
        cid = input("Camper ID: ").strip()
        res = self.service.register_camper(sid, cid, self.current_user)
        print(res.message)

    def _cancel_flow(self) -> None:
        sid = input("Session ID: ").strip()
        cid = input("Camper ID: ").strip()
        res = self.service.cancel_registration(sid, cid, self.current_user)
        print(res.message)

    def _generate_reports(self) -> None:
        print(self.service.generate_summary(self.current_user))


if __name__ == "__main__":
    AdminConsole().run()
