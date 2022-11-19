# Revive

## How to run
1. Make sure you have installed. If not, then run: 
2. docker-compose build
3. docker-compose up -d
4. Wait for spark job to finish. Step 3 log should end with "Batch pipeline completed successfully!"
5. Run the following command to test the output: python3 test.py


## Architecture
![revive](https://user-images.githubusercontent.com/10273101/202862108-47d5782c-6fd0-4cb3-8dad-fd2eace6a679.png)


## Debugging errors
1. If you get "Port already in use" error while runing step 3 (from "How to run"), then find and kill the process already running on that port. Re-run step 3
2. Clean up existing container: docker-compose down --remove-orphans


## Future Enhancements
1. Currently, flask app is not production ready. Move Flask app to nginx
2. Make batch pipeline more scalable by adding spark executors
3. Take input data from a S3/GCS bucket
