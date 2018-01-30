from selenium import webdriver
import time
import requests
import os
from tkinter import *

#Global variables
askName = ""
askPass = ""
DesiredID = ""
noOfPosts = None
data = []
imageLinks = []
driver = None

app = Tk()
app["bg"] = "#333"
app.title("Instagram Photo Downloader")
app.geometry('330x350+200+100')

Done = Label(app,
                text = '',
                bg = '#333',
                fg = 'white',
                height = '1',
                font=("segoe ui", 11)
                )

def scrollDownAndGather():
    global noOfPosts,data
    lastHeight = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        newHeight = driver.execute_script("return document.body.scrollHeight")
        if newHeight == lastHeight:
            break
        lastHeight = newHeight

    data = driver.find_elements_by_xpath('//div[@class="_4rbun"]/img')
    if(len(data) != noOfPosts):
        scrollDownAndGather()
    else:
        return

def exractLinks():
    global data,imageLinks
    for element in data:
        link = element.get_attribute('src')
        imageLinks.append(link)

    driver.quit()

def folderCheck():
    folderPath = r'C:' + "\\" + DesiredID
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
        os.chdir(folderPath)
    else:
        os.chdir(folderPath)

def downloader():
    global imageLinks,noOfPosts
    folderCheck()
    ctr = 0
    for link in imageLinks:
        ctr += 1
        r = requests.get(link)
        with open(str(ctr) + ".jpg", 'wb') as f:
            f.write(r.content)


def starter():
    global driver, askName, askPass, DesiredID, noOfPosts
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(60)
    driver.get("https://www.instagram.com/accounts/login/")
    uname = driver.find_element_by_name('username')
    pwd = driver.find_element_by_name('password')
    logIn = driver.find_element_by_tag_name('button')
    uname.send_keys(askName)
    pwd.send_keys(askPass)
    logIn.click()
    time.sleep(3)
    driver.get("https://www.instagram.com/" + DesiredID + "/")
    noOfPosts = driver.find_element_by_xpath('//li[@class="_bnq48"]/span/span').text
    noOfPosts = int(noOfPosts.replace(',', ''))

def soul():
    starter()
    scrollDownAndGather()
    exractLinks()
    downloader()



Info  = Label(app,
                text = '',
                bg = '#333',
                fg = 'white',
                height = '1',
                font=("segoe ui", 11)
                )

def e1Karya(*args):
        global askName
        askName = e1.get()

def e2Karya(*args):
        global askPass
        askPass = e2.get()

def e3Karya(*args):
        global DesiredID
        DesiredID = e3.get()
        Info['text'] = "Images will be stored in C:\\{}".format(DesiredID)

heading = Label(app,
                text = "Instagram Photo Downloader",
                bg = '#ff3e3e',
                fg = 'white',
                height = '1',
                font=("segoe ui", 16)
                ).grid(row = 0, column =0, sticky='w',padx=30)

enterID = Label(app,
                text = "User ID",
                bg = '#35b1ea',
                fg = 'white',
                height = '1',
                font=("segoe ui", 14)
                ).grid(row = 1, column =0, sticky='w',padx=5, pady=10)
e1 = Entry(app,
                bg = 'white',
                fg = 'black',
                font=("segoe ui", 14)
                )
e1.bind("<KeyRelease>", e1Karya)
e1.place(x = 113, y =47)

enterPswd = Label(app,
                text = "Password",
                bg = '#35b1ea',
                fg = 'white',
                height = '1',
                font=("segoe ui", 14)
                ).grid(row = 2, column =0, sticky='w',padx=5)
e2 = Entry(
                bg = 'white',
                fg = 'black',
                font=("segoe ui", 14),
                show = '*'
                )
e2.bind("<KeyRelease>", e2Karya)
e2.place(x = 113 , y =88 )

RequiredID  = Label(app,
                text = "Required ID",
                bg = '#35b1ea',
                fg = 'white',
                height = '1',
                font=("segoe ui", 14)
                ).grid(row = 3, column =0, columnspan=2, sticky='w',padx=5, pady=10, )
e3 = Entry(
                bg = 'white',
                fg = 'black',
                font=("segoe ui", 14),
                )
e3.bind("<KeyRelease>", e3Karya)
e3.place(x = 113 , y =128 )

goButton = Button(app,
        text = "Do it !",
        #height = '1',
        width = '10',
        bd = '5',
        font=("segoe ui", 12),
        command = soul,
        ).place(x = 110 , y = 200)

Info.place(x=10, y=250)
Done.place(x = 10 , y = 270)

app.mainloop()