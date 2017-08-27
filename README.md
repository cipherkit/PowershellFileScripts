# PowershellFileScripts
Scripts for manipulating files on Windows or other powershell based systems.

## Archive Script

This script will create Zip archives of about a certain size. It includes a master manifest of all files in the Zip files and Zip file manifests in the Zip file itself. The script greedily divides the files into the directories to be Zipped.

## Tagging Script

This script uses [TMSU](https://tmsu.org/) to tag files in an existing database. It is meant to be used with a structured file system as it will use directories as tags in addition to other metadata.
