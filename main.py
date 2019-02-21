from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import Credentials
import time

class LazyLinkedIn(object):
    driver = webdriver.Chrome(executable_path="C:\\Users\\Stratos\\Desktop\\LazyLinkedIn\\venv\\chromedriver.exe")
    driver.implicitly_wait(4)
    driver.maximize_window()
    user = Credentials.User();

    def login(self):
        self.driver.get("https://www.linkedin.com")
        usernameField = self.driver.find_element(By.XPATH, '//*[@id = "login-email"]')
        passwordField = self.driver.find_element(By.XPATH, '//*[@id = "login-password"]')
        usernameField.send_keys(self.user.username)
        passwordField.send_keys(self.user.password)
        passwordField.send_keys(Keys.RETURN)
        return self
    def jobs(self):
        jobsButton = self.driver.find_element_by_id("jobs-tab-icon")
        jobsButton.click()
        jobName=self.driver.find_element(By.XPATH,"//input[contains(@id,'jobs-search-box-keyword-id')]")
        jobLocation=self.driver.find_element(By.XPATH,"//input[contains(@id,'jobs-search-box-location')]")
        time.sleep(1.2)
        jobName.send_keys(self.user.job) #TODO FIND SOMETHING BETTER CAUSE THIS SUX
        jobLocation.send_keys(self.user.location)
        time.sleep(2)
        jobLocation.send_keys(Keys.RETURN)
        return self

    def filters(self):
        self.driver.find_element(By.XPATH,"//h3[contains(.,'LinkedIn Features')]").click()
        self.driver.find_element(By.XPATH,"//label[contains(.,'"+self.user.linkedInFeature+"')]").click()
        self.driver.find_element(By.XPATH,"//*[@id='linkedin-features-facet-values']//button[contains(.,'Apply')]").click()
        self.driver.find_element(By.XPATH, "//h3[contains(.,'Experience')]").click()
        self.driver.find_element(By.XPATH, "//label[contains(.,'" + self.user.experience+"')]").click()
        self.driver.find_element(By.XPATH,"//*[@id='experience-level-facet-values']//button[contains(.,'Apply')]").click()
        return self

    def getJobList(self):
        totalJobs=self.driver.find_element(By.XPATH,"//div[contains(.,'results') and contains(@class,'t-12')]").get_attribute("innerText")
        return [totalJobs, self.driver.find_elements(By.XPATH,"//ul[contains(@class,'jobs-search-results__list')]/li")]


    def parseThroughList(self,current=1):
        self.currentPage=current
        i = 0
        #currentPage=1
        time.sleep(2)
        totalJobs= self.getJobList()[0]
        list = self.getJobList()[1]
        for x in list:
            i = i + 1
            print("vlepw doulia noumero:",i,"selida:",self.currentPage)
            if(i==25):
                self.currentPage+=1
                print("paw selida:", self.currentPage)
                self.driver.find_element(By.XPATH,"//button[contains(@aria-label,'Page "+str(self.currentPage)+"')]").click()
                self.parseThroughList(self.currentPage)
            try:
                x.click()
            except:
                pass
            try:
                self.driver.find_element(By.XPATH,"//button[@class='jobs-apply-button--top-card artdeco-button--3 artdeco-button--primary jobs-apply-button artdeco-button ember-view']").click()
                time.sleep(1)
            except:
                continue
            try:
                self.currentTabApplication()
            except:
                self.newTabApplication()


    def currentTabApplication(self):
        self.driver.find_element(By.XPATH,"//button[@class='jobs-apply-form__submit-button button-primary-large ']").click()
        time.sleep(2)
        self.driver.find_element(By.XPATH, "//button[@class='artdeco-dismiss']").click()

    def newTabApplication(self):
        self.driver.switch_to_window(self.driver.window_handles[1])
        time.sleep(2)
        self.driver.find_element(By.XPATH, "//button[contains(.,'Submit')]").click()
        time.sleep(2)
        self.driver.close()
        time.sleep(2)
        self.driver.switch_to_window(self.driver.window_handles[0])
        time.sleep(3)
        self.parseThroughList(self.currentPage)

def main():
   bot = LazyLinkedIn()
   bot.login().jobs().filters()
   while(1):
       bot.parseThroughList()

main()

