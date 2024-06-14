#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
About: Simple video streaming client.
"""

import socket

SERVICE_IP = "10.0.0.12"
SERVICE_PORT = 8888

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = b"Stream video, please!"

    print("Streaming has started...")

    while True:
        sock.sendto(data, (SERVICE_IP, SERVICE_PORT))
        buffer, _ = sock.recvfrom(65535)
        if buffer:
            print("Receiving video stream data...")
        else:
            break