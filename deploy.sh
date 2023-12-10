
rsync -av --filter=':- .gitignore' . opc@158.178.206.102:~/freq-test

ssh opc@158.178.206.102 "bash -lc 'cd ~/freq-test; docker compose up -d;'"
