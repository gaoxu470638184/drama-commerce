# drama-commerce skill installer (Windows PowerShell)
# 用法：
#   powershell -ExecutionPolicy Bypass -File .\install.ps1
#   powershell -ExecutionPolicy Bypass -File .\install.ps1 -Target C:\path\to\skills
param(
    [string]$Target = ""
)

$ErrorActionPreference = "Stop"
$SkillName = "drama-commerce"
$SrcDir = Split-Path -Parent $MyInvocation.MyCommand.Path

if ([string]::IsNullOrWhiteSpace($Target)) {
    $wb = Join-Path $env:USERPROFILE ".workbuddy"
    $cc = Join-Path $env:USERPROFILE ".claude"
    if (Test-Path $wb) {
        $Target = Join-Path $wb "skills"
    } elseif (Test-Path $cc) {
        $Target = Join-Path $cc "skills"
    } else {
        $Target = Join-Path $cc "skills"
    }
}

$Dest = Join-Path $Target $SkillName

if (Test-Path $Dest) {
    $Backup = "$Dest.bak." + (Get-Date -Format "yyyyMMddHHmmss")
    Write-Host "已存在，备份到：$Backup"
    Move-Item -Path $Dest -Destination $Backup
}

New-Item -ItemType Directory -Path $Target -Force | Out-Null
Copy-Item -Path (Join-Path $SrcDir "*") -Destination $Dest -Recurse -Force

$junk = @(".git", ".github", "examples", "scripts", "install.sh",
          "install.ps1", "CONTRIBUTING.md", "CHANGELOG.md")
foreach ($x in $junk) {
    Remove-Item -Path (Join-Path $Dest $x) -Recurse -Force -ErrorAction SilentlyContinue
}

Write-Host ""
Write-Host "✅ 安装完成：$Dest" -ForegroundColor Green
Write-Host "   文件清单："
Get-ChildItem -Path $Dest -Recurse -File | Sort-Object FullName | ForEach-Object {
    Write-Host ("     " + $_.FullName.Replace($Dest + [IO.Path]::DirectorySeparatorChar, ""))
}
Write-Host ""
Write-Host "👉 重启会话后说「帮我做一条短剧带货视频」即可触发。"
