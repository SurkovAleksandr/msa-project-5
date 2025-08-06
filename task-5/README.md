**Подсказки по подготовке окружения**

1. Установите Docker и Docker Compose
2. Для удобства просмотра кода может понадобиться:

   a. Установите JDK 17
   b. Установите Gradle (или используйте встроенную в Idea)

   c. Установите Idea

   **Сборка приложения**

   ```
   ./gradlew build
   ```


**Создание образа**

   ```
   docker build . -t batch-processin
   ```


**Запуск приложения**

   ```bash
   docker-compose up 
   ```

При запуске приложения необходимо создать таблицы в БД использую любой удобный клиент, используя скрипты расположенные здесь

    *task-4/initial/src/main/resources/schema-all.sql*

Получаемые компоненты:
- PostgreSQL (порт 5432)(5432 host машина)


- batch-processing
- grafana
- prometheus
- filebnat
- logstash
- elasticsearch


