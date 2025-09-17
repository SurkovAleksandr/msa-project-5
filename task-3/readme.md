Необходимо из БД выгрузить данные и сохранить это в CSV файле.
Делать это нужно с использованием CronJob - ежедневное выполнение задачи.

Запуск БД PostgreSQL. Делаем внешнюю БД по отношению к kubernetes
```shell
docker run -d --name task3-db \
  -p 5432:5432 \
  -e "POSTGRES_USER=postgres" \
  -e "POSTGRES_DB=postgres" \
  -e "POSTGRES_PASSWORD=postgres" \
  -v $(pwd)/results/shipments.csv:/data/shipments.csv \
  postgres:17.5
```

Создание таблицы
```postgresql
CREATE TABLE shipments (
   id SERIAL PRIMARY KEY,
   customer_name VARCHAR(100) NOT NULL,
   shipment_date DATE NOT NULL,
   status VARCHAR(50) NOT NULL,
   amount NUMERIC(10, 2) NOT NULL
);
```

Импорт csv файла в таблицу
```shell
docker exec -i task3-db psql -U postgres -d postgres -c "copy shipments FROM '/data/shipments.csv' DELIMITER ';' CSV HEADER;"
```

Подготовка параметров и доступа из сервиса к БД
```shell
kubectl apply -f ./results/config-map.yaml
kubectl apply -f ./results/service-external-name.yaml
```

Сборка и деплой джобы
```shell
export_to_csv=1.14
docker build -t export_to_csv:$export_to_csv ./results/app
minikube image load export_to_csv:$export_to_csv
# Это deployment - нужен был для отладки.
#sed "s/IMAGE_TAG_PLACEHOLDER/$export_to_csv/" ./results/deployment.yaml | kubectl apply -f -
sed "s/IMAGE_TAG_PLACEHOLDER/$export_to_csv/" ./results/cronjob.yaml | kubectl apply -f -
```

Монтирование локальной папки к volume в minikube. Сначала надо примонтировать, потом запустится джоба и появится файл output.csv  
```shell
minikube mount /home/u-user/IdeaProjects/курсы/sprint4/msa-project-5/task-3/export-data:/export-data
```
