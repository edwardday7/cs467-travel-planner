# Crowd-Sourced Travel Planner

## Development

For setting up and running locally, follow the below instructions.

### Prerequisites

- Python 3.9+
- MySQL 8.0

### Installation

It is recommended to use a [virtual environment](https://realpython.com/python-virtual-environments-a-primer/#create-it). To install dependencies:

`pip install -r requirements.txt`

`npm install bootstrap@5.3.0`

Options for Downloading and Running MySQL: 
- Direct install - https://dev.mysql.com/downloads/mysql/
- Through Docker - `docker run -d --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=root-password -e MYSQL_DATABASE=test -e MYSQL_USER=test -e MYSQL_PASSWORD=test mysql:8.0`

After install, set the following environment variables:
- DB_USER - Your database username
- DB_PASSWORD - Your database password
- DB_HOST - Host address. Likely localhost unless you're using a cloud instance
- DB_NAME - The name of your created database

In addition to setting up MySQL, you will also need to set the following environment variable:
- AZURE_STORAGE_CONNECTION_STRING - Obtain this value from Edward as it's a secret. Allows for photo uploads.
- MAPBOX_TOKEN - Obtain from Sterling. Mapbox token API key.
- OPEN_WEATHER_TOKEN" - Obtain from Sterling. Weather API key.

### Running Locally

Run application:

`python3 run.py`

### Changes to Packages

If you add additional python packages, please make sure to add them to the requirements.txt file in the repository as the container build depends on that file. Otherwise, your build might fail.

## Making Changes and Deploying

When you are ready to incorporate your changes, open a Pull Request. Upon a successful merge of the Pull Request, a deployment will automatically be kicked off. You can check the status of the deployment on the "Actions" tab. Changes will be available at the following url:

- https://capstone-travel-app.bravesmoke-8633c4f4.eastus.azurecontainerapps.io
