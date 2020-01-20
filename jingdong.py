import requests
from bs4 import BeautifulSoup
import xlwt
import time
from selenium import webdriver

def h5_se(page):
    driver = webdriver.Chrome()
    try :
        b1=driver.get('https://list.jd.com/list.html?cat=12218,12221&page='+ str(page)+'&sort=sort_totalsales15_desc&trans=1&JL=4_2_0#J_main"')
        b2=driver.refresh()
        time.sleep(2)
    except Exception as e:
        pass
    time.sleep(2)
    a = driver.page_source
    b3= driver.close()
    return a  
#水果类目下的销量排序结果，1&JL=4_2_0意思是销量排讯

n=1

book=xlwt.Workbook(encoding='utf-8-sig',style_compression=0)

sheet=book.add_sheet('京东水果信息',cell_overwrite_ok=True)
sheet.write(0,0,'商品名称')
sheet.write(0,1,'sku')
sheet.write(0,2,'价格')
sheet.write(0,3,'店铺')
sheet.write(0,4,'标签')
sheet.write(0,5,'链接')

def save_to_excel(soup):
    list = soup.find(class_='gl-warp clearfix').find_all(class_='gl-item')
    
    for item in list:
        item_product_id = item.find(class_='gl-i-wrap j-sku-item').get('data-sku')
        if len(item.find(class_='p-name').find_all('span'))==2:
            item_product_name_be = item.find(class_='p-name').find('em').text.strip('span').split("              ")
            item_product_name=item_product_name_be[len(item_product_name_be)-1]
        else:
            item_product_name = item.find(class_='p-name').find('em').text
        item_product_price = item.find(class_='J_price').text.replace('¥','')
        
        if len(item.find(class_='p-shop'))!=0:
            item_stroe_name = item.find(class_='p-shop').find('a').get('title')
        else:
            item_stroe_name ="~"
            
        item_product_info_all = item.find(class_='p-icons J-pro-icons').text
        item_product_link1 = item.find(class_='p-img').find('a').get('href')
        item_product_link='http:'+item_product_link1
        
        global n
        
        sheet.write(n,0,item_product_name)
        sheet.write(n,1,item_product_id)
        sheet.write(n,2,item_product_price)
        sheet.write(n,3,item_stroe_name)
        sheet.write(n,4,item_product_info_all)
        sheet.write(n,5,item_product_link)
        
        n=n+1

def main(page):
    soup = BeautifulSoup(h5_se(page),"lxml")
    save_to_excel(soup)

if __name__ == '__main__':
    start = time.time()
    for i in range(1, 11):
        main(i)
        i=i+1
    end = time.time()
    print("完成时间: %f s" % (end - start))  
    
 book.save(u'京东水果信息.xls')
