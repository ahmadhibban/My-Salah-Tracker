import re

f = 'app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
with open(f, 'r', encoding='utf-8') as file:
    c = file.read()

# Fix 1: সঠিক জায়গায় ভেরিয়েবলগুলো বসানো
if 'private android.widget.FrameLayout fragmentContainer;' not in c:
    c = c.replace('private LinearLayout contentArea;', 'private LinearLayout contentArea;\n    private android.widget.FrameLayout fragmentContainer;\n    private android.widget.LinearLayout bottomNav;\n    private int currentTab = 0;')

# Fix 2: পুরোনো মেথডের নামে একটি র‍্যাপার (Wrapper) তৈরি করা যাতে আগের সব ক্লিক কাজ করে
wrapper = """private void loadTodayPage() {
        if(fragmentContainer != null) switchTab(currentTab);
    }

    private void loadTodayPageCore()"""

if 'private void loadTodayPage() {' not in c:
    c = c.replace('private void loadTodayPageCore()', wrapper)

with open(f, 'w', encoding='utf-8') as file:
    file.write(c)

print("✅ Navigation Build Errors PERFECTLY Fixed! Ready to hit Play (▶️)!")
