import re
import requests
import socket
from bs4 import BeautifulSoup


if __name__ == '__main__':
    site = 'sstmk.ru'
    # маска под +A(BBB)CCC-CC-CC
    phone_mask = re.compile(r'(\+\d{1,3})?\(\d+\)\d+-\d+-\d+')

    response = requests.get(f'https://www.{site}/')

    # проверяем, что сайт работает
    if response.status_code == 200:
        # узнаём ip адрес хоста, но в задании не было сказано его выводить куда-то, поэтому я и не стал
        ip = socket.gethostbyname(site)
        # находим номер на главной странице
        soup = BeautifulSoup(response.content, 'html.parser')
        # в задании был указан один конкретный сайт, так что я пропарсил именно его конкретную структуру
        phone = soup.find('div', class_='phone-number').contents[0].text
        # "очищаем" номер
        phone = re.sub(' ', '', phone)
        if phone.startswith('8'):
            phone = '+7' + phone[1:]
        """
        Проверяем валидность номера
        Я немного запутался в критериях, потому что там не указанно по сути что мы подразумеваем под номером,
        обязательны ли там скобки, из скольки цифр должен состоять номер и т.д., поэтому сделал всё строго по ТЗ.
        И даже так по сути номер на сайте должен быть не валидным, потому что он не соответствует маске 
        +A(BBB)CCC-CC-CC, так как начинается с "8", а это никак не подогнать под "+А". Я это немного подправил, но всё
        равно как-то криво чувствуется. Я бы поконкретнее хотел обсудить ТЗ, но не письмом, а голосом, а то ещё больше
        путаниц может возникнуть.
        """
        is_phone_valid = bool(phone_mask.match(phone))
        if is_phone_valid:
            print(phone)
        else:
            print(f'Номер {phone} не соответствует критериям')
    else:
        print('Не удалось получить доступ к сайту')
