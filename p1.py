f1 = 'app/src/main/java/com/my/salah/tracker/app/UIComponents.java'
c1 = open(f1).read()
pd = """public static class ProgressDrawable extends android.graphics.drawable.Drawable {
        private int d, t, c, bg; private float dens;
        public ProgressDrawable(int d, int t, int c, int bg, float dens) { this.d=d; this.t=t; this.c=c; this.bg=bg; this.dens=dens; }
        @Override public void draw(android.graphics.Canvas canvas) {
            android.graphics.Rect b = getBounds(); android.graphics.Paint p = new android.graphics.Paint(1);
            p.setStyle(android.graphics.Paint.Style.STROKE); p.setStrokeWidth(2.5f * dens); p.setStrokeCap(android.graphics.Paint.Cap.ROUND);
            float r = Math.min(b.width(), b.height()) / 2f - (2.5f * dens);
            p.setColor(bg); canvas.drawCircle(b.exactCenterX(), b.exactCenterY(), r, p);
            if(d>0){ p.setColor(c); canvas.drawArc(new android.graphics.RectF(b.exactCenterX()-r, b.exactCenterY()-r, b.exactCenterX()+r, b.exactCenterY()+r), -90, 360f*(d/(float)t), false, p); }
        }
        @Override public void setAlpha(int a){} @Override public void setColorFilter(android.graphics.ColorFilter f){} @Override public int getOpacity(){return -3;}
    }

    public View getPremiumIcon"""
if "ProgressDrawable" not in c1: open(f1,'w').write(c1.replace('public View getPremiumIcon', pd))

f2 = 'app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
c2 = open(f2).read()
mh = """public int getStatusColor(String k) {
        if(k==null) return themeColors[4]; SalahRecord r = getRoomRecord(k); int d=0, e=0;
        for(String p : AppConstants.PRAYERS){ String s=getFardStat(r, p); if("yes".equals(s)) d++; else if("excused".equals(s)) e++; }
        if(d+e==0) return android.graphics.Color.TRANSPARENT; if(e==6) return android.graphics.Color.parseColor("#8B5CF6");
        return d==6 ? android.graphics.Color.parseColor("#22C55E") : android.graphics.Color.parseColor("#10B981");
    }
    public android.graphics.drawable.Drawable getProgressBorder(String k, boolean s) {
        int c = getStatusColor(k); int d=0; SalahRecord r = getRoomRecord(k);
        for(String p : AppConstants.PRAYERS){ String st=getFardStat(r, p); if("yes".equals(st)||"excused".equals(st)) d++; }
        if(s){ android.graphics.drawable.GradientDrawable gd=new android.graphics.drawable.GradientDrawable(); gd.setShape(android.graphics.drawable.GradientDrawable.OVAL); gd.setColor(colorAccent); return gd; }
        return new UIComponents.ProgressDrawable(d, 6, c==0?themeColors[4]:c, themeColors[4], DENSITY);
    }

    private void loadTodayPage() {"""
if "getProgressBorder" not in c2: open(f2,'w').write(c2.replace('private void loadTodayPage() {', mh))
print("✅ Part 1 Done!")
