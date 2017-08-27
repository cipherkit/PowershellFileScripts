cls
. F:\DropBox\Invoke-Parallel.ps1

# Script that takes a FileSpace of the first parameter and copies files to an archive 
# at a directory of the second parameter with chunk size of third parameter a fourth
# parameter is the descriptive codename with which each achive and the parent directory
# is to be named. Text-docs-1.zip, Text-docs-2.zip, etc

$ORIGINDIR = "F:\Dropbox\Documents\Backup\Music"
$ARCHIVEDIR = "F:\Archive"
$MB = 1024 * 1024
$CHUNKSIZE = 100 * $MB
$CODENAME = "Documents-Archive"


# 1. Creates a central archive directory for the archives to be stored according to
#    Parameter two checking to see that it's empty.
mkdir $ARCHIVEDIR
$directoryInfo = Get-ChildItem $ARCHIVEDIR
if($directoryInfo.Count -ne 0) {
    echo "Target directory is not empty"
    Exit("GOODBYE")
}

# 2. Divide the work of the main filespace into several filespaces based on the size of 
#    the files. A fit is determined so that it doesn't bust out of chunk size.

$chunks = @()
$Size = 0
$chunk = @() 
$i = 0
ForEach($OBJECT in Get-ChildItem -Recurse $ORIGINDIR) { 
    if(($Size + $OBJECT.Length) -le $CHUNKSIZE) {
        $chunk += $OBJECT
        $Size = $Size + $OBJECT.Length
    } else {
        $Size = 0
        $chunk += $OBJECT
        $chunk_map = @{
            position = $i; 
            chunk = $chunk
        } 
        $chunks += $chunk_map
        $chunk = @()
        $i += 1
    }
}
if($chunk.Length -ge 1) {
    $chunk_map = @{
        position = $i; 
        chunk = $chunk
    }
    $chunks += $chunk_map
}
$CHUNKLENGTH = $chunks.Length

# 3. The program appends each file manifest onto a central manifest stored in
#    the central directory. There is a line that describes which folder and archive 
#    the files underneath are in.

New-Item         -Path $ARCHIVEDIR\$CODENAME.txt -ItemType File
Set-ItemProperty -Path $ARCHIVEDIR\$CODENAME.txt -Name IsReadOnly -Value $false
Add-Content $ARCHIVEDIR\$CODENAME.txt "########## Manifest for $CODENAME ##########"
$CHUNKY = $chunks
ForEach($CHUNKITEM in $CHUNKY) {
    $i = $CHUNKY.IndexOf($CHUNKITEM)
    Add-Content $ARCHIVEDIR\$CODENAME.txt "########## Manifest for $CODENAME-$i ##########"
    foreach($ITEM in $CHUNKITEM.chunk) {
        Add-Content $ARCHIVEDIR\$CODENAME.txt -value $ITEM.BaseName
    }
}

# 4. Splits into threads which take the codename, a file subspace given to them and the
#    location of the archive.

Invoke-Parallel -InputObject $chunks -Throttle 6  -ImportVariables -ScriptBlock {

# 5. Thread creates a manifest of the files in a text file. Saves the file named after 
#    codename and the thread instance number. 

    $INVOKEDCHUNK = $_
    $POSITION = $INVOKEDCHUNK.position
    Write-Output "Create a Directory named: $CODENAME-$POSITION"

# 6. Thread creates a directory named after the codename followed by the thread
#    instance number. 

    New-Item         -Path $ARCHIVEDIR\$CODENAME-$POSITION -ItemType Directory 
    New-Item         -Path $ARCHIVEDIR\$CODENAME-$POSITION\$CODENAME-$POSITION.txt -ItemType File
    Set-ItemProperty -Path $ARCHIVEDIR\$CODENAME-$POSITION\$CODENAME-$POSITION.txt -Name IsReadOnly -Value $false
    Add-Content $ARCHIVEDIR\$CODENAME-$POSITION\$CODENAME-$POSITION.txt "########## Manifest for archive $POSITION ##########"

   $CH = $INVOKEDCHUNK.chunk
# 7. Finally, thread zips the files and saves the archive named after the codename and the 
#    thread instance number into the directory named the same.

   ForEach ($DIROB in $CH) {
        $OLDPATH = $DIROB.FullName 
        $NEWPATH = $OLDPATH.Replace($ORIGINDIR, "$ARCHIVEDIR\$CODENAME-$POSITION")
        $TEXTPATH = $OLDPATH.Replace("$ORIGINDIR\", "")
        Add-Content $ARCHIVEDIR\$CODENAME-$POSITION\$CODENAME-$POSITION.txt -value "$TEXTPATH`n"
        $isFILE = (Get-Item $OLDPATH) -is [System.IO.FileInfo]
        if(-Not (Test-Path $NEWPATH) ) {
            New-Item -Path $NEWPATH -ItemType Directory
        }
        Copy-Item -Path $OLDPATH -Destination $NEWPATH
    }
    Compress-Archive -Path $ARCHIVEDIR\$CODENAME-$POSITION -DestinationPath $ARCHIVEDIR\$CODENAME-$POSITION.Zip 
    Remove-Item -Path $ARCHIVEDIR\$CODENAME-$POSITION -Recurse
}

