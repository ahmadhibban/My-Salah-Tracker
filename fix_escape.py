f = 'app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
with open(f, 'r', encoding='utf-8') as file:
    c = file.read()

# পাইপ ভাঙার জন্য ডাবল ব্যাকস্ল্যাশ (\\|) নিশ্চিত করা
c = c.replace('s.split("\\|")', 's.split("\\\\|")')

with open(f, 'w', encoding='utf-8') as file:
    file.write(c)

print("✅ Escape character FIXED! You can build now.")
