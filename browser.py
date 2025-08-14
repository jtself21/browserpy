from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import getpass
import time
from selenium.webdriver.firefox.options import Options
import os

# Hardcoded username and password
username_str = "jtself21"
password_str = "Adrienne99(("

# URL of the login page
login_url = 'https://www5.benefitsolver.com/benefits/BenefitSolverView'

# Initialize the options for Firefox
options = Options()
options.headless = False # Run in headless mode

# Initialize the WebDriver for Firefox with the specified options
driver = webdriver.Firefox(options=options)

# Use WebDriverWait for waiting for elements to load
wait = WebDriverWait(driver, 5)

try:
    # Navigate to the login page
    driver.get(login_url)

    # Wait for the username field to be available, then fill it in
    username_field = wait.until(EC.visibility_of_element_located((By.ID, 'USERID1')))
    username_field.send_keys(username_str)

    # Wait for the password field to be available, then fill it in
    password_field = wait.until(EC.visibility_of_element_located((By.ID, 'PASSWORD1')))
    password_field.send_keys(password_str)

    # Simulate pressing "Enter" on the password field
    password_field.send_keys(Keys.RETURN)

    # Wait for a few seconds to ensure page elements load completely
    time.sleep(2)

    # Handle the security question and answer
    security_question_text = wait.until(EC.visibility_of_element_located((By.ID, 'LOC_CHALLENGE_TEXT')))

    # Check the text of the security question
    if "make of your first car" in security_question_text.text.lower():
        # This is the car question, provide the answer
        security_question = wait.until(EC.visibility_of_element_located((By.ID, 'LOC_RESPONSE')))
        security_question.send_keys("thunderbird")  # Answer for the car question
    elif "anniversary" in security_question_text.text.lower():
        # This is the anniversary question, provide the answer
        security_question = wait.until(EC.visibility_of_element_located((By.ID, 'LOC_RESPONSE')))
        security_question.send_keys("jan 7")  # Answer for the anniversary question
    else:
        # This is the city question, provide the answer
        security_question = wait.until(EC.visibility_of_element_located((By.ID, 'LOC_RESPONSE')))
        security_question.send_keys("laurens")  # Answer for the city question

    # Find the "Continue" button by ID
    continue_button = wait.until(EC.element_to_be_clickable((By.ID, 'btnSubmit')))

    # Use JavaScript to click the button and avoid potential JavaScript behavior
    driver.execute_script("arguments[0].click();", continue_button)

    wait = WebDriverWait(driver, 10)

    # Find the <a> element with the JavaScript function call by using a partial link text
    my_choice_link = wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "MyChoice Accounts")))

    # Click on the <a> element
    my_choice_link.click()

    # Locate the element containing the dollar amount
    # Update the selector if necessary to match the structure of the actual page
    dollar_amount_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".float-right")))
    dollar_amount = dollar_amount_element.text.strip()

    # Save the dollar amount to a text file
    # current_directory = os.getcwd()
    # file_path = os.path.join(current_directory, 'dollar_amount.txt')
    # with open(file_path, 'w') as file:
    #     file.write(dollar_amount)
    # print(f"Dollar amount saved to {file_path}")



except Exception as e:
    print(f"An error occurred: {e}")