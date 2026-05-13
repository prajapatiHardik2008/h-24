import os

commit = input("[+] Enter the commit message :- ")

if not commit.strip():
    print("[!] Error: Commit message cannot be empty!")

else:

    add_status = os.system("git add .")

    commit_status = os.system(
        f'git commit -m "Changes :- {commit}"'
    )

    if commit_status != 0:
        print("[!] Commit failed or nothing to commit.")

    else:
        push_status = os.system("git push origin main")

        if push_status == 0:
            print("[*] Push successful!")

        else:
            print("[!] Push failed!")