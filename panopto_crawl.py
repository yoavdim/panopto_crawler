#!/usr/bin/env python3

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
#from urllib.request import urlretrieve
from time import sleep
import re

# inputs:
link="https://panoptotech.cloud.panopto.eu/Panopto/Pages/Sessions/List.aspx#folderID=%221e865a58-a282-4879-8eab-acf1010cbaa8%22"
course_name="compilers"

# code:
profile_folder = "profile"
name_regex = r"[ :_\-\*]+"

def run():
    options = Options()
    options.add_argument("--user-data-dir=" + profile_folder) # chrome specific
    driver = webdriver.Chrome(options=options)
    driver.get(link)

    # log-in in the browser if needed
    while(link != driver.current_url):
        sleep(0.5)
    sleep(2) # todo smarter wait

    folder_name = course_name + "/" + driver.find_element(By.ID, "contentHeaderText").get_attribute("innerText")
    print(folder_name) # will distinguish between lectures & toturials

    lecture_anchors = driver.find_elements(By.CLASS_NAME, "detail-title")
    for lecture in [l.get_attribute("href") for l in lecture_anchors if l.get_attribute("href")]:
        # iterate each video site
        print("goto: " + lecture)
        driver.get(lecture)
        sleep(2) #todo: wait onload

        primary   = driver.find_element(By.ID, "primaryVideo"  ).get_attribute("src")
        secondary = driver.find_element(By.ID, "secondaryVideo").get_attribute("src")
        title     = driver.find_element(By.ID, "deliveryTitle" ).get_attribute("innerText")
        #download - for now only print
        title = re.sub(name_regex, "_", title)
        print(title)
        download_video(folder_name, title+"_slides.mp4", driver.get_cookies(), primary)
        download_video(folder_name, title+"_camera.mp4", driver.get_cookies(), secondary)
    # end for
    driver.quit()
    return


def download_video(target_folder, file_name, cookies, url):
    pass
  




if __name__ == '__main__':
    run();
