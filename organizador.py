from pathlib import Path
import shutil
import logging

logger = logging.getLogger(__name__)


class OrganizadorPastas:
    """
    Organiza arquivos da pasta Downloads de acordo com as regras definidas
    na configuração. Usado pelo watcher para mover arquivos individuais
    assim que eles são considerados estáveis (prontos para mover).

    args
    caminho_downloads (Path, optional): Caminho da pasta Downloads.
    config (dict): Dicionário contendo as regras de organização.
    """

    def __init__(self, config, caminho_downloads=None):
        self.regras = config.get("regras")

        if not isinstance(self.regras, dict) or not self.regras:
            raise ValueError("Config inválida: 'regras' deve ser um dict não vazio")

        self.ignorar_extensoes = {
            ext.lower().lstrip(".") for ext in config.get("ignorar_extensoes", [])
        }

        self.caminho_downloads = caminho_downloads or Path.home() / "Downloads"
        if not self.caminho_downloads.exists():
            raise FileNotFoundError(f"Pasta não encontrada: {self.caminho_downloads}")

        self.mapa_extensoes = self._mapear_extensoes()
        self._criar_pastas()

    def _mapear_extensoes(self):
        """
        Converte as regras da configuração em um dicionário {extensão: pasta}
        ex. {"pdf": "Documentos", "jpg": "Imagens"}
        """
        mapa = {}
        for pasta, extensoes in self.regras.items():
            for extensao in extensoes:
                mapa[extensao.lower()] = pasta
        return mapa

    def _criar_pastas(self):
        """
        Cria as pastas de destino definidas na configuração, caso não existam.
        """
        for pasta in self.regras:
            caminho_pasta = self.caminho_downloads / pasta
            if not caminho_pasta.exists():
                logger.info(f"Criando a pasta: {pasta}")
                caminho_pasta.mkdir(exist_ok=True, parents=True)

    def _obter_extensao(self, arquivo):
        """
        Retorna a extensão do arquivo sem o ponto e em minúsculas.
        """
        return arquivo.suffix.lower().lstrip(".")

    def deve_ignorar(self, arquivo: Path) -> bool:
        """
        Decide se um arquivo deve ser ignorado por completo (nunca movido):
        - diretórios
        - arquivos ocultos (começam com '.')
        - extensões de arquivo temporário (tmp, crdownload, part, etc.)
        - arquivos de bloqueio temporário do Office (prefixo '~$')
        """
        if arquivo.is_dir():
            return True
        if arquivo.name.startswith("."):
            return True
        if arquivo.name.startswith("~$"):
            return True
        if self._obter_extensao(arquivo) in self.ignorar_extensoes:
            return True
        return False

    def _gerar_destino_unico(self, destino_base):
        """
        Verifica se o arquivo já existe e gera um caminho único para evitar
        sobrescrever arquivos existentes.
        ex. "arquivo.txt" já existe -> "arquivo(1).txt", "arquivo(2).txt", etc.
        """
        destino = destino_base
        i = 1
        while destino.exists():
            destino = destino_base.with_stem(f"{destino_base.stem}({i})")
            i += 1
        if i > 1:
            logger.warning(f"Duplicata detectada. Renomeando para: {destino.name}")
        return destino

    def mover_arquivo(self, arquivo: Path):
        """
        Move um único arquivo para a pasta correspondente.
        Arquivos sem regra definida são movidos para a pasta 'Outros'.
        """
        extensao = self._obter_extensao(arquivo)
        pasta = self.mapa_extensoes.get(extensao)

        if pasta is None:
            pasta = "Outros"
            logger.warning(f"Extensão sem regra definida: {arquivo.name}")

        destino_base = self.caminho_downloads / pasta / arquivo.name
        destino = self._gerar_destino_unico(destino_base)

        logger.info(f"Movendo {arquivo.name} → {destino.parent.name}/{destino.name}")
        shutil.move(arquivo, destino)

        return pasta
    
    def organizar_downloads(self):
        """
        Percorre a pasta Downloads e processa todos os arquivos existentes.
        """

        movidos = 0
        outros = 0

        for arquivo in self.caminho_downloads.iterdir():

            if self.deve_ignorar(arquivo):
                continue
            
            pasta = self.mover_arquivo(arquivo)
            if pasta == 'Outros':
                Outros += 1
            else:
                movidos += 1

        logger.info(
            f"Organização concluída! {movidos} arquivos movidos, {outros} para Outros."
        )