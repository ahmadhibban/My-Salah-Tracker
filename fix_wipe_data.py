import os
import re

print("🛠️ এরর ফিক্স করা হচ্ছে...")

main_activity = None
for root, dirs, files in os.walk("app/src/main/java"):
    if "MainActivity.java" in files:
        main_activity = os.path.join(root, "MainActivity.java")
        break

if main_activity:
    with open(main_activity, "r", encoding="utf-8") as f:
        content = f.read()

    # ডাটা ডিলিট করার আসল প্রফেশনাল ফাংশন
    wipe_method = """
    private void showWipeDataDialog() {
        new android.app.AlertDialog.Builder(this)
            .setTitle("⚠️ Delete All Data")
            .setMessage("Are you sure you want to delete all data? This will wipe your history, settings, and start fresh. This action cannot be undone.")
            .setPositiveButton("Yes, Delete", (dialog, which) -> {
                android.widget.Toast.makeText(this, "Wiping all data...", android.widget.Toast.LENGTH_SHORT).show();
                if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.KITKAT) {
                    ((android.app.ActivityManager) getSystemService(android.content.Context.ACTIVITY_SERVICE)).clearApplicationUserData();
                }
            })
            .setNegativeButton("Cancel", null)
            .show();
    }
"""

    if "showWipeDataDialog" not in content:
        # ফাইলের একদম শেষের ব্র্যাকেটের আগে কোড বসানো
        content = re.sub(r'}\s*$', wipe_method + '\n}', content)
        
        with open(main_activity, "w", encoding="utf-8") as f:
            f.write(content)
        print("✅ showWipeDataDialog() সফলভাবে যুক্ত হয়েছে! এরর ফিক্সড!")
    else:
        print("⚠️ ফাংশনটি আগে থেকেই যুক্ত আছে।")
else:
    print("❌ MainActivity পাওয়া যায়নি।")
