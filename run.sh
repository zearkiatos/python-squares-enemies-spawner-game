#!/bin/sh

install() {
    pip3 install -r requirements.txt
}

run() {
    python3 main.py
}