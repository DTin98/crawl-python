#!/bin/bash
git pull && git add . && git commit -m "add"

/usr/bin/expect <(cat << EOF
spawn git push
expect "Username for 'https://github.com': "
send -- "DTin98\r"
expect "Password for 'https://DTin98@github.com': "
send -- "truongdaitin98\r"
interact
EOF)
