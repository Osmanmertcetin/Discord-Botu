from tkinter import *
import json
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from tkinter.filedialog import askopenfile
from tkinter import messagebox
from selenium.webdriver.edge.options import Options
import codecs



master = Tk()
master.geometry("350x350")
master.configure(bg="#04726f")
master.resizable(width=False, height=False)
master.title("Discord Veri Botu")
basliklar = Frame(bg="lightgray",width=350,height=25)
basliklar.place(x=0,y=0)

token = StringVar(master)
server = StringVar(master)
channel = StringVar(master)
email = StringVar(master)
sifre = StringVar(master)
dosya_yolu = StringVar(master)
delay = IntVar(master)
istek = IntVar(master)
delay_dakika = IntVar(master)
channel.set(0)

def clearFrame():

    for widget in altFrame.winfo_children():
        widget.destroy()


def importMain():
    
    import main




def veriCekme_Baslat():
    
    if(len(token.get())==0 or len(server.get())==0):
        messagebox.showwarning("Uyarı","Token id veya Server id boş bırakılamaz!")
    
    
    else:
        token_id = token.get()
        server_id = server.get()
        channel_id = channel.get()
        
        dict = {}

        dict["token"] = token_id
        dict["guild_id"] = server_id
        dict["pfp_format"] = "png"
        dict["purge_old_data"] = True
        dict["download_pfp"] = True
        if len(channel.get())==0: dict["channel_id"] = 0 
        else: dict["channel_id"] = int(channel_id)

        json_object = json.dumps(dict, indent=4)
        with open("config.json", "w") as outfile:
            outfile.write(json_object)

        t1 = threading.Thread(target=importMain)

        t1.start()


def arkadasEkle_Baslat():

    if(len(dosya_yolu.get())==0):
        messagebox.showwarning("Uyarı","Arkadaş eklemeyi başlatmadan önce lütfen veri dosyasını seçiniz!")
    else:
        sayac = 0

        with open(dosya_yolu.get(),encoding="utf8") as f:
            lines = f.readlines()
        f.close()

        usernames = []
        for i in lines:
            usernames.append(i[0:-1])
        
        send_email = email.get()
        send_password = sifre.get()

        options = Options()
        options.add_experimental_option("detach", True)

        driver = webdriver.Edge(options=options)

        driver.get("https://discord.com/login")
        time.sleep(5)

        email_input = driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/div[1]/div[1]/div/div/div/div/form/div[2]/div/div[1]/div[2]/div[1]/div/div[2]/input')
        email_input.send_keys(send_email)

        time.sleep(1)

        password_input = driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/div[1]/div[1]/div/div/div/div/form/div[2]/div/div[1]/div[2]/div[2]/div/input')
        password_input.send_keys(send_password)

        time.sleep(1)

        login_button = driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/div[1]/div[1]/div/div/div/div/form/div[2]/div/div[1]/div[2]/button[2]')
        login_button.click()

        time.sleep(4)

        friends_button = driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/div[1]/div[1]/div/div[2]/div/div/div/div/main/section/div[1]/div[4]/div[5]')
        friends_button.click()
        time.sleep(3)
        
        copy_usernames = usernames.copy()
        for username in usernames:
            if(istek.get()!=0 and sayac>istek.get()):
                time.sleep(delay_dakika.get()*60)
                sayac = 0
            try:


                username_input = driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/div[1]/div[1]/div/div[2]/div/div/div/div/main/div/div[1]/header/form/div[2]/div/input')
                username_input.send_keys(username)

                time.sleep(1)

                addfriend_button= driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/div[1]/div[1]/div/div[2]/div/div/div/div/main/div/div[1]/header/form/div[2]/button')
                addfriend_button.click()
                sayac = sayac +1
                copy_usernames.remove(username)
                file = codecs.open(dosya_yolu.get(),"w",encoding="utf-8")
                for x in copy_usernames:
                    file.write(x+"\n")
                time.sleep(delay.get())
                remove_username = username
            
            except:
                try:
                    ok_button = driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/div[1]/div[3]/div[2]/div/div/form/div[2]/button')
                    ok_button.click()
                    time.sleep(3)
                    username_input2 = driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/div[1]/div[1]/div/div[2]/div/div/div/div/main/div/div[1]/header/form/div[2]/div/input')
                    username_input2.clear()
                    time.sleep(1)
                    copy_usernames.remove(remove_username)
                    file = codecs.open(dosya_yolu.get(),"w",encoding="utf-8")
                    file.write("")
                    file.close()
                    file = codecs.open(dosya_yolu.get(),"a",encoding="utf-8")
                    for x in copy_usernames:
                        file.write(x+"\n")
                    continue
                except:
                    pass

            


    

