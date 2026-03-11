import os, re
java_file = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
with open(java_file, "r", encoding="utf-8") as f:
    mc = f.read()

# স্মুথ রিস্টার্ট মেথড তৈরি
if "private void smoothRestart()" not in mc:
    mc = mc.replace("public class MainActivity extends Activity {", "public class MainActivity extends Activity {\n    private void smoothRestart() { android.content.Intent intent = new android.content.Intent(this, MainActivity.class); intent.putExtra(\"RESTORE_DATE\", currentDate.getTimeInMillis()); startActivity(intent); overridePendingTransition(android.R.anim.fade_in, android.R.anim.fade_out); finish(); }")

# পুরনো সব recreate() মুছে নতুন স্মুথ রিস্টার্ট বসানো
mc = re.sub(r'\brecreate\(\)\s*;', 'smoothRestart();', mc)

# অ্যাপ চালুর সময় আগের তারিখ মনে রাখা
restore_logic = """
        long savedDate = getIntent().getLongExtra("RESTORE_DATE", -1L);
        if(savedDate != -1L) {
            currentDate.setTimeInMillis(savedDate);
        }
"""
if "RESTORE_DATE" not in mc.split("onCreate")[1][:2000]:
    mc = re.sub(r'(currentDate\s*=\s*Calendar\.getInstance\(\);)', r'\1\n' + restore_logic, mc)

with open(java_file, "w", encoding="utf-8") as f:
    f.write(mc)
print("✅ ২. Smooth Restart & Date Memory Applied!")
