from bs4 import BeautifulSoup
import os
import requests
from tkinter import simpledialog
import tkinter.messagebox

headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.46"}
filePath = "F:\\AndroidSource"
hrefList=[]
storey=0

def main():
    url = simpledialog.askstring('AS',prompt="网址",initialvalue='http://aospxref.com')
    if(url != None):
        print("download "+url)
        getURLContext(url);

def getURLContext(url):
    global hrefList
    #把list当作一个对象，url存储当前层数的url,1代表
    list=[url,1,0]
    hrefList.append(list)
    recursion(hrefList)

def recursion(hrefList):
    global filePath
    global storey
    if storey<0 or len(hrefList)<1 :
        return
    listcopy=[]
    list = hrefList[storey]
    res = requests.get(list[0],headers=headers)
    soup = BeautifulSoup(res.text,"html.parser")
    trs = soup.find("tbody").find_all("tr")
    if  list[1]>len(trs)-1:
        storey-=1
        del hrefList[len(hrefList)-1]
        print(hrefList)
        hrefList[len(hrefList)-1][1]+=1
        recursion(hrefList)
    elif  len((trs[list[1]].find_all("td"))[2].find_all("a"))>=3:
        path = createFileIsExists(list[0])
        filePath = "F:\\AndroidSource"
        deal_url(list[0],path)
        storey-=1
        del hrefList[len(hrefList)-1]
        if(len(hrefList)==0):
            createFinishWin()
            return;
        hrefList[len(hrefList)-1][1]+=1
        recursion(hrefList)
    else:
        storey+=1
        u =list[0]+"/"+trs[list[1]].find_all("a")[0].text 
        listcopy=[u,1,storey]
        hrefList.append(listcopy)
        listcopy=[]
        recursion(hrefList)
    
def deal_url(url,path):
    global headers
    res = requests.get(url,headers=headers)
    so = BeautifulSoup(res.text,"html.parser")
    list1 = so.find("tbody").find_all("tr")
    for tr in list1:     
        if len(tr.find_all("td"))==5:        
            continue;
        elif len(tr.find_all("td")[2].find_all("a"))>=3:            
            saveFile("http://aospxref.com"+tr.find_all("td")[2].find_all("a")[2].get("href"),path) 
            

def createFileIsExists(url):
    global filePath
    files = url.split("http://aospxref.com/android-12.0.0_r3/xref/")[1].split("/");
    for file in files:    
        filePath+="\\"+file
        if not os.path.exists(filePath):
            os.makedirs(filePath)
    return filePath


#保存文件
def saveFile(href,filepath):
     global headers
     str = href.split("/")[len(href.split("/"))-1] 
     res = requests.get(href,headers=headers)  
     with open(filepath+"\\"+str,"wb+") as f:
      f.write(res.content)
      f.flush()
      f.close()

#弹出结束框
def createFinishWin():
    root = tkinter.Tk()
    root.withdraw()
    tkinter.messagebox.showinfo(title="Andoird",message="Success")


if __name__ == "__main__":
    main()
    



