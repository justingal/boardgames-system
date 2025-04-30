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
    import requests
    import xml.etree.ElementTree as ET
    from core.models import Game

    if bgg_id:
        url = f"https://boardgamegeek.com/xmlapi2/thing?id={bgg_id}&stats=1"
    elif title:
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
        recommended_age = int(item.find("minage").attrib.get("value", 0))

        thumbnail_elem = item.find("thumbnail")
        thumbnail_url = thumbnail_elem.text if thumbnail_elem is not None else ""

        stats = item.find("statistics/ratings")
        average_rating = float(stats.find("average").attrib.get("value", 0)) if stats is not None else None
        complexity = float(stats.find("averageweight").attrib.get("value", 0)) if stats is not None else None
        categories = [link.attrib['value'] for link in item.findall("link[@type='boardgamecategory']")]
        mechanics = [link.attrib['value'] for link in item.findall("link[@type='boardgamemechanic']")]

        # Rank (type='subtype', name='boardgame')
        overall_rank = None
        ranks_elem = stats.find("ranks") if stats is not None else None
        if ranks_elem is not None:
            for rank in ranks_elem.findall("rank"):
                if rank.attrib.get("type") == "subtype" and rank.attrib.get("name") == "boardgame":
                    val = rank.attrib.get("value")
                    if val and val != "Not Ranked":
                        overall_rank = int(val)

        language_dependence = None
        poll = item.find("poll[@name='language_dependence']")
        if poll is not None:
            options = poll.findall("results/result")
            if options:
                most_voted = max(options, key=lambda x: int(x.attrib.get('numvotes', 0)))
                language_dependence = most_voted.attrib.get('value')

        best_player_count = None
        poll = item.find("poll[@name='suggested_numplayers']")
        if poll is not None:
            options = poll.findall("results")
            best_votes = []

            for opt in options:
                player_num = opt.attrib.get("numplayers")
                for result in opt.findall("result"):
                    if result.attrib.get("value") == "Best":
                        numvotes = int(result.attrib.get("numvotes", 0))
                        best_votes.append((player_num, numvotes))

            if best_votes:
                best_votes.sort(key=lambda x: -x[1])
                best_player_count = best_votes[0][0]

        # get_or_create to avoid duplicate error
        game, created = Game.objects.get_or_create(
            bgg_id=bgg_id,
            defaults={
                'title': title,
                'min_players': min_players,
                'max_players': max_players,
                'playtime_minutes': playtime,
                'thumbnail_url': thumbnail_url,
                'average_rating': average_rating,
                'complexity': complexity,
                'overall_rank': overall_rank,
                'recommended_age': recommended_age,
                'categories': categories,
                'mechanics': mechanics,
                'language_dependence': language_dependence,
                'best_player_count': best_player_count,
            }
        )
        game, created = Game.objects.get_or_create(bgg_id=bgg_id)

        # Jeigu buvo sukurtas dabar — užpildom iš karto
        # Jeigu jau egzistavo — atnaujinam duomenis
        game.title = title
        game.min_players = min_players
        game.max_players = max_players
        game.playtime_minutes = playtime
        game.thumbnail_url = thumbnail_url
        game.average_rating = average_rating
        game.complexity = complexity
        game.overall_rank = overall_rank
        game.recommended_age = recommended_age
        game.categories = categories
        game.mechanics = mechanics
        game.language_dependence = language_dependence
        game.save()
        return game

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
            added_games.append({"title": game.title, "thumbnail_url": game.thumbnail_url})

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
            added_games.append({"title": game.title, "thumbnail_url": game.thumbnail_url})

        return Response({
            "added": added_games,
            "skipped": skipped,
        })

