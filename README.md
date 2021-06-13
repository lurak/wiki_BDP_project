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