#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==================================================
 Project Name : C-Row [ VIP ]
 Style        : Cyber Matrix Console (Ergonomic & Clean Reading)
 Platform     : Termux & Windows CMD
 Author       : Javier
==================================================
"""

import os
import sys
import time
import random
import re
import unicodedata

# Impor library non-blocking keyboard input sesuai OS
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

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def loading_spinner(pesan, duration=1.2):
    """Animasi spinner berputar saat proses loading tool"""
    frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    end_time = time.time() + duration
    idx = 0
    while time.time() < end_time:
        frame = frames[idx % len(frames)]
        sys.stdout.write(f"\r  {CYAN}[{frame}]{WHITE} {pesan}...{RESET}")
        sys.stdout.flush()
        time.sleep(0.08)
        idx += 1
    sys.stdout.write(f"\r  {GREEN}[✓]{WHITE} {pesan} selesai!   {RESET}\n\n")

def vlen(s):
    """Menghitung lebar visual karakter (mendukung emoji & aksen ANSI)"""
    s_clean = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', s)
    return sum(2 if unicodedata.east_asian_width(c) in ('W', 'F') else 1 for c in s_clean)

def pad38(text):
    """Memastikan teks berada tepat di tengah dengan lebar 38 kolom visual"""
    cur = vlen(text)
    rem = 38 - cur
    l = max(0, rem // 2)
    r = max(0, rem - l)
    return (' ' * l) + text + (' ' * r)

def get_bin(offset, length):
    return "".join(BINARY_STREAM[(offset + i) % len(BINARY_STREAM)] for i in range(length))

def pad_with_bin(text_to_show, offset):
    cur = vlen(text_to_show)
    rem = 38 - cur
    l = max(0, rem // 2)
    r = max(0, rem - l)
    b_left = f"{DIM_GREEN}" + get_bin(offset, l) + f"{RESET}"
    b_right = f"{DIM_GREEN}" + get_bin(offset + 30, r) + f"{RESET}"
    return b_left + text_to_show + b_right

def skull_welcome_intro():
    """Animasi opening Welcome My Friend dengan ASCII Tengkorak & latar biner hijau Matrix (Fit Layar HP)"""
    clear_screen()
    sys.stdout.write("\033[?25l")  # Sembunyikan kursor terminal
    sys.stdout.flush()

    top_b = f"{HEADER_BORDER} ╔" + ("═" * 38) + f"╗{RESET}"
    bot_b = f"{HEADER_BORDER} ╚" + ("═" * 38) + f"╝{RESET}"
    mid_b = f"{HEADER_BORDER} ╠" + ("═" * 38) + f"╣{RESET}"

    welcome_target = "W E L C O M E   M Y   F R I E N D"
    subtitle_target = "C-Row is here"

    skull_template = [
        ("              .-------.               ", 14, 22),
        ("            .-         -.             ", 12, 24),
        ("           /   (O) (O)   \\            ", 11, 25),
        ("          |       _       |           ", 10, 26),
        ("           \\   \\_____/   /            ", 11, 25),
        ("            \\   | | |   /             ", 12, 24),
        ("             '--'---'--'              ", 13, 23),
    ]

    def get_skull_bg_line(r_idx, tick, eye_color):
        raw, l_bound, r_bound = skull_template[r_idx]
        res = []
        for c_idx, ch in enumerate(raw):
            if c_idx < l_bound or c_idx > r_bound:
                b = BINARY_STREAM[(r_idx * 38 + c_idx + tick) % len(BINARY_STREAM)]
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
                f"{HEADER_BORDER} ║{DIM_GREEN}" + get_bin(i, 38) + f"{RESET}{HEADER_BORDER}║{RESET}",
                *[f"{HEADER_BORDER} ║{l}{HEADER_BORDER}║{RESET}" for l in s_lines],
                f"{HEADER_BORDER} ║{DIM_GREEN}" + get_bin(i + 50, 38) + f"{RESET}{HEADER_BORDER}║{RESET}",
                mid_b,
                f"{HEADER_BORDER} ║" + pad_with_bin(txt1, i) + f"{HEADER_BORDER}║{RESET}",
                f"{HEADER_BORDER} ║{DIM_GREEN}" + get_bin(i + 80, 38) + f"{RESET}{HEADER_BORDER}║{RESET}",
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
                f"{HEADER_BORDER} ║{DIM_GREEN}" + get_bin(j + 40, 38) + f"{RESET}{HEADER_BORDER}║{RESET}",
                *[f"{HEADER_BORDER} ║{l}{HEADER_BORDER}║{RESET}" for l in s_lines],
                f"{HEADER_BORDER} ║{DIM_GREEN}" + get_bin(j + 90, 38) + f"{RESET}{HEADER_BORDER}║{RESET}",
                mid_b,
                f"{HEADER_BORDER} ║" + pad_with_bin(f"{CYAN}{BOLD}{welcome_target}{RESET}", j + 40) + f"{HEADER_BORDER}║{RESET}",
                f"{HEADER_BORDER} ║" + pad_with_bin(txt2, j + 120) + f"{HEADER_BORDER}║{RESET}",
                bot_b
            ]

            sys.stdout.write("\033[H" + "\n".join(content) + "\n")
            sys.stdout.flush()
            time.sleep(0.03)

        time.sleep(0.8)
    except KeyboardInterrupt:
        pass
    finally:
        clear_screen()

def get_multi_beam_h_line(left_c, fill_c, right_c, width, beam_positions, base_color, shine_color):
    """Membuat garis horizontal dengan DUA berkas cahaya yang bergerak terpisah"""
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

def render_main_screen(tick, user_input=""):
    """Merender layar dengan C-ROW bernyawa di atas & Menu Tenang, Nyaman & Mudah Dibaca (Fit Layar HP)"""
    
    # =========================================================================
    # 1. PERHITUNGAN SIRKUIT HEADER (Ungu): Lebar=38, Tinggi=8 -> Total=92 step
    # =========================================================================
    W_H = 38
    H_H = 8
    perim_h = 2 * (W_H + H_H)  # 92
    
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

    top_header = get_multi_beam_h_line(" ╔", "═", "╗", 38, top_beams_h, HEADER_BORDER, YELLOW)
    mid_header = f"{HEADER_BORDER} ╠" + ("═" * 38) + f"╣{RESET}"
    bot_header = get_multi_beam_h_line(" ╚", "═", "╝", 38, bot_beams_h, HEADER_BORDER, YELLOW)

    raw_art = [
        " ██████╗   ██████╗  ██████╗ ██╗    ██╗",
        "██╔════╝   ██╔══██╗██╔═══██╗██║    ██║",
        "██║ █████╗ ██████╔╝██║   ██║██║ █╗ ██║",
        "██║ ╚════╝ ██╔══██╗██║   ██║██║███╗██║",
        "╚██████╗   ██║  ██║╚██████╔╝╚███╔███╔╝",
        " ╚═════╝   ╚═╝  ╚═╝ ╚═════╝  ╚══╝╚══╝ ",
    ]

    # ANIMASI DI HURUF C-ROW + BACKGROUND BINER SAMAR
    beam_crow_x = (tick * 2) % 46
    art_contents = []
    for r_idx, line in enumerate(raw_art):
        line_chars = []
        for col_idx, char in enumerate(line):
            if char == ' ':
                b_digit = BINARY_STREAM[(r_idx * 38 + col_idx + (tick // 2)) % len(BINARY_STREAM)]
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
        header_body.append(f" {l_wall}{content}{r_wall}")

    header_body.append(mid_header)
    
    # Baris VIP + Mahkota Emas Asli 👑 (Lebar visual total = 38)
    info_idx = 7
    l_wall_info = f"{WHITE}║{RESET}" if info_idx in left_walls_h else f"{HEADER_BORDER}║{RESET}"
    r_wall_info = f"{WHITE}║{RESET}" if info_idx in right_walls_h else f"{HEADER_BORDER}║{RESET}"
    
    left_bin = "".join(BINARY_STREAM[(7 * 38 + i + (tick // 2)) % len(BINARY_STREAM)] for i in range(16))
    right_bin = "".join(BINARY_STREAM[(7 * 38 + 16 + 5 + i + (tick // 2)) % len(BINARY_STREAM)] for i in range(17))
    
    vip_line = f" {l_wall_info}{DIM_BINARY}{left_bin}{RESET}{YELLOW}VIP👑{RESET}{DIM_BINARY}{right_bin}{RESET}{r_wall_info}"
    header_body.append(vip_line)

    # =========================================================================
    # 2. TABEL TOOLS: SOLID, TENANG, KONTRAS TINGGI & FIT LAYAR HP (41 KOLOM)
    # =========================================================================
    top_menu      = f"{MENU_BORDER} ┌──────┬───────────────────────────────┐{RESET}"
    connected_div = f"{MENU_BORDER} ├──────┼───────────────────────────────┤{RESET}"
    bot_menu      = f"{MENU_BORDER} └──────┴───────────────────────────────┘{RESET}"

    menu_rows_data = [
        (CYAN,    "[01]", "Tool Scraper & Sosmed         "),
        (GREEN,   "[02]", "Tool Analisis & Keamanan      "),
        (YELLOW,  "[03]", "Tool Otomatisasi & Bot        "),
        (MAGENTA, "[04]", "File Manager & Downloader     "),
        (BLUE,    "[05]", "Pengaturan & Update Tool      "),
        (RED,     "[00]", "Keluar Sistem                 ")
    ]

    menu_body = []
    for idx, (tag_color, tag_id, name) in enumerate(menu_rows_data):
        menu_body.append(f" {MENU_BORDER}│{RESET}{tag_color} {tag_id} {MENU_BORDER}│{WHITE} {name}{MENU_BORDER}│{RESET}")
        if idx < len(menu_rows_data) - 1:
            menu_body.append(connected_div)

    # =========================================================================
    # 3. JUDUL MENU & PROMPT INPUT
    # =========================================================================
    beam_title = (tick * 2) % 30
    title_animated = get_shimmer_text("       [ PILIH MENU TOOLS ]", beam_title, MENU_BORDER, WHITE)

    pulse_palette = [MENU_BORDER, CYAN, WHITE, YELLOW]
    arrow_color = pulse_palette[(tick // 3) % len(pulse_palette)]
    blink_cursor = f"{YELLOW}█{RESET}" if ((tick // 3) % 2 == 0) else " "

    prompt_line1 = f"{MENU_BORDER} ╭── {GREEN}(root㉿termux){MENU_BORDER}─[{WHITE}~/c-row{MENU_BORDER}]{RESET}"
    prompt_line2 = f"{MENU_BORDER} ╰─{arrow_color}➤{WHITE} Masukkan Pilihan [0-5]: {YELLOW}{user_input}{blink_cursor}\033[K"

    # =========================================================================
    # GABUNGKAN SELURUH TAMPILAN
    # =========================================================================
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

    output = "\033[H" + "\n".join(all_lines)
    sys.stdout.write(output)
    sys.stdout.flush()

def get_animated_input():
    """Membaca input keyboard sambil memutar sirkuit cahaya di header"""
    user_input = ""
    tick = 0
    last_frame = time.time()
    
    clear_screen()
    sys.stdout.write("\033[?25l")  # Sembunyikan kursor terminal
    sys.stdout.flush()

    old_settings = None
    if sys.platform != "win32":
        try:
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            tty.setcbreak(fd)
        except Exception:
            pass

    try:
        render_main_screen(tick, user_input)
        
        while True:
            # 1. Cek Tombol Keyboard (Non-blocking)
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

            if has_key:
                if ch in ("\r", "\n"):
                    sys.stdout.write("\033[?25h\n")
                    sys.stdout.flush()
                    return user_input.strip()
                elif ch in ("\b", "\x08", "\x7f"):
                    user_input = user_input[:-1]
                    render_main_screen(tick, user_input)
                elif ch == "\x03":
                    raise KeyboardInterrupt
                elif ch.isprintable():
                    user_input += ch
                    render_main_screen(tick, user_input)

            # 2. Update Animasi Layar (25 FPS sangat halus)
            now = time.time()
            if now - last_frame >= 0.04:
                tick += 1
                render_main_screen(tick, user_input)
                last_frame = now
            else:
                time.sleep(0.008)

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
    print(f"{HEADER_BORDER} ╔══════════════════════════════════════════════════════════╗")
    print(f" ║  {WHITE}[MODUL]{HEADER_BORDER} {WHITE}{nama_tool:<48}{HEADER_BORDER} ║")
    print(f" ╚══════════════════════════════════════════════════════════╝{RESET}\n")
    
    # Animasi loading sebelum menjalankan tool
    loading_spinner(f"Menyiapkan {nama_tool}", duration=1.0)
    
    print(f"{GREEN}  [●] {nama_tool} sedang berjalan...{RESET}")
    print(f"{WHITE}  ------------------------------------------------{RESET}")
    # --- LOGIKA TOOL ANDA MASUK DI SINI ---
    print(f"  {WHITE}(Modul aktif dan siap menerima perintah logika){RESET}")
    print(f"{WHITE}  ------------------------------------------------{RESET}")
    
    input(f"\n{MENU_BORDER}  Tekan Enter untuk kembali ke menu utama...{RESET}")

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
            choice = get_animated_input()
            
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
