from os import system
from os.path import isdir, relpath
from time import sleep
import filecmp
import dropbox

dbx = dropbox.Dropbox("kSX---LHerIAAAAAAAIsrgOPOdYTHPIsFw_92wWvMHmgu6JqZWgXNUlfFEY1EC7f") # Dropbox OAuth2 token.

upload_dir = "/Nibbler001/" # Keep first and last slashes.

def sync_dbx(dcmp):
    for filename in dcmp.right_only:
        absolute_path = dcmp.right + filename if dcmp.right[-1] == "/" else dcmp.right + "/" + filename
        relative_path = relpath(absolute_path, "/mnt/usb_emu/")
        print(absolute_path)
        print(isdir(absolute_path))
        if isdir(absolute_path):
            print("Creating Folder: " + upload_dir + relative_path + " from " + absolute_path)
            dbx.files_create_folder_v2(upload_dir + relative_path, autorename=False)
        else:
            print("Uploading File: " + upload_dir + relative_path + " from " + absolute_path)
            dbx.files_upload(open(absolute_path, "rb").read(), upload_dir + relative_path, mode=dropbox.files.WriteMode("overwrite"),
                             mute=True, autorename=False)
    for filename in dcmp.left_only:
        absolute_path = dcmp.right + filename if dcmp.right[-1] == "/" else dcmp.right + "/" + filename
        relative_path = relpath(absolute_path, "/mnt/usb_emu/")
        print("Deleting File/Folder: " + upload_dir + relative_path + " from " + absolute_path)
        try:
            dbx.files_delete_v2(upload_dir + relative_path)
        except:
            print("File Not Found")
    for filename in dcmp.diff_files:
        absolute_path = dcmp.right + filename if dcmp.right[-1] == "/" else dcmp.right + "/" + filename
        relative_path = relpath(absolute_path, dcmp.right)
        if isdir(absolute_path):
            print("Creating Folder: " + upload_dir + relative_path + " from " + absolute_path)
            dbx.files_create_folder_v2(upload_dir + relative_path, autorename=False)
        else:
            print("Uploading File: " + upload_dir + relative_path + " from " + absolute_path)
            dbx.files_upload(open(absolute_path, "rb").read(), upload_dir + relative_path, mode=dropbox.files.WriteMode("overwrite"),
                             mute=True, autorename=False)
    for cmp in dcmp.subdirs.values():
        print("Running sync_dbx on subdirectory: " + cmp.right)
        sync_dbx(cmp)

system("mount /mnt/usb_emu/")
system("rm -rf /home/pi/usb_mirror/*")
system("cp -r /mnt/usb_emu/. /home/pi/usb_mirror/")
system("umount /mnt/usb_emu/")

while True:
    sleep(1)
    system("mount /mnt/usb_emu/")
    comparison = filecmp.dircmp("/home/pi/usb_mirror/", "/mnt/usb_emu/")
    print("Running sync_dbx")
    sync_dbx(comparison)
    system("rm -rf /home/pi/usb_mirror/*")
    system("cp -r /mnt/usb_emu/. /home/pi/usb_mirror/")
    system("umount /mnt/usb_emu/")
