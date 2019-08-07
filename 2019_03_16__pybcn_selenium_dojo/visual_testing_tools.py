import time
import os

from PIL import ImageOps, Image

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeDriverManager
from webdriver_manager.microsoft import IEDriverManager


def get_driver(browser, width, height):
    if browser == 'Chrome':
        driver = webdriver.Chrome(ChromeDriverManager().install())
    elif browser == 'Firefox':
        driver = webdriver.Firefox(GeckoDriverManager().install())
    elif browser == 'Edge':
        driver = webdriver.Edge(EdgeDriverManager().install())
    elif browser == 'IE':
        driver = webdriver.Ie(IEDriverManager().install())
    else:
        raise Exception(browser + ' is not avaliable')

    driver.set_window_size(width, height)
    return driver


def get_full_page_screenshot_with_fixed_header(driver):

    total_width = driver.execute_script("return document.body.offsetWidth")
    total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
    viewport_width = driver.execute_script("return document.body.clientWidth")
    viewport_height = driver.execute_script("return window.innerHeight")
    pixel_ratio = driver.execute_script("return window.devicePixelRatio")
    header_height = driver.execute_script("return document.getElementsByClassName('s·header')[0].offsetHeight")

    print("Total: ({0}, {1}), Viewport: ({2},{3}), PixelRatio: {4}".format(total_width, total_height, viewport_width,
                                                                           viewport_height, pixel_ratio))
    time.sleep(5)
    slice_index = 0
    driver.get_screenshot_as_file('part_{}.png'.format(slice_index))

    driver.execute_script("document.getElementsByClassName('s·header')[0].style.boxShadow = 'none'")  # hide shadow

    height_without_header = viewport_height - header_height

    for slice_index in range(1, int(total_height / height_without_header)):
        driver.execute_script('window.scrollBy(0, {})'.format(height_without_header))
        time.sleep(1)
        driver.get_screenshot_as_file('part_{}.png'.format(slice_index))
        border = (0, header_height * pixel_ratio, 0, 0)  # left, up, right, bottom
        img = Image.open('part_{}.png'.format(slice_index))
        img = ImageOps.crop(img, border)
        img.save('part_{}.png'.format(slice_index))

    remaining_height = (total_height - viewport_height) % (viewport_height - 104)
    slice_index += 1
    driver.execute_script('window.scrollBy(0, {})'.format(height_without_header))
    time.sleep(0.5)
    driver.get_screenshot_as_file('part_{}.png'.format(slice_index))
    border = (0, (viewport_height - remaining_height) * pixel_ratio, 0, 0)  # left, up, right, bottom
    img = Image.open('part_{}.png'.format(slice_index))
    img = ImageOps.crop(img, border)
    img.save('part_{}.png'.format(slice_index))

    images = [Image.open('part_{}.png'.format(image_index)) for image_index in range(slice_index+1)]

    widths, heights = zip(*(i.size for i in images))

    total_width = max(widths)
    max_height = sum(heights)

    new_im = Image.new('RGB', (total_width, max_height))

    y_offset = 0

    for im in images:
        new_im.paste(im, (0, y_offset))
        os.remove(im.filename)
        y_offset += im.size[1]

    return new_im  # .save('full_screenshot.png')
