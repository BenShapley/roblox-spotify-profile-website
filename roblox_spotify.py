import requests
import webbrowser
import spotipy
import spotipy.util as util
import json
import base64
from roblox import Client
import roblox.thumbnails as thumbnail
import asyncio

asyncio.new_event_loop() 

# Read Roblox Cookie
with open("keys/roblox_cookie.txt", "r") as roblox_file:
    roblox_key = roblox_file.read()


# Load Spotify data
with open("keys/spotify_keys.json", "r") as spotify_files:
    tokens = json.load(spotify_files)

my_client_id = tokens["client_id"]
my_client_secret = tokens["client_secret"]
redirectURI = tokens["redirect"]
username = tokens["username"]

scope = "user-read-private user-read-playback-state user-modify-playback-state playlist-modify-public playlist-modify-private ugc-image-upload"
token = util.prompt_for_user_token(username, scope, client_id=my_client_id, client_secret=my_client_secret, redirect_uri=redirectURI)

sp = spotipy.Spotify(auth=token)

async def create_playlist(desired_user, user_image):
    print(desired_user["name"])

    track_results = sp.search(q=desired_user["name"], type="track", limit=10)
    song_data = track_results["tracks"]["items"]
    song_uris = [song["uri"] for song in song_data]

    my_playlist = sp.user_playlist_create(user=username, name=desired_user["name"], public=True,
                                        description=f"Playlist for the Robloxian {desired_user['name']}!")

    sp.user_playlist_add_tracks(username, my_playlist['id'], song_uris)

    def get_as_base64(url):
        response = requests.get(url)
        return base64.b64encode(response.content).decode('utf-8')

    user_image_base64 = get_as_base64(user_image)
    sp.playlist_upload_cover_image(my_playlist['id'], user_image_base64)

    #webbrowser.open(my_playlist['external_urls']['spotify'])

    print("Playlist ID:", my_playlist["id"])
    return my_playlist["id"]

async def main(desired_name):
    cookie = roblox_key
    client = Client(cookie)
    print("RUNNING MAIN")
    user = await client.get_authenticated_user()
    print("ID:", user.id)

    users = client.user_search(desired_name, max_items=10)
    outputted_names = []
    async for user in users:
        outputted_names.append(user.name)
        outputted_names.append(user.id)

    formatted_names = []
    for i in range(0, len(outputted_names), 2):
        formatted_names.append({'name': outputted_names[i], 'id': outputted_names[i + 1]})

    desired_user = formatted_names[0]
    user = await client.get_user(desired_user["id"])
    user_thumbnails = await client.thumbnails.get_user_avatar_thumbnails(
        users=[user],
        type=thumbnail.AvatarThumbnailType.full_body,
        size=(420, 420)
    )

    user_image = user_thumbnails[0].image_url if user_thumbnails else None

    return await create_playlist(desired_user, user_image)

def search_robloxian2(user_name):
    return asyncio.run(main(user_name))