import time
import mss.tools
import cv2

from pytesseract import pytesseract

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

with mss.mss() as sct:

    #takes a screenshot of the monitor within the parameters we gave it
    areaToScreenshot = {"top": 705, "left": 1120, "width": 125, "height": 25}
    #saves that as the output
    output = "sct-{top}x{left}_{width}x{height}.png".format(**areaToScreenshot)

    #grabs the data of the area to screenshot
    sct_img = sct.grab(areaToScreenshot)

    #outputs the data into a png file
    mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
    print(output)
    
#I personally put time sleep 3 just to give the code time to process the screenshot and ensuring it's there before attempting to read it for strings
#not sure if it is required
time.sleep(3)
#library required to be able to read the image for string
pytesseract.tesseract_cmd = 'C:\\Users\\johal\\tesseract\\tesseract.exe'
#tell the code which png to search through
screenshotTaken = cv2.imread("sct-705x1120_125x25.png")

#take the strings it finds from the image and output it to the console
getWordsInImage = pytesseract.image_to_string(screenshotTaken)
print(getWordsInImage)

#stops the chrome browser created from the code to auto close after completing it's code - allowing it to stay open till i manually close
chrome_options = Options() 
chrome_options.add_experimental_option("detach", True)
#creates the chrome tab
driver = webdriver.Chrome(options=chrome_options)
#what website to go to
driver.get("https://warframe.market")
#looked within the elements of the page and found the searchbar had a placeholder name so told the code that's where we want put the text we found from the image into.
searchBarOnSite = driver.find_element(By.XPATH, "//input[@placeholder='Search...']").send_keys(getWordsInImage + Keys.RETURN)