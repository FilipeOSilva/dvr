import httpx


class BotTelegram:
    def __init__(self, token: str, chat_id: str) -> None:
        self._token: str = token
        self._chat_id: str = chat_id

    def send_message(self, msg: str) -> None:
        url = f'https://api.telegram.org/bot{self._token}/sendMessage'
        params = {
            'chat_id': self._chat_id,
            'text': msg,
        }

        httpx.get(url, params=params)
