import os
from src.utils.logs import logger

def DEPRECATED_is_exists_firewall_rule(dominio):
    try:
        rule_name = f"Bloqueio de {dominio}"
        output = os.popen(
            'netsh advfirewall firewall show rule name="{}"'.format(rule_name)
        ).read()
        return rule_name in output
    except Exception as e:
        logger.error(f"Erro ao verificar regra: {e}")
        return False


def DEPRECATED_domain_block(dominio: str) -> bool:
    try:
        if DEPRECATED_is_exists_firewall_rule(dominio):
            logger.info(f"O domínio {dominio} já está bloqueado.")
            return True

        with open(r"C:\Windows\System32\drivers\etc\hosts", "a") as hosts_file:
            hosts_file.write(f"0.0.0.0 {dominio}\n")

        logger.info(f"Domínio {dominio} bloqueado com sucesso.")
        return True
    except Exception as e:
        logger.error(f"Falha ao bloquear {dominio} no arquivo hosts: {e}")
        return False
