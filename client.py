#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
About: Simple video streaming client.
"""

import socket
import cv2
import numpy as np

SERVICE_IP = "10.0.0.12"
SERVICE_PORT = 8888

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = b"Stream video, please!"

    print("Streaming has started...")

    while True:
        sock.sendto(data, (SERVICE_IP, SERVICE_PORT))
        buffer, _ = sock.recvfrom(65535)
        np_data = np.frombuffer(buffer, dtype=np.uint8)
        frame = cv2.imdecode(np_data, cv2.IMREAD_COLOR)

        if frame is not None:
            cv2.imshow('Streaming Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cv2.destroyAllWindows()
    sock.close()
