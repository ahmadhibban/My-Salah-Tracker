import os

base_dir = "app/src/main/java/com/my/salah/tracker/app"
duplicates = ["FastingFragment.java", "QuranFragment.java", "SalahFragment.java", "StatsFragment.java", "ZikrFragment.java"]

for file_name in duplicates:
    file_path = os.path.join(base_dir, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"✔ Deleted misplaced old file: {file_name}")

print("🚀 DUPLICATES CLEARED PERFECTLY! READY TO BUILD.")
