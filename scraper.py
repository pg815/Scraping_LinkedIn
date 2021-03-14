from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from bs4.element import Tag
from time import sleep
import csv
from parsel import Selector
import parameters
import numpy
from flask_pymongo import PyMongo


class Scraper:

    def __init__(self):
        self.links = []
        self.titles = []
        self.descriptions = []


    # Function call extracting title and linkedin profile iteratively
    def find_profiles(self,result_div):

        for r in result_div:
            # Checks if each element is present, else, raise exception
            try:
                link = r.find('a', href=True)
                title = None
                title = r.find('h3')

                # returns True if a specified object is of a specified type; Tag in this instance
                if isinstance(title, Tag):
                    title = title.get_text()

                description = None
                description = r.find('span', attrs={'class': 'st'})

                if isinstance(description, Tag):
                    description = description.get_text()

                # Check to make sure everything is present before appending
                if link != '' and title != '' and description != '':
                    self.links.append(link['href'])
                    self.titles.append(title)
                    self.descriptions.append(description)


            # Next loop if one element is not present
            except Exception as e:
                print(e)
                continue


    # This function iteratively clicks on the "Next" button at the bottom right of the search page.
    def profiles_loop(self,driver,result_div):
        self.find_profiles(result_div)

        next_button = driver.find_element_by_xpath('//*[@id="pnnext"]')
        next_button.click()


    def get_data(self,query):
        # specifies the path to the chromedriver.exe
        driver = webdriver.Chrome()

        # driver.get method() will navigate to a page given by the URL address
        driver.get('https://www.linkedin.com')

        # locate email form by_class_name
        username = driver.find_element_by_id('session_key')

        # send_keys() to simulate key strokes
        # Enter Your LinkedIn Username
        username.send_keys('YourLinkedInUserName')
        sleep(0.5)

        # locate password form by_class_name
        password = driver.find_element_by_id('session_password')

        # send_keys() to simulate key strokes
        # Enter Your LinkedIn Password
        password.send_keys('YourLinkedInPassword')
        sleep(0.5)

        # locate submit button by_class_name
        log_in_button = driver.find_element_by_class_name('sign-in-form__submit-button')

        # .click() to mimic button click
        log_in_button.click()
        sleep(0.5)

        # driver.get method() will navigate to a page given by the URL address
        driver.get('https://www.google.com')
        sleep(3)

        # locate search form by_name
        search_query = driver.find_element_by_name('q')

        # send_keys() to simulate the search text key strokes
        query = 'site:linkedin.com/in/ AND ' + query
        search_query.send_keys(query)

        # .send_keys() to simulate the return key
        search_query.send_keys(Keys.RETURN)

        soup = BeautifulSoup(driver.page_source, 'lxml')
        result_div = soup.find_all('div', attrs={'class': 'g'})

        # initialize empty lists


        # Function call x10 of function profiles_loop; you can change the number to as many pages of search as you like.
        while len(self.links) <= 100:
            self.profiles_loop(driver,result_div)


        profiles = []
        # Separates out just the First/Last Names for the titles variable
        for data in self.titles:
            try :
                profile = {}
                profile['Name'] = data.split('-')[0]
                profile['Headline'] = data.split('-')[1]
                profile['Company'] = data.split('-')[2]
                profiles.append(profile)
            except:
                continue

        return profiles


if __name__ == "__main__":
    obj = Scraper()
    print(obj.get_data("python developer"))