from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver_path = "C:\\Users\\Nour\\Desktop\\work\\InstagramBot\\chromedriver.exe"
brave_path = "C:\\Program Files (x86)\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"


class InstagramBot:
    def __init__(self):
        self.option = webdriver.ChromeOptions()
        self.option.binary_location = brave_path
        self.option.add_argument("--incognito")
        self.browser = webdriver.Chrome(executable_path=driver_path, chrome_options=self.option)
        self.browser.get("https://www.instagram.com")

    def login(self, username, password):
        sleep(2)
        #self.browser.maximize_window()
        self.username = username
        self.password = password
        # username field
        username_field = self.browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
        username_field.send_keys(username)

        password_field = self.browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
        password_field.send_keys(password)

        login_butten = self.browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]')
        login_butten.click()

        sleep(3)
        # Do not save login info
        self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click()
        sleep(2)
        # Do not turn on notifcation
        self.browser.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]').click()
        self.browser.get("https://www.instagram.com/{}".format(username))

    def get_followers(self):
        sleep(2)
        try:
            self.browser.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a').click()
            sleep(2)
            scroll_box = self.browser.find_element_by_xpath('/html/body/div[4]/div/div/div[2]')
            followers = self._get_names(scroll_box)
            sleep(1)
            self.browser.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div/div[2]/button').click()
        except:
            print('cannt get followers')
            followers = None

        return followers

    def get_following(self):
        sleep(2)
        try:
            self.browser.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a').click()
            sleep(2)
            scroll_box = self.browser.find_element_by_xpath('/html/body/div[4]/div/div/div[2]')
            following = self._get_names(scroll_box)
            sleep(1)
            self.browser.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div/div[2]/button').click()
        except:
            print('cannt get following')
            followers = None

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
        sleep(2)
        # followers = self.get_followers()
        for account in accounts:
            self.browser.get("https://www.instagram.com/{}".format(account))
            sleep(1)
            try:
                self.browser.find_element_by_xpath(
                    '//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/div/span/span[1]/button').click()
            except:
                try:
                    self.browser.find_element_by_xpath(
                        '//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/button').click()
                except:
                    print('cannt follow {}, all ready following or an error occurs'.format(account))
        self.browser.get("https://www.instagram.com/{}".format(self.username))

    def get_accounts(self):
        sleep(2)
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

    # def wait_for(self, xpath):
    #     element = None
    #     ret = None
    #     try:
    #         element = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located(By.XPATH, xpath))
    #         ret = self.browser.find_element_by_xpath(xpath)
    #     except:
    #         print("An error occurs in waiting for page load")
    #     return ret


if __name__ == '__main__':
    bot = InstagramBot()
    bot.login("ig_b_re", "Aa123456")
    # followers = bot.get_followers()
    # following = bot.get_following()
    # print("number of followers = ", len(followers), "\n number of following = ", len(following))
    acc = bot.get_accounts()
    print(len(acc))
    bot._follow_steam(acc)
