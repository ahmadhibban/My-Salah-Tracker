import os

file_path = 'app/build.gradle.kts' if os.path.exists('app/build.gradle.kts') else 'app/build.gradle'

if os.path.exists(file_path):
    with open(file_path, 'r') as f:
        data = f.read()

    is_kts = file_path.endswith('.kts')

    # KAPT এবং কোটলিনের সব কাজকে Java 11 তে বাধ্য করার কোড
    fix_code = """
tasks.withType<org.jetbrains.kotlin.gradle.tasks.KotlinCompile>().configureEach {
    kotlinOptions {
        jvmTarget = "11"
    }
}
""" if is_kts else """
tasks.withType(org.jetbrains.kotlin.gradle.tasks.KotlinCompile).configureEach {
    kotlinOptions {
        jvmTarget = "11"
    }
}
"""

    if "tasks.withType" not in data:
        with open(file_path, 'a') as f:
            f.write("\n" + fix_code + "\n")
        print("✅ KAPT JVM Target mismatch fixed successfully!")
    else:
        print("⚡ Already fixed.")
else:
    print("❌ app/build.gradle not found!")
