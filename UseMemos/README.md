# 💾 Memos Exporter 

A simple **Python** script to export memos from a self-hosted **[Memos](https://www.usememos.com/)** Docker instance into Markdown files. It also exports attachments and copies the database files so your exported memos are always up-to-date.  

## ✨ Features

- 📝 Exports memos as Markdown (`.md`) files.  
- 📂 Saves attachments in separate folders per memo.  
- 💾 Copies database files (`.db`, `.db-wal`, `.db-shm`) for latest changes.  
- 🔄 Menu to choose whether to delete old exports or export memos.  

## 🚀 Usage

1. **Run the script**  

```bash
python memos_exporter.py
```

2. **You'll see a menu:**
```sql
1) Delete existing 'memos_md' folder
2) Export memos
```

3. Choose `1` to **remove old exports**, or `2` to export **current memos**.
   <br>
   Since you usually won't have a `memos_md` folder at first, you would normally select option `2` to start exporting your memos.

## 📂 Output

**Markdown files will be saved in:**

```bash
~/Downloads/memos_md/
```

**Attachments will be inside:**

```bash
~/Downloads/memos_md/memos_assets/
```

**Database files are copied to:**

```bash
~/Downloads/memos_md/memos_db/
```
