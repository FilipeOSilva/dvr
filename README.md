# dvr
Repositório criado para gravação de uma camera IP instalada em uma residência.

## Ambiente
É importante salientar que para o projeto funcionar, deve-se criar um arquivo `.env` na raiz do projeto. Nele estaram todos as informações **"Hardcode"** como o IP da camera, o chat_id e o token do telegram (caso queria usar esse serviço).
O nome das variaveis são:
```
RTSP_URL='[URL RTSP DA CAMERA]'
TELEGRAM_CHAT_ID='[CHAT ID FORNECIDO PELO BOT DO TELEGRAM]'
TELEGRAM_TOKEN='[TOKEN FORNECIDO PELO BOT DO TELEGRAM]'
```
### Ambiente local
Para o desenvolvimento foi utilizado python com Poetry.
*_OBS:_* Todos os comandos a seguir são para serem executados quando estiver dentro do ambiente (environment) criado pelo poetry.
Para cobertura de formatação de código:
```
task lint
```
Para ajustar o código:
```
task format
```
## Docker
Caso não queria utilizar para desenvolver, basta usar via Docker. Para isso acesse a pasta e rode o comando:
```
docker-compose up -d
```
Isto irá criar um conteiner que irá instalar os pacotes e rodar a aplicação.