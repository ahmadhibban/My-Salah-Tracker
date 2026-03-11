import os
import re

file_path = "app/src/main/java/com/my/salah/tracker/app/SalahDatabase.kt"
if os.path.exists(file_path):
    with open(file_path, "r") as f:
        data = f.read()

    if "allowMainThreadQueries()" not in data:
        # .build() এর আগে allowMainThreadQueries() বসানো
        data = re.sub(r'\.build\(\)', '.allowMainThreadQueries().build()', data)
        with open(file_path, "w") as f:
            f.write(data)
        print("✅ Room DB Main Thread permission granted!")
    else:
        print("⚡ Permission already exists.")
else:
    print("❌ SalahDatabase.kt not found!")
