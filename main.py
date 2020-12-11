from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from tqdm import tqdm

id = "bible2"
pw = "bible22"

books = ["", "창세기", "출애굽기", "레위기", "민수기", "신명기", "여호수아", "사사기", "룻기", "사무엘상", "사무엘하", "열왕기상", "열왕기하", "역대상", "역대하", "에스라", "느헤미야", "에스더", "욥기", "시편", "잠언", "전도서", "아가", "이사야", "예레미야", "예레미야애가", "에스겔", "다니엘", "호세아", "요엘", "아모스", "오바댜", "요나", "미가", "나훔", "하박국", "스바냐", "학개", "스가랴", "말라기", "마태복음", "마가복음", "누가복음", "요한복음", "사도행전", "로마서", "고린도전서", "고린도후서", "갈라디아서", "에베소서", "빌립보서", "골로새서", "데살로니가전서", "데살로니가후서", "디모데전서", "디모데후서", "디도서", "빌레몬서", "히브리서", "야고보서", "베드로전서", "베드로후서", "요한1서", "요한2서", "요한3서", "유다서", "요한계시록"]

options = webdriver.ChromeOptions()
options.add_argument("headless")
options.add_argument("window-size=1920x1080")
options.add_argument("disable-gpu")
options.add_argument("log-level=3")

driver = webdriver.Chrome('chromedriver.exe', options=options)
driver.implicitly_wait(2)
driver.get('http://www.purebible.co.kr/user/login.php?returl=%2Fmain%2F')
driver.implicitly_wait(1)
driver.find_element_by_name("id").send_keys(id)
driver.find_element_by_name("pass").send_keys(pw)
driver.find_element_by_name("pass").submit()
driver.implicitly_wait(1)

print("로그인에 성공했습니다. ID: {0}".format(id))

book = input("작업을 시작할 성경을 입력하세요: ")
bookc = books.index(book)
chapter = input("몇 장부터 시작합니까? ")

driver.get('http://www.purebible.co.kr/bible/write.php?book={0}&chapter={1}&'.format(bookc, chapter))
driver.implicitly_wait(1)

chapters = driver.find_elements_by_class_name("btns2")

print("[#] {0} {1}장 확인되었습니다.".format(book, len(chapters)))
print("┌────────────────────────────────────────────────────────────────────────────────────────┐")

for o in range(int(chapter), len(chapters) + 1):
    driver.get('http://www.purebible.co.kr/bible/write.php?book={0}&chapter={1}&'.format(bookc, o))
    driver.implicitly_wait(1)
    nofont = driver.find_elements_by_class_name("nofont")
    for e in tqdm(nofont, bar_format="{l_bar}{bar:20}{r_bar}", desc="{0: >16}".format("{0} {1}장".format(book, str(o).zfill(2)))):
        m = driver.find_element_by_id("area{0}".format(nofont.index(e) + 1))
        if not "color:blue" in m.get_attribute("innerHTML"):
            parag = driver.find_element_by_id("area{0}".format(nofont.index(e) + 1)).get_attribute("txt")
            driver.find_element_by_id('txt').send_keys(parag)
            driver.find_element_by_id('txt').send_keys(Keys.ENTER)
    driver.switch_to.alert.accept()

print("└────────────────────────────────────────────────────────────────────────────────────────┘")
print("[#] {0} 작업이 완료되었습니다. 완료 장 수: {1}".format(book, len(chapters) - int(chapter) + 1))
print("")

for f in range(books.index(book) + 1, len(books)):
    driver.get('http://www.purebible.co.kr/bible/write.php?book={0}&'.format(f))
    driver.implicitly_wait(1)

    chapters = driver.find_elements_by_class_name("btns2")
    
    print("[#] {0} {1}장 확인되었습니다.".format(books[f], len(chapters)))
    print("┌────────────────────────────────────────────────────────────────────────────────────────┐")

    for o in range(1, len(chapters) + 1):
        driver.get('http://www.purebible.co.kr/bible/write.php?book={0}&chapter={1}&'.format(f, o))
        driver.implicitly_wait(1)
        nofont = driver.find_elements_by_class_name("nofont")
        for e in tqdm(nofont, bar_format="{l_bar}{bar:20}{r_bar}", desc="{0: >16}".format("{0} {1}장".format(books[f], str(o).zfill(2)))):
            m = driver.find_element_by_id("area{0}".format(nofont.index(e) + 1))
            if not "color:blue" in m.get_attribute("innerHTML"):
                parag = driver.find_element_by_id("area{0}".format(nofont.index(e) + 1)).get_attribute("txt")
                driver.find_element_by_id('txt').send_keys(parag)
                driver.find_element_by_id('txt').send_keys(Keys.ENTER)
        driver.switch_to.alert.accept()
    print("└────────────────────────────────────────────────────────────────────────────────────────┘")
    print("[#] {0} 작업이 완료되었습니다. 완료 장 수: {1}".format(books[f], len(chapters)))
    print("")

print("[#] 성경 1회독을 완료했습니다.")

driver.quit()