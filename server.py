#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
About: Simple video streaming server.
"""

import argparse
import signal
import socket
import os
import cv2
import time

INTERNAL_IP_H2 = "192.168.0.12"
INTERNAL_IP_H3 = "192.168.0.13"
INTERNAL_PORT = 9999
SERVICE_IP = "10.0.0.12"
SERVICE_PORT = 8888
VIDEO_FILE = 'xxx.mpa'

def recv_state(host_name):
    if host_name == "h2":
        recv_ip = INTERNAL_IP_H2
    else:
        recv_ip = INTERNAL_IP_H3
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((recv_ip, INTERNAL_PORT))

    state, _ = sock.recvfrom(1024)
    state = int(state.decode("utf-8"))
    return state

def stream_video(sock, addr, cap):
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        sock.sendto(buffer.tobytes(), addr)
        # Simulate a delay to mimic real-time streaming
        time.sleep(0.04)  # 25 frames per second

def run(host_name, get_state=False):
    counter = 0
    if get_state:
        counter = recv_state(host_name)
        print("Get the init counter state: {}".format(counter))

    def term_signal_handler(signum, frame):
        if host_name == "h2":
            dest_ip = INTERNAL_IP_H3
        else:
            dest_ip = INTERNAL_IP_H2
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for _ in range(6):
            sock.sendto(str(counter).encode("utf-8"), (dest_ip, INTERNAL_PORT))
        sock.close()

    signal.signal(signal.SIGTERM, term_signal_handler)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((SERVICE_IP, SERVICE_PORT))

    video_path = os.path.join(os.path.dirname(__file__), VIDEO_FILE)
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return

    while True:
        _, addr = sock.recvfrom(1024)
        stream_video(sock, addr, cap)
        cap.release()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple video streaming server.")
    parser.add_argument(
        "hostname",
        type=str,
        help="The name of the host on which the server is deployed.",
    )
    parser.add_argument(
        "--get_state", action="store_true", help="Get state from network."
    )

    args = parser.parse_args()

    run(args.hostname, args.get_state)