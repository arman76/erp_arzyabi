# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from time import sleep
from telegram import ReplyKeyboardMarkup
import app


reply_keyboard = [['20'],
                  ['19'],
                  ['18'],
                  ['17'],
                  ['16'],
                  ['15'],
                  ['14'],
                  ['13'],
                  ['12']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def main(user_data, bot, update):
    with open('n.txt', 'w') as f:
        f.write('1')
    driver = webdriver.PhantomJS()
    try:
        driver.get("http://erp.guilan.ac.ir/Dashboard.aspx")
        if 'erp.guilan.ac.ir/GoToDashboard.aspx' in driver.current_url:
            driver.find_element_by_class_name('refreshDash').click()

        wait = WebDriverWait(driver, 10)
        elem = wait.until(ec.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'ورود به س')))
        elem.click()
        elem = wait.until(ec.presence_of_element_located((By.ID, 'iframe_040101')))

        driver.get(elem.get_property('src'))
        elem = driver.find_element_by_name('SSMUsername_txt')
        elem.send_keys(user_data['username'])

        elem = driver.find_element_by_name('SSMPassword_txt')
        elem.send_keys(user_data['password'] + Keys.ENTER)
        elem = wait.until(ec.presence_of_element_located((By.ID, 'FLASH_URL_TAB_ID')))
        elem.click()

        elem22 = wait.until(ec.presence_of_element_located((By.ID, 'iframe_FLASH_URL_TAB_ID')))
        driver.get(elem22.get_property('src'))
        elemfs = wait.until(ec.presence_of_all_elements_located((By.CLASS_NAME, 'Eval-grid')))
        while True:
            elemfs[0].click()
            sleep(2)
            tabs = driver.window_handles
            driver.close()
            driver.switch_to.window(tabs[1])
            elems = wait.until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, 'input[type="button"]')))
            while True:
                elems[0].click()
                sleep(2)
                tabs = driver.window_handles
                print(tabs)
                driver.switch_to.window(tabs[1])
                elem = wait.until(ec.presence_of_element_located((By.ID, 'InfoLbl')))
                print(elem.text)
                bot.send_message(chat_id=update.message.chat.id, text= elem.text + '\n نمره رو بزن:' , reply_markup=markup)
                t = 0
                print('tt')
                while t <= 20:
                    print('t1')
                    if user_data['nomre'] == -1:
                        if t == 20:
                            reply_keyboard2 = [['فرستادن نام کاربری و کلمه عبور (username, password)'],
                                               ['شروع']]
                            markup2 = ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=True)

                            bot.send_message(chat_id=update.message.chat.id, text='خب تایمت تموم شد! بای بای!', reply_markup=markup2)
                            driver.close()
                            with open('n.txt', 'w') as f:
                                f.write('0')
                            exit()
                        sleep(1)
                        t += 1
                    else:
                        break
                nomre = user_data['nomre']
                print(nomre)
                els = wait.until(ec.presence_of_all_elements_located((By.TAG_NAME, 'input')))
                avali = 1
                for el in els:
                    if avali == 1:
                        if nomre == 8:
                            nomre -= 1
                        else:
                            nomre += 1
                        avali = 0
                    if el.get_attribute('id')[:3] == 'rb' + str(nomre):
                        el.click()
                elem = wait.until(ec.presence_of_element_located((By.ID, 'btnContinue')))
                elem.click()
                sleep(2)
                driver.close()
                driver.switch_to.window(tabs[0])
                user_data['nomre'] = -1
                if len(elems) == 1:
                    break
                elems = wait.until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, 'input[type="button"]')))
            if len(elemfs) == 1:
                break
            driver.get(elem22.get_property('src'))
            elemfs = wait.until(ec.presence_of_all_elements_located((By.CLASS_NAME, 'Eval-grid')))
        bot.send_message(chat_id=update.message.chat.id, text='خب تموم شششددددد !!!!!')
        driver.close()
        with open('n.txt', 'w') as f:
            f.write('0')
        exit(0)

    except Exception as e:
        print(e.args)
        print(user_data)
        reply_keyboard2 = [['فرستادن نام کاربری و کلمه عبور (username, password)'],
                          ['شروع']]
        markup2 = ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=True)

        bot.send_message(chat_id=update.message.chat.id, text='به ارور برخوردیم! شاید فرم ارزشیابی تموم شده باشه شایدم یوزر پسورد اشتباه باشه', reply_markup=markup2)
        try:
            driver.close()
            with open('n.txt', 'w') as f:
                f.write('0')
        except Exception as e:
            print(e.args)
            pass
