# 🔥 WSLOSTRER 🔥  
**Military-Grade Link Extraction System v7.5 (PHANTOM STRIKE)**  

![WSLostEreR](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)  
![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square)  
![Security](https://img.shields.io/badge/Security-Advanced-red?style=flat-square)  

---

## 🚀 About  
**WSLOSTRER** is a powerful and stealthy **link extraction & reconnaissance tool** built for deep web analysis. It efficiently extracts visible, hidden, and sensitive URLs from a website using:  

✔️ **Multi-Threading** for lightning-fast results  
✔️ **Tor Proxy Support** for anonymous operations  
✔️ **Stealth Mode** to detect hidden endpoints  
✔️ **Advanced Filtering** to categorize extracted links  
✔️ **Auto-Save Reports** in structured format  

This tool is ideal for **ethical hackers, penetration testers, and researchers** who need a high-performance link extraction system.  

---

## 🛠 Features  
🔹 **Multi-threaded processing** (15 parallel threads)  
🔹 **Extracts hidden & admin links** (e.g., `/admin`, `/login`, `.git/`)  
🔹 **Smart detection** (checks HTTP response codes)  
🔹 **Tor support** (rotates identity for anonymity)  
🔹 **Auto-saving system** (structured results in organized folders)  
🔹 **Military-style ASCII art & real-time output**  

---

📌 Installation & Usage Commands

1️⃣ Clone the Repository

git clone https://github.com/Sabirtanvir12/wslosetrer.git
cd wslosetrer

2️⃣ Install Dependencies

pip install -r requirements.txt

3️⃣ Run the Tool (Without Tor)

python wslosetrer.py
# [?] Enter Target Coordinates: https://example.com
# [?] Enable Stealth Protocol (Tor)? [y/N]: N

4️⃣ Run the Tool (With Tor for Stealth Mode)

python wslosetrer.py
# [?] Enter Target Coordinates: https://example.com
# [?] Enable Stealth Protocol (Tor)? [y/N]: Y

5️⃣ View Extracted Links

ls extracted_links/example.com/
cat extracted_links/example.com/normal.txt

6️⃣ Enable Tor Service (if not running)

sudo systemctl start tor

7️⃣ Check Tor IP Rotation (Optional)

curl --socks5-hostname 127.0.0.1:9050 http://check.torproject.org

8️⃣ Remove the Tool (If Needed)

cd ..
rm -rf wslosetrer

---

📁 Output Structure

Extracted links are automatically saved inside a folder named after the website’s domain:

📂 extracted_links/
 ├── 📂 example.com/
 │   ├── normal.txt       # Regular extracted links
 │   ├── hidden.txt       # Hidden & sensitive links
 │   ├── forbidden.txt    # Links returning 403/401
 │   ├── redirect.txt     # Links causing redirects
 │   ├── client_error.txt # Links returning 4xx errors
 │   ├── server_error.txt # Links returning 5xx errors
 │   ├── error.txt        # Links that failed


---

🎭 ASCII Art & Real-Time Status


The tool features live real-time scanning output with color-coded results!

✅ Normal Links → Green
⚠️ Hidden Links → Yellow
🚫 Forbidden (403/401) → Red
🔄 Redirects (301/302) → Cyan


---

⚠️ Legal Disclaimer

This tool is developed for educational & research purposes only.
DO NOT use it on websites without permission. The developer is not responsible for any misuse!


---

👑 Credits

Developer: CyberShade (Z3R0)
📌 GitHub Repo: WSLostEreR

🔹 Stay Anonymous. Stay Ethical. 🔹