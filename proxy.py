from textwrap import dedent
import os
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

########################################################################################################################
# Functions

BASE_DIR = os.path.dirname(os.path.abspath("file"))


def get_proxy_auth_extension(proxy):
    if proxy.strip() == '':
        return None
    cred, prox = proxy.split('@')
    PROXY_USER, PROXY_PASS = cred.split(':')
    PROXY_HOST, PROXY_PORT = prox.split(':')
    manifest_json = """
                    {
                        "version": "1.0.0",
                        "manifest_version": 2,
                        "name": "Chrome Proxy",
                        "permissions": [
                            "proxy",
                            "tabs",
                            "unlimitedStorage",
                            "storage",
                            "<all_urls>",
                            "webRequest",
                            "webRequestBlocking"
                        ],
                        "background": {
                            "scripts": ["background.js"]
                        },
                        "minimum_chrome_version":"22.0.0"
                    }
                    """

    background_js = """
                    var config = {
                            mode: "fixed_servers",
                            rules: {
                            singleProxy: {
                                scheme: "http",
                                host: "%s",
                                port: parseInt(%s)
                            },
                            bypassList: ["localhost"]
                            }
                        };

                    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

                    function callbackFn(details) {
                        return {
                            authCredentials: {
                                username: "%s",
                                password: "%s"
                            }
                        };
                    }

                    chrome.webRequest.onAuthRequired.addListener(
                                callbackFn,
                                {urls: ["<all_urls>"]},
                                ['blocking']
                    );
                    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)
    fn = os.path.join(BASE_DIR, 'proxy_ext')
    if not os.path.exists(fn):
        os.mkdir(fn)
    m_path = os.path.join(fn, "manifest.json")
    b_path = os.path.join(fn, "background.js")
    with open(m_path, 'w') as f:
        f.write(dedent(manifest_json))
    with open(b_path, 'w') as f:
        f.write(dedent(background_js))
    return fn


def get_file_data(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        data = file.read().strip().split('\n')
    return data

with open('proxies.txt', 'r') as file:
    # Iterate over each line in the file
    for line in file:
        # Do something with each line, for example, print it
        print(line.strip())


my_proxy = random.choice(get_file_data("proxies.txt"))
options = webdriver.ChromeOptions()

proxy = get_proxy_auth_extension(my_proxy)
options.add_argument(f'--load-extension={proxy}')
driver = webdriver.Chrome(options=options)
driver.maximize_window()

driver.get("https://whatismyipaddress.com/")
input("addd: ")



#addproxy like this: username:psswd@ip:port




driver.quit()