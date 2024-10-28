import requests
from typing import List, Dict, Any, Optional


class PaginatedAPIClient:
    def __init__(self, base_url: str, headers: Optional[Dict[str, str]] = None) -> None:

        """
        Initialise un nouveau client API.

        :param base_url: L'URL de base de l'API.
        :param headers: (Optionnel) Un dictionnaire contenant les en-têtes HTTP à envoyer avec chaque requête.
        """
        self.base_url = base_url
        self.headers = headers if headers is not None else {}

    def get(self, endpoint:str, params=None) -> requests.Response:
        """
        Effectue une requête GET à l'API.

        :param endpoint: Le point de terminaison de l'API à appeler.
        :param params: (Optionnel) Un dictionnaire contenant les paramètres de requête.
        :return: La réponse de l'API sous forme de dictionnaire.
        """
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()  # Lève une exception pour les codes de statut HTTP 4xx/5xx
        return response
    
    def fetch_all_pages(self, endpoint: str, page_size: int = 10) -> List[Dict[str, Any]]:
        """
        Récupère toutes les pages de l'API.

        :param endpoint: Le point de terminaison de l'API à appeler.
        :param page_size: Le nombre d'éléments par page.
        :return: Une liste contenant tous les éléments récupérés de l'API.
        """
        all_items: List[Dict[str, Any]] = []
        current_page: int = 1

        while True:
            response = self._fetch_page(endpoint, current_page, page_size)
            data = response.json()
            
            all_items.extend(data['items'])
            
            if current_page >= data['pages']:
                break
            
            current_page += 1

        return all_items

    def _fetch_page(self, endpoint: str, page: int, size: int) -> requests.Response:
        """
        Récupère une page spécifique de l'API.

        :param endpoint: Le point de terminaison de l'API à appeler.
        :param page: Le numéro de la page à récupérer.
        :param size: Le nombre d'éléments par page.
        :return: La réponse de l'API.
        """
        params = {'page': page, 'size': size}
        response = self.get(endpoint=endpoint, params=params)
        response.raise_for_status()  # Lève une exception pour les codes de statut HTTP 4xx/5xx
        return response