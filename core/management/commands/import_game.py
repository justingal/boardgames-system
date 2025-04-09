import requests
import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand
from core.models import Game

class Command(BaseCommand):
    help = 'Import a board game from BoardGameGeek by name'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='Game name to search and import')

    def handle(self, *args, **kwargs):
        name = kwargs['name']
        print(f"🔍 Searching BGG for game: {name}")

        search_url = f"https://boardgamegeek.com/xmlapi2/search?query={name}&type=boardgame"
        response = requests.get(search_url)
        if response.status_code != 200:
            print("❌ Failed to fetch search results.")
            return

        root = ET.fromstring(response.content)
        items = root.findall('item')

        if not items:
            print("⚠️ No games found.")
            return

        # Imame pirmą rezultatą
        first = items[0]
        bgg_id = first.attrib['id']
        print(f"✅ Found game ID: {bgg_id}")

        # Gauname detales
        detail_url = f"https://boardgamegeek.com/xmlapi2/thing?id={bgg_id}"
        detail_response = requests.get(detail_url)
        detail_root = ET.fromstring(detail_response.content)

        item = detail_root.find('item')
        title = item.find("name").attrib['value']
        min_players = item.find("minplayers").attrib['value']
        max_players = item.find("maxplayers").attrib['value']
        playtime = item.find("playingtime").attrib['value']
        thumbnail = item.find("thumbnail")
        thumbnail_url = thumbnail.text if thumbnail is not None else None

        game, created = Game.objects.get_or_create(
            bgg_id=bgg_id,
            defaults={
                "title": title,
                "min_players": min_players,
                "max_players": max_players,
                "playtime_minutes": playtime,
                "thumbnail_url": thumbnail_url
            }
        )

        if created:
            print(f"✅ Game '{title}' added to DB.")
        else:
            print(f"ℹ️ Game '{title}' already exists in DB.")
