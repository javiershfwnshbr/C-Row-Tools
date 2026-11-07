#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==================================================
 Project Name : C-Row [ VIP ]
 Style        : Cyber Matrix Console (Fit Screen 48 Cols)
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
import shutil
import signal

# Flag deteksi perubahan ukuran terminal (misal saat Gboard dibuka / ditutup)
RESIZED = False

def handle_sigwinch(signum, frame):
    global RESIZED
    RESIZED = True

if hasattr(signal, "SIGWINCH"):
    try:
        signal.signal(signal.SIGWINCH, handle_sigwinch)
    except Exception:
        pass

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

# Ukuran Lebar Layar: 48 Kolom Presisi
SCREEN_WIDTH = 48
INNER_WIDTH  = 46

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
    """Animasi opening Welcome My Friend dengan ASCII Tengkorak & latar biner hijau Matrix (Full 48 Kolom)"""
    clear_screen()
    sys.stdout.write("\033[?25l")  # Sembunyikan kursor terminal
    sys.stdout.flush()

    top_b = f"{HEADER_BORDER}╔" + ("═" * INNER_WIDTH) + f"╗{RESET}"
    bot_b = f"{HEADER_BORDER}╚" + ("═" * INNER_WIDTH) + f"╝{RESET}"
    mid_b = f"{HEADER_BORDER}╠" + ("═" * INNER_WIDTH) + f"╣{RESET}"

    welcome_target = "W E L C O M E   M Y   F R I E N D"
    subtitle_target = "C-Row is here"

    skull_template = [
        ("                  .-------.                   ", 18, 26),
        ("                .-         -.                 ", 16, 28),
        (r"               /   (O) (O)   \                ", 15, 29),
        ("              |       _       |               ", 14, 30),
        (r"               \   \_____/   /                ", 15, 29),
        (r"                \   | | |   /                 ", 16, 28),
        ("                 '--'---'--'                  ", 17, 27),
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
    """Merender menu C-ROW: Presisi 48 Kolom, Responsif Tinggi (Auto Compact saat Keyboard Terbuka)"""
    
    term_cols, term_lines = shutil.get_terminal_size((48, 24))

    # 1. Tabel Menu Tools (Total Lebar 48 Kolom - Pembatas Garis Tiap Tool Rapi & Enak Dibaca)
    right_col_w = SCREEN_WIDTH - 9  # 39
    top_menu      = f"{MENU_BORDER}┌──────┬" + ("─" * right_col_w) + f"┐{RESET}"
    connected_div = f"{MENU_BORDER}├──────┼" + ("─" * right_col_w) + f"┤{RESET}"
    bot_menu      = f"{MENU_BORDER}└──────┴" + ("─" * right_col_w) + f"┘{RESET}"

    menu_rows_data = [
        (CYAN,    "[01]", "C-Row APK Controller"),
        (GREEN,   "[02]", "Tool Analisis & Keamanan"),
        (YELLOW,  "[03]", "Tool Otomatisasi & Bot"),
        (MAGENTA, "[04]", "File Manager & Downloader"),
        (BLUE,    "[05]", "Pengaturan & Update Tool"),
        (RED,     "[00]", "Keluar Sistem")
    ]

    menu_body = []
    for idx, (tag_color, tag_id, name) in enumerate(menu_rows_data):
        row_text = f"{name:<36}"
        menu_body.append(f"{MENU_BORDER}│{RESET}{tag_color} {tag_id} {MENU_BORDER}│ {tag_color}>{WHITE} {row_text}{MENU_BORDER}│{RESET}")
        if idx < len(menu_rows_data) - 1:
            menu_body.append(connected_div)

    pulse_palette = [MENU_BORDER, CYAN, WHITE, YELLOW]
    arrow_color = pulse_palette[(tick // 3) % len(pulse_palette)]
    blink_cursor = f"{YELLOW}█{RESET}" if ((tick // 3) % 2 == 0) else " "

    prompt_line1 = f"{MENU_BORDER}╭── {GREEN}(root㉿termux){MENU_BORDER}─[{WHITE}~/c-row{MENU_BORDER}]{RESET}"
    prompt_line2 = f"{MENU_BORDER}╰─{arrow_color}➤{WHITE} Masukkan Pilihan [0-5]: {YELLOW}{user_input}{blink_cursor}\033[K"

    # MODE COMPACT (Jika keyboard virtual Android Gboard sedang terbuka / layar < 28 baris)
    # Total tinggi 16 baris -> Rapi & Tidak Akan Pernah Scroll / Rusak!
    if term_lines < 28:
        compact_title = f"{HEADER_BORDER}╔══ {WHITE}C-ROW {HEADER_BORDER}[ {YELLOW}VIP👑 {HEADER_BORDER}] " + ("═" * 27) + f"╗{RESET}"
        all_lines = [
            compact_title,
            top_menu,
            *menu_body,
            bot_menu,
            prompt_line1,
            prompt_line2
        ]
    else:
        # MODE FULL (Ketika keyboard tertutup / layar normal >= 23 baris)
        # ASCII C-ROW BESAR & 3D: 7 baris gagah, tinggi & panjang presisi 46 kolom lebar (48 dengan border)
        raw_art = [
            "   ██████╗    ██████╗   ██████╗  ██╗    ██╗   ",
            "  ██╔════╝    ██╔══██╗ ██╔═══██╗ ██║    ██║   ",
            "  ██║         ██████╔╝ ██║   ██║ ██║ █╗ ██║   ",
            "  ██║ █████╗  ██╔══██╗ ██║   ██║ ██║███╗██║   ",
            "  ██║ ╚════╝  ██║  ██║ ██║   ██║ ██║███╗██║   ",
            "  ╚██████╗    ██║  ██║ ╚██████╔╝ ╚███╔███╔╝   ",
            "   ╚═════╝    ╚═╝  ╚═╝  ╚═════╝   ╚══╝╚══╝    "
        ]

        # Perhitungan Sirkuit Header Ungu (Lebar=46, Tinggi=9 -> Keliling=110)
        W_H = INNER_WIDTH
        H_H = len(raw_art) + 2  # 9
        perim_h = 2 * (W_H + H_H)  # 110
        
        step1_h = (tick * 2) % perim_h
        step2_h = (tick * 2 + (perim_h // 2)) % perim_h
        
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

        beam_crow_x = (tick * 2) % 56
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
        
        # Baris VIP + Mahkota 👑
        info_idx = len(raw_art) + 1
        l_wall_info = f"{WHITE}║{RESET}" if info_idx in left_walls_h else f"{HEADER_BORDER}║{RESET}"
        r_wall_info = f"{WHITE}║{RESET}" if info_idx in right_walls_h else f"{HEADER_BORDER}║{RESET}"
        
        left_bin = "".join(BINARY_STREAM[(8 * INNER_WIDTH + i + (tick // 2)) % len(BINARY_STREAM)] for i in range(20))
        right_bin = "".join(BINARY_STREAM[(8 * INNER_WIDTH + 20 + 5 + i + (tick // 2)) % len(BINARY_STREAM)] for i in range(21))
        
        vip_line = f"{l_wall_info}{DIM_BINARY}{left_bin}{RESET}{YELLOW}VIP👑{RESET}{DIM_BINARY}{right_bin}{RESET}{r_wall_info}"
        header_body.append(vip_line)

        beam_title = (tick * 2) % 30
        title_animated = get_shimmer_text(" [ PILIH MENU TOOLS ]", beam_title, MENU_BORDER, WHITE)

        all_lines = [
            top_header,
            *header_body,
            bot_header,
            title_animated,
            top_menu,
            *menu_body,
            bot_menu,
            prompt_line1,
            prompt_line2
        ]

    # In-place overwrite menggunakan \033[H
    output = "\033[H" + "\n".join(all_lines)
    sys.stdout.write(output)
    sys.stdout.flush()

def get_live_interactive_input():
    """Animasi terus bergerak saat idle, otomatis berhenti saat user ngetik, dan jalan lagi saat berhenti ngetik"""
    global RESIZED
    user_input = ""
    tick = 0
    last_frame = time.time()
    last_keystroke_time = 0.0
    is_typing = False
    IDLE_RESUME_DELAY = 1.8 # Jeda 1.8 detik setelah berhenti mengetik sebelum animasi lanjut jalan
    FRAME_INTERVAL = 0.05   # Kecepatan frame super mulus (20 FPS): Cepat, hidup, tidak delay
    VALID_CHARS = "0123456789exitquitxX" # Filter ketat karakter valid

    clear_screen()
    sys.stdout.write("\033[?25l") # Sembunyikan kursor terminal bawaan agar tidak ada kotak putih berkedip
    sys.stdout.flush()

    old_settings = None
    if sys.platform != "win32":
        try:
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            new_settings = termios.tcgetattr(fd)
            # Matikan ECHO agar ketikan tidak dobel di Android Termux
            new_settings[3] = new_settings[3] & ~termios.ECHO
            new_settings[3] = new_settings[3] & ~termios.ICANON
            new_settings[6][termios.VMIN] = 0
            new_settings[6][termios.VTIME] = 0
            termios.tcsetattr(fd, termios.TCSANOW, new_settings)
        except Exception:
            pass

    last_term_lines = shutil.get_terminal_size((48, 24)).lines

    try:
        render_main_screen(tick, user_input)

        while True:
            now = time.time()

            # Deteksi resize layar secara efisien
            if RESIZED:
                RESIZED = False
                curr_term_lines = shutil.get_terminal_size((48, 24)).lines
                if curr_term_lines != last_term_lines:
                    last_term_lines = curr_term_lines
                    is_typing = True
                    last_keystroke_time = now
                    clear_screen()
                    render_main_screen(tick, user_input)

            # 1. Cek tombol keyboard non-blocking (responsif instan < 10ms)
            has_key = False
            ch = ""

            if sys.platform == "win32":
                if msvcrt.kbhit():
                    ch = msvcrt.getwch()
                    if ch in ('\x00', '\xe0'):
                        if msvcrt.kbhit():
                            msvcrt.getwch()
                        continue
                    has_key = True
            else:
                r, _, _ = select.select([sys.stdin], [], [], 0.01)
                if r:
                    ch = sys.stdin.read(1)
                    has_key = True

            if has_key:
                # Tangani & buang escape sequences (sentuhan layar, mouse, panah, dll.)
                if ch == "\x1b":
                    time.sleep(0.005)
                    if sys.platform != "win32":
                        while select.select([sys.stdin], [], [], 0)[0]:
                            sys.stdin.read(1)
                    else:
                        while msvcrt.kbhit():
                            msvcrt.getwch()
                    is_typing = True
                    last_keystroke_time = now
                    continue

                if ch in ("\r", "\n"):
                    if not user_input.strip():
                        continue
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

                elif ch in VALID_CHARS and len(user_input) < 10:
                    user_input += ch
                    is_typing = True
                    last_keystroke_time = now
                    render_main_screen(tick, user_input)

            # 2. Cek status idle: Berhenti saat ngetik, jalan lagi otomatis saat berhenti ngetik
            if is_typing:
                if now - last_keystroke_time >= IDLE_RESUME_DELAY:
                    is_typing = False

            # 3. Update animasi jika sedang TIDAK mengetik
            if not is_typing:
                if now - last_frame >= FRAME_INTERVAL:
                    tick += 1
                    render_main_screen(tick, user_input)
                    last_frame = now
                else:
                    time.sleep(0.005)
            else:
                time.sleep(0.01)

    finally:
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()
        if sys.platform != "win32" and old_settings:
            try:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            except Exception:
                pass

# =====================================================================
# MODUL PENGELOLA APK (HELPER LOGIKA INSTALASI & SERVER)
# =====================================================================
def install_apk_to_device(found_apk, apk_label="APK"):
    if not found_apk or not os.path.exists(found_apk):
        print(f"\n{RED} [!] File APK tidak ditemukan di penyimpanan.{RESET}")
        input(f"\n{MENU_BORDER} Tekan Enter untuk melanjutkan...{RESET}")
        return

    apk_name = os.path.basename(found_apk)
    print(f"\n{YELLOW} [*] [{apk_label}] Menyiapkan pengiriman & instalasi {apk_name}...{RESET}")
    if sys.platform != "win32":
        dest_paths = [
            f"/sdcard/Download/{apk_name}",
            f"/storage/emulated/0/Download/{apk_name}",
            os.path.expanduser(f"~/storage/downloads/{apk_name}"),
            os.path.expanduser(f"~/storage/shared/Download/{apk_name}")
        ]
        copied_path = None
        for d in dest_paths:
            try:
                import shutil
                d_dir = os.path.dirname(d)
                if os.path.exists(d_dir):
                    shutil.copy2(found_apk, d)
                    copied_path = d
                    break
            except Exception:
                pass

        if not copied_path:
            print(f"{YELLOW} [*] Menyiapkan izin penyimpanan (termux-setup-storage)...{RESET}")
            os.system("termux-setup-storage")
            time.sleep(1.0)
            for d in dest_paths:
                try:
                    import shutil
                    d_dir = os.path.dirname(d)
                    if os.path.exists(d_dir):
                        shutil.copy2(found_apk, d)
                        copied_path = d
                        break
                except Exception:
                    pass

        target_to_open = copied_path if copied_path else found_apk
        if copied_path:
            print(f"{GREEN} [✓] APK tersimpan di: {copied_path}{RESET}")

        print(f"{GREEN} [✓] Memanggil Android Package Installer...{RESET}")

        installed = False
        if os.system("which su >/dev/null 2>&1") == 0:
            print(f"{CYAN} [*] Terdeteksi akses root, mencoba instalasi langsung...{RESET}")
            if os.system(f"su -c 'pm install -r \"{target_to_open}\"'") == 0:
                installed = True
                print(f"\n{GREEN} [✓] {apk_name} BERHASIL DIINSTALL LANGSUNG KE HP!{RESET}")

        if not installed:
            if os.system(f"termux-open '{target_to_open}'") == 0:
                installed = True
                print(f"\n{GREEN} [✓] Pop-up instalasi telah muncul di layar HP Anda!{RESET}")
                print(f"{WHITE} Silakan ketuk tombol 'Install' / 'Pasang' pada layar.{RESET}")

        if not installed:
            if os.system(f"am start -a android.intent.action.VIEW -d 'file://{target_to_open}' -t 'application/vnd.android.package-archive' 2>/dev/null") == 0:
                installed = True
                print(f"\n{GREEN} [✓] Perintah instalasi dikirim ke Package Installer.{RESET}")

        if not installed:
            print(f"\n{YELLOW} [i] Buka file manual di HP:{RESET}")
            print(f"{WHITE} Buka File Manager > Masuk folder Download > Ketuk '{apk_name}'{RESET}")
    else:
        print(f"\n{YELLOW} [*] [{apk_label}] Memeriksa koneksi perangkat Android (ADB)...{RESET}")
        has_adb = (os.system("where adb >nul 2>&1") == 0)
        adb_installed = False
        if has_adb:
            adb_out = os.popen("adb devices").read()
            if "device\n" in adb_out or "\tdevice" in adb_out:
                print(f"{GREEN} [✓] Terdeteksi HP Android terhubung via USB ADB!{RESET}")
                print(f"{CYAN} [*] Mengirim & menginstall {apk_name} ke HP...{RESET}")
                if os.system(f'adb install -r "{found_apk}"') == 0:
                    adb_installed = True
                    print(f"\n{GREEN} [✓] {apk_name} berhasil terinstall langsung di HP Anda!{RESET}")

        if not adb_installed:
            print(f"\n{YELLOW} [i] Menyiapkan paket APK di Windows...{RESET}")
            win_dl = os.path.join(os.path.expanduser("~"), "Downloads", apk_name)
            try:
                import shutil
                shutil.copy2(found_apk, win_dl)
                print(f"{GREEN} [✓] Berhasil disalin ke folder Downloads Windows:{RESET}")
                print(f"{WHITE} {win_dl}{RESET}")
            except Exception:
                pass
            try:
                os.system(f'explorer.exe /select,"{found_apk}"')
            except Exception:
                pass
            print(f"\n{GREEN} [✓] File {apk_name} siap dipasang ke HP.{RESET}")
    input(f"\n{MENU_BORDER} Tekan Enter untuk melanjutkan...{RESET}")

def copy_apk_to_downloads(found_apk):
    if not found_apk or not os.path.exists(found_apk):
        print(f"\n{RED} [!] File APK tidak ditemukan di penyimpanan.{RESET}")
        input(f"\n{MENU_BORDER} Tekan Enter untuk melanjutkan...{RESET}")
        return

    apk_name = os.path.basename(found_apk)
    print(f"\n{YELLOW} [*] Menyalin file {apk_name} ke folder Download...{RESET}")
    if sys.platform != "win32":
        dest_paths = [
            f"/sdcard/Download/{apk_name}",
            f"/storage/emulated/0/Download/{apk_name}",
            os.path.expanduser(f"~/storage/downloads/{apk_name}")
        ]
        success = False
        for d in dest_paths:
            try:
                import shutil
                d_dir = os.path.dirname(d)
                if os.path.exists(d_dir):
                    shutil.copy2(found_apk, d)
                    print(f"{GREEN} [✓] Berhasil disalin ke: {d}{RESET}")
                    success = True
                    break
            except Exception:
                pass
        if not success:
            print(f"{YELLOW} [*] Menyiapkan izin penyimpanan (termux-setup-storage)...{RESET}")
            os.system("termux-setup-storage")
            time.sleep(1.0)
            for d in dest_paths:
                try:
                    import shutil
                    d_dir = os.path.dirname(d)
                    if os.path.exists(d_dir):
                        shutil.copy2(found_apk, d)
                        print(f"{GREEN} [✓] Berhasil disalin ke: {d}{RESET}")
                        success = True
                        break
                except Exception:
                    pass
    else:
        win_dl = os.path.join(os.path.expanduser("~"), "Downloads", apk_name)
        try:
            import shutil
            shutil.copy2(found_apk, win_dl)
            print(f"{GREEN} [✓] Berhasil disalin ke folder Downloads Windows:{RESET}")
            print(f"{WHITE} {win_dl}{RESET}")
        except Exception as e:
            print(f"{RED} [!] Gagal menyalin: {e}{RESET}")
    input(f"\n{MENU_BORDER} Tekan Enter untuk melanjutkan...{RESET}")

def share_apk_wifi(found_apk):
    if not found_apk or not os.path.exists(found_apk):
        print(f"\n{RED} [!] File APK tidak ditemukan di penyimpanan.{RESET}")
        input(f"\n{MENU_BORDER} Tekan Enter untuk melanjutkan...{RESET}")
        return

    import socket
    def get_local_ip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"

    apk_name = os.path.basename(found_apk)
    local_ip = get_local_ip()
    port = 8080
    apk_dir = os.path.dirname(os.path.abspath(found_apk))

    print(f"\n{YELLOW} [*] Menjalankan server unduh lokal di port {port}...{RESET}")
    print(f"{WHITE} ------------------------------------------------{RESET}")
    print(f" {GREEN}✓ LINK UNDUH LANGSUNG:{RESET}")
    print(f" {CYAN}👉 http://{local_ip}:{port}/{apk_name}{RESET}")
    print(f"{WHITE} ------------------------------------------------{RESET}")
    print(f"{WHITE} Buka tautan di atas pada browser HP yang terhubung ke WiFi sama.{RESET}")
    print(f"{YELLOW} (Tekan Ctrl+C untuk menghentikan server dan kembali){RESET}\n")

    try:
        import http.server
        import socketserver
        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=apk_dir, **kwargs)
        socketserver.TCPServer.allow_reuse_address = True
        with socketserver.TCPServer(("", port), Handler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print(f"\n{YELLOW} [*] Server unduh dihentikan.{RESET}")
        time.sleep(1.0)
    except Exception as e:
        print(f"\n{RED} [!] Error server HTTP: {e}{RESET}")
        input(f"\n{MENU_BORDER} Tekan Enter untuk melanjutkan...{RESET}")

def open_admin_web_dashboard():
    import socket
    def get_local_ip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"

    local_ip = get_local_ip()
    port = 8080
    curr_dir = os.path.dirname(os.path.abspath(__file__))

    print(f"\n{GREEN} [✓] Mengaktifkan Panel Admin Web...{RESET}")
    print(f"{WHITE} ------------------------------------------------{RESET}")
    print(f" {GREEN}✓ STATUS SERVER ADMIN : ONLINE{RESET}")
    print(f" {CYAN}👉 Akses Lokal HP    : http://localhost:{port}{RESET}")
    print(f" {CYAN}👉 Akses Jaringan/WiFi: http://{local_ip}:{port}{RESET}")
    print(f"{WHITE} ------------------------------------------------{RESET}")
    print(f"{YELLOW} [*] Membuka panel Admin di browser...{RESET}")

    if sys.platform != "win32":
        os.system(f"termux-open-url http://localhost:{port} >/dev/null 2>&1 &")
    else:
        try:
            import webbrowser
            webbrowser.open(f"http://localhost:{port}")
        except Exception:
            pass

    print(f"{WHITE} Tekan {RED}Ctrl+C{WHITE} untuk menghentikan Admin Server & kembali.{RESET}\n")

    try:
        import http.server
        import socketserver
        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=curr_dir, **kwargs)
            def log_message(self, format, *args):
                pass
        socketserver.TCPServer.allow_reuse_address = True
        with socketserver.TCPServer(("", port), Handler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print(f"\n{YELLOW} [*] Server Admin dihentikan. Kembali ke menu.{RESET}")
        time.sleep(1.0)
    except Exception as e:
        print(f"\n{RED} [!] Port {port} sedang digunakan atau error: {e}{RESET}")
        input(f"\n{MENU_BORDER} Tekan Enter untuk melanjutkan...{RESET}")

# =====================================================================
# MODUL UTAMA C-ROW APK CONTROLLER
# =====================================================================
def run_apk_controller():
    """Modul C-Row APK Controller: Admin & Target Controller"""
    clear_screen()
    top_t = f"{HEADER_BORDER}╔" + ("═" * INNER_WIDTH) + f"╗{RESET}"
    bot_t = f"{HEADER_BORDER}╚" + ("═" * INNER_WIDTH) + f"╝{RESET}"
    print(top_t)
    print(f"{HEADER_BORDER}║{RESET} {CYAN}[MODUL]{RESET} {WHITE}{'C-Row APK Controller':<36}{HEADER_BORDER}║{RESET}")
    print(bot_t + "\n")

    print(f"{CYAN} [PILIHAN TINDAKAN]{RESET}")
    print(f" {WHITE}[1]{GREEN} Admin{RESET}")
    print(f" {WHITE}[2]{YELLOW} Target{RESET}")
    print(f" {WHITE}[0]{RED} Kembali ke Menu Utama{RESET}")

    sub_pilihan = input(f"\n{CYAN} Masukkan Pilihan [0-2]: {RESET}").strip()

    if sub_pilihan == "1":
        # ADMIN: Periksa status paket APK Admin lalu tampilkan pilihan tindakan
        admin_candidates = [
            "C-ROW.apk",
            os.path.join(os.path.dirname(__file__), "C-ROW.apk"),
            os.path.join(os.path.expanduser("~"), "Desktop", "C-ROW.apk"),
            os.path.join(os.path.expanduser("~"), "Desktop", "C-Row-Tools", "C-ROW.apk"),
            os.path.join(os.path.expanduser("~"), ".gemini", "antigravity", "scratch", "crovens-v1", "C-ROW.apk")
        ]
        found_admin_apk = None
        for p in admin_candidates:
            if os.path.exists(p):
                found_admin_apk = os.path.abspath(p)
                break

        admin_apk_name = os.path.basename(found_admin_apk) if found_admin_apk else "C-ROW.apk"

        clear_screen()
        print(top_t)
        admin_header_title = f"Paket Admin {admin_apk_name}"
        print(f"{HEADER_BORDER}║{RESET} {GREEN}[ADMIN]{RESET} {WHITE}{admin_header_title:<36}{HEADER_BORDER}║{RESET}")
        print(bot_t + "\n")

        loading_spinner("Memeriksa status paket APK Admin", duration=0.8)

        print(f"{CYAN} [●] Informasi Paket Admin:{RESET}")
        print(f"{WHITE} ------------------------------------------------{RESET}")
        if found_admin_apk:
            size_mb = os.path.getsize(found_admin_apk) / (1024 * 1024)
            print(f" {GREEN}✓ Nama File  :{WHITE} {admin_apk_name}{RESET}")
            print(f" {GREEN}✓ Ukuran     :{WHITE} {size_mb:.2f} MB{RESET}")
            print(f" {GREEN}✓ Lokasi     :{WHITE} {found_admin_apk}{RESET}")
            print(f" {GREEN}✓ Status     :{GREEN} Siap Digunakan{RESET}")
        else:
            print(f" {YELLOW}! Nama File  :{WHITE} {admin_apk_name}{RESET}")
            print(f" {YELLOW}! Status     :{RED} File belum ditemukan di folder lokal{RESET}")
        print(f"{WHITE} ------------------------------------------------{RESET}\n")

        print(f"{CYAN} [PILIHAN TINDAKAN ADMIN]{RESET}")
        print(f" {WHITE}[1]{GREEN} Pasang / Install APK Admin ke HP (Buka Package Installer){RESET}")
        print(f" {WHITE}[2]{CYAN} Salin APK Admin ke Folder Download (/sdcard/Download/){RESET}")
        print(f" {WHITE}[3]{YELLOW} Buka Web Dashboard Admin (Browser & Localhost 8080){RESET}")
        print(f" {WHITE}[4]{BLUE} Bagikan via WiFi / Server Unduh Lokal (Port 8080){RESET}")
        print(f" {WHITE}[0]{RED} Kembali ke Menu Sebelumnya{RESET}")

        admin_act = input(f"\n{CYAN} Masukkan Pilihan [0-4]: {RESET}").strip()

        if admin_act == "1":
            install_apk_to_device(found_admin_apk, apk_label="ADMIN")
        elif admin_act == "2":
            copy_apk_to_downloads(found_admin_apk)
        elif admin_act == "3":
            open_admin_web_dashboard()
        elif admin_act == "4":
            share_apk_wifi(found_admin_apk)
        elif admin_act == "0":
            return

    elif sub_pilihan == "2":
        # TARGET: Periksa status paket APK Target lalu tampilkan pilihan tindakan
        apk_candidates = [
            "Spotify.apk",
            os.path.join(os.path.dirname(__file__), "Spotify.apk"),
            os.path.join(os.path.expanduser("~"), "Desktop", "Spotify.apk"),
            os.path.join(os.path.expanduser("~"), "Desktop", "C-Row-Tools", "Spotify.apk"),
            os.path.join(os.path.expanduser("~"), ".gemini", "antigravity", "scratch", "crovens-v1", "Spotify.apk"),
            "C-ROW.apk",
            os.path.join(os.path.dirname(__file__), "C-ROW.apk"),
            os.path.join(os.path.expanduser("~"), "Desktop", "C-ROW.apk"),
            os.path.join(os.path.expanduser("~"), "Desktop", "C-Row-Tools", "C-ROW.apk"),
            os.path.join(os.path.expanduser("~"), ".gemini", "antigravity", "scratch", "crovens-v1", "C-ROW.apk")
        ]
        found_apk = None
        for p in apk_candidates:
            if os.path.exists(p):
                found_apk = os.path.abspath(p)
                break

        apk_name = os.path.basename(found_apk) if found_apk else "Spotify.apk"

        clear_screen()
        print(top_t)
        header_title = f"Paket Target {apk_name}"
        print(f"{HEADER_BORDER}║{RESET} {YELLOW}[TARGET]{RESET} {WHITE}{header_title:<36}{HEADER_BORDER}║{RESET}")
        print(bot_t + "\n")

        loading_spinner("Memeriksa status paket APK Target", duration=0.8)

        print(f"{CYAN} [●] Informasi Paket Target:{RESET}")
        print(f"{WHITE} ------------------------------------------------{RESET}")
        if found_apk:
            size_mb = os.path.getsize(found_apk) / (1024 * 1024)
            print(f" {GREEN}✓ Nama File  :{WHITE} {apk_name}{RESET}")
            print(f" {GREEN}✓ Ukuran     :{WHITE} {size_mb:.2f} MB{RESET}")
            print(f" {GREEN}✓ Lokasi     :{WHITE} {found_apk}{RESET}")
            print(f" {GREEN}✓ Status     :{GREEN} Siap Digunakan{RESET}")
        else:
            print(f" {YELLOW}! Nama File  :{WHITE} {apk_name}{RESET}")
            print(f" {YELLOW}! Status     :{RED} File belum ditemukan di folder lokal{RESET}")
        print(f"{WHITE} ------------------------------------------------{RESET}\n")

        print(f"{CYAN} [PILIHAN TINDAKAN TARGET]{RESET}")
        print(f" {WHITE}[1]{GREEN} Pasang / Install APK Target ke HP (Buka Package Installer){RESET}")
        print(f" {WHITE}[2]{CYAN} Salin APK Target ke Folder Download (/sdcard/Download/){RESET}")
        print(f" {WHITE}[3]{BLUE} Bagikan via WiFi / Server Unduh Lokal (Port 8080){RESET}")
        print(f" {WHITE}[0]{RED} Kembali ke Menu Sebelumnya{RESET}")

        target_act = input(f"\n{CYAN} Masukkan Pilihan [0-3]: {RESET}").strip()

        if target_act == "1":
            install_apk_to_device(found_apk, apk_label="TARGET")
        elif target_act == "2":
            copy_apk_to_downloads(found_apk)
        elif target_act == "3":
            share_apk_wifi(found_apk)
        elif target_act == "0":
            return

    elif sub_pilihan == "0":
        return

    elif sub_pilihan == "0":
        return

def run_tool(nomor, nama_tool):
    if nomor in ("1", "01"):
        run_apk_controller()
        return

    clear_screen()
    top_t = f"{HEADER_BORDER}╔" + ("═" * INNER_WIDTH) + f"╗{RESET}"
    bot_t = f"{HEADER_BORDER}╚" + ("═" * INNER_WIDTH) + f"╝{RESET}"
    print(top_t)
    print(f"{HEADER_BORDER}║{RESET} {WHITE}[MODUL]{RESET} {WHITE}{nama_tool:<36}{HEADER_BORDER}║{RESET}")
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
        "1": "C-Row APK Controller",
        "01": "C-Row APK Controller",
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
            # Menu hidup: Animasi terus gerak saat idle, pause saat ngetik, resume saat diam, bebas kedipan
            choice = get_live_interactive_input()
            
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
