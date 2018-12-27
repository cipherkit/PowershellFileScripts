cls

. F:\dropbox/scripts/Invoke-Parallel.ps1
#Script that deletes empty directories after putting the information on a list

$ORIGINDIR = "F:\owner"
$CODENAME = "Deleted Directories"
$FILESPACE = Get-ChildItem -Recurse -Directory $ORIGINDIR
$MaxThreads = 20

$Length = $FILESPACE.Length
$ChunkSize = [Math]::Round($Length / $MaxThreads) + 1

Write-Output $ChunkSize
$chunks = @()
$chunk = @()
foreach($Item in $FILESPACE) {
    if(($FILESPACE.IndexOf($Item) % $ChunkSize) -ne 0) {
        $chunk += $Item
    } else {
        $chunk += $Item
        $chunks += $chunk
        $chunk = @()
    }
}

Invoke-Parallel -InputObject $chunks -Throttle $MaxThreads  -ImportVariables -ScriptBlock {
    $CH = $_
    foreach($DIROB in $CH) {
        $OLDPATH = $DIROB.FullName
        $isFILE = (Get-Item $OLDPATH) -is [System.IO.FileInfo]
        $isDIR = (Get-Item $OLDPATH) -is [System.IO.DirectoryInfo]
        # Write-Output "isFile? " + $isFILE
        if($isFILE) {
            # Do nothing
        } else {
            if($isDIR) {
                if($DIROB.getFiles().count -eq 0 -and $DIROB.getDirectories().count -eq 0) {
                    Write-Output "Removed: $OLDPATH"
                    Remove-Item $OLDPATH
                }
            }
        }
    }
}