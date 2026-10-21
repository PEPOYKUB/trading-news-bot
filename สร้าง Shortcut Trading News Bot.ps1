$project = Split-Path -Parent $MyInvocation.MyCommand.Path
$desktop = [Environment]::GetFolderPath('Desktop')
$shortcutPath = Join-Path $desktop 'Trading News Bot.lnk'
$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = Join-Path $project 'เปิด Trading News Bot.bat'
$shortcut.WorkingDirectory = $project
$shortcut.Description = 'เปิด Trading News Intelligence Bot'
$shortcut.IconLocation = "$env:SystemRoot\System32\SHELL32.dll,13"
$shortcut.Save()
Write-Host "สร้าง Shortcut ที่: $shortcutPath"
Read-Host 'กด Enter เพื่อปิด'
