import os

fpath = "app/src/main/java/com/my/salah/tracker/app/fragments/ZikrFragment.java"
with open(fpath, "r", encoding="utf-8") as f:
    code = f.read()

if "getField" not in code:
    inject_method = """
    private Object getField(String name) {
        try { java.lang.reflect.Field f = getActivity().getClass().getDeclaredField(name); f.setAccessible(true); return f.get(getActivity()); } catch (Exception e) { return null; }
    }
"""
    code = code.replace("public class ZikrFragment extends Fragment {", "public class ZikrFragment extends Fragment {" + inject_method)

theme_vars = """
        Context ctx = getContext();
        final int[] themeColors = (int[]) getField("themeColors");
        final int colorAccent = themeColors != null ? (Integer) getField("colorAccent") : android.graphics.Color.parseColor("#00BFA5");
        com.my.salah.tracker.app.LanguageEngine lang = (com.my.salah.tracker.app.LanguageEngine) getField("lang");
        boolean isBnTemp = false; try { isBnTemp = lang.get("Fajr").equals("ফজর"); } catch(Exception e){}
        final boolean isBn = isBnTemp;
        android.graphics.Typeface[] fonts = (android.graphics.Typeface[]) getField("appFonts");
        if (fonts != null) bnFont = fonts[1];
"""
code = code.replace("Context ctx = getContext();", theme_vars)

# স্ট্যাটিক কালারগুলোকে ডাইনামিক থিম কালারে রূপান্তর করা
code = code.replace('android.graphics.Color.parseColor("#F5F5F5")', 'themeColors != null ? themeColors[0] : android.graphics.Color.parseColor("#F5F5F5")')
code = code.replace('android.graphics.Color.parseColor("#CFD8DC")', 'themeColors != null ? themeColors[1] : android.graphics.Color.parseColor("#CFD8DC")')
code = code.replace('android.graphics.Color.BLACK', 'themeColors != null ? themeColors[2] : android.graphics.Color.BLACK')
code = code.replace('android.graphics.Color.GRAY', 'themeColors != null ? themeColors[3] : android.graphics.Color.GRAY')
code = code.replace('android.graphics.Color.parseColor("#37474F")', 'themeColors != null ? themeColors[2] : android.graphics.Color.parseColor("#37474F")')
code = code.replace('android.graphics.Color.parseColor("#263238")', 'themeColors != null ? themeColors[2] : android.graphics.Color.parseColor("#263238")')
code = code.replace('android.graphics.Color.parseColor("#546E7A")', 'themeColors != null ? themeColors[3] : android.graphics.Color.parseColor("#546E7A")')
code = code.replace('android.graphics.Color.parseColor("#D1DBE0")', 'themeColors != null ? themeColors[4] : android.graphics.Color.parseColor("#D1DBE0")')
code = code.replace('android.graphics.Color.parseColor("#1B5E20")', 'colorAccent')
code = code.replace('android.graphics.Color.parseColor("#00FBFF")', 'colorAccent')
code = code.replace('android.graphics.Color.parseColor("#A3FFFD")', 'colorAccent')
code = code.replace('android.graphics.Color.WHITE', 'themeColors != null ? themeColors[1] : android.graphics.Color.WHITE')

# ভাষা বা ল্যাঙ্গুয়েজ আপডেট করা
code = code.replace('"Swipe left or right to change Dua"', 'isBn ? "দোয়া পরিবর্তন করতে ডানে বা বামে সোয়াইপ করুন" : "Swipe left or right to change Dua"')
code = code.replace('"সর্বমোট: "', 'isBn ? "সর্বমোট: " : "Total: "')

with open(fpath, "w", encoding="utf-8") as f:
    f.write(code)
print("✅ ZikrFragment Theme & Language synced perfectly!")
