sed -i 's/setDuration(100)/setDuration(35)/g' MainActivity.java
sed -i 's/setDuration(250)/setDuration(120)/g' MainActivity.java
sed -i 's/refreshWidget(); }}, 150)/refreshWidget(); }}, 20)/g' MainActivity.java
echo "✅ Step 1: UI Response Time and Animation Speed Optimized."
