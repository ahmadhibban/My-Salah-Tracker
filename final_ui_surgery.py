import os
import re

def main():
    target_main = None
    search_paths = ['.', '/storage/emulated/0/AndroidIDEProjects', '/storage/emulated/0/']
    
    for r in search_paths:
        if not os.path.exists(r): continue
        for root, dirs, files in os.walk(r):
            if 'Android/data' in root or '.git' in root: continue
            if 'MainActivity.java' in files: 
                target_main = os.path.join(root, 'MainActivity.java')
                break
        if target_main: break

    if target_main:
        with open(target_main, 'r', encoding='utf-8') as f:
            content = f.read()

        # ==========================================
        # ফিক্স ১: ট্যাগ যুক্ত করা (যাতে শুধু পার্সেন্টেজ আপডেট হয়)
        # ==========================================
        if 'setTag("PERCENT_TEXT")' not in content:
            content = re.sub(r'(pT\.setText\([^;]+;)', r'\1 pT.setTag("PERCENT_TEXT");', content)
            content = re.sub(r'(subBtm\.setText\([^;]+;)', r'\1 subBtm.setTag("SUB_TEXT");', content)

        # ==========================================
        # ফিক্স ২: লাইভ আপডেট মেথড তৈরি করা
        # ==========================================
        if "updateLivePercentage" not in content:
            method = """
    private void updateLivePercentage(String dK) {
        try {
            int nC = 0; 
            SalahRecord currR = SalahDatabase.getDatabase(this).salahDao().getRecordByDate(dK);
            if(currR != null) {
                for(String pr : AppConstants.PRAYERS) { 
                    String s = getFardStat(currR, pr); 
                    if(s.equals("yes") || s.equals("excused")) nC++; 
                }
            }
            TextView pT = getWindow().getDecorView().findViewWithTag("PERCENT_TEXT");
            TextView subBtm = getWindow().getDecorView().findViewWithTag("SUB_TEXT");
            if(pT != null) pT.setText(lang.bnNum(nC*100/6) + "%");
            if(subBtm != null) subBtm.setText(statusMsgs[nC]);
        } catch(Exception e){}
    }
"""
            content = content.replace("private void loadTodayPage() {", method + "\n    private void loadTodayPage() {")
            # যদি public void থাকে তার জন্যও ব্যাকআপ
            content = content.replace("public void loadTodayPage() {", method + "\n    public void loadTodayPage() {")

        # ==========================================
        # ফিক্স ৩: রিস্টার্ট বাগ চিরতরে মুছে ফেলা
        # ==========================================
        # ফরজ এবং সুন্নতের ক্লিক থেকে loadTodayPage() মুছে আমাদের লাইভ আপডেট বসানো হচ্ছে
        def kill_restart(match):
            s = match.group(0)
            s = re.sub(r'loadTodayPage\(\);', '/* রিস্টার্ট বন্ধ */ updateLivePercentage(dKey);', s)
            return s
            
        content = re.sub(r'chk\.setOnClickListener.*?refreshWidget\(\);[^\}]*\}\s*\)?\s*;', kill_restart, content, flags=re.DOTALL)
        content = re.sub(r'sBox\.setOnClickListener.*?refreshWidget\(\);[^\}]*\}\s*\)?\s*;', kill_restart, content, flags=re.DOTALL)

        # ==========================================
        # ফিক্স ৪: ফোর্সফুল কার্ড সাইজ কমানো (এক পেজে ফিট)
        # ==========================================
        # মার্জিন একদম 0 এবং প্যাডিং একদম মিনিমাম 1/2 করা হলো
        content = re.sub(r'cardParams\.setMargins\([^;]+;', 'cardParams.setMargins((int)(15*DENSITY), 0, (int)(15*DENSITY), 0);', content)
        content = re.sub(r'card\.setPadding\([^;]+;', 'card.setPadding((int)(15*DENSITY), (int)(1*DENSITY), (int)(15*DENSITY), (int)(1*DENSITY));', content)
        
        content = re.sub(r'headerParams\.setMargins\([^;]+;', 'headerParams.setMargins((int)(15*DENSITY), 0, (int)(15*DENSITY), 0);', content)
        content = re.sub(r'pCard\.setPadding\([^;]+;', 'pCard.setPadding((int)(15*DENSITY), (int)(2*DENSITY), (int)(15*DENSITY), (int)(2*DENSITY));', content)
        
        # সুন্নাহ লিস্টের ভেতরের গ্যাপ 0
        content = re.sub(r'sList\.setPadding\([^;]+;', 'sList.setPadding(0, 0, 0, 0);', content)

        with open(target_main, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print("✅ ম্যাজিক সম্পন্ন! ওপরের আইকনগুলোর রিস্টার্ট বাগ ফিক্স করা হয়েছে এবং কার্ডগুলো এক পেজে ফিট করা হয়েছে।")
    else:
        print("❌ MainActivity.java পাওয়া যায়নি।")

if __name__ == '__main__': main()
