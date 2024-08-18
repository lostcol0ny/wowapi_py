from api import WowGameDataApi, WowProfileDataApi
from wow_game_data import SearchQuery

client_id = "770114edfc63482fbc58e903322d215e"
client_secret = "3TqQuqzB6wG5IFjzbfXYSpbkReCZQuwl"
locale = "en_US"
region = "us"

profile_api = WowProfileDataApi(client_id, client_secret)
data_api = WowGameDataApi(client_id, client_secret)

character_images = profile_api.get_character_images("us", "en_US", "illidan", "beyloc")
token_data = data_api.get_token_price("us", "en_US")
pet_collection_data = profile_api.get_character_pets_collection_summary("us", "en_US", "illidan", "beyloc")

print(pet_collection_data)