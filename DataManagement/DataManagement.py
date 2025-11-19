import os
import threading
import datetime
import shutil

class DataManagement:
    def __init__(self, baseDirectory="Data/", backUpFolder="Data-Bak/", reportsFolder = "Reports/"):
        self.data_files = [
            "camper.txt",
            "log.txt",
            "session.txt",
            "summary.txt",
            "users.txt"
        ]
        self.baseDirectory = baseDirectory
        self.backUpFolder = backUpFolder
        self.reportsFolder = reportsFolder
        self.lock = threading.Lock()
        self.ensureDirectory()
    
    def logAction(self, id, name, action: str):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        record = f"{id}:{name}:{action}:{timestamp}\n"
        success = self.write("log.txt", record, append=True)
        if not success:
            print("⚠️ Failed to log session.")

    def ensureDirectory(self):
        if not os.path.exists(self.baseDirectory):
            os.makedirs(self.baseDirectory)
            print(f"📁 Created base directory: {self.baseDirectory}")
        
        if not os.path.exists(self.backUpFolder):
            os.makedirs(self.backUpFolder)
            print(f"📁 Created backUp directory: {self.baseDirectory}")
        
        if not os.path.exists(self.reportsFolder):
            os.makedirs(self.reportsFolder)
            print(f"📁 Created reports directory: {self.reportsFolder}")

    def getFilePath(self, filename):
        return os.path.join(self.baseDirectory, filename)
    
    def read(self, filename):
        path = self.getFilePath(filename)
        self.ensureFileExists(path)

        try:
            with open(path, "r", encoding="utf-8") as file:
                lines = file.readlines()
            return [line.strip() for line in lines if line.strip()]
        
        except Exception as e:
            print(f"⚠️ Error reading {filename}: {e}")
            self.recoverCorruptedFile(path)
            return []
    
    def write(self, filename, data, append=False):
        path = self.getFilePath(filename)
        self.ensureFileExists(path)
        mode = "a" if append else "w"

        with self.lock:
            try:
                with open(path, mode, encoding="utf-8") as file:
                    if isinstance(data, list):
                        for line in data:
                            file.write(line if line.endswith("\n") else f"{line}\n")
                    else:
                        file.write(data if data.endswith("\n") else f"{data}\n")
                return True
            except Exception as e:
                print(f"❌ Write failed for {filename}: {e}")
                return False

    def ensureFileExists(self, path):
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                pass
            print(f"📝 Created new data file: {os.path.basename(path)}")
    
    def recoverCorruptedFile(self, path):
        corruptedPath = path + ".corrupted"
        try:
            os.rename(path, corruptedPath)
            print(f"⚠️ Corrupted file renamed to {os.path.basename(corruptedPath)}.")
            self.ensureFileExists(path)
            print(f"✅ New clean file created: {os.path.basename(path)}")
        except Exception as e:
            print(f"❌ Recovery failed for {path}: {e}")
    
    def exportSummary(self, summaryFile="summary.txt"):
        summaryPath = self.getFilePath(summaryFile)
        with self.lock:
            try:
                with open(summaryPath, "w", encoding="utf-8") as summary:
                    summary.write("==== SYSTEM DATA SUMMARY ====\n\n")
                    for filename in os.listdir(self.baseDirectory):
                        if filename == summaryFile:
                            continue
                        path = self.getFilePath(filename)
                        summary.write(f"--- {filename} ---\n")
                        try:
                            with open(path, "r", encoding="utf-8") as f:
                                summary.writelines(f.readlines())
                        except Exception as e:
                            summary.write(f"[Error reading {filename}: {e}]\n")
                        summary.write("\n")
                print(f"✅ Summary exported successfully to {summaryFile}.")
                return True
            except Exception as e:
                print(f"❌ Export summary failed: {e}")
                return False
    
    def createReport(self, sourceFilename, filteredLines):
        dateStr = datetime.datetime.now().strftime("%m.%d.%y")
        baseName = os.path.splitext(sourceFilename)[0]
        reportName = f"{baseName}-{dateStr}.txt"

        self.write(reportName, filteredLines, append=False)
        print(f"📄 Report generated: {reportName}")

        return reportName
    
    def filterCampers(
        self,
        camper_id=None,
        parent_id=None,
        admin_id=None,
        staff_id=None,
        name=None,
        min_age=None,
        max_age=None,
        eligible_only=False,
        logic="AND"
    ):
        records = self.read("camper.txt")
        results = []

        for line in records:
            parts = line.split(":")
            if len(parts) < 5:
                continue

            c_id, c_name, c_age, c_parent, c_med = parts
            c_age = int(c_age)

            checks = []

            if camper_id:
                checks.append(c_id == camper_id)

            if parent_id:
                checks.append(c_parent == parent_id)

            if name:
                checks.append(name.lower() in c_name.lower())

            if min_age is not None:
                checks.append(c_age >= min_age)

            if max_age is not None:
                checks.append(c_age <= max_age)

            if eligible_only:
                checks.append(6 <= c_age <= 17)

            #Apply logic
            if logic == "AND" and all(checks):
                results.append(line)
            elif logic == "OR" and any(checks):
                results.append(line)

        return results
    
    def backupAll(self):
        print("\n📁 Starting backup process...")

        for filename in self.data_files:
            source_path = os.path.join(self.baseDirectory, filename)
            backup_name = filename.replace(".txt", ".bak.txt")
            backup_path = os.path.join(self.backUpFolder, backup_name)

            if not os.path.exists(source_path):
                print(f"⚠️ Skipped missing file: {filename}")
                continue

            if os.path.exists(backup_path):
                os.remove(backup_path)

            shutil.copyfile(source_path, backup_path)

            print(f"✅ Backed up {filename} → {backup_name}")

        print("🎉 Backup completed successfully.\n")