# crypto_monitor

Crypto_monitor is a platform for monitoring the Bitcoin network.
```
.
├── app                          # Modules
├── alembic                      # Database migrations
├── .env.example                 # Example of .env file
├── Dockerfile                   
├── requirements.txt             # Concrete python requirements
├── prometheus.yml               # Prometheus scraping configuration
├── requirements.in              # Requirements for compilation
├── docker-compose-kafka.yml     # Kafka docker deployment
├── docker-compose-modules.yml   # Python modules docker deployment
├── docker-compose-metrics.yml   # Metrics docker deployment
├── LICENSE 
├── crypto_watch_db_backup_with_inserts.tar # Snapshot of DB, made by pg_dump 12.2
├── .gitignore
└── README.md
```

## Installation

In case of the local testing

```bash
# 1.Properly filled .env file , example in .env.example 
# 2.DB strings in alembic.ini 
# 3.Update DB to newest migration
alembic upgrade head #migrate DB

# Kafka and Database have to be UP
python -m app.module_name #module name can be address_pooler, address_publisher, node_watcher
```

## DB Migration
```bash
#Do changes in Models
alembic revision --autogenerate -m 'Migration message'
alembic upgrade head
```

## Usage

Deployment
```bash
#Properly filled .env file , example in .env.example and DB to newest migration
#Kafka have to run first

docker-compose -f docker-compose-kafka.yml up --build
docker-compose -f docker-compose-modules.yml up --build
docker-compose -f docker-compose-metrics.yml up --build #prometheus.yml have to properly set scraped exporters
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
