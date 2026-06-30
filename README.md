# Organizador de Downloads (Tempo Real)

Sistema de automação em Python baseado em eventos que organiza automaticamente a pasta Downloads em tempo real.

Arquivos são detectados e movidos automaticamente para suas categorias assim que o download é concluído.

O sistema mantém a pasta Downloads continuamente organizada sem intervenção manual.

---

## Problema que resolve

A pasta Downloads tende a se tornar desorganizada com o tempo, dificultando a localização de arquivos.

Este sistema automatiza a organização contínua da pasta, cobrindo tanto arquivos existentes quanto novos downloads.

---

## Funcionamento do sistema

O sistema opera em dois fluxos:

* Processamento inicial da pasta Downloads (arquivos já existentes)
* Monitoramento contínuo para novos arquivos em tempo real

### Camada de estabilidade de arquivos

Antes de mover qualquer arquivo, o sistema valida se o download foi concluído de fato, monitorando a estabilidade do tamanho do arquivo ao longo do tempo.

Arquivos só são processados quando não há mais alterações no seu tamanho, evitando movimentação prematura durante downloads em andamento.

A arquitetura interna é dividida em três etapas:

#### 1. Leitura inicial

Escaneia e processa todos os arquivos existentes na pasta Downloads.

#### 2. Motor de organização

Classifica arquivos por extensão e define o destino correto.

#### 3. Monitoramento em tempo real

Detecta novos arquivos via eventos do sistema (watchdog) e os processa automaticamente.

---

## Regras de organização

* Arquivos com extensão conhecida são movidos para suas categorias
* Arquivos sem extensão ou não mapeados vão para `Outros`
* Diretórios são ignorados automaticamente

---

## Funcionalidades

* Organização automática por extensão
* Processamento inicial da pasta Downloads
* Monitoramento contínuo em tempo real
* Criação automática de pastas
* Tratamento de duplicatas
* Pasta fallback "Outros"
* Configuração via `config.json`
* Sistema de logs para rastreabilidade

---

## Logs do sistema

Exemplos de eventos:

```text
30-06-2026 14:24:50 | INFO | monitor | Processando arquivos existentes...
30-06-2026 14:24:50 | INFO | organizador | Movendo arquivo.png → Imagens/arquivo.png
30-06-2026 14:24:50 | INFO | organizador | Movendo arquivo.pdf → Documentos/arquivo.pdf
30-06-2026 14:24:50 | INFO | organizador | Organização concluída! 2 arquivos movidos, 0 para Outros.
30-06-2026 14:24:50 | INFO | monitor | Watchdog iniciado. Monitorando: /home/user/Downloads
```

---

## Execução como serviço (systemd)

O sistema pode rodar como um serviço do systemd, iniciando automaticamente no boot da máquina, sem depender de login gráfico.

### 1. Criar o ambiente virtual

```bash
cd /caminho/do/projeto
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
```

### 2. Criar o unit file

```bash
sudo nano /etc/systemd/system/organizador-downloads.service
```

Conteúdo (ajuste `User` e os caminhos conforme seu ambiente):

```ini
[Unit]
Description=Organizador de Downloads em tempo real
After=network.target

[Service]
Type=simple
User=SEU_USUARIO
WorkingDirectory=/caminho/do/projeto
ExecStart=/caminho/do/projeto/venv/bin/python main.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

### 3. Ativar e iniciar o serviço

```bash
sudo systemctl daemon-reload
sudo systemctl enable organizador-downloads.service
sudo systemctl start organizador-downloads.service
```

### 4. Comandos do dia a dia

```bash
# Verificar status
sudo systemctl status organizador-downloads.service

# Acompanhar logs em tempo real
journalctl -u organizador-downloads.service -f

# Reiniciar (após atualizar o código com git pull)
sudo systemctl restart organizador-downloads.service

# Parar/iniciar manualmente
sudo systemctl stop organizador-downloads.service
sudo systemctl start organizador-downloads.service
```

`WorkingDirectory` deve apontar para a pasta onde está o `config.json`, já que ele é carregado por caminho relativo. `Restart=on-failure` garante que o serviço reinicia sozinho caso ocorra algum erro inesperado.

---

## Evolução

* CLI instalável via pip
* Suporte a Windows Service

---

## Autor

Thayron Higlânder
LinkedIn: [https://www.linkedin.com/in/thayron-higlander](https://www.linkedin.com/in/thayron-higlander)