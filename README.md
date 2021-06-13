# Big Data Project(Topic3 - Wiki)

# Архітектура проєкту

![Diagram](./documentation/diagrams/Diagram.png)

1) За допомогою Kafka Producer ми зчитуємо дані з Wiki
2) Kafka Producer пише ці дані в Kafka
3) За допомогою Spark Streaming опрацьовуєм ці дані і пише
   в базу даних
4) Spark Bath Processing вичитує дані з бази даних за
   період часу(6 годин) і формує звіти, які потім записує
   в Google Bucket
5) Django server робить запити в базу даних для того, щоб сформувати корисутвачу
ad-hoc queries і віддає їх користувачу
6) Django server зчитує звіти з Google Bucket і віддає користувачу   


# Структура бази даних

![Diagram](./documentation/diagrams/DB_schema.png)

# REST API
### 1 Query
![ad_hoc_1](./documentation/rest_api/ad_hoc_1.png)
Перша ad-hoc query, яка повертає список всіх доменів,
які існуюють.

URL:
```
 /wiki/domains/
```
### 2 Query
![ad_hoc_2](./documentation/rest_api/ad_hoc_2.png)
Друга ad-hoc query, яка повертає список всіх статей,
які написав конкретний юзер за його id.

URL:
```
 /wiki/user/index=<str:pk>/
```
Де `<str:pk>` - це юзер id
### 3 Query
![ad_hoc_3](./documentation/rest_api/ad_hoc_3.png)
Третя ad-hoc query, яка повертає кількість статтей,
які написані під конкретним доменом.

URL:
```
 /wiki/domain/name=<str:pk>/
```
Де `<str:pk>` - це ім'я домену
### 4 Query
![ad_hoc_4](./documentation/rest_api/ad_hoc_4.png)
Четверта ad-hoc query, яка повертає інформацію про статтю
за її id.

URL:
```
 /wiki/page/index=<str:pk>/
```
Де `<str:pk>` - це id сторінки
### 5 Query
![ad_hoc_5](./documentation/rest_api/ad_hoc_5.png)
П'ята ad-hoc query, яка повертає інформацію про юзерів,
які створили хоча б одну сторінку за даний проміжок часу.

URL:
```
 /wiki/time/start=<str:date_start>&end=<str:date_end>
```
Де `<str:date_start>` - це початок часового проміжку
   `<str:date_end>` - це кінець часового проміжку 

# Файл змінних середовища
Для більшого захисту паролю і інші даних про базу даних,
яка розгорнута на клауді були винесені в ``.env`` файл.
Його потрібно створити в кореневій папці.
Його структура:
```
   export DB_HOST = ''
   export DB_NAME = ''
   export DB_USER = ''
   export DB_PASSWORD = ''
   export DB_PORT = ''
```