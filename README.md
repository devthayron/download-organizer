# Organizador de Downloads

Ferramenta em Python para automação da organização da pasta Downloads, movendo arquivos para subpastas por categoria com base em regras definidas em um arquivo JSON de configuração.

---

## Funcionalidades

* Move arquivos da pasta Downloads para subpastas por extensão
* Suporte a regras configuráveis via arquivo JSON
* Cria pastas automaticamente quando necessário
* Trata arquivos duplicados sem sobrescrever
* Ignora pastas e arquivos ocultos
* Ignora arquivos sem regra definida durante a organização
* Restaura arquivos organizados de volta para a pasta Downloads
* Sistema de logging para monitoramento das operações (terminal + arquivo)

---

## Pré-requisitos

* Python 3.9 ou superior
* Apenas bibliotecas da biblioteca padrão do Python

---

## Instalação

Clone o repositório:

```bash
git clone https://github.com/devthayron/download-organizer.git
cd download-organizer
```

---

## Configuração

Edite o arquivo `config.json` conforme suas necessidades:

```json
{
    "regras": {
        "Imagens": ["jpg", "jpeg", "png", "gif", "webp", "svg"],
        "Videos": ["mp4", "mkv", "avi", "mov", "webm"],
        "Documentos": ["pdf", "docx", "doc", "txt", "odt"],
        "Planilhas": ["xls", "xlsx", "csv", "ods"],
        "Apresentacoes": ["ppt", "pptx", "odp"],
        "Compactados": ["zip", "rar", "7z", "tar", "gz"],
        "Configuracao": ["cfg", "json", "yaml", "yml", "ini"]
    }
}
```

> Recomenda-se manter o arquivo `config.json` fora da pasta `Downloads` para evitar movimentações acidentais.

---

## Uso

Organizar os arquivos:

```bash
python main.py
```

ou

```bash
python main.py organizar
```

Restaurar os arquivos para a pasta Downloads:

```bash
python main.py desfazer
```

---

## Exemplo

Antes:

```text
Downloads/
├── foto.jpg
├── planilha.xlsx
├── documento.pdf
├── video.mp4
```

Após executar:

```bash
python main.py
```

Resultado:

```text
Downloads/
├── Imagens/
│   └── foto.jpg
├── Planilhas/
│   └── planilha.xlsx
├── Documentos/
│   └── documento.pdf
└── Videos/
    └── video.mp4
```

---

## Como funciona

* As pastas de destino são criadas automaticamente caso não existam.
* Arquivos ocultos e diretórios são ignorados.
* Arquivos com extensões não cadastradas permanecem no local original.
* Extensões sem regra definida são exibidas no terminal:

```text
Arquivo ignorado (sem regra definida): arquivo.xyz
```

## Tratamento de duplicatas

Caso já exista um arquivo com o mesmo nome no destino, um sufixo numérico é adicionado automaticamente:

```text
foto.jpg
foto(1).jpg
foto(2).jpg
```

---

## Estrutura do Projeto

```text
organizador-downloads/
├── main.py
├── organizador.py
├── config.json
└── README.md
```

---

## Autor

**Thayron Higlânder**

LinkedIn: https://www.linkedin.com/in/thayron-higlander
