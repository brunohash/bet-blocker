from enum import Enum
import tkinter as tk
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
        blacklist_filepath = get_path_from_context("blacklist.txt")

def request_admin_grant() -> bool:
    """ # Função para solicitar permissão de administrador """
    if ctypes.windll.shell32.IsUserAnAdmin():
        return True
    else:
        # Se não for administrador, solicita permissão
        ctypes.windll.shell32.ShellExecuteW(None, "runas", os.sys.executable, " ".join(os.sys.argv), None, 1)
        return False


def blacklist_load():
    """Carrega a lista de sites bloqueados do arquivo blacklist.txt."""
    try:
        blacklist_file_path = get_path_from_context("blacklist.txt")
        with open(blacklist_file_path, "r") as file:
            sites = file.readlines()
            if not sites:
                messagebox.showinfo("Informação", "A lista de sites bloqueados está vazia.")
            else:
                for site in sites:
                    site = site.strip()  # Remove espaços em branco
                    if site:  # Adiciona apenas se não estiver vazio
                        lista.insert(tk.END, site)
    except FileNotFoundError:
        logger.error("Arquivo de blacklist não encontrado. Criando um novo arquivo.")
        with open(blacklist_file_path, "w") as file:
            file.write("")  # Cria um novo arquivo se não existir
        messagebox.showerror("Erro", "Arquivo de blacklist não encontrado. Um novo arquivo foi criado.")
        blacklist_load()

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