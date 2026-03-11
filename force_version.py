import os, re
app = 'app/build.gradle'
if os.path.exists(app):
    with open(app, 'r', encoding='utf-8') as f: c = f.read()
    c = re.sub(r"implementation\s+['\"]com.github.fornewid:neumorphism.*?['\"]", "", c)
    c = c.replace("dependencies {", "dependencies {\n    implementation 'com.github.fornewid:neumorphism:0.3.2'")
    with open(app, 'w', encoding='utf-8') as f: f.write(c)
    print("✔ Version set to 0.3.2")
