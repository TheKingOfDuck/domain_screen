# -*- coding: utf-8 -*-

__author__ = 'CoolCat'

import asyncio
from pyppeteer import launch
import sys
import shutil

# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     srcScan
   Description :
   Author :       CoolCat
   date：          2019/3/14
-------------------------------------------------
   Change Activity:
                   2019/3/14:
-------------------------------------------------
"""

# coding=utf-8

import re
import requests
import time
import os
import socket

global info
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
htmlHeader = """
<!DOCTYPE html>
<head>

  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <link href="../template_files/main.css" rel="stylesheet" type="text/css">
  <title>子域名扫描报告</title></head>
<body style="padding-right: 320px;">
  <div class="main-inner">
    <div id="posts" class="posts-expand">
      <header class="post-header">
        <h1 class="post-title" itemprop="name headline">子域名扫描报告</h1>
        <div class="post-meta">
          <span class="post-time">
            <span class="post-meta-item-text">生成于</span>
            <time title="Post created" itemprop="dateCreated datePublished">timeaaaaaaa</time></span>
        </div>
      </header>
      <div class="post-body" itemprop="articleBody">
"""

htmlcat = """
        <aside id="sidebar" class="sidebar sidebar-active" style="display: block; width: 320px;">
          <div class="sidebar-inner">
            <ul class="sidebar-nav motion-element" style="opacity: 1; display: block; transform: translateX(0px);">
              <li class="sidebar-nav-toc sidebar-nav-active" data-target="post-toc-wrap">目录</li></ul>
            <!--noindex-->
            <section class="post-toc-wrap motion-element sidebar-panel sidebar-panel-active" style="opacity: 1; display: block; transform: translateX(0px);">
              <div class="post-toc" style="max-height: 750px; width: calc(100% + 0px);">
                <div class="post-toc-content">
                  <ol class="nav">
"""

htmlfooter = """
      <div>
        <div style="padding: 10px 0; margin: 20px auto; width: 90%; text-align: center;">
          <div>扫描赞赏二维码，救救没钱的孩子吧！</div>
          <div id="QR" style="display: block;">
            <div id="wechat" style="display: inline-block">
                <img id="wechat_qr" src="../template_files/wechat.jpg" ></a>
              <p>微   信</p>
            </div>
            <div id="alipay" style="display: inline-block">
                <img id="alipay_qr" src="../template_files/alipay.png" ></a>
              <p>支付宝</p>
            </div>
          </div>
        </div>

"""

htmlcat2 = """
                    <li class="nav-item nav-level-1">
                        <a class="nav-link" href="#domain.com">
                            <span class="nav-number">nnnnn.</span>
                            <span class="nav-text">domain.com</span></a>
                    </li>
"""


def getIP(domain):
    myaddr = socket.getaddrinfo(domain, 'http')
    return "IP：" + str(myaddr[0][4][0])


def getInfo(res):
    try:
        Server = res.headers["Server"]
    except:
        Server = None
        pass
    try:
        code = res.headers["X-Powered-By"]
    except:
        code = None
        pass
    return "Server:" + str(Server) + "\t    Code:" + str(code)


def scanurl(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}
    res = requests.get(url=url, headers=headers, timeout=5, verify=False)
    return res


def urlformat(site):
    site = site.replace("\"", "").replace("\n", "")
    if "http" in site:
        return site
    elif site.strip():
        return "http://" + site + "/"
    else:
        pass


def outPut(target, title, imageName):
    ip = getIP(str(re.compile('http://(.*?)/').findall(target)[0]))

    domain = target.replace("https://", "").replace("http://", "").replace("/", "")

    temp = """
          <h1 id="domain1234">title1234</h1>
          <a href="httpurl1234" target="_blank">httpurl1234</a></br>
          <a>ip1234</a></br>
          <a>info1234</a></br>
          <img src="cat.png1234">
          </br>
    """

    ### temp瞎几把加了几个1234是为了防止提取到的信息中包含这几个字符串，会乱掉。

    temp = temp.replace('domain1234', domain).replace('title1234', title).replace('httpurl1234', target).replace(
        'ip1234', ip).replace('info1234', info).replace('cat.png1234', "../images/" + imageName)

    with open("./reports/" + reportFile, "a") as f:
        f.write(temp + "\n")


async def screenshot(url):
    browser = await launch({'headless': True,
                            'args': [
                                '--disable-extensions',
                                '--disable-infobars',
                                '--hide-scrollbars',
                                '–disable-dev-shm-usage',
                                '--mute-audio',
                                '–disable-setuid-sandbox',
                                '–no-sandbox',
                                '–no-zygote',
                                '--window-size=1024,768',
                                '--disable-gpu',
                            ],
                            # 防止多开页面卡死
                            'dumpio': True,
                            'ignoreHTTPSErrors': True,
                            'executablePath': '/Applications/Chromium.app/Contents/MacOS/Chromium'})
    page = await browser.newPage()
    await page.goto(url, timeout=10000)
    await page.setViewport({'width': 1000, 'height': 698})
    await page.waitFor(1000)
    imageName = url.replace("https://", "").replace("http://", "").replace("/", "") + ".png"
    await page.screenshot({'path': './images/' + imageName})
    try:
        element = await page.querySelector('title')
        title = await page.evaluate('(element) => element.textContent', element)
    except:
        title = 'no title'
    await browser.close()
    outPut(url, title, imageName)


if __name__ == '__main__':
    for root, dirs, files in os.walk(os.getcwd(), topdown=False):
        for name in files:
            file = os.path.splitext(name)
            txtfilename, type = file
            if type == '.txt' and 'finished' not in root:
                srcfile = (root + '/' + name)
                dstfile = (root + '/finished/' + name)
                reportFilename = txtfilename
                if not os.path.exists('reports') or not os.path.exists('images'):
                    try:
                        os.makedirs("reports")
                    except:
                        pass
                    try:
                        os.makedirs("images")
                    except:
                        pass

                htmlHeader = htmlHeader.replace('timeaaaaaaa', str(time.strftime("%Y-%m-%d")))

                reportFile = str(time.strftime("%Y-%m-%d-{}".format(reportFilename))) + ".html"

                if os.path.exists("./reports/" + reportFile):
                    os.remove("./reports/" + reportFile)

                with open("./reports/" + reportFile, "w") as f:
                    f.write(htmlHeader)

                n = 0
                tmp = ""
                with open(srcfile) as sites:
                    for site in sites:
                        site = site.replace("\r", "").replace("\n", "").replace(" ", "")
                        if site == "":
                            pass
                        else:

                            url = urlformat(site)
                            print(url)
                            try:
                                res = scanurl(url)
                                print("[*]" + str(res.status_code) + "\t" + url)
                                try:
                                    info = getInfo(res)
                                except:
                                    info = None
                                    pass

                                if res.status_code == 200 or res.status_code == 403 or res.status_code == 404:
                                    n += 1
                                    domain = url.replace("https://", "").replace("http://", "").replace("/", "")

                                    try:
                                        asyncio.get_event_loop().run_until_complete(screenshot(url))
                                        tmp += htmlcat2.replace("domain.com", domain).replace("nnnnn", str(n)) + "\n"
                                    except Exception as e:
                                        pass

                            except:

                                pass

                    # 写目录1

                    with open("./reports/" + reportFile, "a") as f:
                        f.write(htmlcat)

                    # 写目录2

                    with open("./reports/" + reportFile, "a") as f:
                        f.write(tmp)

                    # 乞讨信息
                    with open("./reports/" + reportFile, "a") as f:
                        f.write(htmlfooter)

                    shutil.move(srcfile, dstfile)
