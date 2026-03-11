import os, re
java_file = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
with open(java_file, "r", encoding="utf-8") as f:
    mc = f.read()

restore_logic = """
        long savedDate = getIntent().getLongExtra("RESTORE_DATE", -1L);
        if(savedDate != -1L) {
            selectedDate[0] = sdf.format(new java.util.Date(savedDate));
            calendarViewPointer.setTimeInMillis(savedDate);
        }
"""
if "RESTORE_DATE" not in mc:
    mc = mc.replace("calendarViewPointer = Calendar.getInstance();", "calendarViewPointer = Calendar.getInstance();\n" + restore_logic)

intent_logic = """
        Intent intent = new Intent(MainActivity.this, MainActivity.class);
        try { intent.putExtra("RESTORE_DATE", sdf.parse(selectedDate[0]).getTime()); } catch(Exception e){}
        startActivity(intent);
"""
mc = mc.replace("startActivity(getIntent());", intent_logic.strip())

with open(java_file, "w", encoding="utf-8") as f:
    f.write(mc)
print("✅ ৪. Restart State Preserved!")
