import httpx
from .settings import CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN
import traceback


class ZohoClient:
    BASE_URL = "https://www.zohoapis.com"
    TOKEN_URL = "https://accounts.zoho.com/oauth/v2/token"

    def __init__(self) -> None:
        self.client = httpx.AsyncClient()
        self.access_token = None

    async def close(self) -> None:
        if not self.client.is_closed:
            await self.client.aclose()

    async def refresh_token(self):
        data = {
            'refresh_token': REFRESH_TOKEN,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': 'refresh_token'
        }
        response = await self.client.post(self.TOKEN_URL, data=data)
        response.raise_for_status()
        self.access_token = response.json()['access_token']

    async def send_lead(self, lead_data):
        print(lead_data)

        headers = {'Authorization': f'Zoho-oauthtoken {self.access_token}', 'Content-Type': 'application/json'}
        wrapped_lead_data = {'data': [lead_data]}

        try:
            response = await self.client.post(
                f"{self.BASE_URL}/crm/v2/Leads",
                json=wrapped_lead_data,
                headers=headers
            )
            if response.status_code == 401:
                await self.refresh_token()
                return await self.send_lead(lead_data)
            elif response.status_code == 400:
                print("Ошибка запроса: Проверьте данные и формат запроса.")
                print("Ответ сервера:", response.text)
                return None

            response.raise_for_status()
            return response.json()

        except Exception as e:
            print("Произошла ошибка:", e)
            traceback.print_exc()
        return None


zoho_client = ZohoClient()
