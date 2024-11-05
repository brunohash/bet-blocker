import os
import ctypes
import shutil
from enum import Enum

import tkinter as tk
from tkinter import BooleanVar, ttk, messagebox
from PIL import Image, ImageTk

from src.utils.get_paths import get_path_from_context
from src.functions.blocker import restrict_sites
from src.utils.logs import logger


class AppColors(Enum):
    CINZA_CLARO = "#f0f3f5"
    BRANCO = "#feffff"
    VERDE = "#3fb5a3"
    VERMELHO = "#f25f5c"
    PRETO = "#403d3d"


class AppButtonColors(Enum):
    AZUL = "#3f9dfb"
    VERDE = "#3fb5a3"
    BRANCO = "#ffffff"
    LARANJA = "orange"


class AppInitializer:
    def __init__(self):
        # Setup main app window
        self.app_window = tk.Tk()
        self.app_window.title(
            "Bloqueador de Apostas"
        )  # Corrigido para setar o título corretamente
        self.app_window.geometry("410x460")
        self.app_window.configure(background=AppColors.CINZA_CLARO.value)
        self.app_window.resizable(width=False, height=False)

        # Setup frames
        self.setup_frames()

        # Setup components
        self.setup_frame_logo()
        self.setup_frame_body()

    def setup_frames(self):
        # Logo Frame
        self.app_frame_logo = tk.Frame(
            self.app_window,
            width=410,
            height=60,
            bg=AppColors.CINZA_CLARO.value,
            relief="flat",
        )
        self.app_frame_logo.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # Body Frame
        self.blocklist_path = self.get_or_create_blocklist_path()
        self.app_frame_body = tk.Frame(
            self.app_window,
            width=410,
            height=400,
            bg=AppColors.CINZA_CLARO.value,
            relief="flat",
        )
        self.app_frame_body.grid(row=1, column=0, columnspan=2, sticky="nsew")

    def run(self):
        self.app_window.mainloop()
        logger.info("Aplicação encerrada.")

    def get_or_create_blocklist_path(self):
        file_path = get_path_from_context("blocklist.txt")

        if not os.path.exists(file_path):
            with open(file_path, "w") as file:
                file.write("")

        return file_path

    def setup_frame_logo(self):
        # Logo image
        logo = Image.open(get_path_from_context("assets/block.png")).resize((40, 40))
        self.logo_image = ImageTk.PhotoImage(
            logo
        )  # Guarda a imagem como atributo da classe

        app_label_img = tk.Label(
            self.app_frame_logo,
            height=60,
            image=self.logo_image,
            bg=AppColors.CINZA_CLARO.value,
        )
        app_label_img.place(x=20, y=0)

        # Logo text
        app_label_logo = tk.Label(
            self.app_frame_logo,
            text="Bloqueador de Apostas",
            height=1,
            anchor="ne",
            font=("Ivy", 20),
            bg=AppColors.CINZA_CLARO.value,
            fg=AppColors.PRETO.value,
        )
        app_label_logo.place(x=70, y=12)

        # Divider line
        app_label_line = tk.Label(
            self.app_frame_logo,
            height=1,
            width="445",
            anchor="nw",
            font=("Ivy", 1),
            bg=AppColors.VERDE.value,
        )
        app_label_line.place(x=0, y=57)

    def setup_frame_body(self):
        # Blocklist label
        blocklist = tk.Label(
            self.app_frame_body,
            text="Lista de bets bloqueadas",
            height=1,
            font=("Ivy", 12),
            bg=AppColors.CINZA_CLARO.value,
            fg=AppColors.PRETO.value,
        )
        blocklist.place(x=18, y=20)

        # Blocklist listbox
        lstbox_blocklist = tk.Listbox(
            self.app_frame_body,
            width=40,
            height=14,
            bg=AppColors.BRANCO.value,
            fg=AppColors.PRETO.value,
        )
        lstbox_blocklist.place(x=20, y=50)
        lstbox_blocklist.insert(tk.END, *self.get_sites_from_blocklist())

        # Progress bar
        progress_bar = ttk.Progressbar(
            self.app_frame_body, orient="horizontal", length=360, mode="determinate"
        )
        progress_bar.place(x=20, y=330)

        # Checkbox for agreement
        _chk_choice = BooleanVar()
        check_box = tk.Checkbutton(
            self.app_frame_body,
            text="Ao clicar em 'Bloquear Sites', você concorda em comunicar a sua rede de apoio possíveis situações de jogo compulsivo.",
            variable=_chk_choice,
            bg=AppColors.BRANCO.value,
            fg=AppColors.PRETO.value,
            font=("Ivy", 8),
            wraplength=380,
            anchor="w",
            justify="left",
        )
        check_box.place(x=20, y=370)

        # Buttons
        block_button = tk.Button(
            self.app_frame_body,
            text="Bloquear Firewall",
            width=15,
            height=2,
            bg=AppColors.VERDE.value,
            fg=AppColors.BRANCO.value,
            command=lambda: restrict_sites(
                _chk_choice, lstbox_blocklist, progress_bar, self.app_window
            ),
            relief="flat",
        )
        block_button.place(x=270, y=100)

        copy_hosts_button = tk.Button(
            self.app_frame_body,
            text="Bloquear DNS",
            width=15,
            height=2,
            bg=AppButtonColors.AZUL.value,
            fg=AppColors.BRANCO.value,
            command=copy_hosts,
            relief="flat",
        )
        copy_hosts_button.place(
            x=270, y=150
        )  # Mantém a posição correta para evitar sobreposição

        support_button = tk.Button(
            self.app_frame_body,
            text="Configurações",
            width=15,
            height=2,
            bg=AppButtonColors.LARANJA.value,
            fg=AppColors.BRANCO.value,
            relief="flat",
        )
        support_button.place(x=270, y=200)  # Ajustado para evitar sobreposição

    def get_sites_from_blocklist(self) -> list:
        with open(self.blocklist_path, "r") as file:
            sites = file.readlines()
        return [site.strip() for site in sites if site.strip()]


