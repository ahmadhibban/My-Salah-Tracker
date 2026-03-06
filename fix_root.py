import os

path = 'app/src/main/java/com/my/salah/tracker/app/StatsHelper.java'
if os.path.exists(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    old_text = 'ui.showSmartBanner(root, isBn?"সফল":"Success"'
    new_text = 'android.widget.FrameLayout root = activity.findViewById(android.R.id.content);\n            ui.showSmartBanner(root, isBn?"সফল":"Success"'

    if old_text in content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content.replace(old_text, new_text))
        print("✅ Error Fixed: 'root' variable declared successfully!")
    else:
        print("⚠️ Could not find the text. Already fixed?")
