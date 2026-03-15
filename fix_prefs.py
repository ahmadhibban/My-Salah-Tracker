import os

main_activity = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"

if os.path.exists(main_activity):
    with open(main_activity, "r", encoding="utf-8") as f:
        content = f.read()

    # ভুল ভ্যারিয়েবল 'prefs' কে 'sp' দিয়ে রিপ্লেস করা
    if "prefs.getString" in content or "prefs.getBoolean" in content:
        new_content = content.replace("prefs.getString", "sp.getString").replace("prefs.getBoolean", "sp.getBoolean")
        with open(main_activity, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("✅ Error Fixed! 'prefs' কে 'sp' দ্বারা সফলভাবে পরিবর্তন করা হয়েছে।")
    else:
        print("⚠️ কোডে কোনো ভুল 'prefs' পাওয়া যায়নি।")
else:
    print("❌ MainActivity পাওয়া যায়নি।")
