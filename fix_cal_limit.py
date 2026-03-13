import os, re
for r, d, f in os.walk('.'):
    if 'MainActivity.java' in f and 'build' not in r:
        p = os.path.join(r, 'MainActivity.java')
        with open(p, 'r', encoding='utf-8') as file: c = file.read()
        nav_logic = """java.util.Calendar tCal = java.util.Calendar.getInstance(); int tY = tCal.get(java.util.Calendar.YEAR), tM = tCal.get(java.util.Calendar.MONTH) + 1, tD = tCal.get(java.util.Calendar.DAY_OF_MONTH);
        int tBY = tY - 593; int tBM = 0; if (tM==4 && tD>=14) {tBM=0;} else if(tM==4) {tBM=11; tBY--;} else if (tM==5 && tD<=14) {tBM=0;} else if(tM==5) {tBM=1;} else if (tM==6 && tD<=14) {tBM=1;} else if(tM==6) {tBM=2;} else if (tM==7 && tD<=15) {tBM=2;} else if(tM==7) {tBM=3;} else if (tM==8 && tD<=15) {tBM=3;} else if(tM==8) {tBM=4;} else if (tM==9 && tD<=15) {tBM=4;} else if(tM==9) {tBM=5;} else if (tM==10 && tD<=15) {tBM=5;} else if(tM==10) {tBM=6;} else if (tM==11 && tD<=14) {tBM=6;} else if(m==11) {tBM=7;} else if (tM==12 && tD<=14) {tBM=7;} else if(tM==12) {tBM=8;} else if (tM==1 && tD<=13) {tBM=8; tBY--;} else if(tM==1) {tBM=9; tBY--;} else if (tM==2 && tD<=12) {tBM=9; tBY--;} else if(tM==2) {tBM=10; tBY--;} else if (tM==3 && tD<=14) {tBM=10; tBY--;} else if(tM==3) {tBM=11; tBY--;}
        final boolean isFutureMonth = (bnViewYear > tBY) || (bnViewYear == tBY && bnViewMonth >= tBM);
        int cGYear = bnViewYear + 593 + (bnViewMonth >= 9 ? 1 : 0); final boolean isOldMonth = cGYear <= (tY - 100);
        next.setAlpha(isFutureMonth ? 0.3f : 1f); prev.setAlpha(isOldMonth ? 0.3f : 1f);
        prev.setOnClickListener(new android.view.View.OnClickListener() { @Override public void onClick(final android.view.View v) { 
            if(isOldMonth) { ui.showSmartBanner((android.widget.FrameLayout)findViewById(android.R.id.content), lang.get("Limit Reached"), lang.get("Cannot go back more than 100 years."), "img_warning", colorAccent, null); return; }
            v.animate().scaleX(0.95f).scaleY(0.95f).setDuration(50).withEndAction(new Runnable() { @Override public void run() { v.animate().scaleX(1f).scaleY(1f).setDuration(100).start(); bnViewMonth--; if(bnViewMonth < 0) { bnViewMonth = 11; bnViewYear--; } renderBnGrid(card, dialog); } }).start(); 
        }});
        next.setOnClickListener(new android.view.View.OnClickListener() { @Override public void onClick(final android.view.View v) { 
            if(isFutureMonth) return;
            v.animate().scaleX(0.95f).scaleY(0.95f).setDuration(50).withEndAction(new Runnable() { @Override public void run() { v.animate().scaleX(1f).scaleY(1f).setDuration(100).start(); bnViewMonth++; if(bnViewMonth > 11) { bnViewMonth = 0; bnViewYear++; } renderBnGrid(card, dialog); } }).start(); 
        }});"""
        c = re.sub(r'prev\.setOnClickListener\(.*?\}\}\);.*?next\.setOnClickListener\(.*?\}\}\);', nav_logic, c, flags=re.DOTALL)
        with open(p, 'w', encoding='utf-8') as file: file.write(c)
        print("✅ ৩. ক্যালেন্ডারের মাসের নেভিগেশন (১০০ বছর লিমিট এবং ভবিষ্যৎ ব্লক) ফিক্স করা হয়েছে!")
        break
