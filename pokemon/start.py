from selenium import webdriver
import time

from selenium import webdriver

player1="mmyd123456"
player2="123yyyy"

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
browser = webdriver.Chrome(chrome_options=options)
browser.get('http://play.pokemonshowdown.com/')
browser.implicitly_wait(3)

# 1st player
button_choose_name = browser.find_element_by_name('login')#find choose name button
button_choose_name.click()

browser.find_element_by_name('username').send_keys(player1)#find useranme input
browser.find_element_by_xpath("//div[@class='ps-popup']/form/p[@class='buttonbar']/button[@type='submit']").submit()#player1 log in


# 2nd player
browser.execute_script("window.open('http://play.pokemonshowdown.com/')")  # open another window
browser.switch_to.window(browser.window_handles[1]) # switch to the new window
button_choose_name = browser.find_element_by_name('login')#button to choose name
button_choose_name.click()

browser.find_element_by_name('username').send_keys(player2)#find username input
browser.find_element_by_xpath("//div[@class='ps-popup']/form/p[@class='buttonbar']/button[@type='submit']").submit()#player2 log in

# switch to 1st user
browser.switch_to.window(browser.window_handles[0])

button_find_user = browser.find_element_by_name('finduser')#button to find user
button_find_user.click()

browser.find_element_by_name('data').send_keys(player2)#find username input
browser.find_element_by_xpath("//div[@class='ps-popup']/form/p[@class='buttonbar']/button[@type='submit']").submit()

button_challenge = browser.find_element_by_name('challenge')# make a challenge
browser.implicitly_wait(3)
button_challenge.click()

button_make_challenge = browser.find_element_by_name('makeChallenge')# start a challenge
browser.implicitly_wait(3)
button_make_challenge.click()

# switch to 2nd user
browser.switch_to.window(browser.window_handles[1])
button_accept_challenge = browser.find_element_by_name('acceptChallenge')# accept the challenge
browser.implicitly_wait(3)
button_accept_challenge.click()
