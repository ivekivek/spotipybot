from array import array
import requests, json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager as CM
import time, os, sqlite3, random, string, shutil

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, HardwareType

from tqdm import tqdm

def random_user_agent() -> str: return UserAgent(software_names=[SoftwareName.ANDROID.value], hardware_types={HardwareType.MOBILE.value}, limit=100).get_random_user_agent()
def get_random_name() -> str: return json.loads(requests.get("https://api.namefake.com/").text)["name"]
def get_random_string(length: int) -> str: return "".join(random.choice(string.ascii_lowercase+string.digits) for i in range(length))
def get_random_text(length: int) -> str: return "".join(random.choice(string.ascii_lowercase) for i in range(length))

def make_account(proxy: string=None) -> any:
    name: str = get_random_name()
    passwrd: str = "Vojko12332"
    email: str = name.lower().replace(" ", "") + "@" + get_random_text(5) + ".com"
    headers = {
        "Accept-Encoding": "gzip",
        "Accept-Language": "en-US",
        "App-Platform": "Android",
        "Connection": "Keep-Alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "spclient.wg.spotify.com",
        "User-Agent": f"{random_user_agent()}",
        "Spotify-App-Version": "8.6.26",
        "X-Client-Id": get_random_string(32)
    }     
    data = {
        "creation_point": "client_mobile",
        "gender": "male" if random.randint(0, 1) else "female",
        "birth_year": random.randint(1990, 2000),
        "displayname": name,
        "iagree": "true",
        "birth_month": random.randint(1, 11),
        "password_repeat": passwrd,
        "password": passwrd,
        "key": "142b583129b2df829de3656f9eb484e6",
        "platform": "Android-ARM",
        "email": email,
        "birth_day": random.randint(1, 20)
    }
    if proxy != None:
        proxies = { "http": "http://" + proxy }
        res = requests.post(
            'https://spclient.wg.spotify.com/signup/public/v1/account/',
            headers=headers,
            data=data,
            proxies=proxies
        )
    else:
        res = requests.post(
            'https://spclient.wg.spotify.com/signup/public/v1/account/',
            headers=headers,
            data=data
        )

    print(res.status_code)

    if res.status_code == 200:
        if not os.path.exists("db"):
            os.makedirs("db")
        con = sqlite3.connect("db/database.db")
        cur = con.cursor()
        try: cur.execute("CREATE TABLE accounts (email TEXT, password TEXT)")
        except: pass
        cur.execute(f'INSERT INTO accounts VALUES ("{email}", "{passwrd}")')
        con.commit()
        con.close()
        print("done")

def get_proxies():
    try:
        arr = []
        link_list = ['https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt', 'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt', 'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt', 'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt', 'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/proxy.txt', 'https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt']
        for link in link_list:
            for proxy in requests.get(link).content.decode().split("\n"):
                arr.append(proxy)
        return arr
    except Exception as e:
        print(e)

def split(arr, size):
    arrs = []
    while len(arr) > size:
        arrs.append(arr[:size])
        arr = arr[size:]
    arrs.append(arr)
    return arrs

# proxies = get_proxies()

import threading
# i=0
# while i<250000:
#     try:
#         threads = []
#         for proxy in proxies:
#             # make_account(proxy)
#             threading.Thread(target=make_account, args=[proxy]).start()
#     except Exception as e:
#         print(e)
#     i+=1

proxies = list(filter(None, open("proxies/proxies.txt", "r").read().split("\n")))
# os.remove("db/database.db")
shutil.rmtree("db")
while True:
    for proxy in proxies:
        user = proxy.split(":")[2]
        passwrd = proxy.split(":")[3]
        ip = proxy.split(":")[0]
        port = proxy.split(":")[1]
        proxy_ = f"{user}:{passwrd}@{ip}:{port}"
        threading.Thread(target=make_account(), args=[proxy_]).start()