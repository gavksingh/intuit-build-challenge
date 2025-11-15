#!/usr/bin/env bash
set -e

mkdir -p pc_001 sa_001
touch README.md requirements.txt
touch pc_001/__init__.py sa_001/__init__.py

cat > .gitignore << 'EOF'
# Python
__pycache__/
*.pyc

# Environments
.venv/
env/
venv/

# IDE / editor
.vscode/
.idea/
*.swp

# Cursor
.cursor/
EOF

cat > README.md << 'EOF'
# Intuit Build Challenge

This repository contains solutions to the Intuit coding challenge:

- **PC-001**: Producer–Consumer pattern with thread synchronization.
- **SA-001**: Sales analysis using CSV data and functional-style operations.
EOF

cat > requirements.txt << 'EOF'
pandas
pytest
EOF
