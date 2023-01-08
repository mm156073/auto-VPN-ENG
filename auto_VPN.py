# https://askubuntu.com/questions/774908/provide-password-to-nmcli-con-up-in-terminal-14-04

import os
from typing import List
import subprocess

from selenium import webdriver
from selenium.webdriver.common.by import By
import yaml

URL = "https://tauth-plgw1.t.u-tokyo.ac.jp/ui/"

def get_onetime_pass(params) -> List:
    pattern_list = []
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    browser = webdriver.Chrome(options=options)
    
    browser.get(URL)

    user_id = browser.find_element(By.ID, "uid")
    user_id.send_keys(params["ID"])
    submit = browser.find_element(By.CLASS_NAME, "passlogic_css_submit")
    submit.click()


    tables = ["randamNumbarTable1st", "randamNumbarTable2nd", "randamNumbarTable3rd"]
    for table_name in tables:
        table_1 = browser.find_element(By.ID, table_name)
        boxes = table_1.find_elements(By.CLASS_NAME, "randamNumberBoxRadius")
        for box in boxes:
            num = box.find_element(By.TAG_NAME, "p")
            pattern_list.append(num.text)
    password_list = [pattern_list[idx] for idx in params["PATTERN"]]
    password = ""
    for string in password_list:
        password += string
    return password

def main(params):
    password = "vpn.secrets.password:" + get_onetime_pass(params) + params["SECRET"]
    with open(params["FILE_NAME"], "w") as f:
        f.write(password)
    res = subprocess.run(["nmcli", "con", "up", "id", params["VPN"], "passwd-file", params["FILE_NAME"]])
    os.remove(params["FILE_NAME"])

if __name__ == "__main__":
    with open('params.yaml') as file:
        params = yaml.safe_load(file)
    main(params)