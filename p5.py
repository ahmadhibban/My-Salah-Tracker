import re
f5 = 'app/src/main/java/com/my/salah/tracker/app/StatsHelper.java'
c5 = open(f5).read()
opc = """radius, paint); \n                } \n                else if (allDone || hasExcused) { \n                    paint.setColor(colorAccent); paint.setStyle(Paint.Style.STROKE); paint.setStrokeWidth(3f); canvas.drawCircle(cx, cy, radius, paint); paint.setStyle(Paint.Style.FILL);\n                } \n                else { \n                    paint.setColor(Color.parseColor("#FFEBEE")); paint.setStyle(Paint.Style.FILL); canvas.drawCircle(cx, cy, radius, paint); \n                }"""
npc = """radius, paint); \n                } \n                else { \n                    int dP=0; boolean exP=false; if(rec!=null){for(String pr:prayers){String s=getFardStat(rec,pr);if(s.equals("yes"))dP++;else if(s.equals("excused")){dP++;exP=true;}}}
                    paint.setColor(android.graphics.Color.parseColor("#F1F5F9")); paint.setStyle(android.graphics.Paint.Style.STROKE); paint.setStrokeWidth(2f); canvas.drawCircle(cx, cy, radius, paint);
                    if(dP>0 && !(cal.after(now) && !dKey.equals(sdf.format(now.getTime())))) {
                        paint.setColor(dP==6?android.graphics.Color.parseColor("#22C55E"):(exP?android.graphics.Color.parseColor("#8B5CF6"):android.graphics.Color.parseColor("#10B981")));
                        canvas.drawArc(new android.graphics.RectF(cx-radius, cy-radius, cx+radius, cy+radius), -90, 360f*(dP/6f), false, paint);
                    } paint.setStyle(android.graphics.Paint.Style.FILL);\n                }"""
open(f5,'w').write(c5.replace(opc, npc))
print("✅ Part 5 Done! ALL FIXED. BUILD NOW.")
