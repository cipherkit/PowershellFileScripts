cls

$DropBoxPath = "F:\Dropbox"
$DropDocsPath = "F:\Dropbox\Documents"
$BertrandPath = "F:\Dropbox\Documents\Bertrand File"
. $DropBoxPath\Invoke-Parallel.ps1
Import-Module -Name F:\DropBox\Tag-It.psm1

Write-Output "Gathering Files..."
$FILESPACE = Get-ChildItem -Recurse  $BertrandPath
Write-Output "Starting to tag."

Invoke-Parallel -InputObject $FILESPACE -Throttle 1 -LogFile F:\DropBox\ResultsBertrand.txt -ImportModules -ImportVariables -ScriptBlock {
    cd $DropBoxPath
    if($_ -is [System.IO.FileInfo]) {
        $FullName = $_.FullName
        $DIR = $_.DirectoryName
        $EXT = $_.Extension
        $DATE = $_.CreationTime.Date.toString().Split(" ").Get(0)
        $TIME = $_.CreationTime.Hour.toString() + ":" + $_.CreationTime.Minute.toString() + ":" + $_.CreationTime.Second.toString()
        #Write-Output "This is the pipe-output $_" #DEBUG
        #Write-Output "this is the Directory $DIR" #DEBUG
        [array]$SPLITDIR = $DIR.Split("\")
        $DIRCOUNT = $SPLITDIR.Count
        #Write-Output "length is $DIRCOUNT" #DEBUG   
        $TAGS = ""
        while($SPLITDIR.Get($DIRCOUNT - 1) -ne "Bertrand File" -or $DIRCOUNT -le 3) {
            $TAGS = $TAGS + " " + $SPLITDIR.Get($DIRCOUNT - 1)
            $DIRCOUNT = $DIRCOUNT - 1        
        }
        $OUTPUT = $TAGS + " " + $EXT.split(".") + " " + "date=" + $DATE + " " + "time=" + $TIME
        Write-Output $OUTPUT
    } else {
        #If we find Empty folders along the way we Tag them with the Dead dir tag 
        if($_.GetFiles().Count -eq 0) {
            $DIR = $_.FullName
            Write-Output "$DIR DeadDir"
            # Tag-It $DIR DeadDir
        }      
    }
}