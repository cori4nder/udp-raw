# Projeto Redes de Computadores

Projeto desenvolvido para a disciplina de Redes de Computadores da Universidade Federal da Paraíba no período 2023.2 com o professor Ewerton. 
O projeto abrange um cliente UDP simples que interage com um servidor remoto para solicitar e receber mensagens e um cliente UDP com socket raw com as mesmas funcionalidades.

Alunos:
- Gustavo Montenegro Maia Chaves 
- Lucas Gomes Dantas 

## Funcionalidades

- **Menu de Opções**: Exibe um menu de opções para o usuário escolher.
- **Envio de Solicitação**: Envia uma solicitação ao servidor.
- **Recebimento de Resposta**: Recebe e exibe a resposta do servidor.

## Requisitos

- Python 3.10
- Módulo `socket`
- Módulo `struct`

## Utilização

Mude o diretório para `test` e execute o arquivo `udp_client.py` para iniciar o cliente padrão e o `udp_client_raw` para o com o socket raw (necessário execução como administrador).

## Estrutura do Projeto

- **client.py**: Contém as classe `ClientUDP` e `ClientUDPRaw` para interação com o servidor.
- **codec/message_codec_template.py**: Define a classe abstrata `CodecTemplate` para codificação e decodificação de mensagens.
- **codec/message_codec.py**: Implementa o codec para mensagens.
- **codec/message_codec_raw.py**: Implementa o codec para mensagens em formato raw.
- **tests**: Pasta contendo módulos de teste.

## Configuração

Para configurar o servidor IP e porta, você pode modificar os argumentos padrão na inicialização dos objetos `ClientUDP` e `ClientUDPRaw` em `client.py`.

## Testes

Há um módulo de teste disponível em `test`, que pode ser executado para verificar o funcionamento do cliente normal.

Execute o seguinte comando no terminal:

```bash
python test/udp_client.py
```

Bem como o RAW:

```bash
python test/udp_client_raw.py
```
