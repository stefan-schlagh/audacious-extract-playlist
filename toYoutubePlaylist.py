import sys,os,time,urllib
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


def main(argv):
    ToYoutubePlaylist(argv)

class ToYoutubePlaylist:
    def __init__(self,argv):
        try:
            self.executeOptions(argv)
            self.readTitles()
            self.createPlaylist()
        except Exception as e:
            traceback.print_exc()
            self.Log("Exited with an error: " + str(e))
    
    def Log(self,val):
        print(val)

    def executeOptions(self,argv):
        if(len(argv) == 0):
            self.Log("no args specified")
        else:
            for arg in argv:
                if("--src=" in arg):
                    self.srcPath = arg.replace("--src=","")

    def readTitles(self):
        f = open(self.srcPath, 'r',encoding='cp850')
        content = f.read().split("\n")
        f.close()
        titles = []
        for line in content:
            titles.append(line)
        self.titles = titles
    
    def createPlaylist(self):

        chrome_options = Options()    
        chrome_options.add_argument("--user-data-dir=chrome-data")
        driver = webdriver.Chrome('chromedriver.exe',options=chrome_options)
        
        i=61
        while i < len(self.titles):

            title = self.titles[i]

            #urlencode
            query = urllib.parse.urlencode({"search_query" : title})
            driver.get("https://www.youtube.com/results?" + query)
            time.sleep(0.9)
            # wait for searchbox
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#search-input.ytd-searchbox-spt")))
            # get video
            videoSelector = "ytd-video-renderer.style-scope:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > h3:nth-child(1) > a:nth-child(2)"
            videoElem = driver.find_element(By.CSS_SELECTOR, "ytd-thumbnail:nth-child(1) a:nth-child(1)")
            videoElem.click()

            time.sleep(0.4)
            #inputElem.send_keys("pycon")
            #inputElem.send_keys(Keys.RETURN)
            # wait for video
            saveSelector = "ytd-button-renderer.style-scope:nth-child(4) > a:nth-child(1) > yt-icon-button:nth-child(1) > button:nth-child(1)"
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, saveSelector)))
            saveElem = driver.find_element(By.CSS_SELECTOR, saveSelector)
            saveElem.click()

            time.sleep(0.2)

            # wait for playlist
            playlistSelector = "ytd-playlist-add-to-option-renderer.style-scope:nth-child(2) > tp-yt-paper-checkbox:nth-child(1) > div:nth-child(1)"
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, playlistSelector)))
            playlistElem = driver.find_element(By.CSS_SELECTOR, playlistSelector)
            playlistElem.click()

            time.sleep(2.5)

            self.Log(title + " saved!")
 
            i = i + 1

        self.Log("all songs saved!")

        driver.close()

if __name__ == "__main__":
   main(sys.argv[1:])