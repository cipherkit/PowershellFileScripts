cls

$DropBoxPath = "F:\Dropbox"
$DropBoxBertrand = "F:\Dropbox\Bertrand File"
$DropBoxBackup = "F:\Dropbox\Backup"
$DropDocsPath = "F:\Dropbox\Documents"

. $DropBoxPath\Invoke-Parallel.ps1
Import-Module -Name F:\DropBox\Tag-It.psm1

Write-Output "Gathering Files..."
$FILESPACE = Get-ChildItem -Recurse  $DropBoxPath
Write-Output "Starting to tag."
Invoke-Parallel -InputObject $FILESPACE -Throttle 1 -LogFile F:\DropBox\Results.txt -ImportModules -ImportVariables -ScriptBlock {
    cd $DropBoxPath
    if($_ -is [System.IO.FileInfo]) {
        $FullName = $_.FullName
        $DIR = $_.DirectoryName
        $EXT = $_.Extension
        # Write-Output "This is the pipe-output $_" #DEBUG
        # Write-Output "this is the Directory $DIR" #DEBUG
        [array]$SPLITDIR =  $DIR.Split("\")
        $DIRCOUNT = $SPLITDIR.Count
        # Write-Output "length is $DIRCOUNT" #DEBUG   

        #This takes care of the Non-Documents folders while at the same time 
        #Tagging Documents with the Documents tag
        $INBOX = ""
        if($SPLITDIR.Get($DIRCOUNT - 1) -eq "Dropbox" -or $SPLITDIR.Get($DIRCOUNT - 1) -eq "Bertrand File" -or $SPLITDIR.Get($DIRCOUNT - 1) -eq "Backup") {
            $INBOX = "Inbox"
        }    
        while($SPLITDIR.Get($DIRCOUNT - 1) -ne "Dropbox") {
            Tag-It $FullName $SPLITDIR.Get($DIRCOUNT - 1)
            $DIRCOUNT = $DIRCOUNT - 1    
        }    
        $OUTPUT = "{0} {1} {2}" -f $EXT, $INBOX, $TAGS
        if($EXT) {
            Tag-It $FullName $EXT
        }
        if($INBOX) {
            Tag-It $FullName $INBOX
        }
    } else {
        #If we find Empty folders along the way we Tag them with the Dead dir tag 
        if($_.GetFiles().Count -eq 0) {
            $DIR = $_.FullName
            Tag-It $DIR DeadDir
            while($LASTEXITCODE -eq -1) {
                Write-Output $LASTEXITCODE
                $TIMER = Get-Random -Maximum 1000 -Minimum 100
                Start-Sleep -Miliseconds $TIMER
                tmsu tag $DIR DeadDir
            }
        }      
    }
}