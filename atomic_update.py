import os, shutil

def safe_replace(file_path, old_text, new_text):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if old_text not in content:
        return
        
    # ১. অ্যাটমিক রাইটের জন্য ব্যাকআপ তৈরি
    backup_path = file_path + '.bak'
    shutil.copy2(file_path, backup_path)
    
    # ২. নতুন কোড টেম্পরারি ফাইলে লেখা
    new_content = content.replace(old_text, new_text)
    temp_path = file_path + '.tmp'
    
    with open(temp_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    # ৩. সব ঠিক থাকলে মূল ফাইল রিপ্লেস করা (১০০% নিরাপদ)
    os.replace(temp_path, file_path)
    print(f"Successfully updated: {file_path}")

for root, _, files in os.walk('.'):
    for file in files:
        if file.endswith('.java'):
            path = os.path.join(root, file)
            
            # XML থ্রিডি শ্যাডোটিকে জাভাতে ডাইনামিকভাবে অ্যাপ্লাই করার কোড
            old_code = "card.setBackground(cb);"
            new_code = """
            android.graphics.drawable.LayerDrawable shadowDrawable = (android.graphics.drawable.LayerDrawable) androidx.core.content.ContextCompat.getDrawable(card.getContext(), R.drawable.premium_3d_shadow);
            android.graphics.drawable.GradientDrawable mainCard = (android.graphics.drawable.GradientDrawable) shadowDrawable.getDrawable(1);
            mainCard.setColor(((android.graphics.drawable.ColorDrawable)cb).getColor());
            card.setBackground(shadowDrawable);
            """
            
            safe_replace(path, old_code, new_code)

print("Atomic update complete! No manual copy-paste needed.")
