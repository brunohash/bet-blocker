from enum import Enum
import tkinter as tk
from PIL import Image, ImageTk
from src.utils.get_paths import get_path_from_context


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
        self.app_window = tk.Tk()
        self.app_window.title = "Bloqueador de Apostas"
        self.app_window.geometry("410x460")
        self.app_window.configure(background=AppColors.CINZA_CLARO.value)
        self.app_window.resizable(width=False, height=False)
        self.app_frame_logo = tk.Frame(self.app_window, width=410, height=60, bg=AppColors.CINZA_CLARO.value, relief="flat")
        self.app_frame_logo.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.app_frame_body = tk.Frame(self.app_window, width=410, height=400, bg=AppColors.CINZA_CLARO.value, relief="flat")

        self.setup_frame_logo()


    def setup_frame_logo(self):
        logo = Image.open(get_path_from_context("assets/block.png"))
        logo.resize((40, 40))
        logo = ImageTk.PhotoImage(logo)
        app_label_img = tk.Label(self.app_frame_logo, height=60, image=logo,
                                      bg=AppColors.CINZA_CLARO.value)
        app_label_img.place(x=20, y=0)
        app_label_logo = tk.Label(self.app_frame_logo, text="Bloqueador de Apostas", height=1, anchor="ne",                               font=('Ivy', 20), bg=AppColors.CINZA_CLARO.value, fg=AppColors.PRETO.value)
        app_label_logo.place(x=70, y=12)
        app_label_line = tk.Label(self.app_frame_logo, text="Bloqueador de Apostas", height=1, width="445",
                                       anchor="nw", font=('Ivy', 1), bg=AppColors.VERDE.value)
        app_label_line.place(x=0, y=57)

    def setup_frame_body(self):
        blocklist = tk.Label(self.app_frame_body,
                             text="Lista de bets bloqueadas",
                             height=1, font=('Ivy', 12),
                             bg=AppColors.CINZA_CLARO.value, fg=AppColors.PRETO.value)

        def setup_app_logo(self):
            tk.Label(self.app_frame_logo,
                     height=60,
                     image=self.app_logo,
                     bg=AppColors.CINZA_CLARO.value,
                     text="Bloqueador de Apostas"
            self.app_label_logo.place(x=20, y=0)

        # blocklist_filepath = get_path_from_context("blocklist.txt")

def request_admin_grant() -> bool:
    """ # Função para solicitar permissão de administrador """
    if ctypes.windll.shell32.IsUserAnAdmin():
        return True
    else:
        # Se não for administrador, solicita permissão
        ctypes.windll.shell32.ShellExecuteW(None, "runas", os.sys.executable, " ".join(os.sys.argv), None, 1)
        return False


def blocklist_load():
    """Carrega a lista de sites bloqueados do arquivo blocklist.txt."""
    try:
        blocklist_file_path = get_path_from_context("blocklist.txt")
        with open(blocklist_file_path, "r") as file:
            sites = file.readlines()
            if not sites:
                messagebox.showinfo("Informação", "A lista de sites bloqueados está vazia.")
            else:
                for site in sites:
                    site = site.strip()  # Remove espaços em branco
                    if site:  # Adiciona apenas se não estiver vazio
                        lista.insert(tk.END, site)
    except FileNotFoundError:
        logger.error("Arquivo de blocklist não encontrado. Criando um novo arquivo.")
        with open(blocklist_file_path, "w") as file:
            file.write("")  # Cria um novo arquivo se não existir
        messagebox.showerror("Erro", "Arquivo de blocklist não encontrado. Um novo arquivo foi criado.")
        blocklist_load()

def domain_block(dominio: str) -> bool:
    """Adiciona uma entrada ao arquivo hosts para bloquear um domínio."""
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