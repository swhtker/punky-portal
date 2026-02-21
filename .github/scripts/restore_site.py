#!/usr/bin/env python3
"""One-shot Coolify punky-site restore script — runs on GitHub Actions runner."""
import paramiko, sys, os

HOST  = "49.12.236.136"
USER  = "root"
PASS  = os.environ["SSH_PASS"]
UUID  = "ccoss8so04kksc4c80kwgg84"

print(f"Connecting to {HOST}…", flush=True)
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, port=22, username=USER, password=PASS,
               timeout=30, allow_agent=False, look_for_keys=False)
print("SSH connected", flush=True)

NOW_CMD = 'date -u +"%Y-%m-%d %H:%M:%S"'

SQL = (
    "INSERT OR IGNORE INTO applications "
    "(uuid,name,description,environment_id,destination_id,source_id,"
    "git_repository,git_branch,build_pack,base_directory,fqdn,status,"
    "custom_labels,repository_project_id,created_at,updated_at) "
    "VALUES "
    f"(\'{UUID}\','punky-site','Punky landing site',"
    "2,0,1,'swhtker/punky-portal','main','dockerfile','/',"
    "'https://punky.jspriggins.com,https://site.jspriggins.com',"
    "'stopped','',1157959841,"
    "$(\'date -u +\"%Y-%m-%d %H:%M:%S"\'),"
    "$(\'date -u +\"%Y-%m-%d %H:%M:%S"\'));"
)

# Use simpler approach: shell script on server
sh = """
UUID="ccoss8so04kksc4c80kwgg84"
NOW=$(date -u +'%Y-%m-%d %H:%M:%S')
docker exec coolify sqlite3 /data/coolify/database.sqlite "INSERT OR IGNORE INTO applications (uuid,name,description,environment_id,destination_id,source_id,git_repository,git_branch,build_pack,base_directory,fqdn,status,custom_labels,repository_project_id,created_at,updated_at) VALUES (\'$UUID\','punky-site','Punky landing site',2,0,1,'swhtker/punky-portal','main','dockerfile','/','https://punky.jspriggins.com,https://site.jspriggins.com','stopped','',1157959841,\'$NOW\',\'$NOW\');"
echo "--- verify ---"
docker exec coolify sqlite3 /data/coolify/database.sqlite "SELECT uuid,name,source_id,status FROM applications WHERE uuid=\'$UUID\';"
"""

_, stdout, stderr = client.exec_command(sh, timeout=45)
out = stdout.read().decode()
err = stderr.read().decode()
print("STDOUT:", out)
if err: print("STDERR:", err)
client.close()

if UUID in out:
    print("SUCCESS: row verified in Coolify DB")
    sys.exit(0)
else:
    print("WARNING: could not verify row — check manually")
    sys.exit(0)  # non-fatal; deploy step will confirm
