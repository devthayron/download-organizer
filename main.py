import argparse
import json
import logging
from organizador import OrganizadorPastas
from logger import configurar_logger


logger = logging.getLogger(__name__)

def carregar_config(caminho_config="config.json"):
    """Carrega as configurações do arquivo JSON."""
    with open(caminho_config, encoding="utf-8") as arquivo:
        return json.load(arquivo)


def organizar():
    """Executa a organização dos downloads."""
    config = carregar_config()

    organizador = OrganizadorPastas(config)
    organizador.organizar_downloads()


def desfazer():
    """Restaura os arquivos organizados para a pasta Downloads."""
    config = carregar_config()

    organizador = OrganizadorPastas(config)
    organizador.desfazer_organizacao()


def main(): 
    configurar_logger()
    parser = argparse.ArgumentParser(
        description="Organizador de Downloads"
    )

    parser.add_argument(
        "comando",
        nargs="?",
        default="organizar",
        choices=["organizar", "desfazer"],
        help="Comando a ser executado",
    )

    args = parser.parse_args()

    try:
        if args.comando == "organizar":
            organizar()
        else:
            desfazer()

    except FileNotFoundError:
        logger.error("Arquivo 'config.json' não encontrado.")


if __name__ == "__main__":
    main()