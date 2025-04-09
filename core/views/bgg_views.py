import requests
import xml.etree.ElementTree as ET
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

class BGGSearchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.GET.get('query')
        if not query:
            return Response({'error': 'Missing query parameter'}, status=400)

        url = f"https://boardgamegeek.com/xmlapi2/search?query={query}&type=boardgame"
        response = requests.get(url)
        if response.status_code != 200:
            return Response({'error': 'Failed to reach BGG'}, status=500)

        root = ET.fromstring(response.content)
        results = []

        for item in root.findall('item'):
            game_id = int(item.attrib['id'])
            name_el = item.find("name")
            year_el = item.find("yearpublished")
            title = name_el.attrib['value'] if name_el is not None else "Unknown"
            year = int(year_el.attrib['value']) if year_el is not None else None

            results.append({
                "bgg_id": game_id,
                "title": title,
                "year": year
            })

        return Response(results)
