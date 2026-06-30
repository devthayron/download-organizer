import logging
import sys

from monitor import iniciar_watcher

logger = logging.getLogger(__name__)


def main():
    try:
        iniciar_watcher()
    except FileNotFoundError as erro:
        logger.error(f"Erro de configuração: {erro}")
        sys.exit(1)
    except Exception as erro:
        logger.exception(f"Erro inesperado: {erro}")
        sys.exit(1)


if __name__ == "__main__":
    main()