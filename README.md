# HTTP-Endpoint-Health-Checker
This program monitors the health of HTTP endpoints specified in a YAML file. It supports multiple HTTP methods, logs availability percentages, and handles unsupported methods gracefully.

## Features
* Supports GET (default), POST, PUT, and DELETE methods.
* Handles invalid HTTP methods with clear error messages.
* Logs availability percentages for each domain after every test cycle.
* Gracefully exits and shows final statistics when interrupted.


## Prerequisites

* Python: Version 3.8 or higher. (Download Python if not already installed.)
* Pip: Python’s package manager for installing dependencies.
* Internet Access: Required for testing endpoints.

## Setup Instructions

### 1. Download or Clone the Project

If hosted on GitHub or similar, use:
```
git clone <repository_url> cd <repository_folder>
```
Alternatively, download and extract the source code manually.

### 2. Install Dependencies

Run the following command to install the required libraries:
```
pip install requests pyyaml
```
If pip is not recognized, try:
```
python3 -m pip install requests pyyaml
```
### 3. Prepare a Configuration File

Create a YAML file (e.g., config.yaml) with the endpoints to test. Example:
```
- name: Valid GET Request (Google homepage)
  url: https://www.google.com/
  method: GET
  headers:
    user-agent: fetch-synthetic-monitor

- name: Valid POST Request (JSONPlaceholder API)
  url: https://jsonplaceholder.typicode.com/posts
  method: POST
  headers:
    content-type: application/json
    user-agent: fetch-synthetic-monitor
  body: '{"title": "foo", "body": "bar", "userId": 1}'

- name: Valid PUT Request (JSONPlaceholder API)
  url: https://jsonplaceholder.typicode.com/posts/1
  method: PUT
  headers:
    content-type: application/json
    user-agent: fetch-synthetic-monitor
  body: '{"id": 1, "title": "updated title", "body": "updated body", "userId": 1}'

- name: Valid DELETE Request (JSONPlaceholder API)
  url: https://jsonplaceholder.typicode.com/posts/1
  method: DELETE
  headers:
    user-agent: fetch-synthetic-monitor

- name: Default GET Request
  url: https://example.com/
  headers:
    user-agent: fetch-synthetic-monitor

- name: Invalid HTTP Method
  url: https://www.google.com/
  method: INVALID
  headers:
    user-agent: fetch-synthetic-monitor
```
### Running the Program

Run the program from the terminal and provide the path to the YAML file as an argument:
```
python health_check.py config.yaml
```
If python refers to Python 2 on your system, use:
```
python3 health_check.py config.yaml
```
### Expected Output

For each test cycle, the program logs the status of each endpoint and calculates availability percentages for each domain. Example:
```
Starting health checks. Press CTRL+C to exit.
Valid GET Request (google.com): UP (Latency: 50.23 ms)
Valid POST Request (jsonplaceholder.typicode.com): UP (Latency: 120.34 ms)
Valid PUT Request (jsonplaceholder.typicode.com): UP (Latency: 200.12 ms)
Valid DELETE Request (jsonplaceholder.typicode.com): DOWN (Latency: N/A)
Default GET Request (example.com): UP (Latency: 30.12 ms)
Invalid HTTP Method (google.com): ERROR (Unsupported HTTP method: INVALID)

Availability Statistics:
google.com has 67% availability
jsonplaceholder.typicode.com has 50% availability
example.com has 100% availability
--------------------------------------------------
```
Press CTRL+C to exit. The final availability statistics will be displayed.

## Troubleshooting

Common Issues and Fixes
* Python Not Recognized:
	* Ensure Python is installed and added to your PATH.
* Missing Dependencies:
	* Install the missing libraries using:
```
pip install requests pyyaml
```

* Invalid YAML File:
	* Ensure the YAML file follows proper formatting. Validate it using tools like YAML Lint.


## Platform Compatibility

This program is platform-independent and works on:
* Windows
* macOS
* Linux

Use Python 3.8+ for best results.
