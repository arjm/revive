# Revive

## How to run
1. Make sure you have installed. If not, then run: 
2. sudo docker-compose build
3. sudo docker-compose up -d

## Architecture
![revive](https://user-images.githubusercontent.com/10273101/202862108-47d5782c-6fd0-4cb3-8dad-fd2eace6a679.png)

## Future Enhancements
1. Currently, flask app is not production ready. Move Flask app to nginx
2. Make batch pipeline more scalable by adding spark executors
3. Take input data from a S3/GCS bucket
