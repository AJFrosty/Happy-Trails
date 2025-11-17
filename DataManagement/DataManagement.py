import os
import threading
import datetime

class DataManagement:
    def __init__(self, baseDirectory="Data/"):
        self.baseDirectory = baseDirectory
        self.lock = threading.Lock()
        self.ensureDirectory()
    
    def logAction(self, id, name, action: str):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        record = f"{id}:{name}:{action}:{timestamp}\n"
        success = self.write("session.txt", record, append=True)
        if not success:
            print("⚠️ Failed to log session.")

    def ensureDirectory(self):
        if not os.path.exists(self.baseDirectory):
            os.makedirs(self.baseDirectory)
            print(f"📁 Created base directory: {self.baseDirectory}")

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