import os
import hashlib
from send2trash import send2trash
from tqdm import tqdm


def get_file_hash(filepath):
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        buf = f.read(4096)
        while buf:
            hasher.update(buf)

            buf = f.read(4096)
    return hasher.hexdigest()


def find_duplicates(folder_path):
    hashes = {}
    duplicates = []

    print(f"Scanning {folder_path}...")
    for root, dirs, files in os.walk(folder_path):
        for filename in tqdm(files):
            filepath = os.path.join(root, filename)
            try:
                file_hash = get_file_hash(filepath)
                if file_hash in hashes:
                    duplicates.append((filepath, hashes[file_hash]))  
                else:
                    hashes[file_hash] = filepath
            except Exception as e:
                print(f"Error reading {filepath}: {e}")
    return duplicates


def delete_duplicates(duplicates):
    print("\nFound duplicates:")
    for dup, original in duplicates:
        print(f"🗑️ {dup} (duplicate of {original})")
    
    confirm = input("\nDo you want to delete all duplicates? (y/n): ").strip().lower()
    if confirm == 'y':
        for dup, _ in duplicates:
            try:
                send2trash(dup)  
                print(f"Deleted: {dup}")
            except Exception as e:
                print(f"Failed to delete {dup}: {e}")
    else:
        print("No files were deleted.")


if __name__ == "__main__":
    folder = input("🔍 Enter the full path to the folder you want to scan for duplicates: ").strip()
    if os.path.exists(folder):
        dupes = find_duplicates(folder)
        if dupes:
            delete_duplicates(dupes)
        else:
            print("🎉 No duplicates found.")
    else:
        print("❌ That path does not exist.")
