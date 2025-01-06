import yaml
import requests
import time
from collections import defaultdict

def load_config(file_path):
    """
    Load the YAML configuration file containing the HTTP endpoints.
    """
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def send_request(endpoint):
    """
    Send an HTTP request to the endpoint based on the method, headers, and body.
    Returns whether the request is UP (True) or DOWN (False) and the response latency.
    """
    url = endpoint['url']
    method = endpoint.get('method', 'GET').upper()  # Default to GET
    headers = endpoint.get('headers', {})
    body = endpoint.get('body', None)

    try:
        start_time = time.time()

        # Handle HTTP methods
        if method == 'GET':
            response = requests.get(url, headers=headers, timeout=2)
        elif method == 'POST':
            response = requests.post(url, headers=headers, data=body, timeout=2)
        elif method == 'PUT':
            response = requests.put(url, headers=headers, data=body, timeout=2)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers, timeout=2)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        latency = (time.time() - start_time) * 1000  # Convert to milliseconds

        # Determine if the request is UP
        is_up = response.status_code in range(200, 300) and latency < 500
        return is_up, latency
    except requests.RequestException:
        return False, None

def calculate_availability(domain_stats):
    """
    Calculate the availability percentage for each domain.
    """
    availability = {}
    for domain, stats in domain_stats.items():
        total = stats['total']
        up = stats['up']
        availability[domain] = round((up / total) * 100) if total > 0 else 0
    return availability

def main(config_file):
    """
    Main function to execute the health checks, log availability, and handle graceful exit.
    """
    endpoints = load_config(config_file)
    domain_stats = defaultdict(lambda: {'total': 0, 'up': 0})

    print("Starting health checks. Press CTRL+C to exit.")

    try:
        while True:
            for endpoint in endpoints:
                domain = endpoint['url'].split('/')[2]  # Extract domain from URL
                is_up, latency = send_request(endpoint)

                domain_stats[domain]['total'] += 1
                if is_up:
                    domain_stats[domain]['up'] += 1

                status = "UP" if is_up else "DOWN"
                latency_display = f"{latency:.2f} ms" if latency is not None else "N/A"
                print(f"{endpoint['name']} ({domain}): {status} (Latency: {latency_display})")

            # Log availability
            availability = calculate_availability(domain_stats)
            print("\nAvailability Statistics:")
            for domain, percent in availability.items():
                print(f"{domain} has {percent}% availability")
            print("-" * 50)

            time.sleep(15)

    except KeyboardInterrupt:
        print("\nExiting program. Final statistics:")
        availability = calculate_availability(domain_stats)
        for domain, percent in availability.items():
            print(f"{domain} has {percent}% availability")
        print("Goodbye!")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="HTTP Endpoint Health Checker")
    parser.add_argument("config_file", help="Path to the YAML configuration file")
    args = parser.parse_args()

    main(args.config_file)