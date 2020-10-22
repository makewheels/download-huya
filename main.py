import requests
from lxml import etree


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


if __name__ == '__main__':
    for page in range(1, 7):
        videoIdList = parseHtmlPage("https://v.huya.com/u/1428788783/livevideo.html?p=" + str(page))
        print(videoIdList)
