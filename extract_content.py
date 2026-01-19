import zipfile
import os
import shutil
import re
import json

zip_path = "ExportBlock-034d76d1-7f4d-426a-92f3-85ea6c5d3965-Part-1.zip"
content_dir = "contents"
map_file = "content_map.json"

# Clean up existing content dir
if os.path.exists(content_dir):
    shutil.rmtree(content_dir)
os.makedirs(content_dir)

mapping = []

print("Extracting markdown files...")

with zipfile.ZipFile(zip_path, 'r') as z:
    for i, info in enumerate(z.infolist()):
        # Attempt to handle filename encoding
        # Notion zips usually have utf-8 names, but python zipfile might misinterpret headers if flags aren't set
        # Try to fix "garbage" characters
        try:
            fname = info.filename.encode('cp437').decode('utf-8')
        except:
            fname = info.filename

        if fname.endswith(".md"):
            # Skip CSV generated MDs if any, focus on the ones in subfolder usually
            # The structure seemed to be "신학자료/Title ID.md"
            
            # Generate a safe filename
            safe_id = f"article_{i}"
            safe_filename = f"{safe_id}.md"
            target_path = os.path.join(content_dir, safe_filename)
            
            # Extract to temp, then move/rename
            # We can't use z.extract(info) directly with renaming easily if we want to flatten structure
            
            with z.open(info) as source, open(target_path, "wb") as target:
                shutil.copyfileobj(source, target)
            
            # Parse the filename to get potential title for matching
            # Format: "Path/Title ID.md" -> "Title"
            basename = os.path.basename(fname)
            # Remove the Notion ID suffix (usually 32 hex chars at end) if present
            # Example: "Title 10282849954d8012ae3ad372320fd17e.md"
            # Regex to find title before the hash
            match = re.match(r"(.*)\s+[a-f0-9]{32}\.md$", basename)
            if match:
                title_candidate = match.group(1).strip()
            else:
                title_candidate = basename.replace(".md", "").strip()
            
            mapping.append({
                "id": safe_id,
                "file": safe_filename,
                "original_title": title_candidate,
                "full_original_path": fname
            })
            print(f"Extracted: {title_candidate} -> {safe_filename}")

# Save mapping
with open(map_file, "w", encoding="utf-8") as f:
    json.dump(mapping, f, ensure_ascii=False, indent=2)

print(f"Done. Extracted {len(mapping)} files.")
