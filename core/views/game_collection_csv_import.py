import csv
import io
import json
import requests
import xml.etree.ElementTree as ET

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from core.models.game import Game
from core.models.game_collection import GameCollection

def fetch_game_from_bgg(bgg_id=None, title=None):
    if bgg_id:
        url = f"https://boardgamegeek.com/xmlapi2/thing?id={bgg_id}&type=boardgame"
    elif title:
        # Naudojame paieškos API
        search_url = f"https://boardgamegeek.com/xmlapi2/search?query={title}&type=boardgame"
        search_response = requests.get(search_url)
        if search_response.status_code != 200:
            return None
        try:
            search_root = ET.fromstring(search_response.content)
            first_item = search_root.find("item")
            if first_item is not None:
                bgg_id = first_item.attrib.get("id")
                if bgg_id:
                    return fetch_game_from_bgg(bgg_id=bgg_id)
            return None
        except:
            return None
    else:
        return None

    response = requests.get(url)
    if response.status_code != 200:
        return None

    try:
        root = ET.fromstring(response.content)
        item = root.find("item")
        if item is None:
            return None

        title_elem = item.find("name[@type='primary']")
        title = title_elem.attrib["value"] if title_elem is not None else "Nežinomas pavadinimas"

        min_players = int(item.find("minplayers").attrib.get("value", 0))
        max_players = int(item.find("maxplayers").attrib.get("value", 0))
        playtime = int(item.find("playingtime").attrib.get("value", 0))

        thumbnail_elem = item.find("thumbnail")
        thumbnail_url = thumbnail_elem.text if thumbnail_elem is not None else ""

        return Game.objects.create(
            bgg_id=bgg_id,
            title=title,
            min_players=min_players,
            max_players=max_players,
            playtime_minutes=playtime,
            thumbnail_url=thumbnail_url
        )

    except Exception as e:
        print(f"Klaida parsisiunčiant iš BGG: {e}")
        return None


class GameCollectionCSVImportView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)

        if file.name.endswith('.json'):
            return self.handle_json_import(file, request)

        decoded_file = file.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)
        reader = csv.DictReader(io_string)

        added_games = []
        skipped = []

        for row in reader:
            bgg_id = row.get("bgg_id")
            title = row.get("title")

            game = None

            if bgg_id:
                try:
                    game = Game.objects.get(bgg_id=int(bgg_id))
                except Game.DoesNotExist:
                    game = fetch_game_from_bgg(bgg_id=int(bgg_id))
                    if not game:
                        skipped.append({"reason": "bgg_id not found (BGG fetch failed)", "row": row})
                        continue
            elif title:
                try:
                    game = Game.objects.filter(title__iexact=title).first()
                    if not game:
                        game = fetch_game_from_bgg(title=title)
                        if not game:
                            skipped.append({"reason": "title not found (BGG fetch failed)", "row": row})
                            continue
                except:
                    skipped.append({"reason": "invalid title", "row": row})
                    continue
            else:
                skipped.append({"reason": "no identifiers", "row": row})
                continue

            if GameCollection.objects.filter(user=request.user, game=game).exists():
                skipped.append({"reason": "already in collection", "row": row})
                continue

            GameCollection.objects.create(user=request.user, game=game)
            added_games.append(game.title)

        return Response({
            "added": added_games,
            "skipped": skipped,
        })

    def handle_json_import(self, file, request):
        try:
            content = json.load(file)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON file."}, status=status.HTTP_400_BAD_REQUEST)

        added_games = []
        skipped = []

        for entry in content:
            bgg_id = entry.get("bgg_id")
            title = entry.get("title")

            game = None

            if bgg_id:
                try:
                    game = Game.objects.get(bgg_id=int(bgg_id))
                except Game.DoesNotExist:
                    game = fetch_game_from_bgg(bgg_id=int(bgg_id))
                    if not game:
                        skipped.append({"reason": "bgg_id not found (BGG fetch failed)", "entry": entry})
                        continue
            elif title:
                try:
                    game = Game.objects.filter(title__iexact=title).first()
                    if not game:
                        game = fetch_game_from_bgg(title=title)
                        if not game:
                            skipped.append({"reason": "title not found (BGG fetch failed)", "entry": entry})
                            continue
                except:
                    skipped.append({"reason": "invalid title", "entry": entry})
                    continue
            else:
                skipped.append({"reason": "no identifiers", "entry": entry})
                continue

            if GameCollection.objects.filter(user=request.user, game=game).exists():
                skipped.append({"reason": "already in collection", "entry": entry})
                continue

            GameCollection.objects.create(user=request.user, game=game)
            added_games.append(game.title)

        return Response({
            "added": added_games,
            "skipped": skipped,
        })
