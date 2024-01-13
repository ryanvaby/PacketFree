# import statements
from flask import Flask, render_template, request
from scapy.all import IP, TCP, sr1
import time
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io
import matplotlib
import matplotlib.pyplot as plt 
import base64

matplotlib.use('Agg')

# Setup for flask application
app = Flask(__name__)
# Declaring the following main_func() method as the code to run when user requests the home page of site
@app.route("/")
def main_func():

    # Determing whether the use wants to input their own domains or use the hard-coded ones
    print("Would you like to use our database or input your own web addresses to test? Type 'My own' or 'Yours'")
    response = input()
    if response.lower() == "my own":
        print ("Sounds good! Enter at least two domains (ie. \"google.com\") then write \"STOP\" and hit enter!")
        
        # Blank list for the incoming domains
        CustomDomains = []
        element = input()
        
        # Collecting the user's desire domains and running the measure_RTT function to store the average RTT of each domain
        while element.lower() != "stop":
            CustomDomains.append(element)
            element = input()
            print("Working on your data now!")
            RTT = dict()
            for domain in CustomDomains:
                rtt = measure_RTT(domain, 80) * 1000
                RTT.update({domain : rtt})
                if rtt is not None:
                    print('The round-trip time is {rtt} ms (milliseconds).')
                else:
                    print('No SYN-ACK response received.')
        
        # Sorting the dictionary and inverting key/value pairs
        s = sorted(RTT.items(), key=lambda item : item[1])
        print(s)

        # Actually plotting the graph using matplotlib library
        fig, ax = plt.subplots()
        RTTX = list(RTT.keys())
        RTTY = list(RTT.values())
        ax.bar(RTTX, RTTY)

        # Formatting the axis and labelling on the graph.
        ax.set_ylabel('ROUND TRIP TIME (MS)')
        ax.set_xlabel('\nPACKET DESTINATION')
        ax.set_title('RTT vs. PACKET DEST.')
        plt.xticks(rotation=90)
        plt.subplots_adjust(bottom=0.479)

        # Convert plot to PNG image
        pngImage = io.BytesIO()
        FigureCanvas(fig).print_png(pngImage)
        
        # Encode PNG image to base64 string
        pngImageB64String = "data:image/png;base64,"
        pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
        
        return render_template("image_render.html", image=pngImageB64String)

    # Performing the same functions on pre-entered domains
    if response.lower() == "yours":
        # Sample USA and International domains for the user to try
        USdomains = ["google.com", "microsoft.com", "nike.com", "timberland.com", "adidas.com", "amazon.com", "apple.com", "asics.com", "underarmour.com", "gap.com", "bing.com", "linkedin.com", "ditch.la", "youtube.com", "docs.google.com", "issaquah.instructure.com", "mail.google.com", "nfl.com", "bbc.com", "adobe.com", "espn.com", "scapy.net", "riotgames.com", "stackoverflow.com", "earth.google.com", "starbucks.com", "spotify.com"]
        NATIONALdomains = ["amazon.in", "nike.in", "amazon.co.uk", "google.co.uk", "adidas.co.uk", "apple.co.uk", "microsoft.co.uk", "gap.co.uk", "bing.co.uk", "linkedin.co.uk", "myntra.com", "amazon.au"]

        # Selecting US or International domains
        print("Would you like to test US or International domains? Respond with \"US\" or \"International\"")
        domains = []
        domainResponse = input().lower()
        if domainResponse == "us":
            domains = USdomains
        if domainResponse == "international":
            domains = NATIONALdomains

        # Running the measure_RTT function to store the average RTT of each domain
        RTT = dict()
        for domain in domains:
            rtt = measure_RTT(domain, 80) * 1000
            RTT.update({domain : rtt})
            if rtt is not None:
                print(f'The round-trip time is {rtt} ms (milliseconds).')
            else:
                print('No SYN-ACK response received.')

        # Sorting the dictionary and inverting key/value pairs
        s = sorted(RTT.items(), key=lambda item : item[1])
        print(s)

        # Formatting the axis and labelling on the graph.
        fig, ax = plt.subplots()
        RTTX = list(RTT.keys())
        RTTY = list(RTT.values())
        ax.bar(RTTX, RTTY)

    # Formatting the axis and labelling on the graph.
    ax.set_ylabel('ROUND TRIP TIME')
    ax.set_xlabel('\nPACKET DESTINATION')
    ax.set_title('RTT vs. PACKET DEST.')
    plt.xticks(rotation=90)
    plt.subplots_adjust(bottom=0.479)

    # Convert plot to PNG image
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    
    # Encode PNG image to base64 string
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    
    return render_template("image_render.html", image=pngImageB64String)

    
@app.route("/printHola")
def print_hola():
    return "<h1 style='color:blue;'>HOLA SENOR!!</h1>"

# Core method to measure the RTT (round-trip time) of packets to different addresses
# Inputs:
#   target_ip : domain to send packet to
#   target_port : which port to send and recieve from
# Output: Round trip time of the packet
def measure_RTT(target_ip, target_port):
    # Create and send SYN packet
    packet = IP(dst=target_ip)/TCP(dport=target_port, flags='S')
    # Starting internal timer
    start_time = time.time()
    response = sr1(packet, verbose=1)

    # Check for the response SYN-ACK packet
    if response[TCP].flags == 'SA':
        # Calculating RTT
        rtt = time.time() - start_time
        return rtt
    else:
        return None