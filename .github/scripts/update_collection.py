import os
import re
import urllib.parse

repo_url = "https://github.com/fr0st-iwnl/hub.fr0st.xyz/blob/master"

# find root-level folders (ignore hidden + .github)
folders = [f for f in os.listdir(".") if os.path.isdir(f) and not f.startswith(".") and f != ".github"]
folders.sort()

# build collection list
collection_lines = []
for i, folder in enumerate(folders, 1):
    folder_url = urllib.parse.quote(folder)  # encode spaces and special chars
    collection_lines.append(f"- `{i}`. [{folder}]({repo_url}/{folder_url}/README.md)")

collection = "## 🔧 Collection\n\n" + "\n".join(collection_lines) + "\n"

# read current README.md
if os.path.exists("README.md"):
    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()
else:
    readme = ""

# check if collection section exists
if "## 🔧 Collection" in readme:
    # replace old collection section (between ## 🔧 Collection and next ## or EOF)
    pattern = r"(## 🔧 Collection\n)(.*?)(\n## |\Z)"  # match until next heading or EOF
    new_readme = re.sub(pattern, f"{collection}\n\\3", readme, flags=re.S)
else:
    # prepend collection at the top if not present
    new_readme = collection + "\n" + readme

# write updated README.md
with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_readme)

print("✅ README.md collection updated!")
