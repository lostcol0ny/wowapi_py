from dataclasses import dataclass, field
from typing import Any, Optional, Dict, Callable, Union
from api import Api, RegionType
import custom_types
from functools import wraps


def method_cache(func: Callable):
    cache = {}

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = func(self, *args, **kwargs)
        return cache[key]

    return wrapper


@dataclass
class WowProfileDataApi:
    """
    All World of Warcraft Profile Data API methods.

    This class provides methods to interact with the World of Warcraft Profile Data API.
    It uses the Blizzard API credentials for authentication.

    Attributes:
        client_id: A string representing the client ID for API authentication.
        client_secret: A string representing the client secret for API authentication
        api: An instance of the Api class for making API requests.
    """

    client_id: str
    client_secret: str

    api: Api = field(init=False)

    def __post_init__(self):
        self.api = Api(self.client_id, self.client_secret)

    # Context manager support
    def __enter__(self) -> "WowProfileDataApi":
        return self

    def __exit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[Exception],
        exc_tb: Optional[Any],
    ) -> None:
        self.api.__exit__(exc_type, exc_val, exc_tb)

    @method_cache
    def _get_data(
        self, resource: str, region: RegionType, locale: str, **kwargs
    ) -> Dict[str, Any]:
        query_params = {"locale": locale, **kwargs}
        return self.api.get(resource, region, params=query_params)

    # Character Achievements API

    def get_character_achievements_summary(
        self, region: RegionType, locale: str, realm_slug: str, character_name: str
    ) -> custom_types.CharacterAchievementSummary:
        """
        Retrieve a summary of the given character's achievements.

        Args:
            region (RegionType): The region of the data to retrieve.
            locale (str): The locale to use for the request.
            realm_slug (str): The slug of the realm the character is on.
            character_name (str): The name of the character to retrieve achievements for.

        Returns:
            CharacterAchievementSummary: A dictionary representing the character's achievements summary.
            _links: Links
            total_quantity: int
            total_points: int
            achievements: List[KeyValue]
        """
        resource = f"/profile/wow/character/{realm_slug}/{character_name}/achievements"
        return self._get_data(resource, region, locale, namespace=f"profile-{region}")

    def get_character_achievements_statistics(
        self, region: RegionType, locale: str, realm_slug: str, character_name: str
    ) -> custom_types.CharacterAchievementStatistics:
        """
        Retrieve a summary of the given character's achievements.

        Args:
            region (RegionType): The region of the data to retrieve.
            locale (str): The locale to use for the request.
            realm_slug (str): The slug of the realm the character is on.
            character_name (str): The name of the character to retrieve data for.

        Returns:
            CharacterAchievementStatistics: A dictionary representing the character's achievements statistics.
            _links: Links
            character: CharacterAchievementStatisticsCharacterReference
            categories: List[CharacterAchievementStatisticsCategory]

        """
        resource = f"/profile/wow/character/{realm_slug}/{character_name}/achievements/statistics"
        return self._get_data(resource, region, locale, namespace=f"profile-{region}")

    # Character Appearance API

    def get_character_appearance_summary(
        self, region: RegionType, locale: str, realm_slug: str, character_name: str
    ) -> custom_types.CharacterAppearanceSummary:
        """
        Retrieve a summary of the given character's achievements.

        Args:
            region (RegionType): The region of the data to retrieve.
            locale (str): The locale to use for the request.
            realm_slug (str): The slug of the realm the character is on.
            character_name (str): The name of the character to retrieve data for.

        Returns:
            CharacterAppeaaranceSummary: A dictionary representing the character's appearance summary.
            _links: Links
            character: CharacterAppearanceSummaryCharacterReference
            playable_race: KeyValue
            playable_class: KeyValue
            active_spec: KeyValue
            gender: PlayableClassGender
            faction: FactionType
            guild_crest: CharacterAppearanceSummaryGuildCrest
            items: List[CharacterAppearanceSummaryCharacterItem]
            customizations: List[CharacterAppearanceSummaryCharacterCustomization]
        """
        resource = f"/profile/wow/character/{realm_slug}/{character_name}/appearance"
        return self._get_data(resource, region, locale, namespace=f"profile-{region}")

    # Character Collections API

    def get_character_collections_index(
        self, region: RegionType, locale: str, realm_slug: str, character_name: str
    ) -> custom_types.CharacterCollectionsIndex:
        """
        Returns an index of collection types for a character.

        Args:
            region (RegionType): The region of the data to retrieve.
            locale (str): The locale to use for the request.
            realm_slug (str): The slug of the realm the character is on.
            character_name (str): The name of the character to retrieve data for.

        Returns:
            CharacterCollectionsIndex: A dictionary representing the character's collections index.
            _links: Links
            pets: Link
            mounts: Link
            heirlooms: Link
            toys: Link
            character: CharacterCollectionsIndexCharacter
            transmogs: Link
        """
        resource = f"/profile/wow/character/{realm_slug}/{character_name}/collections"
        return self._get_data(resource, region, locale, namespace=f"profile-{region}")

    def get_character_heirlooms_collection_summary(
        self, region: RegionType, locale: str, realm_slug: str, character_name: str
    ) -> custom_types.CharacterHeirloomsCollectionSummary:
        """
        Returns a summary of the heirlooms a character has obtained.

        Args:
            region (RegionType): The region of the data to retrieve.
            locale (str): The locale to use for the request.
            realm_slug (str): The slug of the realm the character is on.
            character_name (str): The name of the character to retrieve data for.

        Returns:
            CharacterHeirlomsCollectionSummary: A dictionary representing the character's heirlooms collection summary.
            _links: Links
            heirlooms: List[CharacterHeirloomsCollectionSummaryHeirloom]
        """
        resource = f"/profile/wow/character/{realm_slug}/{character_name}/collections/heirlooms"
        return self._get_data(resource, region, locale, namespace=f"profile-{region}")

    def get_character_mounts_collection_summary(
        self, region: RegionType, locale: str, realm_slug: str, character_name: str
    ) -> custom_types.CharacterMountsCollectionSummary:
        """
        Returns a summary of the mounts a character has obtained.

        Args:
            region (RegionType): The region of the data to retrieve.
            locale (str): The locale to use for the request.
            realm_slug (str): The slug of the realm the character is on.
            character_name (str): The name of the character to retrieve data for.

        Returns:
            CharacterMountsCollectionSummary: A dictionary representing the character's mounts collection summary.
            _links: Links
            mounts: List[CharacterMountsCollectionSummary]
        """
        resource = (
            f"/profile/wow/character/{realm_slug}/{character_name}/collections/mounts"
        )
        return self._get_data(resource, region, locale, namespace=f"profile-{region}")

    def get_character_pets_collection_summary(
        self, region: RegionType, locale: str, realm_slug: str, character_name: str
    ) -> custom_types.CharacterPetsCollectionSummary:
        """
        Returns a summary of the pets a character has obtained.

        Args:
            region (RegionType): The region of the data to retrieve.
            locale (str): The locale to use for the request.
            realm_slug (str): The slug of the realm the character is on.
            character_name (str): The name of the character to retrieve data for.

        Returns:
            CharacterPetsCollectionSummary: A dictionary representing the character's pets collection summary.
            _links: Links
            pets: List[CharacterPetsCollectionSummary]
        """
        resource = (
            f"/profile/wow/character/{realm_slug}/{character_name}/collections/pets"
        )
        return self._get_data(resource, region, locale, namespace=f"profile-{region}")

    def get_character_toys_collection_summary(
        self, region: RegionType, locale: str, realm_slug: str, character_name: str
    ) -> custom_types.CharacterToysCollectionSummary:
        """
        Returns a summary of the toys a character has obtained.

        Args:
            region (RegionType): The region of the data to retrieve.
            locale (str): The locale to use for the request.
            realm_slug (str): The slug of the realm the character is on.
            character_name (str): The name of the character to retrieve data for.

        Returns:
            CharacterToysCollectionSummary: A dictionary representing the character's toys collection summary.

        """
        resource = (
            f"/profile/wow/character/{realm_slug}/{character_name}/collections/toys"
        )
        return self._get_data(resource, region, locale, namespace=f"profile-{region}")

    def get_character_transmogs_collection_summary(
        self, region: RegionType, locale: str, realm_slug: str, character_name: str
    ) -> custom_types.CharacterTransmogsCollectionSummary:
        """
        Returns a summary of the transmogs a character has obtained.

        Args:
            region (RegionType): The region of the data to retrieve.
            locale (str): The locale to use for the request.
            realm_slug (str): The slug of the realm the character is on.
            character_name (str): The name of the character to retrieve data for.

        Returns:
            CharacterTransmogsCollectionSummary: A dictionary representing the character's transmogs collection summary.
            _links: Links
            appearance_sets: List[KeyValue]
            slots: list[CharacterTransmogsCollectionSummarySlots]

        """
        resource = f"/profile/wow/character/{realm_slug}/{character_name}/collections/transmogs"
        return self._get_data(resource, region, locale, namespace=f"profile-{region}")

    # Character Encounters API

    def get_character_encounters_summary(
        self, region: RegionType, locale: str, realm_slug: str, character_name: str
    ) -> custom_types.CharacterEncountersSummary:
        """
        Returns a summary of a character's encounters.

        Args:
            region (RegionType): The region of the data to retrieve.
            locale (str): The locale to use for the request.
            realm_slug (str): The slug of the realm the character is on.
            character_name (str): The name of the character to retrieve data for.

        Returns:
            CharacterEncountersSummary: A dictionary representing the character's encounters summary.
            _links: Links
            character: CharacterAchievementStatisticsCharacterReference
            dungeons: Link
            raids: Link

        """
        resource = f"/profile/wow/character/{realm_slug}/{character_name}/encounters"
        return self._get_data(resource, region, locale, namespace=f"profile-{region}")

    def get_character_dungeons(
        self, region: RegionType, locale: str, realm_slug: str, character_name: str
    ) -> custom_types.CharacterEncountersSummary:
        """
        Returns a summary of a character's completed dungeons.

        Args:
            region (RegionType): The region of the data to retrieve.
            locale (str): The locale to use for the request.
            realm_slug (str): The slug of the realm the character is on.
            character_name (str): The name of the character to retrieve data for.

        Returns:
            CharacterDungeonsSummary: A dictionary representing the ccharacter's completed dungeons.
            _links: Links
            expansions: List[Expansion]

        """
        resource = (
            f"/profile/wow/character/{realm_slug}/{character_name}/encounters/dungeons"
        )
        return self._get_data(resource, region, locale, namespace=f"profile-{region}")

    def get_character_raids(
        self, region: RegionType, locale: str, realm_slug: str, character_name: str
    ) -> custom_types.CharacterDungeons:
        """
        Returns a summary of a character's completed raids.

        Args:
            region (RegionType): The region of the data to retrieve.
            locale (str): The locale to use for the request.
            realm_slug (str): The slug of the realm the character is on.
            character_name (str): The name of the character to retrieve data for.

        Returns:
            CharacterDungeonsSummary: A dictionary representing the character's completed raids.
            _links: Links
            expansions: List[Expansion]

        """
        resource = (
            f"/profile/wow/character/{realm_slug}/{character_name}/encounters/raids"
        )
        return self._get_data(resource, region, locale, namespace=f"profile-{region}")

    # Character Equipment API

    def get_character_equipment_summary(
        self, region: RegionType, locale: str, realm_slug: str, character_name: str
    ) -> custom_types.CharacterEquipmentSummary:
        """
        Returns a summary of the items equipped by a character.

        Args:
            region (RegionType): The region of the data to retrieve.
            locale (str): The locale to use for the request.
            realm_slug (str): The slug of the realm the character is on.
            character_name (str): The name of the character to retrieve data for.

        Returns:
            CharacterEquipmentSummary: A dictionary representing the character's equipment summary.
            _links: Links
            character: CharacterEquipmentSummaryCharacterReference
            equipped_items: List[CharacterEquipmentSummaryEquippedItem]
            equipped_item_sets: List[CharacterEquipmentSummaryEquippedItemSet]

        """
        resource = f"/profile/wow/character/{realm_slug}/{character_name}/equipment"
        return self._get_data(resource, region, locale, namespace=f"profile-{region}")

    # Character Hunter Pets API

    def get_character_hunter_pets(
        self, region: RegionType, locale: str, realm_slug: str, character_name: str
    ) -> custom_types.CharacterHunterPetsSummary:
        """
        If the character is a hunter, returns a summary of the character's hunter pets. Otherwise, returns an HTTP 404 Not Found error.

        Args:
            region (RegionType): The region of the data to retrieve.
            locale (str): The locale to use for the request.
            realm_slug (str): The slug of the realm the character is on.
            character_name (str): The name of the character to retrieve data for.

        Returns:
            CharacterHunterPetsSummary: A dictionary representing the character's hunter pets summary.
            _links: Links
            character: CharacterAchievementStatisticsCharacterReference
            hunter_pets: List[CharacterHunterPetsSummaryHunterPets]

        """
        resource = f"/profile/wow/character/{realm_slug}/{character_name}/hunter-pets"
        return self._get_data(resource, region, locale, namespace=f"profile-{region}")

    # Character Media API

    def get_character_media_summary(
        self, region: RegionType, locale: str, realm_slug: str, character_name: str
    ) -> custom_types.CharacterMediaSummary:
        """
        Returns a summary of the media assets available for a character (such as an avatar render).

        Args:
            region (RegionType): The region of the data to retrieve.
            locale (str): The locale to use for the request.
            realm_slug (str): The slug of the realm the character is on.
            character_name (str): The name of the character to retrieve data for.

        Returns:
            CharacterMediaSummary: A dictionary representing the character's media summary.
            _links: Links
            character: CharacterAchievementStatisticsCharacterReference
            assets: List[JournalInstanceMediaAsset]

        """
        resource = (
            f"/profile/wow/character/{realm_slug}/{character_name}/character-media"
        )
        return self._get_data(resource, region, locale, namespace=f"profile-{region}")

    def get_character_images(
        self, region: RegionType, locale: str, realm_slug: str, character_name: str
    ) -> Dict[str, Optional[str]]:
        """
        Returns the URLs of the character's avatar, inset, and main-raw images.

        Args:
            region (RegionType): The region of the data to retrieve.
            locale (str): The locale to use for the request.
            realm_slug (str): The slug of the realm the character is on.
            character_name (str): The name of the character to retrieve data for.

        Returns:
            Dict[str, Optional[str]]: A dictionary containing the URLs of the character's images.
                                      Keys are 'avatar', 'inset', and 'main-raw'.
                                      Values are the corresponding URLs or None if not found.
        """
        media_summary = self.get_character_media_summary(
            region, locale, realm_slug, character_name
        )

        image_urls = {"avatar": None, "inset": None, "main-raw": None}

        for asset in media_summary.get("assets", []):
            asset_key = asset.get("key")
            if asset_key in image_urls:
                image_urls[asset_key] = asset.get("value")

        return image_urls

    # Character Mythic Keystone Profile API

    def get_character_character_mythic_keystone_profile_index(
        self,
        region: RegionType,
        locale: str,
        realm_slug: str,
        character_name: str,
        season_id: Optional[int] = None,
    ) -> custom_types.CharacterMythicKeystoneProfileIndex:
        """
        Returns the Mythic Keystone profile index for a character.

        Args:
            region (RegionType): The region of the data to retrieve.
            locale (str): The locale to use for the request.
            realm_slug (str): The slug of the realm the character is on.
            character_name (str): The name of the character to retrieve data for.
            season_id (int): The ID of the season to retrieve data for.

        Returns:
            CharacterMythicKeystoneProfile: A dictionary representing the character's Mythic Keystone profile.
            _links: Links
            current_period: CharacterMythicKeystoneProfileCurrentPeriod
            seasons: List[GenericID]
            character: KeyValue
            current_mythic_rating: CharacterMythicKeystoneProfileRating

        """
        resource = f"/profile/wow/character/{realm_slug}/{character_name}/mythic-keystone-profile"

        query_params = {}
        if season_id is not None:
            query_params["season"] = season_id

        return self._get_data(
            resource, region, locale, namespace=f"profile-{region}", **query_params
        )

    def get_character_character_mythic_keystone_season_details(
        self,
        region: RegionType,
        locale: str,
        realm_slug: str,
        character_name: str,
        season_id: Optional[int] = None,
    ) -> custom_types.CharacterMythicKeystoneSeasonDetails:
        """
        Returns the Mythic Keystone season details for a character.
        Returns a 404 Not Found for characters that have not yet completed a Mythic Keystone dungeon for the specified season.

        Args:
            region (RegionType): The region of the data to retrieve.
            locale (str): The locale to use for the request.
            realm_slug (str): The slug of the realm the character is on.
            character_name (str): The name of the character to retrieve data for.
            season_id (int): The ID of the season to retrieve data for.

        Returns:
            CharacterMythicKeystoneSeasonDetails: A dictionary representing the character's Mythic Keystone season details.
            _links: Links
            current_period: CharacterMythicKeystoneProfileCurrentPeriod
            seasons: List[GenericID]
            character: KeyValue
            current_mythic_rating: CharacterMythicKeystoneProfileRating
        """
        resource = f"/profile/wow/character/{realm_slug}/{character_name}/mythic-keystone-profile/season/{season_id}"
        query_params = {}
        if season_id is not None:
            query_params["season"] = season_id

        return self._get_data(
            resource, region, locale, namespace=f"profile-{region}", **query_params
        )

    def get_character_mythic_keystone_rating(
        self,
        region: RegionType,
        locale: str,
        realm_slug: str,
        character_name: str,
        season_id: int,
        round_result: bool = True,
    ) -> Union[float, int]:
        """
        Returns the character's current-season M+ rating.

        Args:
            region (RegionType): The region of the data to retrieve.
            locale (str): The locale to use for the request.
            realm_slug (str): The slug of the realm the character is on.
            character_name (str): The name of the character to retrieve data for.

        Returns:
            float: The character's current-season M+ rating, or 0 if not available.
        """
        character_mythic_plus_summary = (
            self.get_character_character_mythic_keystone_profile_index(
                region, locale, realm_slug, character_name, season_id
            )
        )

        current_rating = character_mythic_plus_summary.get(
            "current_mythic_rating", {}
        ).get("rating", 0)

        if round_result:
            return round(current_rating)
        else:
            return current_rating

    # Character Professions API

    def get_character_professions_summary(
        self, region: RegionType, locale: str, realm_slug: str, character_name: str
    ) -> custom_types.CharacterProfessionsSummary:
        """
        Returns a summary of professions for a character.

        Args:
            region (RegionType): The region of the data to retrieve.
            locale (str): The locale to use for the request.
            realm_slug (str): The slug of the realm the character is on.
            character_name (str): The name of the character to retrieve data for.

        Returns:
            CharacterProfessionsSummary: A dictionary representing the character's professions summary.
            _links: Links
            character: CharacterAchievementStatisticsCharacterReference
            primaries: List[CharacterProfessionsSummaryPrimaries]
            secondaries: List[CharacterProfessionsSummarySecondaries]
        """
        resource = f"/profile/wow/character/{realm_slug}/{character_name}/professions"
        return self._get_data(resource, region, locale, namespace=f"profile-{region}")

    # Character Profile API

    def get_character_profile_summary(
        self, region: RegionType, locale: str, realm_slug: str, character_name: str
    ) -> custom_types.CharacterProfileSummary:
        """
        Returns a profile summary for a character.


        Args:
            region (RegionType): The region of the data to retrieve.
            locale (str): The locale to use for the request.
            realm_slug (str): The slug of the realm the character is on.
            character_name (str): The name of the character to retrieve data for.

        Returns:
            CharacterProfileSummary: A dictionary representing the character's profile summary.
            _links: Links
            id: int
            name: str
            gender: GenericType
            faction: FactionType
            race: KeyValue
            character_class: KeyValue
            active_spec: KeyValue
            realm: Realm
            guild: Optional['CharacterProfileSummaryGuild']
            level: int
            experience: int
            achievement_points: int
            achievements: Link
            titles: Link
            pvp_summary: Link
            encounters: Link
            media: Link
            last_login_timestamp: int
            average_item_level: int
            equipped_item_level: int
            specializations: Link
            statistics: Link
            mythic_keystone_profile: Link
            equipment: Link
            appearance: Link
            collections: Link
            active_title: Optional['CharacterProfileSummaryTitle']
            reputations: Link
            quests: Link
            achievements_statistics: Link
            professions: Link
            covenant_progress: Optional['CharacterProfileSummaryCovenantProgress']
            name_search: str
        """
        resource = f"/profile/wow/character/{realm_slug}/{character_name}/"
        return self._get_data(resource, region, locale, namespace=f"profile-{region}")

    def get_character_profile_status(
        self, region: RegionType, locale: str, realm_slug: str, character_name: str
    ) -> custom_types.CharacterProfileSummary:
        """
        Returns the status and a unique ID for a character. A client should delete information about a character from their application if any of the following conditions occur:

            an HTTP 404 Not Found error is returned
            the is_valid value is false
            the returned character ID doesn't match the previously recorded value for the character

        The following example illustrates how to use this endpoint:

            A client requests and stores information about a character, including its unique character ID and the timestamp of the request.
            After 30 days, the client makes a request to the status endpoint to verify if the character information is still valid.
            If character cannot be found, is not valid, or the characters IDs do not match, the client removes the information from their application.
            If the character is valid and the character IDs match, the client retains the data for another 30 days.

        Args:
            region (RegionType): The region of the data to retrieve.
            locale (str): The locale to use for the request.
            realm_slug (str): The slug of the realm the character is on.
            character_name (str): The name of the character to retrieve data for.

        Returns:
            CharacterProfileStatus: A dictionary representing the character's profile status.
            _links: Links
            id: int
            is_valid: bool
        """
        resource = f"/profile/wow/character/{realm_slug}/{character_name}/status"
        return self._get_data(resource, region, locale, namespace=f"profile-{region}")

    # Character PvP API

    def get_character_pvp_bracket_statistics(
        self,
        region: RegionType,
        locale: str,
        realm_slug: str,
        character_name: str,
        pvp_bracket: Optional[str] = None,
    ) -> custom_types.CharacterPvPBracketStatistics:
        """
        Returns the PvP bracket statistics for a character.

        Args:
            region (RegionType): The region of the data to retrieve.
            locale (str): The locale to use for the request.
            realm_slug (str): The slug of the realm the character is on.
            character_name (str): The name of the character to retrieve data for.
            pvp_bracket (str): The PvP bracket to retrieve statistics for. Valid values are 2v2, 3v3, etc.

        Returns:
            CharacterPvPBracketStatistics: A dictionary representing the character's PvP bracket statistics.
            _links: Links
            character: CharacterAchievementStatisticsCharacterReference
            faction: GenericType
            bracket: PvPSeasonLeaderboardBracket
            rating: int
            season: GenericID
            tier: GenericID
            season_match_statistics: CharacterPvPBracketStatisticsBreakdown
            weekly_match_statistics: CharacterPvPBracketStatisticsBreakdown
        """

        query_params = {}
        if pvp_bracket is not None:
            query_params["pvp_bracket"] = pvp_bracket

        resource = f"/profile/wow/character/{realm_slug}/{character_name}/pvp-bracket/{pvp_bracket}"
        return self._get_data(
            resource, region, locale, namespace=f"profile-{region}", **query_params
        )

    def get_character_pvp_summary(
        self, region: RegionType, locale: str, realm_slug: str, character_name: str
    ) -> custom_types.CharacterPvPSummary:
        """
        Returns a PvP summary for a character.

        Args:
            region (RegionType): The region of the data to retrieve.
            locale (str): The locale to use for the request.
            realm_slug (str): The slug of the realm the character is on.
            character_name (str): The name of the character to retrieve data for.

        Returns:
            CharacterPvPSummary: A dictionary representing the character's PvP summary.
            _links: Links
            honor_level: int
            pvp_map_statistics: List[CharacterPvPSummaryMapStatistics]
            honorable_kills: int
            character: CharacterAchievementStatisticsCharacterReference
        """
        resource = f"/profile/wow/character/{realm_slug}/{character_name}/pvp-summary"
        return self._get_data(resource, region, locale, namespace=f"profile-{region}")

    # Character Quests API

    def get_character_quests(
        self, region: RegionType, locale: str, realm_slug: str, character_name: str
    ) -> custom_types.CharacterQuests:
        """
        Returns a character's active quests as well as a link to the character's completed quests.

        Args:
            region (RegionType): The region of the data to retrieve.
            locale (str): The locale to use for the request.
            realm_slug (str): The slug of the realm the character is on.
            character_name (str): The name of the character to retrieve data for.

        Returns:
            CharacterQuests: A dictionary representing the character's quests.
            _links: Links
            character: CharacterAchievementStatisticsCharacterReference
            in_progress: List[KeyValue]
            completed: Link
        """
        resource = f"/profile/wow/character/{realm_slug}/{character_name}/quests"
        return self._get_data(resource, region, locale, namespace=f"profile-{region}")

    def get_character_completed_quests(
        self, region: RegionType, locale: str, realm_slug: str, character_name: str
    ) -> custom_types.CharacterCompletedQuests:
        """
        Returns a list of quests that a character has completed.

        Args:
            region (RegionType): The region of the data to retrieve.
            locale (str): The locale to use for the request.
            realm_slug (str): The slug of the realm the character is on.
            character_name (str): The name of the character to retrieve data for.

        Returns:
            CharacterCompletedQuests: A dictionary representing the character's completed quests.
            _links: Links
            character: CharacterAchievementStatisticsCharacterReference
            quests: List[KeyValue]
        """
        resource = (
            f"/profile/wow/character/{realm_slug}/{character_name}/quests/completed"
        )
        return self._get_data(resource, region, locale, namespace=f"profile-{region}")

    # Character Reputations API

    def get_character_reputations_summary(
        self, region: RegionType, locale: str, realm_slug: str, character_name: str
    ) -> custom_types.CharacterReputations:
        """
        Returns a summary of a character's reputations.

        Args:
            region (RegionType): The region of the data to retrieve.
            locale (str): The locale to use for the request.
            realm_slug (str): The slug of the realm the character is on.
            character_name (str): The name of the character to retrieve data for.

        Returns:
            CharacterReputations: A dictionary representing the character's reputations.
            _links: Links
            character: CharacterAchievementStatisticsCharacterReference
            reputations: List[CharacterReputationsReference]
        """
        resource = f"/profile/wow/character/{realm_slug}/{character_name}/reputations"
        return self._get_data(resource, region, locale, namespace=f"profile-{region}")

    # Character Soulbinds API

    def get_character_soulbinds(
        self, region: RegionType, locale: str, realm_slug: str, character_name: str
    ) -> custom_types.CharacterSoulbinds:
        """
        Returns a character's soulbinds.

        Args:
            region (RegionType): The region of the data to retrieve.
            locale (str): The locale to use for the request.
            realm_slug (str): The slug of the realm the character is on.
            character_name (str): The name of the character to retrieve data for.

        Returns:
            CharacterSoulbinds: A dictionary representing the character's soulbinds.
            _links: Links
            character: CharacterAchievementStatisticsCharacterReference
            chosen_covenant: KeyValue
            renown_level: int
        """
        resource = f"/profile/wow/character/{realm_slug}/{character_name}/soulbinds"
        return self._get_data(resource, region, locale, namespace=f"profile-{region}")

    # Character Specializations API

    def get_character_specializations_summary(
        self, region: RegionType, locale: str, realm_slug: str, character_name: str
    ) -> custom_types.CharacterSpecializationsSummary:
        """
        Returns a summary of a character's specializations.

        Args:
            region (RegionType): The region of the data to retrieve.
            locale (str): The locale to use for the request.
            realm_slug (str): The slug of the realm the character is on.
            character_name (str): The name of the character to retrieve data for.

        Returns:
            CharacterSpecializationsSummary: A dictionary representing the character's specializations.
            _links: Links
            specializations: List['Specialization']
            active_specialization: KeyValue
            character: CharacterReference
            active_hero_talent: Optional[dict]
        """
        resource = (
            f"/profile/wow/character/{realm_slug}/{character_name}/specializations"
        )
        return self._get_data(resource, region, locale, namespace=f"profile-{region}")

    # Character Statistics API

    def get_character_statistics_summary(
        self, region: RegionType, locale: str, realm_slug: str, character_name: str
    ) -> custom_types.CharacterStatisticsSummary:
        """
        Returns a statistics summary for a character.

        Args:
            region (RegionType): The region of the data to retrieve.
            locale (str): The locale to use for the request.
            realm_slug (str): The slug of the realm the character is on.
            character_name (str): The name of the character to retrieve data for.

        Returns:
            CharacterStatisticsSummary: A dictionary representing the character's statistics summary.
            _links: Links
            health: int
            power: int
            power_type: KeyValue
            speed: CharacterStatisticsSummaryValue
            strength: CharacterStatisticsSummaryEffective
            agility: CharacterStatisticsSummaryEffective
            intellect: CharacterStatisticsSummaryEffective
            stamina: CharacterStatisticsSummaryEffective
            melee_crit: CharacterStatisticsSummaryValue
            melee_haste: CharacterStatisticsSummaryValue
            mastery: CharacterStatisticsSummaryValue
            bonus_armor: int
            lifesteal: CharacterStatisticsSummaryValue
            versatility: int
            versatility_damage_done_bonus: float
            versatility_healing_done_bonus: float
            versatility_damage_taken_bonus: float
            avoidance: CharacterStatisticsSummaryValue
            attack_power: int
            main_hand_damage_min: float
            main_hand_damage_max: float
            main_hand_speed: float
            main_hand_dps: float
            off_hand_damage_min: float
            off_hand_damage_max: float
            off_hand_speed: float
            off_hand_dps: float
            spell_power: int
            spell_penetration: int
            spell_crit: CharacterStatisticsSummaryValue
            mana_regen: int
            mana_regen_combat: int
            armor: CharacterStatisticsSummaryEffective
            dodge: CharacterStatisticsSummaryValue
            parry: CharacterStatisticsSummaryValue
            block: CharacterStatisticsSummaryValue
            ranged_crit: CharacterStatisticsSummaryValue
            ranged_haste: CharacterStatisticsSummaryValue
            spell_haste: CharacterStatisticsSummaryValue
            character: CharacterReference
        """
        resource = f"/profile/wow/character/{realm_slug}/{character_name}/statistics"
        return self._get_data(resource, region, locale, namespace=f"profile-{region}")

    # Character Titles API

    def get_character_titles_summary(
        self, region: RegionType, locale: str, realm_slug: str, character_name: str
    ) -> custom_types.CharacterSpecializationsSummary:
        """
        Returns a summary of titles a character has obtained.

        Args:
            region (RegionType): The region of the data to retrieve.
            locale (str): The locale to use for the request.
            realm_slug (str): The slug of the realm the character is on.
            character_name (str): The name of the character to retrieve data for.

        Returns:
            CharacterTitlesSummary: A dictionary representing the character's titles.
            _links: Links
            character: CharacterReference
            active_title: CharacterProfileSummaryTitle
            titles: List[KeyValue]
        """
        resource = f"/profile/wow/character/{realm_slug}/{character_name}/titles"
        return self._get_data(resource, region, locale, namespace=f"profile-{region}")

    # Guild API

    def get_guild(
        self, region: RegionType, locale: str, realm_slug: str, guild_name_slug: str
    ) -> custom_types.Guild:
        """
        Returns a single guild by its name and realm.

        Args:
            region (RegionType): The region of the data to retrieve.
            locale (str): The locale to use for the request.
            realm_slug (str): The slug of the realm the character is on.
            character_name (str): The name of the character to retrieve data for.
            guild_name_slug (str): The slug of the guild to retrieve data for.

        Returns:
            Guild: A dictionary representing the guild.
            _links: Links
            id: int
            name: str
            faction: FactionType
            achievement_points: int
            member_count: int
            realm: GuildRealm
            crest: GuildCrest
            roster: Link
            achievements: Link
            created_timestamp: int
            activity: Link
            name_search: str
        """
        resource = f"/data/wow/guild/{realm_slug}/{guild_name_slug}"
        return self._get_data(resource, region, locale, namespace=f"profile-{region}")

    def get_guild_activity(
        self, region: RegionType, locale: str, realm_slug: str, guild_name_slug: str
    ) -> custom_types.GuildActivity:
        """
        Returns a single guild's activity by name and realm.

        Args:
            region (RegionType): The region of the data to retrieve.
            locale (str): The locale to use for the request.
            realm_slug (str): The slug of the realm the character is on.
            character_name (str): The name of the character to retrieve data for.
            guild_name_slug (str): The slug of the guild to retrieve data for.

        Returns:
            GuildActivity: A dictionary representing the guild's activity.
            _links: Links
            guild: GuildActivityGuild
            activities: List[GuildActivities]
        """
        resource = f"/data/wow/guild/{realm_slug}/{guild_name_slug}/activity"
        return self._get_data(resource, region, locale, namespace=f"profile-{region}")

    def get_guild_achievements(
        self, region: RegionType, locale: str, realm_slug: str, guild_name_slug: str
    ) -> custom_types.GuildAchievements:
        """
        Returns a single guild's activity by name and realm.

        Args:
            region (RegionType): The region of the data to retrieve.
            locale (str): The locale to use for the request.
            realm_slug (str): The slug of the realm the character is on.
            character_name (str): The name of the character to retrieve data for.
            guild_name_slug (str): The slug of the guild to retrieve data for.

        Returns:
            GuildAchievements: A dictionary representing the guild's achievements.
            _links: Links
            guild: GuildActivityGuild
            activities: List[GuildActivities]
        """
        resource = f"/data/wow/guild/{realm_slug}/{guild_name_slug}/achievements"
        return self._get_data(resource, region, locale, namespace=f"profile-{region}")

    def get_guild_roster(
        self, region: RegionType, locale: str, realm_slug: str, guild_name_slug: str
    ) -> custom_types.GuildRoster:
        """
        Returns a single guild's activity by name and realm.

        Args:
            region (RegionType): The region of the data to retrieve.
            locale (str): The locale to use for the request.
            realm_slug (str): The slug of the realm the character is on.
            character_name (str): The name of the character to retrieve data for.
            guild_name_slug (str): The slug of the guild to retrieve data for.

        Returns:
            GuildActivity: A dictionary representing the guild's activity.
            _links: Links
            guild: GuildActivityGuild
            activities: List[GuildActivities]
        """
        resource = f"/data/wow/guild/{realm_slug}/{guild_name_slug}/roster"
        return self._get_data(resource, region, locale, namespace=f"profile-{region}")
