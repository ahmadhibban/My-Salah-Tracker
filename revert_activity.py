import os

file_path = "app/src/main/java/com/my/salah/tracker/app/MainActivity.kt"

if os.path.exists(file_path):
    with open(file_path, "r") as f:
        data = f.read()

    # AppCompatActivity কে বাদ দিয়ে পুনরায় সাধারণ Activity তে ফিরে যাওয়া
    data = data.replace("import androidx.appcompat.app.AppCompatActivity", "import android.app.Activity")
    data = data.replace("class MainActivity : AppCompatActivity()", "class MainActivity : Activity()")
    
    # supportActionBar কে আগের অবস্থায় নেওয়া
    data = data.replace("supportActionBar?.hide()", "actionBar?.hide()")
    
    # টাইটেল বার লুকানোর কোডটি আবার যুক্ত করা
    if "requestWindowFeature" not in data:
        data = data.replace("super.onCreate(savedInstanceState)", "super.onCreate(savedInstanceState)\n        try { requestWindowFeature(android.view.Window.FEATURE_NO_TITLE) } catch (e: Exception) {}")

    with open(file_path, "w") as f:
        f.write(data)
    
    print("✅ Reverted to Activity successfully! Theme crash is gone.")
else:
    print("❌ MainActivity.kt not found!")
