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


savePath = 'D:\\huya-download'
filename = 'fffff.ts'

if __name__ == '__main__':
    for page in range(1, 7):
        videoIdList = parseHtmlPage("https://v.huya.com/u/1428788783/livevideo.html?p=" + str(page))
        for videoId in videoIdList:
            jsonText = requests.get(
                "https://v-api-player-ssl.huya.com/?callback=jQuery112407112155431315372_1603350254420&r=vhuyaplay%2Fvideo&vid="
                + videoId + "&format=mp4%2Cm3u8&_=1603350254446").text
            jsonText = jsonText.replace('jQuery112407112155431315372_1603350254420(', '')
            jsonText = jsonText[0:len(jsonText) - 1]
            download_message = json.loads(jsonText)
            items = download_message['result']['items']
            item = items[len(items) - 1]
            m3u8_url = item['transcode']['urls'][0]
            m3u8Downloader.download(m3u8_url, savePath, filename)
            break
        break
