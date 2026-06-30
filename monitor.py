import json
import logging
import threading
import time
from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from organizador import OrganizadorPastas
from logger import configurar_logger

logger = logging.getLogger(__name__)


def carregar_config(caminho_config="config.json"):
    """Carrega as configurações do arquivo JSON."""
    with open(caminho_config, encoding="utf-8") as arquivo:
        return json.load(arquivo)


class MonitorDownloads(FileSystemEventHandler):
    """
    Reage a eventos de criação/modificação na pasta Downloads.
    Para cada arquivo novo/alterado, dispara uma checagem de estabilidade
    de tamanho em background antes de mover (evita mover download incompleto).
    """

    def __init__(self, organizador: OrganizadorPastas, intervalo_estabilidade: float):
        self.organizador = organizador
        self.intervalo_estabilidade = intervalo_estabilidade
        # Evita disparar múltiplas threads de checagem para o mesmo arquivo
        self._em_checagem = set()
        self._lock = threading.Lock()

    def on_created(self, event):
        self._tratar_evento(event)

    def on_moved(self, event):
        # cobre o caso de downloads que terminam com rename (ex: .crdownload -> nome final)
        if not event.is_directory:
            caminho = Path(event.dest_path)
            self._agendar_checagem(caminho)

    def on_modified(self, event):
        self._tratar_evento(event)

    def _tratar_evento(self, event):
        if event.is_directory:
            return
        self._agendar_checagem(Path(event.src_path))

    def _agendar_checagem(self, arquivo: Path):
        if self.organizador.deve_ignorar(arquivo):
            return

        with self._lock:
            if arquivo in self._em_checagem:
                return
            self._em_checagem.add(arquivo)

        thread = threading.Thread(
            target=self._checar_estabilidade_e_mover,
            args=(arquivo,),
            daemon=True,
        )
        thread.start()

    def _formatar_tamanho(self, tamanho):
        unidades = ["B", "KB", "MB", "GB", "TB"]

        for unidade in unidades:
            if tamanho < 1024:
                return f"{tamanho:.1f} {unidade}"
            tamanho /= 1024

        return f"{tamanho:.1f} PB"

    def _checar_estabilidade_e_mover(self, arquivo: Path):
        try:
            tamanho_anterior = arquivo.stat().st_size
            download_detectado = False

            while True:
                time.sleep(self.intervalo_estabilidade)

                if not arquivo.exists():
                    return

                tamanho_atual = arquivo.stat().st_size

                if tamanho_atual == tamanho_anterior:
                    break
                
                if not download_detectado:
                    logger.info(f"Download em andamento: {arquivo.name}")
                    download_detectado = True

                tamanho_anterior = tamanho_atual

            if download_detectado:
                logger.info(
                    f"Download concluído: {arquivo.name} "
                    f"({self._formatar_tamanho(tamanho_atual)})"
                )

            if arquivo.exists():
                self.organizador.mover_arquivo(arquivo)
        finally:
            with self._lock:
                self._em_checagem.discard(arquivo)


def iniciar_watcher():
    configurar_logger()

    config = carregar_config()

    organizador = OrganizadorPastas(config)

    logger.info("Processando arquivos existentes...")
    organizador.organizar_downloads()

    intervalo = config.get("intervalo_estabilidade_segundos", 2)

    handler = MonitorDownloads(organizador, intervalo)

    observer = Observer()

    observer.schedule(handler, str(organizador.caminho_downloads), recursive=False)

    observer.start()

    logger.info(f"Watchdog iniciado. Monitorando: {organizador.caminho_downloads}")

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        logger.info("Encerrando watcher...")
        observer.stop()

    observer.join()