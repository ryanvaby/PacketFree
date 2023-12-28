from scapy.all import IP, TCP, sr1
from tqdm import *
import time

def measure_response_time(target_ip, target_port):
    """
    This function sends a SYN packet to a specified server and waits for the SYN-ACK response to calculate the round-trip time.

    Args:
    target_ip (str): The IP address of the target server.
    target_port (int): The port of the target server.

    Returns:
    float: The round-trip time in seconds.
    """
    # Create a SYN packet
    packet = IP(dst=target_ip)/TCP(dport=target_port, flags='S')

    # Send the packet and record the start time
    start_time = time.time()
    response = sr1(packet, verbose=1)

    # Check if the response is a SYN-ACK packet
    if response[TCP].flags == 'SA':
        # Calculate the round-trip time
        rtt = time.time() - start_time
        return rtt
    else:
        return None

# Test the function

USdomains = ["google.com", "microsoft.com", "nike.com", "timberland.com", "adidas.com", "amazon.com", "apple.com", "asics.com", "underarmour.com", "gap.com", "bing.com", "linkedin.com"]
USRTT = dict()
for domain in USdomains:
    rtt = measure_response_time(domain, 80) * 1000
    USRTT.update({domain : rtt})
    if rtt is not None:
        print(f'The round-trip time is {rtt} ms (milliseconds).')
    else:
        print('No SYN-ACK response received.')

s = sorted(USRTT.items(), key=lambda item : item[1])
print(s)