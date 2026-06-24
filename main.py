import argparse
import json

from organizador import OrganizadorPastas


def carregar_config(caminho_config="config.json"):
    """Carrega as configurações do arquivo JSON."""
    with open(caminho_config, encoding="utf-8") as arquivo:
        return json.load(arquivo)


def organizar():
    """Executa a organização dos downloads."""
    config = carregar_config()

    organizador = OrganizadorPastas(config)
    organizador.organizar_downloads()

    print("✓ Downloads organizados com sucesso!")


def desfazer():
    """Restaura os arquivos organizados para a pasta Downloads."""
    config = carregar_config()

    organizador = OrganizadorPastas(config)
    organizador.desfazer_organizacao()

    print("✓ Organização desfeita!")


def main():
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
        print("Erro: arquivo 'config.json' não encontrado.")


if __name__ == "__main__":
    main()