#! venv/bin/python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from time import sleep
import csv
import os


def login(driver, user, passwd):
    """
    Log into survey planet
    Parameters: None
    Returns: None
    """
    username = driver.find_element_by_id('email')
    password = driver.find_element_by_id('password')
    submit = driver.find_element_by_id('login-button')

    username.send_keys(user)
    password.send_keys(passwd)

    submit.send_keys(Keys.RETURN)


def go_to_email_list(driver):
    """
    Navigate to the email list of the first survey on the page.
    Parameters: None
    Returns: None
    """
    sleep(2) 
    event = driver.find_element_by_css_selector('.results-survey-button.icon-result')
    event.click()

    sleep(2) 
    participants = driver.find_element_by_link_text('Participants')
    participants.click()


def get_emails(driver):
    """
    Gather email addresses from the rows, page by page.
    Parameters: None
    Returns: list of email addresses
    """
    # This current method of grabbing emails sucks. Every email address visible
    # is grabbed each time we page down. So it grabs the same ones over and over.
    # I don't think I want it to load them all first though. Might add that option later

    all_emails = []
    page = driver.find_element_by_tag_name('html')

    # 'limit' is just used for testing now, might change it to 'while True' later
    page_limit = 10
    while page_limit > 0:
        emails = driver.find_elements_by_class_name('participant-item-email')
        for email in emails:
            # 'email' contains other info we don't care about right now
            email = email.text.split('\n')[0]
            # some participants are anonymous
            if '@' in email and email not in all_emails:
                all_emails.append(email)
                print(f'Found new email: {email}')
            else:
                pass

        page.send_keys(Keys.END)
        sleep(1)
        page_limit -= 1

    return all_emails


def save_to_csv(emails, filename):
    """
    Save the list of email addresses to a csv.
    Parameters: emails - list of emails
                filename - name of the new csv file
    Returns: None
    """
    abs_path = os.path.join(os.getcwd(), filename)

    print(f'Saving emails to {filename}...')
    
    with open(abs_path, 'w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        for email in emails:
            csv_writer.writerow([email])

    print(f'Finished saving emails to {filename}')


def main():
    driver = webdriver.Firefox()
    driver.get('http://surveyplanet.com/login')
    sleep(1)
    
    # replace 'USERNAME' and 'PASSWORD' with login info
    user = 'USERNAME'
    passwd = 'PASSWORD'
    login(driver, user, passwd)

    go_to_email_list(driver)
    emails = get_emails(driver)

    sleep(2)
    driver.close()

    filename = 'emails.csv'
    save_to_csv(emails, filename)
    

if __name__ == '__main__':
    main()