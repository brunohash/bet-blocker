import os
import tkinter as tk

from PIL import Image, ImageTk
from tkinter import BooleanVar
from tkinter import ttk

import ctypes
import shutil

from src.functions.blocker import bloquear_sites
from src.utils.logs import logger
from src.utils.get_paths import get_path_from_context

# Cores da interface
co0 = "#f0f3f5" # Cinza claro
co1 = "#feffff" # Branco
co2 = "#3fb5a3" # Verde
co3 = "#f25f5c" # Vermelho
co4 = "#403d3d" # Preto

azul_color = "#3f9dfb"  # Azul para o botão
green_color = "#3fb5a3"  # Verde para o botão
white_color = "#ffffff"  # Branco para a fonte
orange_color = "orange"  # Laranja para o botão

# Configuração da janela principal
janela = tk.Tk()
janela.title("Bloqueador de Apostas")
janela.geometry("410x460")  # Aumente a altura da janela para a barra de progresso
janela.configure(background=co1)
janela.resizable(width=False, height=False)

# Caminho do arquivo de blacklist
CURRENT_FOLDER = get_path_from_context()











def is_exists_firewall_rule(dominio) -> bool:
    """Verifica se a regra de bloqueio já existe no firewall."""
    try:
        rule_name = f'Bloqueio de {dominio}'
        output = os.popen('netsh advfirewall firewall show rule name="{}"'.format(rule_name)).read()
        return rule_name in output
    except Exception as e:
        logger.error(f"Erro ao verificar regra: {e}")
        return False


# Frames
frame_logo = tk.Frame(janela, width=410, height=60, bg=co1, relief="flat")
frame_logo.grid(row=0, column=0, columnspan=2, sticky="nsew")

frame_corpo = tk.Frame(janela, width=410, height=400, bg=co1, relief="flat")
frame_corpo.grid(row=1, column=0, columnspan=2, sticky="nsew")

# Configurando frame logo
imagem = Image.open(os.path.join(CURRENT_FOLDER, "assets/block.png"))
imagem = imagem.resize((40, 40))
image = ImageTk.PhotoImage(imagem)

l_image = tk.Label(frame_logo, height=60, image=image, bg=co1)
l_image.place(x=20, y=0)

l_logo = tk.Label(frame_logo, text="Bloqueador de Apostas", height=1, anchor="ne", font=('Ivy', 20), bg=co1, fg=co4)
l_logo.place(x=70, y=12)

l_linha = tk.Label(
    frame_logo,
    text="Bloqueador de Apostas",
    height=1,
    width="445",
    anchor="nw",
    font=('Ivy', 1),
    bg=co2
)
l_linha.place(x=0, y=57)

# Configurando frame corpo font negrito
l_blacklist = tk.Label(
    frame_corpo,
    text="Lista de bets bloqueadas",
    height=1, font=('Ivy', 12),
    bg=co1,
    fg=co4,
    anchor="w",
    justify="left",
    wraplength=380
)
l_blacklist.place(x=18, y=20)

# Lista de sites bloqueados
lista = tk.Listbox(
    frame_corpo, width=40, height=14, bg=co0, fg=co4
)
lista.place(x=20, y=50)

# Barra de Progresso
progresso = ttk.Progressbar(
    frame_corpo, orient="horizontal", length=360, mode="determinate"
)
progresso.place(x=20, y=330)

# Checkbox para concordar em participar da rede de apoio
checkbox_var = BooleanVar()
checkbox = tk.Checkbutton(
    frame_corpo,
    text="Ao clicar em 'Bloquear Sites', você concorda em comunicar a sua rede de apoio possíveis situações de jogo compulsivo.",
    variable=checkbox_var,
    bg=co1,
    fg=co4,
    font=('Ivy', 8),
    wraplength=380,
    anchor="w",
    justify="left"
)
checkbox.place(x=16, y=290)

# Botão de bloquear site
b_bloquear = tk.Button(
    frame_corpo, text="Bloquear Firewall", width=15, height=2,
    bg=green_color, fg=white_color, command=lambda: bloquear_sites(checkbox_var, lista, progresso, janela), relief="flat"
)
b_bloquear.place(x=270, y=50)

# Chame a função copiar_hosts em algum lugar do seu código, como em um botão
botao_copiar_hosts = tk.Button(
    frame_corpo, text="Bloquear DNS", width=15, height=2,
    bg=azul_color, fg=white_color, command=hosts_file_copy, relief="flat"
)
botao_copiar_hosts.place(x=270, y=100)

# Chame a função copiar_hosts em algum lugar do seu código, como em um botão
botao_apoio = tk.Button(
    frame_corpo, text="Configurações", width=15, height=2,
    bg=orange_color, fg=white_color, relief="flat"
)
botao_apoio.place(x=270, y=150)

# Carregar a blacklist na inicialização
blacklist_load()

# Iniciar o loop da interface
janela.mainloop()
