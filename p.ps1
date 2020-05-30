$username="AMBrown0"
$password="@li%M05US6aq"
$shell_command='git push https://' + $username+ ":" + $password + '@github.com/AMBrown0/DataVizAss01.git --all'
Write-Host $shell_command
#Invoke-Command $shell_command