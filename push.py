import os

commit = input("[+] Enter the commit message :- ")

if not commit.strip():
    print("[!] Error: Commit message cannot be empty!")
else:
    os.system("git add .")
    # Single quotes ki jagah double quotes use karna better hai for messages
    os.system(f'git commit -m "Changes :- {commit}"')
    os.system("git push origin main")
    print("[*] Push successful!")