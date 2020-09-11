from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver_path = "C:\\Users\\Nour\\Desktop\\work\\InstagramBot\\chromedriver.exe"
brave_path = "C:\\Program Files (x86)\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
chrome = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"



class InstagramBot:
    def __init__(self):
        self.username = None
        self.password = None
        self.option = webdriver.ChromeOptions()
        self.option.binary_location = brave_path
        self.option.add_argument("--incognito")
        self.browser = webdriver.Chrome(executable_path=driver_path, chrome_options=self.option)
        self.browser.get("https://www.instagram.com")


    def login(self, username, password):
        # self.browser.maximize_window()
        # element paths with XPATH
        username_field_path = '//*[@id="loginForm"]/div/div[1]/div/label/input'
        password_field_path = '//*[@id="loginForm"]/div/div[2]/div/label/input'
        login_butten_path = '//*[@id="loginForm"]/div/div[3]'
        dont_save_pass_path = '//*[@id="react-root"]/section/main/div/div/div/div/button'
        no_notifcation_path = '/html/body/div[4]/div/div/div/div[3]/button[2]'


        self.username = username
        self.password = password

        # username field
        username_field = self.wait_for(username_field_path)
        username_field.send_keys(username)

        password_field = self.wait_for(password_field_path)
        password_field.send_keys(password)

        login_butten = self.wait_for(login_butten_path)
        login_butten.click()

        # Do not save login info
        login_save_pass = self.wait_for(dont_save_pass_path)
        login_save_pass.click()

        # Do not turn on notifcation
        no_notifcation = self.wait_for(no_notifcation_path)
        no_notifcation.click()
        self.browser.get("https://www.instagram.com/{}".format(username))

    def get_followers(self):
        followers_path = '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a'
        scroll_box_path = '/html/body/div[4]/div/div/div[2]'
        close_path = '/html/body/div[4]/div/div/div[1]/div/div[2]/button'

        try:
            self.wait_for(followers_path).click()
            scroll_box = self.wait_for(scroll_box_path)
            followers = self._get_names(scroll_box)
            self.wait_for(close_path).click()
        except:
            print('cannt get followers')
            followers = None

        return followers

    def get_following(self):
        following_path = '//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a'
        scroll_box_path = '/html/body/div[4]/div/div/div[2]'
        close_path = '/html/body/div[4]/div/div/div[1]/div/div[2]/button'

        try:
            self.wait_for(following_path).click()
            scroll_box = self.wait_for(scroll_box_path)
            following = self._get_names(scroll_box)
            self.wait_for(close_path).click()
        except:
            print('cannt get following')
            following = None

        return following

    def _get_names(self, scroll_box):
        sleep(2)
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(1)
            ht = self.browser.execute_script("""
                        arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                        return arguments[0].scrollHeight;
                        """, scroll_box)
        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        return names

    def _follow_steam(self, accounts):
        # followers = self.get_followers()
        follow_back_path = \
            '//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/div/div/div/span/span[1]/button'
        follow_path = '//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/button'

        for account in accounts:
            self.browser.get("https://www.instagram.com/{}".format(account))
            try:
                self.wait_for(follow_back_path).click()
            except:
                try:
                    self.wait_for(follow_path).click()
                except:
                    print('cannt follow {}, all ready following or an error occurs'.format(account))
        self.browser.get("https://www.instagram.com/{}".format(self.username))

    def get_accounts(self):
        self.browser.get("https://www.instagram.com/{}".format(self.username))
        followers = self.get_followers()
        accounts = []
        accounts.extend(followers)
        for follower in followers:
            self.browser.get("https://www.instagram.com/{}".format(follower))
            follower_followers = self.get_followers()
            if follower_followers is not None:
                accounts.extend(follower_followers)

        return accounts

    def wait_for(self, elem_path):
        element = None
        try:
            element = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, elem_path)))
        except:
            print("An error occurs in waiting for page load")
        return element


if __name__ == '__main__':
    bot = InstagramBot()
    bot.login("ig_b_re", "Aa123456")
    # followers = bot.get_followers()
    # following = bot.get_following()
    # print("number of followers = ", len(followers), "\n number of following = ", len(following))
    acc = bot.get_accounts()
    bot._follow_steam(acc)
