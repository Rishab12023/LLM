## Installation

To get started, please follow these steps:

1. Create a Virtual Environment and install the required dependencies by running the following command:
```
pip install -r requirements.txt
```

2. Start the Docker daemon.

3. Run the following command to start the Docker container:
```
docker run -it \
    --rm \
    --name elasticsearch \
    -m 4GB \
    -p 9200:9200 \
    -p 9300:9300 \
    -e "discovery.type=single-node" \
    -e "xpack.security.enabled=false" \
    docker.elastic.co/elasticsearch/elasticsearch:8.4.3

```

4. To start the api use the command
```
python uvicorn main:app --reload

then go to localhost/docs to start the swagger.
```


