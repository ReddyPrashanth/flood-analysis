## Sudan Flood Analysis File Extraction

### Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configiration)
- [Example](#example)
- [Requirements](#requirements)

## Installation

To run this script, ensure you have Python installed on your machine. You will also need to install the boto3 library if you haven't already.

1. Install Python: [Download and install Python](https://www.python.org/downloads/).
2. Creating a python virtual environment on Windows

   ```
   > python -m venv analysis

   > analysis\Scripts\activate
   ```

   OR

3. Creating a python virtual environment on Linux

   ```
   > python -m venv analysis

   > source analysis/bin/activate
   ```

4. Install boto3: Install the boto3 and other dependencies using pip.

   ```
   > pip install -r requirements.txt
   ```

## Usage

1. AWS Credentials: Ensure your AWS credentials are configured properly. You can configure them by setting environemnt variables.

   ```
   > export AWS_ACCESS_KEY_ID='YOUR_ACCESS_KEY'

   > export AWS_SECRET_ACCESS_KEY='YOUR_SECRET_KEY'
   ```

2. Running the Script: Use the following command to run the script.

   ```
   > python main.py
   ```

## Configiration

1. set below config variables in **config.py** file

   ```
    BUCKET = 'BUCKET_NAME'

    PREFIX = 'BUCKET_PREFIX'

    PATTERN = ['GRID_FORMAT_1', 'GRID_FORMAT_2']
   ```

## EXAMPLE

Here is an example of how to use the script:

```
> analysis\Scripts\activate (activates python venv)

> python main.py
```

## Requirements

- Python 3.11
- Python virtual environment
- boto3 library
- AWS ACCESS_KEY and SECRET_KEY for the S3 bucket