def veriCekme_sekmesi():

    clearFrame()

    token_label = Label(altFrame,text="Token:")
    token_label.place(x=15,y=35)
    token_entry = Entry(altFrame,textvariable=token,width=45)
    token_entry.place(x=60,y=35)

    serverId_label = Label(altFrame,text="Server Id:")
    serverId_label.place(x=15,y=70)
    serverId_entry = Entry(altFrame,textvariable=server,width=40)
    serverId_entry.place(x=89,y=70)

    channelId_label = Label(altFrame,text="Channel Id:")
    channelId_label.place(x=15,y=105)
    channelId_entry = Entry(altFrame,textvariable=channel,width=40)
    channelId_entry.place(x=89,y=105)

    veriCekmeBaslat_butonu = Button(altFrame,text="Veri Çekmeyi Başlat",command=veriCekme_Baslat)
    veriCekmeBaslat_butonu.place(x=115, y=160)



def arkadasEkle_sekmesi():
    
    clearFrame()
    delay.set(3)
    email_label = Label(altFrame,text="E-mail:")
    email_label.place(x=15,y=25)
    email_entry = Entry(altFrame,textvariable=email,width=40)
    email_entry.place(x=70,y=25)

    sifre_label = Label(altFrame,text="Şifre:")
    sifre_label.place(x=15,y=60)
    sifre_entry = Entry(altFrame,textvariable=sifre,width=40)
    sifre_entry.place(x=70,y=60)

    veriYolu_label = Label(altFrame,text="Veri\nDosyası:")
    veriYolu_label.place(x=15,y=95)
    veriYolu_entry = Entry(altFrame,textvariable=dosya_yolu,width=40,state="disabled")
    veriYolu_entry.place(x=70,y=102)

    delay_label = Label(altFrame,text="İstekler Arası Bekleme Süresi (Saniye):")
    delay_label.place(x=15,y=140)
    delay_entry = Entry(altFrame,textvariable=delay,width=15)
    delay_entry.place(x=220,y=140)

    istekSayisi_label = Label(altFrame,text="Kaç İstekten Sonra Beklemeye Girsin:")
    istekSayisi_label.place(x=15,y=175)
    istekSayisi_entry = Entry(altFrame,textvariable=istek,width=15)
    istekSayisi_entry.place(x=220,y=175)

    delayDakika_label = Label(altFrame,text="Kaç Dakika Beklesin:")
    delayDakika_label.place(x=15,y=210)
    delayDakika_entry = Entry(altFrame,textvariable=delay_dakika,width=15)
    delayDakika_entry.place(x=220,y=210)

    veriSec_butonu = Button(altFrame,text="Veri Dosyasını Seç",command=dosya_sec)
    veriSec_butonu.place(x=20, y=260)

    arkadasEkleBaslat_butonu = Button(altFrame,text="Arkadaş Eklemeyi Başlat",command=arkadasEkle_Baslat)
    arkadasEkleBaslat_butonu.place(x=175, y=260)

def dosya_sec():

    dosya_yolu.set(askopenfile(filetypes=[("Txt","*.txt")]).name)

def hakkinda():
    messagebox.showinfo("Hakkında","Bu Program pyHunter tarafından yapılmıştır.\n İletişim:instagram.com/pyhunter \n bionluk.com/pyhunter \n Discord:pyHunter#0698")

altFrame = Frame(bg="#5865f2",width=350,height=325)
altFrame.place(x=0,y=25)


veriCekme_butonu = Button(basliklar,text="Veri Çekme",command=veriCekme_sekmesi)
veriCekme_butonu.place(x=0, y=0)

arkadasEkle_butonu = Button(basliklar,text="Arkadaş Ekle",command=arkadasEkle_sekmesi)
arkadasEkle_butonu.place(x=70, y=0)

hakkinda_butonu = Button(basliklar,text="Hakkında",command=hakkinda)
hakkinda_butonu.place(x=146, y=0)

veriCekme_sekmesi()

master.mainloop()





