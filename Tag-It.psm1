

function Tag-It {
param ([string[]]$FILE, [string[]]$TAGS)
    # Write-Output "tagging... $FILE $TAGS"
    
    tmsu tag $FILE $TAGS
    while($LASTEXITCODE -eq -1) {
        Write-Output $LASTEXITCODE
        $TIMER = Get-Random -Maximum 1000 -Minimum 100
        Start-Sleep -Miliseconds $TIMER
        tmsu tag $FILE $TAGS
    }
}
