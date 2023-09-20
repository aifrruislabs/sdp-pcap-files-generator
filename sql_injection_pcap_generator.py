#!/usr/bin/python
# SQL Injection PCAP Packet Generator

from scapy.all import *

# Create the pcap file
pcap_file = "sql_injection.pcap"

# Create the network packet capture
packets = []

_src_ip = "154.74.154.80"
_dst_ip = "207.231.110.239"
_src_port = 1234
_injection_host = "sdp.aifrruislabs.com"

# Create a TCP SYN packet
syn_packet = IP(src=_src_ip, dst=_dst_ip) / TCP(sport=_src_port, dport=80, flags="S")
packets.append(syn_packet)

# Create a TCP SYN-ACK packet
syn_ack_packet = IP(src=_src_ip, dst=_dst_ip) / TCP(sport=80, dport=1234, flags="SA")
packets.append(syn_ack_packet)

# Create an HTTP GET request with SQL injection payload
http_request = IP(src=_src_ip, dst=_dst_ip) / TCP(sport=1234, dport=80, flags="A") /\
               Raw(load="GET /index.php?id=1' OR '1'='1 HTTP/1.1\r\nHost: "+_injection_host+"\r\n\r\n")
packets.append(http_request)

# Create a TCP RST packet
rst_packet = IP(src=_src_ip, dst=_dst_ip) / TCP(sport=80, dport=1234, flags="R")
packets.append(rst_packet)

# Write the packets to the pcap file
wrpcap(pcap_file, packets)