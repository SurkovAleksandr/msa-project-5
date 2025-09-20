**Подсказки по подготовке окружения**
- [Объяснение работы Spring Batch - Importing CSV Data into PostgreSQL using Spring Boot Batch](https://stacktips.com/articles/importing-csv-data-into-postgresql-using-spring-boot-batch)
- [Пример использования jbatch](https://github.com/dalexandrov/jbatch-demo)
  [Очень полезное Видео](https://www.youtube.com/watch?v=4_dQHnkQ1lg) - Дмитрий Александров — JBatch или далеко не самые большие данные
  Объясняются темы:
  - checkpoint
  - partition
  - flow/split
  - desicion
  - метрики

**Подготовка окружения**

1. Установите Docker и Docker Compose
2. Для удобства просмотра кода может понадобиться:

   a. Установите JDK 17
   b. Установите Gradle (или используйте встроенную в Idea)

   c. Установите Idea

   **Сборка приложения**

```shell
cd ./complete 
./gradlew build
```

**Создание образа**
```shell
docker rmi batch-processing
docker build -t batch-processing ./complete
```


**Запуск приложения**

```shell
docker compose -f ./complete/docker-compose.yml up 
```

При запуске приложения необходимо создать таблицы в БД использую любой удобный клиент, используя скрипты расположенные здесь

    *task-4/initial/src/main/resources/schema-all.sql*

Получаемые компоненты:
- PostgreSQL (порт 5432)(5432 host машина)


- batch-processing  