## Auxiliares
def solicitar_permissao():
    if ctypes.windll.shell32.IsUserAnAdmin():
        return True
    else:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", os.sys.executable, " ".join(os.sys.argv), None, 1
        )
        return False


def copy_hosts():
    """Copia o arquivo ./hosts para C:\Windows\System32\drivers\etc\hosts."""
    if solicitar_permissao():
        try:
            origem = get_path_from_context("hosts")
            destino = r"C:\Windows\System32\drivers\etc\hosts"
            shutil.copyfile(origem, destino)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao copiar o arquivo hosts: {e}")
            logger.error(f"Erro ao copiar o arquivo hosts: {e}")


def request_admin_grant() -> bool:
    if ctypes.windll.shell32.IsUserAnAdmin():
        return True
    else:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", os.sys.executable, " ".join(os.sys.argv), None, 1
        )
        return False


def is_exists_firewall_rule(dominio):
    try:
        rule_name = f"Bloqueio de {dominio}"
        output = os.popen(
            'netsh advfirewall firewall show rule name="{}"'.format(rule_name)
        ).read()
        return rule_name in output
    except Exception as e:
        logger.error(f"Erro ao verificar regra: {e}")
        return False


def domain_block(dominio: str) -> bool:
    try:
        if is_exists_firewall_rule(dominio):
            logger.info(f"O domínio {dominio} já está bloqueado.")
            return True

        with open(r"C:\Windows\System32\drivers\etc\hosts", "a") as hosts_file:
            hosts_file.write(f"0.0.0.0 {dominio}\n")

        logger.info(f"Domínio {dominio} bloqueado com sucesso.")
        return True
    except Exception as e:
        logger.error(f"Falha ao bloquear {dominio} no arquivo hosts: {e}")
        return False
