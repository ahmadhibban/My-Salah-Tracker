import os

# StatsHelper.kt ফাইলটি খোঁজা
file_path = "app/src/main/java/com/my/salah/tracker/app/StatsHelper.kt"

if os.path.exists(file_path):
    with open(file_path, "r") as f:
        data = f.read()

    # color = lC[i] কে setColor(lC[i]) দিয়ে রিপ্লেস করা
    if "color = lC[i]" in data:
        data = data.replace("color = lC[i]", "setColor(lC[i])")
        with open(file_path, "w") as f:
            f.write(data)
        print("✅ Fixed ColorStateList issue in StatsHelper.kt!")
    else:
        print("⚡ Issue already fixed or not found.")
else:
    print("❌ StatsHelper.kt not found in the expected path!")
