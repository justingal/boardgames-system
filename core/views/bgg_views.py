import requests
import xml.etree.ElementTree as ET
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from core.models.game_collection import GameCollection

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
                "year": year,
                "thumbnail_url": f"https://cf.geekdo-images.com/thumb/img/blank/games/{game_id}.jpg"  # optional fallback
            })

        return Response(results)

class ImportGameByBGGId(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        bgg_id = request.data.get("bgg_id")
        if not bgg_id:
            return Response({"error": "bgg_id is required"}, status=400)

        try:
            game = fetch_game_from_bgg(bgg_id=int(bgg_id))
            if not game:
                return Response({"error": "Nepavyko atsisiųsti žaidimo iš BGG."}, status=400)

            if GameCollection.objects.filter(user=request.user, game=game).exists():
                return Response({"message": "Žaidimas jau yra kolekcijoje."}, status=200)

            GameCollection.objects.create(user=request.user, game=game)
            return Response({"message": f"Pridėtas: {game.title}"}, status=201)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
