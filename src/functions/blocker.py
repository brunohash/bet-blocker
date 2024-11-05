import tkinter as tk
from tkinter import messagebox

from src.functions.firewall import firewall_block
from src.utils.logs import logger
from src.utils.get_paths import get_path_from_context


def restrict_sites(checkbox_var, lista, progresso, janela):
    """Bloqueia os sites listados na blocklist se o usuário concordar em participar da rede de apoio."""
    if not checkbox_var.get():
        messagebox.showwarning(
            "Aviso", "Você precisa concordar em participar da rede de apoio."
        )
        return

    try:
        blocklist_path = get_path_from_context(file_name="blocklist.txt")
        logger.info(f"Usando o seguinte arquivo de blocklist: {blocklist_path}")

        with open(blocklist_path, "r") as file:
            sites = file.readlines()
            if not sites:
                messagebox.showwarning(
                    "Aviso", "A lista de sites a serem bloqueados está vazia."
                )
                return

            total_sites = len(sites)
            for index, site in enumerate(sites):
                site = site.strip()  # Remove espaços em branco
                if site:  # Ignorar linhas vazias
                    if firewall_block(site):
                        lista.delete(
                            lista.get(0, tk.END).index(site)
                        )  # Remove o site da lista
                    else:
                        logger.warning(f"Não foi possível bloquear o site: {site}")

                # Atualiza a barra de progresso
                progresso["value"] = (index + 1) / total_sites * 100
                janela.update_idletasks()  # Atualiza a interface para mostrar a mudança

        messagebox.showinfo("Informação", "Sites bloqueados com sucesso.")
        progresso["value"] = (
            100  # Certifique-se de que a barra de progresso vá até o final
        )

    except Exception as e:
        # Loga o erro e mostra uma mensagem para o usuário
        logger.error(f"Erro ao bloquear os sites: {e}")
        messagebox.showerror("Erro", f"Não foi possível bloquear os sites: {e}")
