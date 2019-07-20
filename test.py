# -*- coding: utf-8 -*-

__author__ = 'CoolCat'

import asyncio
from pyppeteer import launch


async def screenshot(url):
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.setViewport({'width': 1920, 'height': 1080})
    await page.goto(url)
    imageName = url.replace("https://", "").replace("http://", "").replace("/","") + ".png"
    await page.screenshot({'path': imageName})
    await browser.close()
url = 'http://www.qq.com/'
asyncio.get_event_loop().run_until_complete(screenshot(url))