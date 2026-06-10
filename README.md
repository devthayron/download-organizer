# Organizador de Downloads

Script Python que organiza automaticamente os arquivos da pasta `Downloads` em subpastas por categoria, com base em regras definidas em um arquivo de configuração.

---

## Funcionalidades

- Organiza arquivos da pasta `Downloads` em subpastas por categoria
- Configuração via arquivo `config.json`
- Trata duplicatas automaticamente
- Avisa no terminal quando um arquivo não tem regra definida

---

## Pré-requisitos

- Python 3.4+
- Biblioteca padrão (`pathlib`, `shutil`, `json`)

---

## Como usar


**1. Configure o `config.json`**

Edite as categorias e extensões conforme necessário:

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

> Mantenha o `config.json` fora da pasta Downloads para evitar que ele seja movido.

---

## Como funciona

As pastas de destino são criadas automaticamente se não existirem.

Arquivos ocultos e pastas dentro de Downloads são ignorados.

Se já existir um arquivo com o mesmo nome no destino, o novo arquivo é renomeado com sufixo numérico: `foto.jpg` vira `foto(1).jpg`.

Extensões que não correspondem a nenhuma regra são exibidas no terminal:

```
[SEM REGRA] arquivo.xyz
```

---
