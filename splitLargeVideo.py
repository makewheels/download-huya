import os

if __name__ == '__main__':
    basePath = 'D:/huya-download'
    list = os.listdir(basePath)
    # 遍历
    for fileName in list:
        # 如果是文件
        fullPath = basePath + '/' + fileName
        basePath = basePath.replace('\\', '/')
        if os.path.isfile(fullPath):
            # 如果大小超过4g
            fileSize = os.path.getsize(fullPath)
            if fileSize >= 4 * 1024 * 1024 * 1024:
                baseName = fileName[0:fileName.rindex('.')]
                targetFolder = basePath + '/' + baseName
                if not os.path.exists(targetFolder):
                    os.makedirs(targetFolder)
                cmd1 = 'ffmpeg -i \"' + fullPath + '\" -ss 00:00:00 -t 02:30:00 -c copy \"' \
                       + targetFolder + '/' + baseName + '_1.mp4\"'
                cmd2 = 'ffmpeg -i \"' + fullPath + '\" -ss 02:30:00 -c copy \"' \
                       + targetFolder + '/' + baseName + '_2.mp4\"'
                print(cmd1)
                os.system(cmd1)
                print(cmd2)
                os.system(cmd2)
