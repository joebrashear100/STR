# PowerShell Script to Get SharePoint IDs for STR Migration

# Install module if needed
# Install-Module Microsoft.Graph -Scope CurrentUser

# Connect to Microsoft Graph with required scopes
Write-Host "Connecting to Microsoft Graph..." -ForegroundColor Cyan
Connect-MgGraph -Scopes "Sites.Read.All", "Lists.ReadWrite.All", "Files.ReadWrite.All", "Directory.Read.All"

# Define the SharePoint site URL
$siteUrl = "https://deltaairlines.sharepoint.com/sites/DL001597/PDO"

Write-Host "Looking up site: $siteUrl" -ForegroundColor Cyan

# Get the site
try {
    $site = Get-MgSite -Search "DL001597" | Where-Object {$_.WebUrl -eq $siteUrl}
    if (-not $site) {
        Write-Host "Site not found by search, trying alternative method..." -ForegroundColor Yellow
        $site = Get-MgSite -Search "PDO" | Where-Object {$_.WebUrl -eq $siteUrl}
    }
    
    if ($site) {
        $siteId = $site.Id
        Write-Host "✓ Site ID found: $siteId" -ForegroundColor Green
    } else {
        Write-Host "✗ Could not find site. Try this alternative:" -ForegroundColor Red
        Write-Host "Go to SharePoint site > Settings > Site information > copy the Site ID"
        exit 1
    }
}
catch {
    Write-Host "Error getting site: $_" -ForegroundColor Red
    exit 1
}

# Get the STRDocuments library
Write-Host "Looking up STRDocuments library..." -ForegroundColor Cyan
try {
    $drive = Get-MgSiteDrive -SiteId $siteId | Where-Object {$_.Name -eq "STRDocuments"}
    
    if ($drive) {
        $driveId = $drive.Id
        Write-Host "✓ Drive ID found: $driveId" -ForegroundColor Green
    } else {
        Write-Host "Available drives:" -ForegroundColor Yellow
        Get-MgSiteDrive -SiteId $siteId | Select-Object Name, Id
        exit 1
    }
}
catch {
    Write-Host "Error getting drive: $_" -ForegroundColor Red
    exit 1
}

# Get the STR_Review_Log_Post_March_2023 list
Write-Host "Looking up STR_Review_Log_Post_March_2023 list..." -ForegroundColor Cyan
try {
    $list = Get-MgSiteList -SiteId $siteId | Where-Object {$_.DisplayName -eq "STR_Review_Log_Post_March_2023"}
    
    if ($list) {
        $listId = $list.Id
        Write-Host "✓ List ID found: $listId" -ForegroundColor Green
    } else {
        Write-Host "Available lists:" -ForegroundColor Yellow
        Get-MgSiteList -SiteId $siteId | Select-Object DisplayName, Id
        exit 1
    }
}
catch {
    Write-Host "Error getting list: $_" -ForegroundColor Red
    exit 1
}

# Output the IDs in a format we can use
Write-Host "`n" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "SHAREPOINT IDs FOR STR MIGRATION" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "Site ID:  $siteId" -ForegroundColor Green
Write-Host "Drive ID: $driveId" -ForegroundColor Green
Write-Host "List ID:  $listId" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Cyan

# Save to file for use in Python
$ids = @{
    siteId = $siteId
    driveId = $driveId
    listId = $listId
} | ConvertTo-Json

$ids | Out-File -FilePath "$PSScriptRoot/sharepoint_ids.json" -Encoding UTF8

Write-Host "`n✓ IDs saved to: sharepoint_ids.json" -ForegroundColor Green
