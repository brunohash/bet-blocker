from enum import Enum
import tkinter as tk, BooleanVar, ttk
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

        self.setup_app_logo()
        self.setup_frame_logo()
        self.setup_frame_body()

        blocklist_load()

        self.app_window.mainloop()


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
                             bg=AppColors.CINZA_CLARO.value,
                             fg=AppColors.PRETO.value)
        blocklist.place(x=18, y=20)

        lstbox_blocklist = tk.Listbox(self.app_frame_body, width=40, height=14, bg=AppColors.BRANCO.value, fg=AppColors.PRETO.value)
        lstbox_blocklist.place(x=20, y=50)

        progress_bar = tk.ttk.Progressbar(self.app_frame_body,
                                          orient="horizontal",
                                          length=360, mode="determinate")

        progress_bar.place(x=20, y=330)

        _chk_choice = BooleanVar()
        check_box = tk.Checkbutton(self.app_frame_body,
                                       text="Ao clicar em 'Bloquear Sites', você concorda em comunicar a sua rede de apoio possíveis situações de jogo compulsivo.",
                                        variable=_chk_choice,
                                        bg=AppColors.BRANCO.value,
                                        fg=AppColors.PRETO.value,
                                        font=('Ivy', 8),
                                        wraplength=380,
                                        anchor="w",
                                        justify="left")
        check_box.place(x=20, y=370)

        block_button =  tk.Button(
                            self.app_frame_body, text="Bloquear Firewall", width=15, height=2,
                            bg=AppColors.VERDE.value,
                            fg=AppColors.BRANCO.value,
                            command=lambda: bloquear_sites(checkbox_var, lista, progresso, janela), relief="flat")

        block_button.place(x=270, y=100)

        copy_hosts_button = tk.Button(
                        self.app_frame_body, text="Bloquear DNS", width=15, height=2,
                        bg=AppColors.AZUL.value,
                        fg=AppColors.BRANCO.value,
                        command=copy_hosts, relief="flat")

        copy_hosts_button.place(x=270, y=150)


        support_button = tk.Button(
                    self.app_frame_body, text="Configurações", width=15, height=2,
                    bg=AppButtonColors.LARANJA.value,
                    fg=AppColors.BRANCO.value,
                    relief="flat")

        support_button.place(x=270, y=150)



    def setup_app_logo(self):

        img =  Image.open(get_path_from_context("assets/block.png"))
        img.resize((40, 40))
        img_tk = ImageTk.PhotoImage(img)

        tk.Label(self.app_frame_logo,
                    height=60,
                    image=img_tk,
                    bg=AppColors.CINZA_CLARO.value,
                    text="Bloqueador de Apostas")
        self.app_label_logo.place(x=20, y=0)



## Auxiliares
def solicitar_permissao():
    if ctypes.windll.shell32.IsUserAnAdmin():
        return True
    else:
        # Se não for administrador, solicita permissão
        ctypes.windll.shell32.ShellExecuteW(None, "runas", os.sys.executable, " ".join(os.sys.argv), None, 1)
        return False

def copy_hosts():
    """Copia o arquivo ./hosts para C:\Windows\System32\drivers\etc\hosts."""
    if solicitar_permissao():
        try:
            # Caminho do arquivo de origem e destino
            origem = os.path.join(diretorio_atual, "hosts")
            destino = r"C:\Windows\System32\drivers\etc\hosts"

            # Copiando o arquivo
            shutil.copyfile(origem, destino)
            messagebox.showinfo("Sucesso", "Arquivo hosts copiado com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao copiar o arquivo hosts: {e}")
            logging.error(f"Erro ao copiar o arquivo hosts: {e}")

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