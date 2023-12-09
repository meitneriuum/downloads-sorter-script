# Downlodads Sorter Script

A script that I wrote to keep my Downloads folder in order. 
The script is executed once a day, and:  
1. Deletes files of some types (mostly images) and folders if they were inactive for 24 hours;
2. For other files creates folders indicating the filetype (e.g. '.exe') and moves them to this folder.

Also the script keeps track of the folders and files that should not be deleted (e.g. the folders like '.exe' and 'archives' will not be deleted if they were previously created during script execution). The "whitelist" of the files and folders that should be ignored is saved to meta.json file.
