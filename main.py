from os import access
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as selEc
from selenium.webdriver.common.by import By as selBy
from selenium.webdriver.support.ui import WebDriverWait
import json, time, threading, random, sys
from modules.spotify import links, xpaths

import requests, json
import time, os, sqlite3, random, string, shutil

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, HardwareType

from tqdm import tqdm

def random_user_agent() -> str: return UserAgent(software_names=[SoftwareName.ANDROID.value], hardware_types={HardwareType.MOBILE.value}, limit=100).get_random_user_agent()
def get_random_name() -> str: return json.loads(requests.get("https://api.namefake.com/").text)["name"]
def get_random_string(length: int) -> str: return "".join(random.choice(string.ascii_lowercase+string.digits) for i in range(length))
def get_random_text(length: int) -> str: return "".join(random.choice(string.ascii_lowercase) for i in range(length))

import time, sqlite3

from src.chrome import Chrome
from src.proxy.proxy import Proxy
from src.recaptcha.captcha_solve import solve

def create_account(driver, i):
    driver.get("https://www.spotify.com/us/signup"); time.sleep(5)
    try: driver.find_element(selBy.XPATH, '//button[@id="onetrust-accept-btn-handler"]').click(); time.sleep(3.5)
    except Exception:
        driver.find_element(selBy.XPATH, "/html/body/div[4]/div[3]/div/div[2]/button").click(); time.sleep(3.5)
    name: str = get_random_name()
    passwrd: str = "Vojko12332"
    email: str = name.lower().replace(" ", "") + "@" + get_random_text(5) + ".com"
    _email = driver.find_element(selBy.XPATH, "//input[@id='email']"); _email.click(); _email.send_keys(email); time.sleep(0.5)
    _email = driver.find_element(selBy.XPATH, "//input[@id='confirm']"); _email.click(); _email.send_keys(email); time.sleep(0.5)
    __name = driver.find_element(selBy.XPATH, "//input[@id='displayname']"); __name.click(); __name.send_keys(name); time.sleep(0.5)
    _password = driver.find_element(selBy.XPATH, "//input[@id='password']"); _password.click(); _password.send_keys(passwrd); time.sleep(0.5)
    try: driver.find_element(selBy.XPATH, "//input[@id='gender_option_male']").click(); time.sleep(0.5)
    except Exception: driver.find_element(selBy.XPATH, "/html/body/div[1]/main/div[2]/div/form/fieldset/div/div[1]/label/span[1]").click(); time.sleep(0.5)
    driver.find_element(selBy.XPATH, "//select[@id='month']/option[@value='01']").click(); time.sleep(0.5)
    day = driver.find_element(selBy.XPATH, "//input[@id='day']"); day.click(); day.send_keys("01"); time.sleep(0.5)
    year = driver.find_element(selBy.XPATH, "//input[@id='year']"); year.click(); year.send_keys("1987"); time.sleep(0.5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)"); time.sleep(1.5)
    driver.find_element(selBy.XPATH, "//iframe[@title='reCAPTCHA']").click(); time.sleep(5)
    solve(driver, i)
    time.sleep(2.5)
    driver.find_elements(selBy.XPATH, "//button[@type='submit']")[0].click()
    time.sleep(7)
def run(_url, _headless, i=None, proxy=None):
    Proxy(proxy, i)
    chrome = Chrome()
    browser = webdriver.Chrome(executable_path=chrome.CHROMEDRIVER, options=chrome.options(i=i, proxy=proxy))
    chrome.execute(browser)
    create_account(browser, i)
    wait = WebDriverWait(browser, 10)
    # btn = wait.until(selEc.element_to_be_clickable((selBy.XPATH, '//button[@id="onetrust-accept-btn-handler"]'))); btn.click()
    browser.get(_url) if _url else browser.get(links["default"])
    time.sleep(10)
    time.sleep(5)
    # login_btn = wait.until(selEc.element_to_be_clickable((selBy.XPATH, xpaths["login_btn"]))); login_btn.click()
    # user_form = wait.until(selEc.element_to_be_clickable((selBy.XPATH, xpaths["user_form"]))); user_form.send_keys(username)
    # pass_form = wait.until(selEc.element_to_be_clickable((selBy.XPATH, xpaths["pass_form"]))); pass_form.send_keys(password)
    # submit_btn = wait.until(selEc.element_to_be_clickable((selBy.XPATH, xpaths["submit_btn"]))); submit_btn.click()
    shuffle_btn = wait.until(selEc.element_to_be_clickable((selBy.XPATH, xpaths["shuffle_btn"])))
    repeat_btn = wait.until(selEc.element_to_be_clickable((selBy.XPATH, xpaths["repeat_btn"])))

    if "control-button--active" not in shuffle_btn.get_attribute("class"):
        time.sleep(1)
        shuffle_btn.click()

    if "spoticon-repeat-16 control-button--active" in repeat_btn.get_attribute("class"):
        pass
    elif "spoticon-repeatonce-16 control-button--active" in repeat_btn.get_attribute("class"):
        time.sleep(1)
        repeat_btn.click()
        time.sleep(1)
        repeat_btn.click()
    else:
        time.sleep(1)
        repeat_btn.click()
    try:
        play_btn = wait.until(selEc.element_to_be_clickable((selBy.XPATH, xpaths["play_btn"])))
        play_btn.click()
    except:
        play_btn = wait.until(selEc.element_to_be_clickable((selBy.XPATH, "/html/body/div[3]/div/div[2]/div[3]/main/div[2]/div[2]/div/div/div[2]/section/div[3]/div/button[1]")))
        play_btn.click()
    while True:
        time.sleep(random.randint(55, 70))
        song_name = wait.until(selEc.presence_of_element_located((selBy.XPATH, xpaths["song_name"]))).text
        print(" * Played {0} for 3".format(song_name))
        skip_btn = wait.until(selEc.element_to_be_clickable((selBy.XPATH, xpaths["skip_btn"])))
        skip_btn.click()

def init():
    print("\n * Bot started.")
    selUrl = input(" * Insert Spotify playlist url (empty for default): ")
    headless = "--headless" in sys.argv
    # proxies = list(filter(None, open("data/proxies/proxies.txt", "r").read().split("\n")))
    i=0
    threads=[]
    while True:
        i+=1
        if len(threads) == 5:
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
            threads=[]
        threads.append(threading.Thread(target=run, args=[selUrl, headless, i]).start())
        time.sleep(1)

if __name__ == '__main__':
    init()