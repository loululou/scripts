#!/usr/bin/env python3

import re
import socket

def is_syntactically_valid(domain: str) -> bool:
    if not domain:
        return False
    
    if len(domain) > 253:
        return False
    
    # Split the domain into labels
    labels = domain.split('.')
    
    # Regex for valid label
    label_regex = re.compile(r'^(?!-)[A-Za-z0-9-]{1,63}(?<!-)$')
    
    for label in labels:
        if not label_regex.match(label):
            return False
    
    return True

def is_resolvable(domain: str) -> bool:
    try:
        socket.gethostbyname(domain)
        return True
    except socket.gaierror:
        return False

def check_domains_from_file(input_file: str, output_file: str):
    valid_domains = []

    with open(input_file, 'r') as f:
        for line in f:
            domain = line.strip()
            if not domain:
                continue  # skip empty lines

            # Check if syntactically valid and resolvable
            if is_syntactically_valid(domain) and is_resolvable(domain):
                valid_domains.append(domain)

    # Write valid domains to the output file
    with open(output_file, 'w') as f_out:
        for domain in valid_domains:
            f_out.write(domain + '\n')

    # Optionally, also print them to the console
    print("Valid domains:")
    for domain in valid_domains:
        print(domain)

if __name__ == "__main__":
    # Example usage: 
    #   - 'domains.txt' is the input list
    #   - 'valid_domains.txt' will contain only valid domains
    check_domains_from_file('domains.txt', 'valid_domains.txt')
