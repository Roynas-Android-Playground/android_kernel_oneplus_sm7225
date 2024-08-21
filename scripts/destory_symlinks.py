import os
import shutil

def cache_symlinks(base_path):
    symlink_cache = []
    
    for root, dirs, files in os.walk(base_path, followlinks=False):
        # Process directories
        for name in dirs:
            symlink_path = os.path.join(root, name)
            if os.path.islink(symlink_path):
                target_path = os.path.realpath(symlink_path)
                symlink_cache.append((symlink_path, target_path))

        # Process files
        for name in files:
            symlink_path = os.path.join(root, name)
            if os.path.islink(symlink_path):
                target_path = os.path.realpath(symlink_path)
                symlink_cache.append((symlink_path, target_path))

    return symlink_cache

def copy_and_remove_symlinks(symlink_cache):
    for symlink_path, target_path in symlink_cache:
        if os.path.exists(target_path):
            print("Remove", symlink_path, "to make way for", target_path)
            if not os.path.exists(target_path):
                print("warn, nonexistent")
                continue
            # Can use shutil.rmtree to update trees if any
            os.remove(symlink_path)
            if os.path.isdir(target_path):
                print("Copy tree for:", target_path)
                # Copy the directory
                shutil.copytree(target_path, symlink_path, symlinks=True)
            elif os.path.isfile(target_path):
                print("Copy file for:", target_path)
                # Copy the file
                shutil.copy2(target_path, symlink_path)

if __name__ == "__main__":
    base_path = "."  # Set the base path to the current directory or change as needed
    symlink_cache = cache_symlinks(base_path)
    copy_and_remove_symlinks(symlink_cache)

