from time import sleep
import random
from selenium import webdriver
import argparse

classToSelector = {
    "bodypump-mon": "ctl00$MainContent$activitiesGrid$ctl19$lnkListCommand",
    "bodypump-wed": "ctl00$MainContent$activitiesGrid$ctl20$lnkListCommand",
    "insanity-mon": "ctl00$MainContent$activitiesGrid$ctl16$lnkListCommand",
    "insanity-wed": "ctl00$MainContent$activitiesGrid$ctl17$lnkListCommand",
    "circuits-tue": "ctl00$MainContent$activitiesGrid$ctl03$lnkListCommand",
    "circuits-thu": "ctl00$MainContent$activitiesGrid$ctl02$lnkListCommand"
}

# get the args from the command line
parser = argparse.ArgumentParser()
parser.add_argument("memberId", help="Your Member ID")
parser.add_argument("pin", help="The PIN code to login")
parser.add_argument("classId", help="The ID of the class you wish to book", choices=classToSelector.keys())
parser.add_argument("-d", "--driver", help="The path to the web driver executable")
args = parser.parse_args()


# use a webdriver, i'm using the chrome driver which i downloaded from here:
# https://sites.google.com/a/chromium.org/chromedriver/downloads
if args.driver:
    driver = webdriver.Chrome(args.driver)
else:
    # if the driverpath isn't specified in the args, lets hope its on the PATH
    driver = webdriver.Chrome()


# lets start
driver.get("https://sportandwellbeing.soton.ac.uk/connect/")

# Login
user = driver.find_element_by_name("ctl00$MainContent$InputLogin")
user.send_keys(args.memberId) # Student ID
pin = driver.find_element_by_name("ctl00$MainContent$InputPassword")
pin.send_keys(args.pin) # Password
loginButton = driver.find_element_by_name("ctl00$MainContent$btnLogin")
loginButton.click()

# Make a booking section
makeABooking = driver.find_element_by_link_text("Make a Booking")
makeABooking.click()

# High Intensity Highfield section
activityType = driver.find_element_by_name("ctl00$MainContent$activityGroupsGrid$ctl18$lnkListCommand")
activityType.click()

while True:
    classSelector = classToSelector[args.classId]

    # choose the correct class
    classLink = driver.find_element_by_name(classSelector)
    classLink.click()

    # print the details of what we're booking
    className = driver.find_element_by_css_selector("#ctl00_MainContent_gvClasses_ctl02_Desc")
    classDate = driver.find_element_by_css_selector("#ctl00_MainContent_gvClasses > tbody > tr:nth-child(2) > td:nth-child(2)")
    print("Attempting to Book: {} {}".format(className.text, classDate.text))

    # Do the actual booking!
    book = driver.find_element_by_name("ctl00$MainContent$gvClasses$ctl02$btnBook")
    book.click()
    confirmBook = driver.find_element_by_name("ctl00$MainContent$btnBook")
    confirmBook.click()

    # check if we were unsuccesful, and try again
    unsuccesful = driver.find_element_by_css_selector("#formbox > table > tbody > tr:nth-child(1) > td > strong")
    if unsuccesful.text == 'The booking request could not be processed as the requested time is no longer available.':
        backbutton = driver.find_element_by_css_selector("#formbox > table > tbody > tr:nth-child(3) > td > a")
        backbutton.click()

        rsleep = random.randint(1,5)
        print("Unsuccessful, trying again in: {} minutes".format(rsleep))
        sleep(60 * rsleep)
    else:
        break # this never happens, if it can't find the unsucessful message (because it was succesful) it raises an error and stops running the script anyway