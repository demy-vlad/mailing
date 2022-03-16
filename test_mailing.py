from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from loguru import logger
import random


LOGIN_URL = 'https://mail.protonmail.com/'

# Emails for sending messages
email = [
        'main@asiainvestbank.ru',
        'info@absolutbank.ru',
        'info@avangard.ru',
        'bank@agroros.ru',
        'main@asiainvestbank.ru',
        'cc@bspb.ru'
        ]

class Protonmail():
    def __init__(self, email, password, browser='Chrome'):
        options = Options()
        options.headless = False # Using a headless browser version
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # Store credentials for login
        self.email = email
        self.password = password
        if browser == 'Chrome':
            # Use chrome
            self.driver = webdriver.Chrome(options=options, executable_path=ChromeDriverManager().install())
        elif browser == 'Firefox':
            # Set it to Firefox
            self.driver = webdriver.Firefox(options=options, executable_path=GeckoDriverManager().install())
        self.driver.implicitly_wait(20)
        self.driver.get(LOGIN_URL)

    def login(self):
        '''
            1.	Login to any email box.
        '''
        email_element = self.driver.find_element_by_xpath('//*[@id="username"]')
        email_element.send_keys(self.email) # Give keyboard input

        password_element = self.driver.find_element_by_xpath('//*[@id="password"]')
        password_element.send_keys(self.password) # Give password as input too

        login_button = self.driver.find_element_by_css_selector('button.button')
        login_button.click() # Send mouse click
        self.driver.set_page_load_timeout(10)
        assert self.driver.title == 'Proton Account'
    
    def sending_messages_ten_email(self):
        '''
        2.	Send from 10 mails from current box to yourself with:
            •	Theme: Random string with 10 symbols (letters and numbers only)
            •	Body: Random string with 10 symbols (letters and numbers only)
        3.	Check that all 10 mails are delivered.
        '''
        if not email:
            logger.error(f'Email list is empty')
        else:
            for emails in email:
                # Click button new message
                email_address = self.driver.find_element_by_css_selector('button.text-bold.mt0-25.w100.no-mobile').click()
                # Give email address
                # email_address = self.driver.find_elements_by_css_selector('input#to-composer-1310')
                # Give email address
                email_address = self.driver.find_element_by_xpath('/html/body/div[1]/div[4]/div/div/div/div/div/div[2]/div/div/div/div/div/div/input')
                email_address.click()
                email_address.send_keys(emails)
                email_address.send_keys(Keys.ENTER)
                logger.debug(f'Added email: {emails}')

                # Give text subject
                text_subject = mailing.random_string()
                logger.info(f'Random string subject: {text_subject}')
                subject = self.driver.find_element_by_xpath('/html/body/div[1]/div[4]/div/div/div/div/div/div[3]/div/div/input')
                subject.click()
                subject.send_keys(text_subject)

                # Send modul
                self.driver.find_element_by_css_selector('button.editor-toolbar-button:nth-of-type(14)').click()
                self.driver.find_element_by_xpath("//span[contains(text(),'Plain text')]").click()

                # Text message
                text_message = mailing.random_string()
                logger.info(f'Random string message: {text_message}')
                message = self.driver.find_element_by_css_selector('textarea.absolute-cover')
                message.click()
                message.clear()
                message.send_keys(f'{text_message}')

                self.driver.set_page_load_timeout(20)
                # Send email button
                self.driver.find_element_by_css_selector("button.button-group-item.composer-send-button").click()
                text_send = self.driver.find_element_by_xpath("//div[contains(text(),'Message sent')]")

                logger.warning(f'Message sending status: {text_send.text}')
                # assert text_send.text == 'Message sent'

    def data_from_all_incoming_emails(self):
        '''
        4.	Collect data from all incoming mails and save it as Object (Dictionary), where:
                •	Key is theme of mail
                •	Value is body of mail
        '''
        key = [] # Key is theme of mail
        value  = [] # Value is body of mail
        url_email = [] #  URL e-mail list

        # Click the button Inbox
        self.driver.find_element_by_css_selector('a.navigation-link.active').click()
        # GET URL letters 
        all_elements = self.driver.find_elements_by_class_name('flex')
        # Delete None
        for all_element in all_elements:
                element = all_element.get_attribute('data-element-id')
                if not element is None:
                    url_email.append(element) #  Added URL e-mail list
        # URL e-mail list
        for url_inbox in url_email: 
            # https://mail.protonmail.com/u/3/inbox/
            self.driver.get(f'https://mail.protonmail.com/u/3/inbox/{url_inbox}')
            key_mail = self.driver.find_element_by_css_selector('h1.message-conversation-summary-header span')
            key.append(key_mail.text) #  Added is theme of mail
            
            value_body_of_mail = self.driver.find_element_by_css_selector('h1.message-conversation-summary-header span')
            value.append(value_body_of_mail.text) #  Added is body of mail

        # Added dictionary: key, value
        dictionary = dict(zip(key, value))
        if not dictionary:
            logger.error(f'Dictionary is empty')
        else: logger.info(f'Result data from all incoming mails: {dictionary}')

    def send_collected_data_to_yourself(self):
        '''
        5.	Send collected data to yourself as: “Received mail on theme {Theme} with message: {Body}. 
            It contains {Count of letters} letters and {Count of numbers} numbers” (repeat for each mail).
        '''

        # button new message
        self.driver.find_element_by_css_selector('button.button-large').click()

        # Email address
        email_address = self.driver.find_element_by_xpath('/html/body/div[1]/div[4]/div/div/div/div/div/div[2]/div/div/div/div/div/div/input')
        email_address.click()
        email_address.send_keys(self.email)
        email_address.send_keys(Keys.ENTER)
        logger.debug(f'Added email: {self.email}')

        # Text subject
        text_subject = mailing.random_string()
        logger.info(f'Random string subject: {text_subject}')
        subject = self.driver.find_element_by_xpath('/html/body/div[1]/div[4]/div/div/div/div/div/div[3]/div/div/input')
        subject.click()
        subject.send_keys(text_subject)

        # Send modul
        self.driver.find_element_by_css_selector('button.editor-toolbar-button:nth-of-type(14)').click()
        self.driver.find_element_by_xpath("//span[contains(text(),'Plain text')]").click()

        # Text message
        theme = mailing.random_string()
        body = mailing.random_string()
        count_of_letters = mailing.text_without_numbers()
        count_of_numbers = mailing.numbers_without_text()

        text_message = (f"Received mail on theme {theme} with message: {body}. It contains {len(count_of_letters)} letters and {len(count_of_numbers)} numbers")
        logger.info(f'Send collected data to yourself as: {text_message}')
        message = self.driver.find_element_by_css_selector('textarea.absolute-cover')
        message.click()
        message.clear()
        message.send_keys(f'{text_message}')

        # Send email button  
        self.driver.find_element_by_css_selector("button.button-group-item.composer-send-button").click()
        text_send = self.driver.find_element_by_xpath("//div[contains(text(),'Message sent')]")

        self.driver.set_page_load_timeout(10)
        logger.warning(f'Message sending status: {text_send.text}')
        assert text_send.text == 'Message sent'
 
    def delete_all_received_emails(self):
        '''
        6.	Delete all received emails except the last one.
        '''
        # Button Span
        self.driver.find_element_by_css_selector('li.navigation-item:nth-child(3) > a.navigation-link.active').click()
        # # Select all messages
        self.driver.find_element_by_xpath("//input[@id='idSelectAll']").click()
        # # Select last
        self.driver.find_element_by_css_selector("div.flex.flex-nowrap:nth-child(2) > label.item-checkbox-label").click()
        # # Click move to trash
        self.driver.find_element_by_css_selector("div.flex:nth-child(1) > button.flex.flex-item-noshrink:nth-child(7)").click()
        # You have 1 message stored in this folder
        last_message = self.driver.find_element_by_css_selector("p.mb2.text-keep-space:nth-child(2) > strong")

        self.driver.set_page_load_timeout(10)
        print(last_message.text)
        assert last_message.text == "1 message"
        logger.warning(f'You have 1 message stored in this folder: {last_message.text}')

    def random_string(self): 
        chars = ''
        for x in range(10):
            chars = chars + \
                random.choice(
                    list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'))
        return chars

    def text_without_numbers(self):
        '''
        Сlear numbers from text
        '''
        theme = mailing.random_string()
        body = mailing.random_string()
        numbers = ['0','1','2','3','4','5','6','7','8','9']
        
        sum_theme_body = theme + body
        text_without_numbers = sum_theme_body

        for i in numbers:
            if text_without_numbers is i:
                pass
            else:
                res_str = text_without_numbers.replace(i , '')
                text_without_numbers = res_str
        return text_without_numbers

    def numbers_without_text(self):
        '''
        Сlear text from numbers
        '''
        theme = mailing.random_string()
        body = mailing.random_string()
        numbers = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O',
        'P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c',
        'd','e','f','g','h','i','j','k','l','m','n',
        'o','p','q','r','s','t','u','v','w','x','y','z']

        sum_theme_body = theme + body
        numbers_without_text = sum_theme_body

        for i in numbers:
            if numbers_without_text is i:
                pass
            else:
                res_str = numbers_without_text.replace(i , '')
                numbers_without_text = res_str
        return numbers_without_text

    def tearDown(self):
        self.driver.quit()
        logger.info('Browser closed')

if __name__ == '__main__':
    # Enter your login credentials here
    mailing = Protonmail(email='g12Q2dQCux@protonmail.com', password='g12Q2dQCux', browser='Chrome')
    mailing.login()
    mailing.sending_messages_ten_email()
    mailing.data_from_all_incoming_emails()
    mailing.send_collected_data_to_yourself()
    mailing.delete_all_received_emails()
    mailing.tearDown()