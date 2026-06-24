import shutil
from pathlib import Path


class OrganizadorPastas:
    """
    Organiza arquivos da pasta Downloads de acordo com as regras definidas
    na configuração.

    args 
    caminho_downloads (Path, optional): Caminho da pasta Downloads. Se não fornecido, será usado o diretório padrão do usuário.
    config (dict): Dicionário contendo as regras de organização.
    """

    def __init__(self, config, caminho_downloads=None):
        self.regras = config["regras"]
        self.caminho_downloads = caminho_downloads or Path.home() / "Downloads"
        self.mapa_extensoes = self._mapear_extensoes()

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
            (self.caminho_downloads / pasta).mkdir(exist_ok=True, parents=True)

    def _ignorar_arquivo(self, arquivo):
        """
        Ignora diretórios e arquivos ocultos.
        """
        return arquivo.is_dir() or arquivo.name.startswith(".")

    def _obter_extensao(self, arquivo):
        """
        Retorna a extensão do arquivo sem o ponto e em minúsculas.
        """
        return arquivo.suffix.lower().lstrip(".")

    def _gerar_destino_unico(self, destino_base):
        """
        Verifica se o arquivo já existe e gera um caminho único para evitar sobrescrever arquivos existentes.
        ex. se "arquivo.txt" já existe, ele será renomeado para "arquivo(1).txt", "arquivo(2).txt", etc.
        """
        destino = destino_base
        i = 1

        while destino.exists():
            destino = destino_base.with_stem(f"{destino_base.stem}({i})")
            i += 1

        return destino

    def _mover_arquivo(self, arquivo, pasta_destino):
        destino_base = self.caminho_downloads / pasta_destino / arquivo.name
        destino = self._gerar_destino_unico(destino_base)

        shutil.move(arquivo, destino)

    def organizar_downloads(self):
        """
        Percorre a pasta de downloads e move os arquivos para as pastas
        correspondentes conforme as regras configuradas.
        """
        self._criar_pastas()

        for arquivo in self.caminho_downloads.iterdir():
            if self._ignorar_arquivo(arquivo):
                continue

            extensao = self._obter_extensao(arquivo)

            pasta = self.mapa_extensoes.get(extensao)

            if pasta:
                self._mover_arquivo(arquivo, pasta)
            else:
                print(f"Arquivo ignorado (sem regra definida): {arquivo.name}")
    def desfazer_organizacao(self):
        """
        Move os arquivos de volta para a pasta Downloads e remove as pastas criadas.
        """
        for pasta in self.regras:
            caminho = self.caminho_downloads / pasta

            if not caminho.exists():
                continue

            for arquivo in caminho.iterdir():
                destino_base = self.caminho_downloads / arquivo.name
                destino = self._gerar_destino_unico(destino_base)

                shutil.move(arquivo, destino)

            caminho.rmdir()
