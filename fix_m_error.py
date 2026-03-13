import os
for r, d, f in os.walk('.'):
    if 'MainActivity.java' in f and 'build' not in r:
        p = os.path.join(r, 'MainActivity.java')
        with open(p, 'r', encoding='utf-8') as file: c = file.read()
        c = c.replace('else if(m==11) {tBM=7;}', 'else if(tM==11) {tBM=7;}')
        with open(p, 'w', encoding='utf-8') as file: file.write(c)
        print("✅ এরর ফিক্স করা হয়েছে!")
        break
