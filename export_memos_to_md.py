# export_memos_to_md.py
#
# A script to export memos from a self-hosted Memos Docker instance into Markdown files, 
# including attachments organized per memo
#
# Author: @fr0st-iwnl
#=================================================================
# Repository: update this later
#-----------------------------------------------------------------
# Issues: update this later
# Pull Requests: update this later
#-----------------------------------------------------------------

import sqlite3
import os
import subprocess
import sys

# colors and emojis :) always love em
GREEN = "\033[92m"
CYAN = "\033[96m"
EMOJI_DB = "💾"
EMOJI_MEMO = "📝"
EMOJI_ATTACH = "📎"
EMOJI_DONE = "🎉"
RESET = "\033[0m"

try:
    print(f"")
    print(f"{CYAN}🪄 Welcome to Memos Exporter :P{RESET}")
    print(f"{CYAN}═══════════════════════════════════════════════════════{RESET}")

    # Determine home directory
    if "SUDO_USER" in os.environ:
        home_dir = os.path.expanduser(f"~{os.environ['SUDO_USER']}")
    else:
        home_dir = os.path.expanduser("~")

    downloads_dir = os.path.join(home_dir, "Downloads")
    os.makedirs(downloads_dir, exist_ok=True)

    # Find running Memos docker container
    try:
        result = subprocess.run(
            ["docker", "ps", "--format", "{{.ID}} {{.Image}}"],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError:
        raise Exception("Cannot access Docker. Run with sudo or add your user to the docker group.")

    container_id = None
    for line in result.stdout.strip().split("\n"):
        if "memos" in line.lower():
            container_id = line.split()[0]
            break

    if not container_id:
        raise Exception("No running Memos container found!")

    print(f"{EMOJI_DB} Found Memos container: {container_id}")

    # Main output folder for Markdown memos
    output_dir = os.path.join(downloads_dir, "memos_md")
    os.makedirs(output_dir, exist_ok=True)

    # Folder for attachments
    assets_dir = os.path.join(output_dir, "memos_assets")
    os.makedirs(assets_dir, exist_ok=True)

    # Folder for the database
    db_dir = os.path.join(output_dir, "memos_db")
    os.makedirs(db_dir, exist_ok=True)

    # Copy database into memos_db folder
    db_path = os.path.join(db_dir, "memos_prod.db")
    print(f"{EMOJI_DB} Copying database to {db_path} ...")
    subprocess.run(
        ["docker", "cp", f"{container_id}:/var/opt/memos/memos_prod.db", db_path],
        check=True,
        stdout=subprocess.DEVNULL,  # <-- suppress output
        stderr=subprocess.DEVNULL   # <-- suppress errors too
    )
    print(f"{GREEN}{EMOJI_DB} Database copied successfully!{RESET}")

    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Fetch all memos
    cursor.execute("SELECT id, content FROM memo;")
    memos = cursor.fetchall()

    print(f"{EMOJI_MEMO} Exporting {len(memos)} memos...")

    total_attachments = 0
    for memo_id, content in memos:
        # Save markdown
        md_file = os.path.join(output_dir, f"memo_{memo_id}.md")
        with open(md_file, "w", encoding="utf-8") as f:
            f.write(content)

        # Fetch attachments
        cursor.execute("SELECT filename, blob FROM resource WHERE memo_id = ?", (memo_id,))
        resources = cursor.fetchall()

        # Only save attachments if they exist
        attachments_saved = 0
        if resources:
            memo_assets_dir = os.path.join(assets_dir, f"memo_{memo_id}_assets")
            for filename_res, blob_data in resources:
                if blob_data:
                    os.makedirs(memo_assets_dir, exist_ok=True)
                    file_path = os.path.join(memo_assets_dir, filename_res)
                    with open(file_path, "wb") as f_res:
                        f_res.write(blob_data)
                    attachments_saved += 1

        total_attachments += attachments_saved

    print(f"{EMOJI_ATTACH} {total_attachments} attachments saved")
    print(f"{GREEN}{EMOJI_DONE} Export complete! Exported {len(memos)} memos and {total_attachments} attachments to {output_dir}{RESET}")
    print(f"")
    conn.close()

except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)