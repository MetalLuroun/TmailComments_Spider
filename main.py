import requests                          #https://mp.weixin.qq.com/s/9FUWopB--BPYe0f-K2lT2g       爬取天猫商品评论
from bs4 import  BeautifulSoup as bs
import json
import csv
import re

#宏变量存储目标js的URL列表
COMMENT_PAGE_URL = []

#生成链接列表
def Get_Url(num):
    urlFront = 'https://rate.tmall.com/list_detail_rate.htm?itemId=632024255161&spuId=0&sellerId=3821987386&order=3&currentPage='
    urlRear = '&append=0&content=1&tagId=&posi=&picture=&groupId=&ua=098%23E1hvgpvpvB9vUvCkvvvvvjiWP2Lh1j3URLdZtjEUPmPyAj1HnLsv0j38PFqw1jlhRvhvCvvvphmevpvhvvCCB29CvvpvvhCvvvhvC9mvphvvvv9CvhACIVByjwmOV1Oqb64B9Cka%2BfvsxI2hV36t%2BFBCAfyp%2Bu6wjo2hQC465i3lBWAQRqJ6WeCpqU0QKfUpwZLIAfUTKFyK2ixrVXeK5FXXKvhv8vvvphvvvvvvvvCVB9vvvcyvvhXVvvmCWvvvByOvvUhwvvCVB9vv9BAUvpvVvpCmp%2F2wuvhvmvvvpLJrCP7d29hvCvvvMM%2FVvpvhvUCvpvOCvvDw7rMNzjl71GK%2BvpvEvUHpZ46vvviidvhvmpvCnLCUvvmxS4QCvvyv9WLCRpvvD5VvvpvZ7DSfvUNw7Di4kCM5MvCfWHdWz69gvpvhvvCvpv%3D%3D&needFold=0&_ksTS=1608113068972_1889&callback=jsonp1890'
    for i in range(0,num):
        COMMENT_PAGE_URL.append(urlFront+str(1+i)+urlRear)


#获取评论数据
def GetInfo(num):
    #定义需要的字段
    nickname = []
    auctionSku = []
    ratecontent = []
    ratedate = []
    #循环获取每一页评论
    for i in range(num):
        #头文件，没有头文件会返回错误的js
        headers = {
            'cookie':'cna=qMU/EQh0JGoCAW5QEUJ1/zZm; enc=DUb9Egln3%2Fi4NrDfzfMsGHcMim6HWdN%2Bb4ljtnJs6MOO3H3xZsVcAs0nFao0I2uau%2FbmB031ZJRvrul7DmICSw%3D%3D; lid=%E5%90%91%E6%97%A5%E8%91%B5%E7%9B%9B%E5%BC%80%E7%9A%84%E5%A4%8F%E5%A4%A9941020; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; hng=CN%7Czh-CN%7CCNY%7C156; x=__ll%3D-1%26_ato%3D0; t=2c579f9538646ca269e2128bced5672a; _m_h5_tk=86d64a702eea3035e5d5a6024012bd40_1551170172203; _m_h5_tk_enc=c10fd504aded0dc94f111b0e77781314; uc1=cookie16=V32FPkk%2FxXMk5UvIbNtImtMfJQ%3D%3D&cookie21=U%2BGCWk%2F7p4mBoUyS4E9C&cookie15=UtASsssmOIJ0bQ%3D%3D&existShop=false&pas=0&cookie14=UoTZ5bI3949Xhg%3D%3D&tag=8&lng=zh_CN; uc3=vt3=F8dByEzZ1MVSremcx%2BQ%3D&id2=UNcPuUTqrGd03w%3D%3D&nk2=F5RAQ19thpZO8A%3D%3D&lg2=U%2BGCWk%2F75gdr5Q%3D%3D; tracknick=tb51552614; _l_g_=Ug%3D%3D; ck1=""; unb=3778730506; lgc=tb51552614; cookie1=UUBZRT7oNe6%2BVDtyYKPVM4xfPcfYgF87KLfWMNP70Sc%3D; login=true; cookie17=UNcPuUTqrGd03w%3D%3D; cookie2=1843a4afaaa91d93ab0ab37c3b769be9; _nk_=tb51552614; uss=""; csg=b1ecc171; skt=503cb41f4134d19c; _tb_token_=e13935353f76e; x5sec=7b22726174656d616e616765723b32223a22393031623565643538663331616465613937336130636238633935313935363043493362302b4d46454e76646c7243692b34364c54426f4d4d7a63334f44637a4d4455774e6a7378227d; l=bBIHrB-nvFBuM0pFBOCNVQhjb_QOSIRYjuSJco3Wi_5Bp1T1Zv7OlzBs4e96Vj5R_xYB4KzBhYe9-etui; isg=BDY2WCV-dvURoAZdBw3uwj0Oh2yUQwE5YzQQ9qAfIpm149Z9COfKoZwV-_8q0HKp',
            'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'referer': 'https://detail.tmall.com/item.htm?spm=a1z10.5-b-s.w4011-17205939323.51.30156440Aer569&id=41212119204&rn=06f66c024f3726f8520bb678398053d8&abbucket=19&on_comment=1&sku_properties=134942334:3226348',
            'accept': '*/*',
            'accept-encoding':'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9'
        }
        #解析JS文件内容
        content = requests.get(COMMENT_PAGE_URL[i],headers=headers).text
        nk = re.findall('"displayUserNick":"(.*?)"', content)
        nickname.extend(nk)
        print(nk)
        auctionSku.extend(re.findall('"auctionSku":"(.*?)"', content))
        ratecontent.extend(re.findall('"rateContent":"(.*?)"', content))
        ratedate.extend(re.findall('"rateDate":"(.*?)"', content))
    #将数据写入TEXT文件中
    for i in list(range(0, len(nickname))):
        text = ','.join((nickname[i], ratedate[i], auctionSku[i], ratecontent[i])) + '\n'
        with open(r"124.txt", 'a+',encoding='UTF-8') as file:
            file.write(text + ' ')
            print(i+1,":写入成功")

#主函数
if __name__ == "__main__":
    Page_Num = 5               #爬取100页
    Get_Url(Page_Num)            #调用Get_Url()方法
    GetInfo(Page_Num)                 #调用GetInfo()方法
