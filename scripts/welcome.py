#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Huawei eNSP Lite COESS Enterprise Edition
# Co-Branded: Computer Engineering Students Society (COESS)
# Author: Ranilo John Delos Angeles

import netifaces
import curses
import time
import psutil

def get_ip():
    try:
        return netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr']
    except Exception:
        return "10.10.10.137"

def get_cpu():
    return f"{psutil.cpu_percent()}%"

def get_mem():
    mem = psutil.virtual_memory()
    total = round(mem.total / (1024 ** 3), 1)
    used = round(mem.used / (1024 ** 3), 2)
    return f"{used}/{total} GB"

def main():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    stdscr.nodelay(True)

    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    stdscr.bkgd(curses.color_pair(2))
    stdscr.refresh()
    stdscr.clear()

    win_h = 15
    win_w = 70
    
    while True:
        h = min(curses.LINES, win_h)
        w = min(curses.COLS, win_w)
        y = max(0, int((curses.LINES - h) / 2))
        x = max(0, int((curses.COLS - w) / 2))
        
        win = curses.newwin(h, w, y, x)
        win.bkgd(' ', curses.color_pair(2))
        win.box()

        title = " Huawei eNSP Lite | COESS Datacom Center "
        win.addstr(0, max(1, int((w - len(title)) / 2)), title, curses.A_BOLD)

        ip = get_ip()
        curr_time = time.strftime("%Y-%m-%d %H:%M:%S %Z")
        
        lines = [
            (f"Time & Health : {curr_time} | CPU: {get_cpu()} | RAM: {get_mem()}", curses.color_pair(2)),
            ("-" * (w - 4), curses.color_pair(2)),
            (f"[Port 80]   Lab Descriptions : http://{ip}/", curses.color_pair(3) | curses.A_BOLD),
            (f"[Port 8443] Console Env      : https://{ip}:8443/", curses.color_pair(1) | curses.A_BOLD),
            ("-" * (w - 4), curses.color_pair(2)),
            (f"PowerShell SSH Access        : ssh root@{ip}", curses.color_pair(4)),
            (f"Default Root Password        : ensp2026@ensp", curses.color_pair(2)),
            (f"VRP Devices AAA Credentials  : admin / admin (super: super)", curses.color_pair(2)),
            ("-" * (w - 4), curses.color_pair(2)),
            ("Computer Engineering Students Society (COESS)", curses.color_pair(2) | curses.A_BOLD),
            ("Made by Ranilo John Delos Angeles", curses.color_pair(2) | curses.A_DIM),
        ]

        for idx, (text, attr) in enumerate(lines):
            if idx + 1 < h - 1:
                win.addstr(idx + 1, 2, text[:w-4], attr)

        win.refresh()
        time.sleep(1)
        win.clear()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        try:
            curses.nocbreak()
            curses.echo()
            curses.endwin()
        except Exception:
            pass