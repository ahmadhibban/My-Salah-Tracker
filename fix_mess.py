import os

def clean_pro_mess():
    # build.gradle থেকে .pro মুছে ফেলা
    path_g = "app/build.gradle"
    if os.path.exists(path_g):
        with open(path_g, 'r', encoding='utf-8') as f: content = f.read()
        with open(path_g, 'w', encoding='utf-8') as f: f.write(content.replace(".pro", ""))

    # AndroidManifest থেকে .pro মুছে ফেলা
    path_m = "app/src/main/AndroidManifest.xml"
    if os.path.exists(path_m):
        with open(path_m, 'r', encoding='utf-8') as f: content = f.read()
        with open(path_m, 'w', encoding='utf-8') as f: f.write(content.replace(".pro", ""))

clean_pro_mess()
print("Garbage cleaned! Package name and Manifest restored to original.")
