import os
import re

repo_url = "https://github.com/fr0st-iwnl/hub.fr0st.xyz/blob/master"

# find root-level folders (ignore hidden + .github)
folders = [f for f in os.listdir(".") if os.path.isdir(f) and not f.startswith(".") and f != ".github"]
folders.sort()

# build collection list
collection = "## 🔧 Collection\n\n"
for i, folder in enumerate(folders, 1):
    collection += f"- `{i}`. [{folder}]({repo_url}/{folder}/README.md)\n"

# read current README.md
with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

# replace old collection section (between ## 🔧 Collection and next ##)
pattern = r"(## 🔧 Collection\n)(.*?)(\n## |\Z)"  # match until next heading or EOF
new_readme = re.sub(pattern, f"{collection}\n\\3", readme, flags=re.S)

# write updated README.md
with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_readme)

print("✅ README.md collection updated!")
