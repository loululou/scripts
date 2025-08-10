import requests
import os
import subprocess

def check_status(url, timeout=3):
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code
    except requests.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return None

def capture_screenshot(url, output_path, capture_timeout=5):
    try:
        subprocess.run(["wkhtmltoimage", url, output_path], check=True, timeout=capture_timeout)
        print(f"Screenshot saved to {output_path}")
    except subprocess.TimeoutExpired:
        print(f"Timeout capturing screenshot for {url}")
    except subprocess.CalledProcessError as e:
        print(f"Error capturing screenshot for {url}: {e}")

def write_summary(summary_file, valid, err403, err404, err405, timeout_list):
    """
    Writes a summary of domains categorized by their HTTP responses to a text file.
    """
    with open(summary_file, "w") as f:
        f.write("Summary of Domain Statuses\n")
        f.write("==========================\n\n")
        
        f.write("Valid Domains (HTTP 200):\n")
        if valid:
            for domain in valid:
                f.write(f"- {domain}\n")
        else:
            f.write("None\n")
        f.write("\n")
        
        f.write("HTTP 403 Domains:\n")
        if err403:
            for domain in err403:
                f.write(f"- {domain}\n")
        else:
            f.write("None\n")
        f.write("\n")
        
        f.write("HTTP 404 Domains:\n")
        if err404:
            for domain in err404:
                f.write(f"- {domain}\n")
        else:
            f.write("None\n")
        f.write("\n")
        
        f.write("HTTP 405 Domains:\n")
        if err405:
            for domain in err405:
                f.write(f"- {domain}\n")
        else:
            f.write("None\n")
        f.write("\n")
        
        f.write("Timeout/Unresponsive Domains:\n")
        if timeout_list:
            for domain in timeout_list:
                f.write(f"- {domain}\n")
        else:
            f.write("None\n")
        f.write("\n")
    
    print(f"Summary written to {summary_file}")

def main():
    domain_file = "domains.txt"
    output_dir = "screenshots"
    os.makedirs(output_dir, exist_ok=True)
    
    valid_domains = []
    domains_403 = []
    domains_404 = []
    domains_405 = []
    timeout_domains = []
    
    with open(domain_file, "r") as f:
        domains = [line.strip() for line in f if line.strip()]
    
    for domain in domains:
        if not domain.startswith("http://") and not domain.startswith("https://"):
            url = "http://" + domain
        else:
            url = domain
        
        print(f"Processing {url}...")
        
        # Check HTTP status with a short timeout
        status = check_status(url, timeout=3)
        print(f"HTTP Status for {url}: {status}")
        
        # Categorize based on status
        if status is None:
            timeout_domains.append(domain)
        elif status == 200:
            valid_domains.append(domain)
        elif status == 403:
            domains_403.append(domain)
        elif status == 404:
            domains_404.append(domain)
        elif status == 405:
            domains_405.append(domain)
        else:
            print(f"Status {status} for {domain} is not categorized.")
        
        sanitized_domain = domain.replace("http://", "").replace("https://", "").replace("/", "_")
        screenshot_file = os.path.join(output_dir, f"{sanitized_domain}.png")
        capture_screenshot(url, screenshot_file, capture_timeout=5)
    
    summary_file = "summary.txt"
    write_summary(summary_file, valid_domains, domains_403, domains_404, domains_405, timeout_domains)

if __name__ == "__main__":
    main()
