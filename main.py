import random

from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import autoit
import os
import config as conf


class InstagramBot:
    def __init__(self):
        self.username = conf.USERNAME
        self.password = conf.PASSWORD
        self.option = None
        self.browser = None

    def config_driver(self):
        self.option = webdriver.ChromeOptions()
        self.option.binary_location = conf.CHROME_PATH
        self.option.add_argument("--incognito")
        self.browser = webdriver.Chrome(executable_path=conf.DRIVER_PATH, chrome_options=self.option)
        self.browser.get("https://www.instagram.com")

    def login(self):
        # self.browser.maximize_window()
        # element paths with XPATH
        username_field_path = '//*[@id="loginForm"]/div/div[1]/div/label/input'
        password_field_path = '//*[@id="loginForm"]/div/div[2]/div/label/input'
        login_butten_path = '//*[@id="loginForm"]/div/div[3]'
        dont_save_pass_path = '//*[@id="react-root"]/section/main/div/div/div/div/button'
        no_notifcation_path = '/html/body/div[4]/div/div/div/div[3]/button[2]'

        # username field
        username_field = self.wait_for(username_field_path)
        username_field.send_keys(self.username)

        password_field = self.wait_for(password_field_path)
        password_field.send_keys(self.password)

        login_butten = self.wait_for(login_butten_path)
        login_butten.click()

        # Do not save login info
        login_save_pass = self.wait_for(dont_save_pass_path)
        login_save_pass.click()

        # Do not turn on notifcation
        no_notifcation = self.wait_for(no_notifcation_path)

        no_notifcation.click()
        self.random_wait(10)
        self.browser.get("https://www.instagram.com/{}".format(self.username))

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
            self.random_wait(20)
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
            self.random_wait(15)
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

    def post_pic(self):
        login_slct = '//*[@id="react-root"]/section/main/article/div/div/div/div[2]/button'
        username = '//*[@id="loginForm"]/div[1]/div[3]/div/label/input'
        password = '//*[@id="loginForm"]/div[1]/div[4]/div/label/input'
        login_btn = '//*[@id="loginForm"]/div[1]/div[6]/button'
        not_now = '//*[@id="react-root"]/section/main/div/div/div/button'
        post_btn = '//*[@id="react-root"]/section/nav[2]/div/div/div[2]/div/div/div[3]'
        next_btn = '//*[@id="react-root"]/section/div[1]/header/div/div[2]/button'
        caption_path = '//*[@id="react-root"]/section/div[2]/section[1]/div[1]/textarea'
        share_btn = '//*[@id="react-root"]/section/div[1]/header/div/div[2]/button'

        image_path = conf.IMAGE_PATH
        caption = conf.CAPTION

        # self.browser.quit()
        # mobile_emulation = {"deviceName": "Pixel 2"}
        # self.option.add_experimental_option("mobileEmulation", mobile_emulation)
        # self.browser = webdriver.Chrome(executable_path=conf.DRIVER_PATH, chrome_options=self.option)
        # self.browser.get("https://www.instagram.com")
        mob_bot = self.open_mob_browser()

        mob_bot.wait_for(login_slct).click()
        mob_bot.wait_for(username).send_keys(self.username)
        mob_bot.wait_for(password).send_keys(self.password)
        mob_bot.wait_for(login_btn).click()
        mob_bot.wait_for(not_now).click()

        mob_bot.wait_for(post_btn).click()
        autoit.win_wait_active("Open", 5)
        autoit.send(os.getcwd() + image_path)
        autoit.send("{ENTER}")

        mob_bot.wait_for(next_btn).click()
        self.random_wait(5)
        mob_bot.wait_for(caption_path).send_keys(caption)
        mob_bot.wait_for(share_btn).click()
        sleep(10)
        mob_bot.browser.quit()

    def open_mob_browser(self):
        mob_bot = InstagramBot()
        mob_bot.option = webdriver.ChromeOptions()
        mob_bot.option.binary_location = conf.CHROME_PATH
        mobile_emulation = {"deviceName": "Pixel 2"}
        mob_bot.option.add_experimental_option("mobileEmulation", mobile_emulation)
        mob_bot.option.add_argument("--incognito")
        mob_bot.browser = webdriver.Chrome(executable_path=conf.DRIVER_PATH, chrome_options=mob_bot.option)
        mob_bot.browser.get("https://www.instagram.com")
        return mob_bot

    def follow_balance(self):
        followers = self.get_followers()
        following = self.get_following()

        unfollow_list = []
        for acc in following:
            if acc not in followers:
                unfollow_list.append(acc)
        self.unfollow(unfollow_list)
        self.browser.get("https://www.instagram.com/{}".format(self.username))

    def unfollow(self, accounts):
        allready_followed_btn = '//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/div/div[2]/div/span/span[1]/button'
        unfollow_path = '/html/body/div[4]/div/div/div/div[3]/button[1]'

        for account in accounts:
            self.random_wait(15)
            self.browser.get("https://www.instagram.com/{}".format(account))
            try:
                self.wait_for(allready_followed_btn).click()
                self.wait_for(unfollow_path).click()
            except:
                print('cannt unfollow {}'.format(account))

    def like_pics(self):
        self.browser.get("https://www.instagram.com")

        for i in range(1, 6):
            img_path = '//*[@id="react-root"]/section/main/section/div[1]/div[2]/div/article[' + str(
                i) + ']/div[3]/section[1]/span[1]/button'
            self.wait_for(img_path).click()
            self.random_wait(10)

    def hashtag_search(self):
        search_bar = '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input'
        follow_btn = '/html/body/div[5]/div[2]/div/article/header/div[2]/div[1]/div[2]/button'
        close_btn = '/html/body/div[5]/div[3]/button'

        for topic in conf.SEARCH:
            self.browser.get('https://www.instagram.com')
            search = self.wait_for(search_bar)
            search.send_keys(topic)
            sleep(2)
            search.send_keys(Keys.RETURN)
            search.send_keys(Keys.RETURN)
            ar = self.collect_articles()

            # top = self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]')
            # ar = top.find_elements_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]//*[a]')
            for a in ar:
                self.random_wait(15)
                a.click()
                try:
                    follow = self.wait_for(follow_btn)
                    self.random_wait(15)
                    if follow.text == 'Follow':
                        follow.click()

                except:
                    print('unable to follow poster')

                self.wait_for(close_btn).click()

    def collect_articles(self):
        elements = []
        for i in range(1,2):
            path = '//*[@id="react-root"]/section/main/article/div[1]/div/div/div[' + str(i) + ']//*[a]'
            try:
                tmp = WebDriverWait(self.browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, path)))
                if tmp is not None:
                    elements.extend(tmp)
            except:
                print("there are no photos !!")

        return elements

    def random_wait(self,x):
        wait = random.randint(1,x)
        sleep(wait)

if __name__ == '__main__':
    bot = InstagramBot()
    bot.config_driver()
    bot.login()
    bot.hashtag_search()
    sleep(10)
    bot.browser.quit()

    # bot.post_pic()
    # bot.like_pics()
    # bot.get_followers()
    # bot.like_stream()
    # bot.follow_balance()
    # followers = bot.get_followers()
    # print(followers)
    #
    # following = bot.get_following()
    # print("number of followers = ", len(followers), "\n number of following = ", len(following))
    # acc = bot.get_accounts()
    # bot._follow_steam(followers)
