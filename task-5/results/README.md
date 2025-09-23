Ручное добавление метрики. Проверять в сервисе pushgateway - http://localhost:9091/metrics
```shell
echo "write_count_url 3.5" | curl --data-binary @- http://localhost:9091/metrics/job/pushgateway/instance/instance_name
```

Ручное удаление метрики
```shell
curl -X DELETE http://localhost:9091/metrics/job/pushgateway/instance/instance_name
```