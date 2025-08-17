import os
import shutil

# Define the root directory
root_dir = r"W:\Movies"

def is_video_file(file_path):
    video_extensions = {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'}
    _, ext = os.path.splitext(file_path)
    return ext.lower() in video_extensions

# Folders we consider ignorable if they're the only thing left
IGNORABLE_DIRS = {".wdmc", "subs", "sample"}

# Check if the root directory exists
if not os.path.exists(root_dir):
    print(f"The directory {root_dir} does not exist.")
else:
    for item in os.listdir(root_dir):
        full_path = os.path.join(root_dir, item)

        # Process only directories that are not named "TV"
        if os.path.isdir(full_path) and item != "TV":
            # Move any video files to the root directory
            for f in os.listdir(full_path):
                file_path = os.path.join(full_path, f)

                if os.path.isfile(file_path) and is_video_file(file_path):
                    new_path = os.path.join(root_dir, f)
                    if os.path.exists(new_path):
                        print(f"Skipping '{f}', file already exists in {root_dir}.")
                    else:
                        shutil.move(file_path, new_path)
                        print(f"Moved: {f} -> {root_dir}")

            # Check what remains in the subdirectory
            remaining_items = os.listdir(full_path)

            # ✔ delete if empty
            if not remaining_items:
                os.rmdir(full_path)
                print(f"Deleted empty folder: {item}")
                continue

            # ✔ delete immediately if 'sample.avi' is present, regardless of what else is inside
            if any(x.lower() == "sample.avi" for x in remaining_items):
                shutil.rmtree(full_path)
                print(f"Deleted folder '{item}' because it contains sample.avi")
                continue

            # ✔ delete if the only remaining item is one of the ignorable folders (.wdmc, Subs, Sample)
            if len(remaining_items) == 1:
                only_item = remaining_items[0]
                only_item_path = os.path.join(full_path, only_item)
                if os.path.isdir(only_item_path) and only_item.lower() in IGNORABLE_DIRS:
                    shutil.rmtree(full_path)
                    print(f"Deleted folder containing only directory '{only_item}': {item}")
