# Tao lich su commit chuan: 3 commit ha tang + MOI TEST CASE 1 COMMIT.
# Chay tai thu muc goc du an (da git init):
#     powershell -ExecutionPolicy Bypass -File scripts\commit_all.ps1          # chi commit
#     powershell -ExecutionPolicy Bypass -File scripts\commit_all.ps1 -Push    # commit xong push len GitHub
param([switch]$Push)
$ErrorActionPreference = "Stop"

git rev-parse --is-inside-work-tree *> $null
if ($LASTEXITCODE -ne 0) { Write-Host "Chua git init. Chay: git init -b main" -ForegroundColor Red; exit 1 }

if (git ls-files .env) { Write-Host "CANH BAO: .env dang bi theo doi - hay chay: git rm --cached .env" -ForegroundColor Red; exit 1 }

function Commit-Step([string]$Message, [string[]]$Paths) {
    git add -- $Paths
    git diff --cached --quiet
    if ($LASTEXITCODE -ne 0) {
        git commit -m $Message | Out-Null
        Write-Host "[commit] $Message" -ForegroundColor Green
    } else {
        Write-Host "[bo qua - khong co thay doi] $Message" -ForegroundColor DarkGray
    }
}

Commit-Step "chore: khoi tao du an E2E (README, requirements, pytest.ini, .gitignore, .env.example)" `
    @("README.md", ".gitignore", "requirements.txt", "pytest.ini", ".env.example", "screenshots/.gitkeep", "reports/.gitkeep")
Commit-Step "feat: ha tang chay test (config, conftest, xuat bao cao Excel, anh chup khi loi)" `
    @("config.py", "conftest.py", "utils")
Commit-Step "feat(pages): Page Object trang dang nhap (BasePage, LoginPage, HomePage, ForgotPasswordPage)" `
    @("pages")

# MOI TEST CASE = 1 COMMIT (sap xep theo ten file: tc01, tc02, ...)
Get-ChildItem tests -Filter "test_tc*.py" | Sort-Object Name | ForEach-Object {
    if ($_.BaseName -match '^test_(tc\d+)_(.+)$') {
        $id   = $Matches[1].ToUpper()
        $name = $Matches[2] -replace '_', ' '
        Commit-Step "test(login): $id - $name" @("tests/$($_.Name)")
    }
}

Commit-Step "chore: them script tao lich su commit" @("scripts")

if ($Push) { git push -u origin main }
Write-Host "Xong. Xem lich su: git log --oneline" -ForegroundColor Cyan
