#!/usr/bin/env bash
# Tao lich su commit chuan: 3 commit ha tang + MOI TEST CASE 1 COMMIT.  (Git Bash / Linux / macOS)
#   bash scripts/commit_all.sh          # chi commit
#   bash scripts/commit_all.sh --push   # commit xong push len GitHub
set -euo pipefail

git rev-parse --is-inside-work-tree >/dev/null 2>&1 || { echo "Chua git init. Chay: git init -b main"; exit 1; }
if [ -n "$(git ls-files .env)" ]; then echo "CANH BAO: .env dang bi theo doi - chay: git rm --cached .env"; exit 1; fi

commit_step() {
  local msg="$1"; shift
  git add -- "$@"
  if ! git diff --cached --quiet; then
    git commit -q -m "$msg"; echo "[commit] $msg"
  else
    echo "[bo qua - khong co thay doi] $msg"
  fi
}

commit_step "chore: khoi tao du an E2E (README, requirements, pytest.ini, .gitignore, .env.example)" \
  README.md .gitignore requirements.txt pytest.ini .env.example screenshots/.gitkeep reports/.gitkeep
commit_step "feat: ha tang chay test (config, conftest, xuat bao cao Excel, anh chup khi loi)" \
  config.py conftest.py utils
commit_step "feat(pages): Page Object trang dang nhap (BasePage, LoginPage, HomePage, ForgotPasswordPage)" \
  pages

for f in $(ls tests/test_tc*.py | sort); do
  base=$(basename "$f" .py)                       # test_tc01_mo_trang_dang_nhap
  id=$(echo "$base" | sed -E 's/^test_(tc[0-9]+)_.*/\1/' | tr 'a-z' 'A-Z')
  name=$(echo "$base" | sed -E 's/^test_tc[0-9]+_//' | tr '_' ' ')
  commit_step "test(login): $id - $name" "$f"
done

commit_step "chore: them script tao lich su commit" scripts

[ "${1:-}" = "--push" ] && git push -u origin main
echo "Xong. Xem lich su: git log --oneline"
