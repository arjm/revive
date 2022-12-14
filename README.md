# Revive

## How to run
1. Make sure you have Docker installed and running. If not, then install the latest docker version: https://docs.docker.com/engine/install/
2. ```git clone``` this project. ```cd revive``` . Make sure you don't have an already running mysql service on 3306 port. If yes, stop the existing mysql service
3. ```docker-compose build```
4. ```docker-compose up```
5. Wait for spark job to finish. Step 4 logs should end with "spark exited with code 0", or, if you ran step 4 command in detach (-d) mode then wait for 20 seconds
6. Unit tests will automatically run as a part of step 4, it takes around 30 seconds to start executing unit test cases. To run unittest container on demand, run: ```docker-compose up unittest```


## Architecture
![revive](https://user-images.githubusercontent.com/10273101/202862108-47d5782c-6fd0-4cb3-8dad-fd2eace6a679.png)


## Debugging errors
1. If you get "Port already in use" error while runing step 3 (from "How to run"), then find and kill the process already running on that port. Re-run step 4
2. Clean up existing container: ```docker-compose down --remove-orphans```
3. ```ERROR: for mysql  Cannot start service mysql: Ports are not available: listen tcp 0.0.0.0:3306: bind: address already in use``` - Make sure you don't have an already running mysql service on 3306 port.


## Future Enhancements
1. Currently, flask app is not production ready. Move Flask app to nginx
2. Make batch pipeline more scalable by adding spark executors
3. Take input data from a S3/GCS bucket
