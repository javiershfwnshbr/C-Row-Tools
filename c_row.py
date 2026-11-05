#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==================================================
 Project Name : C-Row [ VIP ]
 Style        : Cyber Matrix Console (Fit Full Screen Termux & Laptop)
 Platform     : Termux & Windows CMD / PowerShell
 Author       : Javier
==================================================
"""

import os
import sys
import time
import random
import re
import unicodedata

# Impor library input keyboard sesuai OS
if sys.platform == "win32":
    import msvcrt
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
else:
    import select
    import termios
    import tty

# --- WARNA (PALET KONTRAS TINGGI & NYAMAN DI MATA) ---
HEADER_BORDER = "\033[38;5;201m\033[1m" # Ungu Neon Menyala / Electric Magenta (Kotak C-ROW)
MENU_BORDER   = "\033[38;5;51m\033[1m"  # Cyan Neon Super Terang (Kotak Menu Tools)
CYAN          = "\033[38;5;51m\033[1m"  # Cyan Neon Super Terang
DIM_BINARY    = "\033[38;5;238m\033[2m" # Abu-abu gelap samar (Biner Transparan Background)
WHITE         = "\033[97m\033[1m"       # Putih Murni Tebal (Teks Menu Tenang & Mudah Dibaca)
YELLOW        = "\033[38;5;226m\033[1m" # Kuning emas neon SUPER TERANG (Electric Gold)
GREEN         = "\033[38;5;46m\033[1m"  # Hijau Neon Terang
NEON_GREEN    = "\033[38;5;46m\033[1m"  # Hijau Matrix Neon Terang
MID_GREEN     = "\033[38;5;34m\033[1m"  # Hijau Matrix Sedang
DIM_GREEN     = "\033[38;5;22m\033[2m"  # Hijau Matrix Gelap Samar
BLUE          = "\033[38;5;45m\033[1m"  # Biru Langit Terang
MAGENTA       = "\033[38;5;207m\033[1m" # Pink / Ungu Terang
RED           = "\033[38;5;196m\033[1m" # Merah Darah Menyala
RESET         = "\033[0m"
BOLD          = "\033[1m"

# Pola angka biner untuk background
BINARY_STREAM = "0110001101110010011011110111011101010110010010010101000000100000101011010010"

# Ukuran Lebar Layar Presisi (50 Kolom Penuh Layar HP Termux & Laptop)
SCREEN_WIDTH = 50
INNER_WIDTH  = 48

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def loading_spinner(pesan, duration=1.0):
    """Animasi spinner berputar saat proses loading tool"""
    frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    end_time = time.time() + duration
    idx = 0
    while time.time() < end_time:
        frame = frames[idx % len(frames)]
        sys.stdout.write(f"\r {CYAN}[{frame}]{WHITE} {pesan}...{RESET}")
        sys.stdout.flush()
        time.sleep(0.08)
        idx += 1
    sys.stdout.write(f"\r {GREEN}[✓]{WHITE} {pesan} selesai!   {RESET}\n\n")

def vlen(s):
    """Menghitung lebar visual karakter (mendukung emoji & aksen ANSI)"""
    s_clean = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', s)
    return sum(2 if unicodedata.east_asian_width(c) in ('W', 'F') else 1 for c in s_clean)

def get_bin(offset, length):
    return "".join(BINARY_STREAM[(offset + i) % len(BINARY_STREAM)] for i in range(length))

def pad_with_bin(text_to_show, offset):
    cur = vlen(text_to_show)
    rem = INNER_WIDTH - cur
    l = max(0, rem // 2)
    r = max(0, rem - l)
    b_left = f"{DIM_GREEN}" + get_bin(offset, l) + f"{RESET}"
    b_right = f"{DIM_GREEN}" + get_bin(offset + 30, r) + f"{RESET}"
    return b_left + text_to_show + b_right

def skull_welcome_intro():
    """Animasi opening Welcome My Friend dengan ASCII Tengkorak & latar biner hijau Matrix (Full 50 Kolom)"""
    clear_screen()
    sys.stdout.write("\033[?25l")  # Sembunyikan kursor terminal
    sys.stdout.flush()

    top_b = f"{HEADER_BORDER}╔" + ("═" * INNER_WIDTH) + f"╗{RESET}"
    bot_b = f"{HEADER_BORDER}╚" + ("═" * INNER_WIDTH) + f"╝{RESET}"
    mid_b = f"{HEADER_BORDER}╠" + ("═" * INNER_WIDTH) + f"╣{RESET}"

    welcome_target = "W E L C O M E   M Y   F R I E N D"
    subtitle_target = "C-Row is here"

    skull_template = [
        ("                   .-------.                    ", 19, 27),
        ("                 .-         -.                  ", 17, 29),
        (r"                /   (O) (O)   \                 ", 16, 30),
        ("               |       _       |                ", 15, 31),
        (r"                \   \_____/   /                 ", 16, 30),
        (r"                 \   | | |   /                  ", 17, 29),
        ("                  '--'---'--'                   ", 18, 28),
    ]

    def get_skull_bg_line(r_idx, tick, eye_color):
        raw, l_bound, r_bound = skull_template[r_idx]
        res = []
        for c_idx, ch in enumerate(raw):
            if c_idx < l_bound or c_idx > r_bound:
                b = BINARY_STREAM[(r_idx * INNER_WIDTH + c_idx + tick) % len(BINARY_STREAM)]
                res.append(f"{DIM_GREEN}{b}{RESET}")
            else:
                if ch == 'O':
                    res.append(f"{eye_color}{ch}{RESET}")
                elif ch == ' ':
                    res.append(' ')
                else:
                    res.append(f"{WHITE}{ch}{RESET}")
        return "".join(res)

    try:
        # Fase 1: Efek typewriter tulisan "W E L C O M E   M Y   F R I E N D"
        for i in range(len(welcome_target) + 1):
            partial1 = welcome_target[:i]
            cursor1 = "█" if i < len(welcome_target) else ""
            txt1 = f"{CYAN}{BOLD}{partial1}{RESET}{YELLOW}{cursor1}{RESET}"

            eye_color = RED if (i % 4 < 2) else YELLOW
            s_lines = [get_skull_bg_line(r, i, eye_color) for r in range(len(skull_template))]

            content = [
                top_b,
                f"{HEADER_BORDER}║{DIM_GREEN}" + get_bin(i, INNER_WIDTH) + f"{RESET}{HEADER_BORDER}║{RESET}",
                *[f"{HEADER_BORDER}║{l}{HEADER_BORDER}║{RESET}" for l in s_lines],
                f"{HEADER_BORDER}║{DIM_GREEN}" + get_bin(i + 50, INNER_WIDTH) + f"{RESET}{HEADER_BORDER}║{RESET}",
                mid_b,
                f"{HEADER_BORDER}║" + pad_with_bin(txt1, i) + f"{HEADER_BORDER}║{RESET}",
                f"{HEADER_BORDER}║{DIM_GREEN}" + get_bin(i + 80, INNER_WIDTH) + f"{RESET}{HEADER_BORDER}║{RESET}",
                bot_b
            ]

            sys.stdout.write("\033[H" + "\n".join(content) + "\n")
            sys.stdout.flush()
            time.sleep(0.035)

        # Fase 2: Efek typewriter tulisan "C-Row is here"
        for j in range(len(subtitle_target) + 1):
            partial2 = subtitle_target[:j]
            cursor2 = "█" if j < len(subtitle_target) else ""
            txt2 = f"{YELLOW}{BOLD}{partial2}{RESET}{YELLOW}{cursor2}{RESET}"

            eye_color = RED if (j % 4 < 2) else YELLOW
            s_lines = [get_skull_bg_line(r, j + 40, eye_color) for r in range(len(skull_template))]

            content = [
                top_b,
                f"{HEADER_BORDER}║{DIM_GREEN}" + get_bin(j + 40, INNER_WIDTH) + f"{RESET}{HEADER_BORDER}║{RESET}",
                *[f"{HEADER_BORDER}║{l}{HEADER_BORDER}║{RESET}" for l in s_lines],
                f"{HEADER_BORDER}║{DIM_GREEN}" + get_bin(j + 90, INNER_WIDTH) + f"{RESET}{HEADER_BORDER}║{RESET}",
                mid_b,
                f"{HEADER_BORDER}║" + pad_with_bin(f"{CYAN}{BOLD}{welcome_target}{RESET}", j + 40) + f"{HEADER_BORDER}║{RESET}",
                f"{HEADER_BORDER}║" + pad_with_bin(txt2, j + 120) + f"{HEADER_BORDER}║{RESET}",
                bot_b
            ]

            sys.stdout.write("\033[H" + "\n".join(content) + "\n")
            sys.stdout.flush()
            time.sleep(0.03)

        time.sleep(0.8)
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()
        clear_screen()

def get_multi_beam_h_line(left_c, fill_c, right_c, width, beam_positions, base_color, shine_color):
    """Membuat garis horizontal dengan berkas cahaya yang bergerak"""
    chars = []
    active_beams = [p for p in beam_positions if p >= 0]
    for i in range(width):
        if active_beams:
            min_dist = min(abs(i - p) for p in active_beams)
        else:
            min_dist = 999
        if min_dist == 0:
            chars.append(f"{WHITE}{fill_c}{RESET}{base_color}")
        elif min_dist <= 2:
            chars.append(f"{shine_color}{fill_c}{RESET}{base_color}")
        else:
            chars.append(f"{base_color}{fill_c}")
    return f"{base_color}{left_c}" + "".join(chars) + f"{base_color}{right_c}{RESET}"

def get_shimmer_text(text, beam_pos, base_color, shine_color):
    """Memberikan efek gelombang cahaya menyapu teks huruf per huruf"""
    res = []
    for i, ch in enumerate(text):
        if ch == ' ':
            res.append(' ')
        else:
            dist = abs(i - beam_pos)
            if dist == 0:
                res.append(f"{WHITE}{BOLD}{ch}{RESET}{base_color}")
            elif dist <= 2:
                res.append(f"{shine_color}{BOLD}{ch}{RESET}{base_color}")
            else:
                res.append(f"{base_color}{ch}")
    return f"{base_color}" + "".join(res) + RESET

def render_main_screen(tick=0, user_input=""):
    """Merender menu C-ROW: Header Besar (Lebar 50 Kol, Panjang 7 Baris), Tools di Pinggir, Bebas Kedipan"""
    
    # 1. Perhitungan Sirkuit Header Ungu (Lebar=48, Tinggi=9 -> Keliling=114)
    W_H = INNER_WIDTH
    H_H = 9
    perim_h = 2 * (W_H + H_H)  # 114
    
    step1_h = tick % perim_h
    step2_h = (tick + (perim_h // 2)) % perim_h
    
    top_beams_h = []
    bot_beams_h = []
    left_walls_h = set()
    right_walls_h = set()

    for s in [step1_h, step2_h]:
        if s < W_H:
            top_beams_h.append(s)
        elif s < W_H + H_H:
            right_walls_h.add(s - W_H)
        elif s < 2 * W_H + H_H:
            bot_beams_h.append((W_H - 1) - (s - W_H - H_H))
        else:
            left_walls_h.add((H_H - 1) - (s - 2 * W_H - H_H))

    top_header = get_multi_beam_h_line("╔", "═", "╗", INNER_WIDTH, top_beams_h, HEADER_BORDER, YELLOW)
    mid_header = f"{HEADER_BORDER}╠" + ("═" * INNER_WIDTH) + f"╣{RESET}"
    bot_header = get_multi_beam_h_line("╚", "═", "╝", INNER_WIDTH, bot_beams_h, HEADER_BORDER, YELLOW)

    # ASCII C-ROW BESAR: 7 baris panjang & 48 kolom lebar (Mantap & Full Kanan)
    raw_art = [
        "    ██████╗    ██████╗   ██████╗  ██╗    ██╗    ",
        "   ██╔════╝    ██╔══██╗ ██╔═══██╗ ██║    ██║    ",
        "   ██║         ██████╔╝ ██║   ██║ ██║ █╗ ██║    ",
        "   ██║ █████╗  ██╔══██╗ ██║   ██║ ██║███╗██║    ",
        "   ██║ ╚════╝  ██║  ██║ ██║   ██║ ██║███╗██║    ",
        "   ╚██████╗    ██║  ██║ ╚██████╔╝ ╚███╔███╔╝    ",
        "    ╚═════╝    ╚═╝  ╚═╝  ╚═════╝   ╚══╝╚══╝     "
    ]

    beam_crow_x = (tick * 2) % 58
    art_contents = []
    for r_idx, line in enumerate(raw_art):
        line_chars = []
        for col_idx, char in enumerate(line[:INNER_WIDTH]):
            if char == ' ':
                b_digit = BINARY_STREAM[(r_idx * INNER_WIDTH + col_idx + (tick // 2)) % len(BINARY_STREAM)]
                line_chars.append(f"{DIM_BINARY}{b_digit}{RESET}")
            else:
                dist = abs(col_idx - beam_crow_x)
                if dist == 0:
                    line_chars.append(f"{WHITE}{char}{RESET}")
                elif dist <= 2:
                    line_chars.append(f"{CYAN}{char}{RESET}")
                else:
                    line_chars.append(f"{WHITE}{char}{RESET}")
        art_contents.append("".join(line_chars))

    header_body = []
    for idx, content in enumerate(art_contents):
        l_wall = f"{WHITE}║{RESET}" if idx in left_walls_h else f"{HEADER_BORDER}║{RESET}"
        r_wall = f"{WHITE}║{RESET}" if idx in right_walls_h else f"{HEADER_BORDER}║{RESET}"
        header_body.append(f"{l_wall}{content}{r_wall}")

    header_body.append(mid_header)
    
    # Baris VIP + Mahkota 👑 (Total 48 karakter visual di dalam kotak)
    info_idx = 8
    l_wall_info = f"{WHITE}║{RESET}" if info_idx in left_walls_h else f"{HEADER_BORDER}║{RESET}"
    r_wall_info = f"{WHITE}║{RESET}" if info_idx in right_walls_h else f"{HEADER_BORDER}║{RESET}"
    
    left_bin = "".join(BINARY_STREAM[(8 * INNER_WIDTH + i + (tick // 2)) % len(BINARY_STREAM)] for i in range(21))
    right_bin = "".join(BINARY_STREAM[(8 * INNER_WIDTH + 21 + 5 + i + (tick // 2)) % len(BINARY_STREAM)] for i in range(22))
    
    vip_line = f"{l_wall_info}{DIM_BINARY}{left_bin}{RESET}{YELLOW}VIP👑{RESET}{DIM_BINARY}{right_bin}{RESET}{r_wall_info}"
    header_body.append(vip_line)

    # 2. Tabel Menu Tools: Di Pinggir & Full Lebar (50 Kolom)
    right_col_w = SCREEN_WIDTH - 9  # 41
    top_menu      = f"{MENU_BORDER}┌──────┬" + ("─" * right_col_w) + f"┐{RESET}"
    connected_div = f"{MENU_BORDER}├──────┼" + ("─" * right_col_w) + f"┤{RESET}"
    bot_menu      = f"{MENU_BORDER}└──────┴" + ("─" * right_col_w) + f"┘{RESET}"

    menu_rows_data = [
        (CYAN,    "[01]", "Tool Scraper & Sosmed"),
        (GREEN,   "[02]", "Tool Analisis & Keamanan"),
        (YELLOW,  "[03]", "Tool Otomatisasi & Bot"),
        (MAGENTA, "[04]", "File Manager & Downloader"),
        (BLUE,    "[05]", "Pengaturan & Update Tool"),
        (RED,     "[00]", "Keluar Sistem")
    ]

    menu_body = []
    for idx, (tag_color, tag_id, name) in enumerate(menu_rows_data):
        row_text = f"{name:<40}"
        menu_body.append(f"{MENU_BORDER}│{RESET}{tag_color} {tag_id} {MENU_BORDER}│{WHITE} {row_text}{MENU_BORDER}│{RESET}")
        if idx < len(menu_rows_data) - 1:
            menu_body.append(connected_div)

    # 3. Judul Menu & Prompt
    beam_title = (tick * 2) % 30
    title_animated = get_shimmer_text(" [ PILIH MENU TOOLS ]", beam_title, MENU_BORDER, WHITE)

    pulse_palette = [MENU_BORDER, CYAN, WHITE, YELLOW]
    arrow_color = pulse_palette[(tick // 3) % len(pulse_palette)]
    blink_cursor = f"{YELLOW}█{RESET}" if ((tick // 3) % 2 == 0) else " "

    prompt_line1 = f"{MENU_BORDER}╭── {GREEN}(root㉿termux){MENU_BORDER}─[{WHITE}~/c-row{MENU_BORDER}]{RESET}"
    prompt_line2 = f"{MENU_BORDER}╰─{arrow_color}➤{WHITE} Masukkan Pilihan [0-5]: {YELLOW}{user_input}{blink_cursor}\033[K"

    all_lines = [
        top_header,
        *header_body,
        bot_header,
        "",
        title_animated,
        top_menu,
        *menu_body,
        bot_menu,
        "",
        prompt_line1,
        prompt_line2
    ]

    # Double buffer in-place tanpa menghapus layar (Zero Flicker / Bebas Kedip)
    output = "\033[H" + "\n".join(all_lines) + "\n"
    sys.stdout.write(output)
    sys.stdout.flush()

def get_smart_interactive_input():
    """Membaca input dengan animasi tetap bergerak saat idle, dan berhenti otomatis saat user mulai ngetik"""
    user_input = ""
    tick = 0
    last_frame = time.time()
    last_keystroke_time = 0.0
    is_typing = False
    IDLE_RESUME_DELAY = 1.2 # Detik diam sebelum animasi otomatis jalan kembali

    clear_screen()
    sys.stdout.write("\033[?25l")  # Sembunyikan kursor terminal bawaan
    sys.stdout.flush()

    old_settings = None
    if sys.platform != "win32":
        try:
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            new_settings = termios.tcgetattr(fd)
            # Matikan ECHO agar ketikan tidak dobel
            new_settings[3] = new_settings[3] & ~termios.ECHO
            new_settings[3] = new_settings[3] & ~termios.ICANON
            new_settings[6][termios.VMIN] = 0
            new_settings[6][termios.VTIME] = 0
            termios.tcsetattr(fd, termios.TCSANOW, new_settings)
        except Exception:
            pass

    try:
        render_main_screen(tick, user_input)

        while True:
            # 1. Cek tombol keyboard secara non-blocking
            has_key = False
            ch = ""

            if sys.platform == "win32":
                if msvcrt.kbhit():
                    ch = msvcrt.getwch()
                    has_key = True
            else:
                r, _, _ = select.select([sys.stdin], [], [], 0.02)
                if r:
                    ch = sys.stdin.read(1)
                    has_key = True

            now = time.time()

            if has_key:
                # Tangani escape sequences (sentuhan layar, mouse, panah, dll.)
                if ch == "\x1b":
                    time.sleep(0.01)
                    while select.select([sys.stdin], [], [], 0)[0]:
                        sys.stdin.read(1)
                    continue

                if ch in ("\r", "\n"):
                    sys.stdout.write("\033[?25h\n")
                    sys.stdout.flush()
                    return user_input.strip()
                elif ch in ("\b", "\x08", "\x7f"):
                    user_input = user_input[:-1]
                    is_typing = True
                    last_keystroke_time = now
                    render_main_screen(tick, user_input)
                elif ch == "\x03":
                    raise KeyboardInterrupt
                elif ch.isprintable() and len(user_input) < 10:
                    user_input += ch
                    is_typing = True
                    last_keystroke_time = now
                    render_main_screen(tick, user_input)

            # 2. Cek status idle: Jika user berhenti mengetik selama 1.2 detik, animasi lanjut jalan!
            if is_typing:
                if now - last_keystroke_time >= IDLE_RESUME_DELAY:
                    is_typing = False

            # 3. Update animasi jika sedang TIDAK mengetik
            if not is_typing:
                if now - last_frame >= 0.06:
                    tick += 1
                    render_main_screen(tick, user_input)
                    last_frame = now
                else:
                    time.sleep(0.01)
            else:
                time.sleep(0.02)

    finally:
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()
        if sys.platform != "win32" and old_settings:
            try:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            except Exception:
                pass

# =====================================================================
# TEMPAT LOGIKA TOOLS ANDA NANTI
# =====================================================================
def run_tool(nomor, nama_tool):
    clear_screen()
    top_t = f"{HEADER_BORDER}╔" + ("═" * INNER_WIDTH) + f"╗{RESET}"
    bot_t = f"{HEADER_BORDER}╚" + ("═" * INNER_WIDTH) + f"╝{RESET}"
    print(top_t)
    print(f"{HEADER_BORDER}║{RESET} {WHITE}[MODUL]{RESET} {WHITE}{nama_tool:<38}{HEADER_BORDER}║{RESET}")
    print(bot_t + "\n")
    
    # Animasi loading sebelum menjalankan tool
    loading_spinner(f"Menyiapkan {nama_tool}", duration=1.0)
    
    print(f"{GREEN} [●] {nama_tool} sedang berjalan...{RESET}")
    print(f"{WHITE} ------------------------------------------------{RESET}")
    # --- LOGIKA TOOL ANDA MASUK DI SINI ---
    print(f" {WHITE}(Modul aktif dan siap menerima perintah logika){RESET}")
    print(f"{WHITE} ------------------------------------------------{RESET}")
    
    input(f"\n{MENU_BORDER} Tekan Enter untuk kembali ke menu...{RESET}")

# =====================================================================
# MAIN LOOP
# =====================================================================
def main():
    # Jalankan animasi opening Welcome My Friend saat pertama kali program dibuka
    skull_welcome_intro()

    tools = {
        "1": "Tool Scraper & Sosmed",
        "01": "Tool Scraper & Sosmed",
        "2": "Tool Analisis & Keamanan",
        "02": "Tool Analisis & Keamanan",
        "3": "Tool Otomatisasi & Bot",
        "03": "Tool Otomatisasi & Bot",
        "4": "File Manager & Downloader",
        "04": "File Manager & Downloader",
        "5": "Pengaturan & Update Tool",
        "05": "Pengaturan & Update Tool",
    }

    while True:
        try:
            # Menu cerdas: Animasi terus gerak saat menunggu, pause saat mengetik, resume saat idle
            choice = get_smart_interactive_input()
            
            if choice in tools:
                run_tool(choice, tools[choice])
            elif choice in ["0", "00", "exit", "quit", "x"]:
                print(f"\n{RED}  [!] Menutup sesi C-Row VIP. Sampai jumpa!{RESET}\n")
                sys.exit(0)
            elif choice == "":
                continue
            else:
                print(f"\n{RED}  [!] Pilihan '{choice}' tidak valid!{RESET}")
                time.sleep(1.0)
        except KeyboardInterrupt:
            print(f"\n\n{RED}  [!] Program dihentikan (Ctrl+C).{RESET}\n")
            sys.exit(0)

if __name__ == "__main__":
    main()
