# _*_ coding:utf-8 _*_

'''


                     ,----------------,              ,---------,
                ,-----------------------,          ,"        ,"|
              ,"                      ,"|        ,"        ,"  |
             +-----------------------+  |      ,"        ,"    |
             |  .-----------------.  |  |     +---------+      |
             |  |                 |  |  |     | -==----'|      |
             |  |  I LOVE PYTHON! |  |  |     |         |      |
             |  |  Bad command or |  |  |/----|`---=    |      |
             |  |  C:\>import fly |  |  |   ,/|==== ooo |      ;
             |  |                 |  |  |  // |(((( [33]|    ,"
             |  `-----------------'  |," .;'| |((((     |  ,"
             +-----------------------+  ;;  | |         |,"
                /_)______________(_/  //'   | +---------+
           ___________________________/___  `,
          /  oooooooooooooooo  .o.  oooo /,   \,"-----------
         / ==ooooooooooooooo==.o.  ooo= //   ,`\--{)B     ,"
        /_==__==========__==_ooo__ooo=_/'   /___________,"
         



目标: 下载快视频首页各类别视频的下载连接(http://k.360kan.com/)
      由于“美女”和“360影视”是连向站外网址的，所以没有进行抓取分类
PYTHON版本: 3.6.3
日期: 2018.4.26
作者: Andy-Leo

'''

import requests
import socket
import json

socket.setdefaulttimeout(10)
channel_id = {
    '推荐': '0'       #Recommend
    '广场舞': '127',  #Square dance
    '搞笑': '2',      #Fun
    '音乐': '13',     #Music
    '社会': '3',      #Sociology
    '影视': '8',      #Movies
    '生活': '18',     #Life
    '健康': '110',    #Healthy
    '军事': '19',     #Military
    '娱乐': '1',      #Entertainment
    '科技': '7',      #Science and Technology
    '游戏': '11',     #Game
    '体育': '12'      #Sport
}


def get_download_link(url):

    respones = requests.get(url)
    list_data = respones.json()
    return list_data['data']['url']


def get_page_index(page_num,channel_id):

    url = 'http://pc.k.360kan.com/pc/list?n=10&p={}&f=json&ajax=1&uid=3ee1bcd645ffd683c7355769152f0516&channel_id={}&dl='.format(str(page_num),channel_id)
    respones = requests.get(url)
    list_data = respones.json()['data']['res']
    return list_data

def get_infor(page_num,channel_id):
    results = get_page_index(page_num,channel_id)
    item = {}
    for result in results:
        playLink = result['exData']['playLink']
        item['title'] = result['t']
        item['author'] = result['f']
        item['download_link'] = get_download_link(playLink)
        yield item, len(results)


def main(category):
    page_num = 1
    items_sum = 10
    with open('%s.json'%category,'w',encoding='utf-8') as f:
        try:
            while True:
                items = get_infor(page_num,channel_id[category])
                for item, _ in items:
                    f.write(json.dumps(item,indent=4,ensure_ascii=False))
                    items_sum = _
                page_num += 1
                print(page_num)#会实时打印抓取到第几页
                if items_sum <5:#返回的项目小于5时退出程序
                    break
        except:
            pass
        finally:
            f.close()

if __name__ == '__main__':

    main('搞笑')  # 要下什么分类栏下的视频在这里改，一定要用英文下的引号""括起来
#下载保存的文件在该py文件所在的同个目录下
#写得比较简陋，高效的翻页没添加进来，感觉连接里p=参数写多大都会有respones返回成功，所以程序不错出的话会一直抓取下去，可能需要手动停止程序
