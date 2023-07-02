# Open Source Travel Planner

## Development

For setting up and running locally, follow the below instructions.

### Prerequisites

- Python 3.9+

### Installation

It is recommended to use a [virtual environment](https://realpython.com/python-virtual-environments-a-primer/#create-it). To install dependencies:

`pip install -r requirements.txt`

`npm install bootstrap@5.3.0`

### Running Locally

Run application:

`python3 run.py`

### Changes to Packages

If you add additional python packages, please make sure to add them to the requirements.txt file in the repository as the container build depends on that file. Otherwise, your build might fail.

## Making Changes and Deploying

When you are ready to incorporate your changes, open a Pull Request. Upon a successful merge of the Pull Request, a deployment will automatically be kicked off. You can check the status of the deployment on the "Actions" tab. Changes will be available at the following url:

- https://capstone-travel-app.bravesmoke-8633c4f4.eastus.azurecontainerapps.io
