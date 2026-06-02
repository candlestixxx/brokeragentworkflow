cat << 'INNEREOF' > VERSION.md
0.27.0
INNEREOF
git add VERSION.md
git commit --amend --no-edit
