# import statements
import base64
import io
import matplotlib
import matplotlib.pyplot as plt 
import time
from PIL import Image

from flask import Flask, render_template, request, redirect, url_for, flash
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from scapy.all import IP, TCP, sr1

matplotlib.use('Agg')

# Setup for flask application
app = Flask(__name__)

# Declaring the following main_func() method as the code to run when user requests the home page of site
    
@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "POST":
        user = request.form['user']
        if not user:
            print('User is required!')

        # Determing whether the use wants to input their own domains or use the hard-coded ones
        if user.lower() == "my own":
            domains = request.form['domains']
            if not domains:
                print('Domains is required!')

            # Collecting the user's desired domains and running the measure_RTT function to store the average RTT of each domain
            return redirect(url_for('output', target_domains=domains))
        # Performing the same functions on pre-entered domains
        elif user.lower() == "yours":
            area = request.form['area']
            if not area:
                print('Area is required!')

            return redirect(url_for('output', target_domains=area))
        else:
            return render_template("home.html")
        
    return render_template("home.html")

#SYN-ACK Info routing
@app.route("/SYN-ACK")
def syn_ack():
    return render_template("syn_ack.html")
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
    
# Method to create a dictionary with each domain and its RTT
# Inputs:
#   domains : list of domains to send SYN-ACK packets to
# Output TODO
def analyze(target_domains):
    RTT = dict()
    for domain in target_domains:
        print(domain)
        rtt = measure_RTT(domain, 80)
        RTT[domain] = rtt

    # Formatting the axis and labelling on the graph.
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
    return pngImageB64String

# Route that utilizes other functions to obtain the final output image data and send it to the html template
@app.route('/output/<target_domains>')
def output(target_domains):
    if target_domains.lower() == "us":
        domains = ["google.com", "microsoft.com", "nike.com", "timberland.com", "adidas.com", "amazon.com", "apple.com", "asics.com", "underarmour.com", "gap.com", "bing.com", "linkedin.com", "ditch.la", "youtube.com", "docs.google.com", "issaquah.instructure.com", "mail.google.com", "nfl.com", "bbc.com", "adobe.com", "espn.com", "scapy.net", "riotgames.com", "stackoverflow.com", "earth.google.com", "starbucks.com", "spotify.com"]
    elif target_domains.lower() == "international":
        domains = ["amazon.in", "nike.in", "amazon.co.uk", "google.co.uk", "adidas.co.uk", "apple.co.uk", "microsoft.co.uk", "gap.co.uk", "bing.co.uk", "myntra.com", "amazon.au"]
    else:
        domains = target_domains.split()
    image = analyze(domains)
    return render_template("image_render.html", image=image)