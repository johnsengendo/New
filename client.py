#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
About: Simple video streaming client.
"""

import socket
import time

SERVICE_IP = "10.0.0.12"
SERVICE_PORT = 8888

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = b"Stream video, please!"

    print("Streaming has started...")

    start_time = time.time()
    counter = 0

    while True:
        sock.sendto(data, (SERVICE_IP, SERVICE_PORT))
        buffer, _ = sock.recvfrom(65535)
        if buffer:
            counter += 1
            print(f"Receiving video stream data... Frame {counter}")
        
        # Check if 8 seconds have passed
        if time.time() - start_time > 8:
            break

    print("Streaming has stopped after 8 seconds.")
    sock.close()
