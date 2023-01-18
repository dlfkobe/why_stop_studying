# 同步编程
# import requests
# import  time
# def download_images(url):
#     print("开始下载：",url)
#     # 发送网络请求，下载图片
#     response = requests.get(url)
#     print("下载完毕")
#     file_name = url.rsplit("_")[-1]
#     with open(file_name,mode='wb') as file_object:
#         file_object.write(response.content)
        
# if __name__ == "__main__":
#     start = time.time()
#     url_list = [
#           'https://www3.autoimg.cn/newsdfs/g26/M02/35/A9/120x90_0_autohomecar__ChsEe12AXQ6AOOH_AAFocMs8nzU621.jpg',
#         'https://www2.autoimg.cn/newsdfs/g30/M01/3C/E2/120x90_0_autohomecar__ChcCSV2BBICAUntfAADjJFd6800429.jpg',
#         'https://www3.autoimg.cn/newsdfs/g26/M0B/3C/65/120x90_0_autohomecar__ChcCP12BFCmAIO83AAGq7vK0sGY193.jpg'
#     ]
#     for item in url_list:
#         download_images(item)
#     end = time.time()
#     print("所花时间{}".format(end-start))

# 大概0.4s

# 基于携程的异步编程

import aiohttp
import asyncio
import time

async def fetch(session,url):
    print("发送请求",url)
    async with session.get(url,verify_ssl=False) as response:
        content = await response.content.read()
        file_name = url.split("_")[-1]
        with open(file=file_name,mode='wb') as file_object:
            file_object.write(content)

async def main():
    async with aiohttp.ClientSession() as session:
        url_list = [
            'https://www3.autoimg.cn/newsdfs/g26/M02/35/A9/120x90_0_autohomecar__ChsEe12AXQ6AOOH_AAFocMs8nzU621.jpg',
            'https://www2.autoimg.cn/newsdfs/g30/M01/3C/E2/120x90_0_autohomecar__ChcCSV2BBICAUntfAADjJFd6800429.jpg',
            'https://www3.autoimg.cn/newsdfs/g26/M0B/3C/65/120x90_0_autohomecar__ChcCP12BFCmAIO83AAGq7vK0sGY193.jpg'
        ]
        tasks = [asyncio.create_task(fetch(session,url)) for url in url_list]
        await asyncio.wait(tasks)
        
if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    end = time.time()
    print("所花时间{}".format(end-start))
    
        
     