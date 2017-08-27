

function Tag-It {
param ([string[]] $FILE, [string[]] $TAG)
    Write-Output "tagging... `"$FILE`"" "`"$TAG`""
    tmsu tag "`"$FILE`"" "`"$TAG`""
}
