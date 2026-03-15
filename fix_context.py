import os

backup_helper = "app/src/main/java/com/my/salah/tracker/app/BackupHelper.java"

if os.path.exists(backup_helper):
    with open(backup_helper, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "// --- DANGER ZONE START ---"
    end_marker = "// --- DANGER ZONE END ---"
    
    if start_marker in content and end_marker in content:
        start_idx = content.find(start_marker)
        end_idx = content.find(end_marker) + len(end_marker)
        
        danger_zone = content[start_idx:end_idx]
        
        # ভুল context কে সঠিক activity দিয়ে রিপ্লেস করা
        fixed_danger_zone = danger_zone.replace("context", "activity")
        
        new_content = content[:start_idx] + fixed_danger_zone + content[end_idx:]
        
        with open(backup_helper, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("✅ Error Fixed! 'context' কে 'activity' দিয়ে সফলভাবে ঠিক করা হয়েছে।")
    else:
        print("⚠️ Danger Zone ব্লকটি ফাইলে পাওয়া যায়নি।")
else:
    print("❌ BackupHelper.java পাওয়া যায়নি।")
