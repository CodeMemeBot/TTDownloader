import os
import time
import requests
import shutil
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options  
import colorama
import argparse
#colorama.init() #Enable this if you use windows
banner=colorama.Fore.CYAN+"Thot Tube Downloader"+colorama.Fore.RESET
proceed=True #used to proceed the loop to get all images
parser = argparse.ArgumentParser(description = banner)
param = parser.parse_args()
chrome_options = Options()
chrome_options.add_argument('log-level=3')

browser = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"),   chrome_options=chrome_options)
os.mkdir("stuff") #creates directory to store images
def findimage(string):
 start= string.find('data-g1-share-image="') #removes the starting garbage chars first
 string=string[start+21::]
 end= string.find('""') #removes the ending garbage chars next
 string=string[:end]
 return string

def printposts():
 #browser.execute_script("")
 global proceed #global variable to proceed the while loop
 i=1 #incremente variable to get all images
 browser.get(input("\n"+colorama.Fore.CYAN+"Insert the album url: "+colorama.Fore.RESET)) #get url and load album
 print(colorama.Fore.CYAN+"Downloading images..."+colorama.Fore.RESET)
 time.sleep(2)
 searchBtn = browser.find_elements_by_class_name("mace-gallery-teaser-button")
 searchBtn = searchBtn[0]
 webdriver.ActionChains(browser).click(searchBtn).perform() #click to open the album
 time.sleep(2)
 while proceed==True: #get all images links
  posts = browser.find_elements_by_class_name('g1-gallery-frame-'+str(i))
  if (len(posts)>0):
   postshtml=posts[0].get_attribute('data-g1-share-image')
   #print(postshtml)
   #stuff to get image and save it
   r = requests.get(postshtml, stream=True,headers={'User-agent': 'Mozilla/5.0'})
   if r.status_code == 200:
    with open("stuff/"+str(i)+".jpg", 'wb') as f:
     r.raw.decode_content = True
     shutil.copyfileobj(r.raw, f)
   i=i+1
  else:
   proceed=False
   browser.quit()
   print(colorama.Fore.GREEN+"Images downloaded successfully"+colorama.Fore.RESET)
   

printposts()
inp=input("Press enter to end")
browser.quit()
 
