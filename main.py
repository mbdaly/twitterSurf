from selenium import webdriver
from time import sleep
import itertools

class TwitterBot:
    def __init__(self, username, password):
        self.driver = webdriver.Chrome()
        self.driver.get("https://twitter.com")
        sleep(2)
        # Click "Log in" button
        self.driver.find_element_by_xpath('/html/body/div/div/div/div/main/div/div/div/div[1]/div/a[2]').click()
        sleep(2)
        # Type username
        self.driver.find_element_by_xpath('/html/body/div/div/div/div[2]/main/div/div/div[1]/form/div/div[1]/label/div/div[2]/div/input').send_keys(username)
        sleep(2)
        # Type password
        self.driver.find_element_by_xpath('/html/body/div/div/div/div[2]/main/div/div/div[1]/form/div/div[2]/label/div/div[2]/div/input').send_keys(password)
        # Click submit
        self.driver.find_element_by_xpath('/html/body/div/div/div/div[2]/main/div/div/div[1]/form/div/div[3]/div/div/span/span').click()
        sleep(5)

    def check_usernames(self):
        # Get all 5 letter combinations
        alphabets = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        testNames = [''.join(i) for i in itertools.product(alphabets, repeat = 5)]
        self.driver.get("https://twitter.com/settings/screen_name")
        sleep(5)    # Let page load
        for name in testNames:
            print("Testing", name)
            # Get username box
            self.driver.find_element_by_xpath('//input[@name=\"typedScreenName\"]').clear()
            self.driver.find_element_by_xpath('//input[@name=\"typedScreenName\"]').send_keys(name)
            sleep(2)
            # Check all possible spans for alert message saying usrname is invalid / taken
            elems = self.driver.find_elements_by_xpath("//span[contains(@class, 'css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0')]")
            validName = True
            for e in elems:
                resp = e.get_attribute('innerHTML')
                if "choose another" in resp:        # Username is taken
                    validName = False
                    break
                if "must be" in resp:               # Username is too long/short
                    validName = False
                    break
                if "unavailable" in resp:           # Username is not allowed
                    validName = False
                    break
            if validName == True:       # Write available names to text file
                print("Available!")
                with open('words_available.txt', 'a+') as fileout:
                    fileout.write(name + "\n")

        sleep(5)

my_bot = TwitterBot('username', 'password')
my_bot.check_usernames()
