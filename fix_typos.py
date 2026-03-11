import os

path = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# কাটা পড়া শব্দগুলো (mainLayou; এবং lis;) মুছে ফেলা হচ্ছে
content = content.replace("mainLayout.setOrientation(LinearLayout.VERTICAL); mainLayou;", "mainLayout.setOrientation(LinearLayout.VERTICAL);")
content = content.replace("list.setOrientation(LinearLayout.VERTICAL); lis;", "list.setOrientation(LinearLayout.VERTICAL);")

# যদি অন্য কোথাও থেকে থাকে, তার জন্য সেফটি
content = content.replace("mainLayou;", "")
content = content.replace(" lis;", "")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Syntax errors (mainLayou, lis) removed successfully!")
