import datetime
import json

import requests
from lxml import etree

import m3u8Downloader


# https://v-api-player-ssl.huya.com/?callback=jQuery112407112155431315372_1603350254420&r=vhuyaplay%2Fvideo&vid=403295673&format=mp4%2Cm3u8&_=1603350254446

# 解析一页html
def parseHtmlPage(url):
    html = requests.get(url).text
    dom = etree.HTML(html)
    divList = dom.xpath('/html/body/div[4]')[0]
    videoIdList = []
    for div in divList:
        if len(div) == 1:
            continue
        videoList = div[1][0]
        for video in videoList:
            videoIdList.append(video[0].get('href')[6:15])
    return videoIdList


def checkVideoId(baseFolderPath, videoId):
    file = open(baseFolderPath + "/downloaded-video-id-list.txt")
    while True:
        line = file.readline()
        line = line[0:len(line) - 1]
        if line == videoId:
            file.close()
            return True
        elif not line:
            file.close()
            return False


baseFolderPath = 'D:\\huya-download'


def saveNewVideoId(videoId):
    file = open(baseFolderPath + "/downloaded-video-id-list.txt", "a")
    file.write(str(videoId) + "\n")
    file.close()


def downloadSingleVideo(videoId):
    jsonText = requests.get(
        "https://v-api-player-ssl.huya.com/?callback=jQuery112407112155431315372_1603350254420&r=vhuyaplay%2Fvideo&vid="
        + str(videoId) + "&format=mp4%2Cm3u8&_=1603350254446").text
    jsonText = jsonText.replace('jQuery112407112155431315372_1603350254420(', '')
    jsonText = jsonText[0:len(jsonText) - 1]
    download_message = json.loads(jsonText)

    ustime = int(download_message['result']['ustime'])
    timeString = datetime.datetime.fromtimestamp(ustime).strftime("%Y-%m-%d_%H-%M-%S")
    items = download_message['result']['items']
    item = items[len(items) - 1]
    m3u8_url = item['transcode']['urls'][0]
    m3u8Downloader.download(m3u8_url, baseFolderPath, timeString + '_' + str(videoId) + '.mp4')

    # 当下载完成时，将videoId写入文件
    saveNewVideoId(videoId)


if __name__ == '__main__':
    # for page in range(7, 1, -1):
    #     videoIdStringList = parseHtmlPage("https://v.huya.com/u/1428788783/livevideo.html?p=" + str(page))
    #     videoIdList = []
    #     for videoIdString in videoIdStringList:
    #         videoIdList.append(int(videoIdString))
    #     videoIdList = sorted(videoIdList)
    #     for videoId in videoIdList:
    #         # 先检查本地存的videoId，如果已经有了，则跳过
    #         result = checkVideoId(baseFolderPath, videoId)
    #         if result:
    #             continue
    #         downloadSingleVideo(videoId)
    downloadSingleVideo(381833223)
