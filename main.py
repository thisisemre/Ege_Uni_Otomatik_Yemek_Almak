import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
import datetime

KULLANICI_ADI = "Lütfen bu alana sadece öğrenci numaranızı giriniz"
SIFRE = "Lütfen bu alana şifrenizi giriniz"

OGLE_YEMEK = "https://sks2noluyemek.ege.edu.tr/YemekRezervasyon.aspx?o=O&Yemekhane=02"
AKSAM_YEMEK = "https://sks2noluyemek.ege.edu.tr/YemekRezervasyon.aspx?o=A&Yemekhane=02"
SEPET = "https://sks2noluyemek.ege.edu.tr/Sepetim.aspx"
bugun = int(datetime.datetime.now().day)
buay = int(datetime.datetime.now().month)
aylar = {
    "ocak": 1,
    "şubat": 2,
    "mart": 3,
    "nisan": 4,
    "mayıs": 5,
    "haziran": 6,
    "temmuz": 7,
    "ağustos": 8,
    "eylül": 9,
    "ekim": 10,
    "kasım": 11,
    "aralık": 12
}

os.environ["PATH"] += "SeleniumDrivers/chromedriver.exe"
driver = webdriver.Chrome()


def yemek_sec():
    yemek_tarih = driver.find_element(By.XPATH, '//*[@id="ctl00"]/div[4]/div[2]/table/tbody/tr[2]/td[2]').text.split(
        " ")
    yemek_tarih_gun = int(yemek_tarih[0])
    yemek_tarih_ay = aylar[yemek_tarih[1].lower()]

    click_sayisi = 0
    if yemek_tarih_ay == buay:
        if yemek_tarih_ay == 2:  # şubat demek 28 çekiyor yani
            if yemek_tarih_gun <= 18:
                alinacak_son_gun = bugun + 10  # kod her perşembe gece 12'den öncki herhangi bir saate çalışıcaktır
                if alinacak_son_gun >= yemek_tarih_gun:
                    click_sayisi = alinacak_son_gun - yemek_tarih_gun + 1
            else:
                alinacak_son_gun = bugun + 10  # kod her perşembe gece 12'den öncki herhangi bir saate çalışıcaktır
                if alinacak_son_gun >= yemek_tarih_gun:
                    click_sayisi = alinacak_son_gun - yemek_tarih_gun + 1-28

        elif yemek_tarih_ay in [1, 3, 5, 7, 8, 10, 12]:  # 31 çekiyor
            if yemek_tarih_gun <= 21:
                alinacak_son_gun = bugun + 10  # kod her perşembe gece 12'den öncki herhangi bir saate çalışıcaktır
                if alinacak_son_gun >= yemek_tarih_gun:
                    click_sayisi = alinacak_son_gun - yemek_tarih_gun + 1
            else:
                alinacak_son_gun = bugun + 10  # kod her perşembe gece 12'den öncki herhangi bir saate çalışıcaktır
                if alinacak_son_gun >= yemek_tarih_gun:
                    click_sayisi = alinacak_son_gun - yemek_tarih_gun + 1 - 31
        else:  # 30 çekiyor
            if yemek_tarih_gun <= 20:
                alinacak_son_gun = bugun + 10  # kod her perşembe gece 12'den öncki herhangi bir saate çalışıcaktır
                if alinacak_son_gun >= yemek_tarih_gun:
                    click_sayisi = alinacak_son_gun - yemek_tarih_gun + 1
            else:
                alinacak_son_gun = bugun + 10  # kod her perşembe gece 12'den öncki herhangi bir saate çalışıcaktır
                if alinacak_son_gun >= yemek_tarih_gun:
                    click_sayisi = alinacak_son_gun - yemek_tarih_gun + 1 - 30

    clickler = driver.find_elements(By.CLASS_NAME, "form-control")
    sayac = 0
    for click in clickler:
        if sayac == click_sayisi:
            break
        else:
            click.click()
            sayac += 1

    driver.find_element(By.ID, "ContentPlaceHolder1_btnSepetEkle").click()


driver.get("https://kimlik.ege.edu.tr/")

username = driver.find_element(By.ID, "username")
username.send_keys(KULLANICI_ADI)

password = driver.find_element(By.ID, "password")
password.send_keys(SIFRE)
password.send_keys(Keys.ENTER)

yemekhane = driver.find_element(By.CSS_SELECTOR, "#yemekhanebtn > span")
yemekhane.click()

sleep(1)
driver.find_element(By.LINK_TEXT, "2 No'lu Yemekhane").click()
sleep(2)  # web sitesi authentication'ı kodun çalıştığı kadar hızlı yapamadığı için burada beklemek hata almamak için gerekli
driver.execute_script("window.open('');")
driver.switch_to.window(driver.window_handles[1])
driver.get(OGLE_YEMEK)

yemek_sec()
driver.switch_to.window(driver.window_handles[2])
driver.get(AKSAM_YEMEK)
yemek_sec()
driver.get(SEPET)

driver.find_element(By.ID, "ContentPlaceHolder1_btnSatinAl").click()

while (True):
    pass
