import os, re

java_file = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"

if os.path.exists(java_file):
    with open(java_file, "r", encoding="utf-8") as f:
        mc = f.read()

    # ১. ভবিষ্যতের দিনগুলোকে জোর করে দৃশ্যমান করা (সব ধরনের লুকানো কোড মুছে ফেলা)
    mc = mc.replace("t.setTextColor(android.graphics.Color.TRANSPARENT);", 't.setTextColor(android.graphics.Color.parseColor("#94A3B8"));')
    mc = mc.replace("t.setTextColor(Color.TRANSPARENT);", 't.setTextColor(android.graphics.Color.parseColor("#94A3B8"));')
    mc = mc.replace("t.setVisibility(android.view.View.INVISIBLE);", "t.setVisibility(android.view.View.VISIBLE);")
    mc = mc.replace("t.setVisibility(View.INVISIBLE);", "t.setVisibility(android.view.View.VISIBLE);")
    mc = mc.replace("t.setAlpha(0f);", "t.setAlpha(1f);")
    mc = mc.replace("t.setAlpha(0.0f);", "t.setAlpha(1f);")

    # ২. রানটাইম ইনজেক্টর (অ্যাপ রান হওয়ার সময় জোর করে সাইজ ও গ্যাপ ঠিক করবে)
    injector = """
        topBtns.post(new Runnable() {
            @Override
            public void run() {
                try {
                    // বাটন দুটোর কন্টেইনারকে ধরে দুই পাশ থেকে ১২ ডিপি চাপ দেওয়া এবং ওপরে-নিচে ২৪ ডিপি বিশাল গ্যাপ দেওয়া
                    android.view.ViewGroup.MarginLayoutParams tbLp = (android.view.ViewGroup.MarginLayoutParams) topBtns.getLayoutParams();
                    if(tbLp != null) {
                        tbLp.setMargins((int)(12*DENSITY), (int)(24*DENSITY), (int)(12*DENSITY), (int)(24*DENSITY));
                        topBtns.setLayoutParams(tbLp);
                    }
                } catch(Exception e){}
            }
        });
    """
    
    # আগের কোনো ইনজেক্টর থাকলে সেটা মুছে ফেলা
    mc = re.sub(r'topBtns\.post\(new Runnable\(\).*?\}\);', '', mc, flags=re.DOTALL)
    
    # নতুন ইনজেক্টর বসানো
    if "topBtns.addView(todayBtn);" in mc:
        mc = mc.replace("topBtns.addView(todayBtn);", "topBtns.addView(todayBtn);\n" + injector)

    with open(java_file, "w", encoding="utf-8") as f:
        f.write(mc)
    print("✔ RUNTIME INJECTOR APPLIED SUCCESSFULLY!")
else:
    print("❌ FILE NOT FOUND!")
