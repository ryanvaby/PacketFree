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
rtt = measure_response_time('google.com', 80) * 1000
if rtt is not None:
    print(f'The round-trip time is {rtt} ms (milliseconds).')
else:
    print('No SYN-ACK response received.')


# capture = tqdm(sniff(filter="tcp", count=10))
# index = 0

# for pkt in capture:
#     tsdata = dict(pkt['TCP'].options)
#     print(tsdata["Timestamp"][0])

