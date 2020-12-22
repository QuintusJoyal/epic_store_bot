from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lib.handler import Handle
from lib.authCode import Getmail
import time
from lib.config import Config

config = Config()

class Bot:
    """
    def __init__(self):
 
        desired_cap = {
            'platform' : "windows 10",
            'browserName' : "chrome",
            'version' :  "88.0",
            "resolution": "1024x768",
            "name": "epicbot",
            "build": "epicbot",
            "headless": False,
            "network": True,
            "video": True,
            "geoLocation" : "US",
            "visual": False,
            "console": True,
        }
 
        # URL: https://{username}:{accessToken}@hub.lambdatest.com/wd/hub
        url = "#"
         
        print("Initiating remote driver on platform: "+desired_cap["platform"]+" browser: "+desired_cap["browserName"]+" version: "+desired_cap["version"])
        self.browser = webdriver.Remote(
            desired_capabilities=desired_cap,
            command_executor= url
        )
    """

    def __init__(self):

        # Heroku
        CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'
        GOOGLE_CHROME_BIN = '/app/.apt/usr/bin/google-chrome'

        # Windows
        #GOOGLE_CHROME_BIN = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
        #CHROMEDRIVER_PATH = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe' # or somewhere else
        
        gChromeOptions = webdriver.ChromeOptions()
        gChromeOptions.binary_location = GOOGLE_CHROME_BIN
        gChromeOptions.add_argument('--disable-gpu')
        gChromeOptions.add_argument('--no-sandbox')
        gChromeOptions.add_argument('--headless')

        self.browser = webdriver.Chrome(chrome_options=gChromeOptions, executable_path=CHROMEDRIVER_PATH)

    def check_if_element(self, browser, xpath):
        try:
            browser.find_element_by_xpath(xpath)
            return True
        except NoSuchElementException as errr:
            print('error chk: ' + str(errr))
            return False


    def fb_login(self, browser):

        wait = WebDriverWait(browser, 10)
                
        wait.until(EC.element_to_be_clickable((By.ID, 'login-with-facebook'))).click() 
                
        browser.switch_to.window(browser.window_handles[1])
        
        try:
            browser.find_element_by_xpath('//button[@data-cookiebanner="accept_button"]').click()
        except NoSuchElementException as eroror:
            print('error i: ' + str(eroror))
                
        username = wait.until(EC.presence_of_element_located((By.NAME, 'email')))
        username.send_keys(config['facebook']['email'])
        time.sleep(5) 
        password = wait.until(EC.presence_of_element_located((By.NAME, 'pass')))      
        password.send_keys(config['facebook']['password'])
        time.sleep(5)
        password.send_keys(Keys.ENTER)

        try:
            browser.find_element_by_xpath('//button[@value="Continue" and @name="submit[Continue]"]').click()
            browser.implicitly_wait(10)
            browser.find_elements_by_xpath('//label[@class="_55sh uiInputLabelInput"]/span')[1].click()
            browser.find_element_by_xpath('//button[@value="Continue" and @name="submit[Continue]"]').click()
            wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@value="Continue"]'))).click()
            code = Getmail().get_code('facebook')
            codefield = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="text" and @placeholder="12345678"]')))
            codefield.send_keys(code)
            browser.find_element_by_xpath('//button[@value="Continue" and @name="submit[Continue]"]').click()
            browser.implicitly_wait(5)
            try:
                code2 = Getmail().get_code('facebook')
                codefield2 = browser.find_element_by_xpath('//input[@type="text" and @placeholder="12345678"]')
                if code != code2:
                    codefield2.send(code2)
                    browser.find_element_by_xpath('//button[@value="Continue" and @name="submit[Continue]"]').click()
            except:
                pass

            try:
                browser.find_element_by_xpath('//button[@name="submit[Yes]" and @value="Yes"]').click()
            except:
                pass
            browser.find_element_by_xpath('//button[@value="Continue" and @name="submit[Continue]"]').click() 
            browser.implicitly_wait(10)
        except NoSuchElementException as err0:
            print(err0)
        
    def login(self, browser):

        browser.get("https://www.epicgames.com/login")
        
        wait = WebDriverWait(browser, 10)

        print('logging in')

        self.fb_login(browser)

        browser.switch_to.window(browser.window_handles[0])

        wait.until(EC.presence_of_element_located((By.XPATH, '//div[@id="user"]')))
        
        browser.implicitly_wait(20)
        
        cookies_l = browser.get_cookies()
        cookies_d = {}
        for i in cookies_l:
            cookies_d[i['name']] = i

        Handle().save_cookies(cookies_d)

                            
        try:
            age_gate_cookie = {"name":"HAS_ACCEPTED_AGE_GATE_ONCE","value":"true","domain":".epicgames.com","path":"/","expires":-1,"size":30,"httpOnly":False,"secure":False,"session":True}
            browser.add_cookie(age_gate_cookie)
        except Exception as e:
            print('error 18: ' + str(e))


    def main(self):
        new_list = Handle().check()

        print(new_list)

        if new_list:
            
            self.login(self.browser)

            browser = self.browser

            for i in new_list:
                
                if i['state'] == 'available':
                
                    wait = WebDriverWait(browser, 10)
                    
                    try:
                        """
                        browser.execute_script("window.open('{}')".format(i['url']))

                        browser.switch_to.window(browser.window_handles[1])
                        """
                        
                        browser.get(i['url'])

                        cookies_l = Handle().get_cookie()

                        for c in cookies_l:
                            try:
                                browser.add_cookie(c)
                            except Exception as errrr:
                                print('error gco: ' + str(errrr))
                                continue
                        

                        browser.refresh()

                        browser.implicitly_wait(10)

                        print(browser.title)
                        print(browser.window_handles)
                        
                        
                        try: 
                            user = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@id="user"]'))).text
                            print('Logged in as ' + str(user))
                        except NoSuchElementException as eor:
                            print('error usr: ' + str(eor))


                        wait.until(EC.presence_of_element_located((By.XPATH, '//button[@data-testid="purchase-cta-button"]')))

                        browser.implicitly_wait(5)
                        
                        # Already owned?
                        if self.check_if_element(browser=browser, xpath='//button[@data-testid="purchase-cta-button"]/span[contains(text(), "Owned")]'):
                            Handle().owned(i['title'], i)
                    
                        else:
                            print('Putchasing...')
                            browser.find_element_by_xpath('//button[@data-testid="purchase-cta-button"]').click()
                            browser.implicitly_wait(30)
                            plaorder = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="order-summary-content"]/div/div/button[@class="btn btn-primary"]/span[.="Place Order"]')))
                            plaorder.click()
                            
                            browser.implicitly_wait(10)

                            wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Thank you for buying")]')))
                            browser.implicitly_wait(15)
                        
                            Handle().owned(i['title'], i)
                            print('Purchased {}'.format(i['title']))
                    
                    except (TimeoutException, NoSuchElementException)  as erro:
                        browser.quit()
                        print('error 111: ' + str(erro))

                else:
                    print(str(i['title']) + ' - Coming_soon( {} )'.format(i['start_date']))
            print('Taking_a_nap_rn')
            browser.quit()
        else:
            print('all_caught_up!!!')
