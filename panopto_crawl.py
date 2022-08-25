#!/usr/bin/env python3

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep
import os.path
import os
import re

# inputs:
link="https://panoptotech.cloud.panopto.eu/Panopto/Pages/Sessions/List.aspx#folderID=%221e865a58-a282-4879-8eab-acf1010cbaa8%22"
course_name="compilers"
results_folder="./vids"
is_folder=True

# code:
profile_folder = "profile"
timeout = 3
name_regex = r"[ :,_/\-\*\\]+"  # remove symbols from file name
suffix = {
    "primary"  : "_camera.mp4",
    "secondary": "_slides.mp4",
    "single"   : "_video.mp4"   # if only a single video is available
}

def run():
    # # log-in in the browser if needed
    # driver = setup_driver()
    # load_n_wait(driver, link)
    # # switch to headless after signup
    # driver.quit() 
    driver = setup_driver(is_headless=True)
    hidden_load_n_wait(driver, link)

    folder_name = os.path.join(results_folder, course_name)
    if is_folder:
        folder_name = os.path.join(folder_name, clean_text(driver.find_element(By.ID, "contentHeaderText").get_attribute("innerText")))
        print(folder_name + ":") # will distinguish between lectures & toturials
        print()

    # get the single-lecture links from the folder
    if is_folder:
        lecture_anchors = driver.find_elements(By.CLASS_NAME, "detail-title")
        lecture_links = [l.get_attribute("href") for l in lecture_anchors if l.get_attribute("href")]
    else:
        lecture_links = [link,]

    # iterate each video site
    for lecture in lecture_links:
        hidden_load_n_wait(driver, lecture)

        title     = driver.find_element (By.ID, "deliveryTitle" ).get_attribute("innerText")
        primary   = driver.find_element (By.ID, "primaryVideo"  ).get_attribute("src")
        secondary = driver.find_elements(By.ID, "secondaryVideo")
        if secondary:  # not always available
            secondary = secondary[0].get_attribute("src")

        #download - doesnt pass cookies, assumes unnecessary 
        title = clean_text(title)
        print(title)
        main_suffix = suffix["primary"] if secondary else suffix["single"]
        download_video(folder_name, title + main_suffix, primary)
        if secondary: 
            download_video(folder_name, title + suffix["secondary"], secondary)
    # end for
    driver.quit()
    return



def download_video(target_folder, file_name, url):
    os.makedirs(target_folder, exist_ok=True)
    file_path = os.path.join(target_folder, file_name)
    if not os.path.exists(file_path):
        os.system( f"wget --show-progress -O '{file_path}' '{url}'" )
    else:
        print( f"Video already exists: '{file_name}'" )
    

def clean_text(text):
    return re.sub(name_regex, "_", text)


def hidden_load_n_wait(driver, url):
    driver.get(url)
    sleep(0.5)
    if url != driver.current_url:  # if login is required again
        # reveal for login
        visible_driver = setup_driver(is_headless=False)
        visible_driver.get(url)
        while url != visible_driver.current_url:  # if login is required again
            sleep(0.5)
        # reload page in headless
        driver.get(url)
        sleep(2)
    else
        sleep(2-0.5)  # wait for assets to load


def load_n_wait(driver, url):
    driver.get(url)
    while url != driver.current_url:  # if login is required again
        sleep(0.5)
    sleep(2) # todo smarter wait


def setup_driver(is_headless=False):
    options = Options()
    options.add_argument("--user-data-dir=" + profile_folder) # chrome specific
    if is_headless:
        options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    return driver


if __name__ == '__main__':
    try:
        run()
    except:
        # sleep(180)
        raise
