#!/usr/bin/env bash
set -euo pipefail

# Usage: ./scripts/new-project.sh <project-name> [target-directory]
# Creates a new project scaffold based on the dev_playbook templates.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLAYBOOK_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TEMPLATES_DIR="$PLAYBOOK_ROOT/templates"

PROJECT_NAME="${1:-}"
TARGET_DIR="${2:-$(pwd)/$PROJECT_NAME}"
DATE="$(date +%Y-%m-%d)"

if [[ -z "$PROJECT_NAME" ]]; then
  echo "Usage: $0 <project-name> [target-directory]"
  exit 1
fi

if [[ -e "$TARGET_DIR" ]]; then
  echo "Error: target directory already exists: $TARGET_DIR"
  exit 1
fi

echo "Creating project '$PROJECT_NAME' in '$TARGET_DIR'..."

# --- Directory structure (§2.1) ---
mkdir -p "$TARGET_DIR"/{docs/{prd,adr,runbooks,api},src,tests,scripts,ci/adapters,compat-data,compatibility,surveillance,.config}

# --- Copy and personalise templates ---
copy_template() {
  local src="$1"
  local dst="$2"
  sed \
    -e "s/{{PROJECT_NAME}}/$PROJECT_NAME/g" \
    -e "s/{{DATE}}/$DATE/g" \
    -e "s/{{AUTHOR}}/${USER:-unknown}/g" \
    "$src" > "$dst"
}

copy_template "$TEMPLATES_DIR/AI-AGENTS.md"      "$TARGET_DIR/AI-AGENTS.md"
copy_template "$TEMPLATES_DIR/CLAUDE.md"         "$TARGET_DIR/CLAUDE.md"
copy_template "$TEMPLATES_DIR/GEMINI.md"         "$TARGET_DIR/GEMINI.md"
copy_template "$TEMPLATES_DIR/PROJECT_STATUS.md" "$TARGET_DIR/PROJECT_STATUS.md"
copy_template "$TEMPLATES_DIR/DEPENDENCIES.md"   "$TARGET_DIR/DEPENDENCIES.md"
copy_template "$TEMPLATES_DIR/CHANGELOG.md"      "$TARGET_DIR/CHANGELOG.md"
copy_template "$TEMPLATES_DIR/COMPATIBILITY.md"  "$TARGET_DIR/COMPATIBILITY.md"

copy_template "$TEMPLATES_DIR/docs/prd/00-prd.md"              "$TARGET_DIR/docs/prd/00-prd.md"
copy_template "$TEMPLATES_DIR/docs/adr/001-template.md"        "$TARGET_DIR/docs/adr/001-template.md"
copy_template "$TEMPLATES_DIR/docs/runbooks/runbook-template.md" "$TARGET_DIR/docs/runbooks/runbook-template.md"

# --- Placeholder files to keep empty dirs in git ---
for dir in src tests ci/adapters compat-data compatibility surveillance .config docs/api; do
  touch "$TARGET_DIR/$dir/.gitkeep"
done

# --- Minimal README ---
cat > "$TARGET_DIR/README.md" <<EOF
# $PROJECT_NAME
EOF

# --- .gitignore ---
cat > "$TARGET_DIR/.gitignore" <<'EOF'
.DS_Store
*.log
node_modules/
__pycache__/
.env
.env.*
!.env.example
dist/
build/
EOF

echo ""
echo "Done. Project structure created at: $TARGET_DIR"
echo ""
echo "Next steps:"
echo "  1. cd $TARGET_DIR"
echo "  2. git init && git add . && git commit -m 'feat: initial project scaffold'"
echo "  3. Fill in AI-AGENTS.md with project-specific rules."
echo "  4. Fill in docs/prd/00-prd.md before writing any code."
