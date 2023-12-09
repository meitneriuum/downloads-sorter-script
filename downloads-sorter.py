import os
import datetime
import json
from typing import Final
import shutil
from send2trash import send2trash

SOURCE: Final = 'C:\\Users\\alexi\\Downloads'
METADATA: Final = 'meta.json'
THRESHOLD: Final = 1   # period of inactivity after which certain filetypes will be deleted (est. in days)
TO_BE_DELETED: Final = '.jpg', '.png', '.jpeg', '.heic', '.webp', '.html', '.avif', '.mp4', '.mkv', '.avi', '.webm', '.gif', '.torrent'
ARCHIVE_FILETYPES: Final = '.zip', '.rar', '.jar', '.7z'
ARCHIVE_FOLDERNAME = 'archives'

def read_metadata(source):
    with open(source, 'r') as f:
        data = json.load(f)
        return data

def update_metadata(source, whitelist):
    json_whitelist = json.dumps(whitelist, indent=4)
    with open(os.path.join(source, METADATA), "w") as f:
        f.write(json_whitelist)
        
def get_metadata(source):
    path = os.path.join(source, METADATA)
    try:
        data = read_metadata(path)
    except FileNotFoundError as e:
        data = [METADATA,]
    return data
        
def create_dir(path, dname, white):
    if not os.path.exists(path):
        os.mkdir(path)
        white.append(dname)
    return white

def shove_intensely(objects):
    root = objects['root']
    whitelist = get_metadata(root)
    for file in objects['files']:
        name = file['name']
        ext = file['ext']
        path = file['path']
        fullname = name + ext
        if  fullname not in whitelist:
            if ext in ARCHIVE_FILETYPES:
                temp = os.path.join(root, ARCHIVE_FOLDERNAME)
                whitelist = create_dir(temp, ARCHIVE_FOLDERNAME, whitelist)
                shutil.copy(path, temp)
                os.remove(path)
            elif ext in TO_BE_DELETED: 
                time_now = datetime.datetime.now()
                last_access_time = datetime.datetime.fromtimestamp(os.path.getatime(path))
                threshold = datetime.timedelta(days=THRESHOLD)
                if time_now - last_access_time >= threshold:
                    send2trash(path)
            else:
                temp = os.path.join(root, ext)
                whitelist = create_dir(temp, ext, whitelist)
                shutil.copy(path, temp)
                os.remove(path)
    for directory in objects['dirs']:
        if directory['name'] not in whitelist:
            send2trash(directory['path'])
    update_metadata(root, whitelist)

def find_all_dirs_n_files_in(source):
    for root, dirs, files in os.walk(source):
        dirs_to_put_away = [{'path': os.path.join(source, d), 'name': d} for d in dirs]
        files_st = [{'path': os.path.join(source, name + ext), 'name': name, 'ext': ext} for name, ext in [os.path.splitext(f) for f in files]]
        return {
            'root': root,
            'dirs': dirs_to_put_away,
            'files': files_st
        }

def main(source=SOURCE):
    all_kinds = find_all_dirs_n_files_in(source)
    shove_intensely(all_kinds)
    print('Sorted!')


if __name__ == '__main__':
    main()
    