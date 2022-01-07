import urllib, pydub, os
import speech_recognition as sr
from random import randint
from time import sleep
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

site = 'https://www.google.com/recaptcha/api2/demo'

option = Options()
option.headless = False

def delay():
    sleep(randint(2,3))
driver = webdriver.Chrome(ChromeDriverManager().install(), options=option)
driver.get(site)

#switch to recaptcha frame
frames = driver.find_elements_by_tag_name('iframe')
driver.switch_to.frame(frames[0])
delay()

#click on checkbox to active recapthca
driver.find_element_by_class_name("recaptcha-checkbox-border").click()

#switch to recaptcha audio control frame
driver.switch_to.default_content()
frames = driver.find_element_by_xpath("/html/body/div[2]/div[4]").find_elements_by_tag_name("iframe")
driver.switch_to.frame(frames[0])
delay()

#click on audio challenge
driver.find_element_by_id("recaptcha-audio-button").click()

#switch to recaptcha audio challenge frame
driver.switch_to.default_content()
frames = driver.find_elements_by_tag_name("iframe")
driver.switch_to.frame(frames[-1])
delay()

#click on the play button
driver.find_element_by_xpath("/html/body/div/div/div[3]/div/button").click()

#get the mp3 audio file
src = driver.find_element_by_id("audio-source").get_attribute("src")
print("[INFO] AUdio src: %s"%src)
#downlaod the mp3 audio file from the source
urllib.request.urlretrieve(src, os.getcwd()+"\\sample.mp3")
sound = pydub.AudioSegment.from_mp3(os.getcwd()+"\\sample.mp3")
sound.export(os.getcwd()+"\\sample.wav",format="wav")
sample_audio = sr.AudioFile(os.getcwd()+"\\sample.wav")
r = sr.Recognizer()
with sample_audio as source:
    audio = r.record(source)

#Tranlate
key = r.recognize_google(audio)
print("[INFO] Recaptcha Passcode: %s"%key)

#Write phrase
driver.find_element_by_xpath('//*[@id="audio-response"]').send_keys(key)
delay()

#Verify
driver.find_element_by_xpath('//*[@id="recaptcha-verify-button"]').send_keys(key)