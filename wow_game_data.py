from dataclasses import dataclass, field
from typing import Any, Optional, Dict, List, Callable, Literal
from api import Api
from urllib.parse import urlencode
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


class SearchQuery:
    def __init__(self):
        self.params: Dict[str, Any] = {}

    def add_field(self, field: str, value: Any):
        self.params[field] = value
        return self

    def add_or(self, field: str, values: List[Any]):
        self.params[field] = "||".join(map(str, values))
        return self

    def add_not(self, field: str, value: Any):
        self.params[f"{field}!"] = value
        return self

    def add_range(self, field: str, min_value: Optional[Any] = None, max_value: Optional[Any] = None, inclusive: bool = True):
        brackets = "[]" if inclusive else "()"
        range_value = f"{brackets[0]}{min_value or ''},{max_value or ''}{brackets[1]}"
        self.params[field] = range_value
        return self

    def set_page(self, page: int):
        self.params['_page'] = page
        return self

    def set_page_size(self, page_size: int):
        self.params['_pageSize'] = page_size
        return self

    def set_order(self, *fields: str):
        self.params['orderby'] = ",".join(fields)
        return self

    def build(self) -> str:
        return urlencode(self.params)

@dataclass
class WowGameDataApi:
    """
    All World of Warcraft Game Data API methods.

    This class provides methods to interact with the World of Warcraft Game Data API.
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
    def __enter__(self) -> "WowGameDataApi":
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
        self, resource: str, region: custom_types.RegionType, locale: str, **kwargs
    ) -> Dict[str, Any]:
        query_params = {"locale": locale, **kwargs}
        return self.api.get(resource, region, params=query_params)

    # Achievements API

    def get_achievements_index(
        self, region: custom_types.RegionType, locale: str
    ) -> custom_types.AchievementIndex:
        """
        Retrieve an index of achievements.

        Args:
            region (RegionType): The region of the data to retrieve.
            locale (str): The locale to use for the request.

        Returns:
            AchievementIndex: An AchievementIndex dictionary containing the a list of AchievementIndexEntries in the index.
            _links: Links
            achievements: List[KeyValue]
        """
        resource = "/data/wow/achievement/index"
        return self._get_data(resource, region, locale, namespace=f"profile-{region}")

    def get_achievement(
        self, region: custom_types.RegionType, locale: str, achievement_id: int
    ) -> custom_types.Achievement:
        """
        Return an achievement by ID.

        Args:
            region (RegionType): The region of the data to retrieve.
            locale (str): The locale to use for the request.
            achievement_id (int): The ID of the achievement to retrieve.

        Returns:
            Achievement: An Achievement dictionary containing the achievement data.
            _links: Links
            id: int
            category: KeyValue
            name: str
            description: str
            points: int
            is_account_wide: bool
            criteria: Criteria
            media: Media
            display_order: int
        """
        resource = f"/data/wow/achievement/{achievement_id}"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_achievement_media(
        self, region: str, locale: str, achievement_id: int
    ) -> custom_types.AchievementMedia:
        """
        Returns media for an achievement by ID.

        Args:
            region (RegionType): The region of the data to retrieve.
            locale (str): The locale to use for the request.
            achievement_id (int): The ID of the achievement to retrieve.

        Returns:
            AchievementMedia: An AchievementMedia object containing the media data.
            _links: Links
            assets: List[Asset]
            id: int
        """
        resource = f"/data/wow/media/achievement/{achievement_id}"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_achievement_categories_index(
        self, region: str, locale: str
    ) -> custom_types.AchievementCategoriesIndex:
        """
        Return an achievement category index.

        Args:
            region (RegionType): The region of the data to retrieve.
            locale (str): The locale to use for the request.

        Returns:
            AchievementCategoryIndex: An AchievementCategory object containing the achievement category data.
        """
        resource = "/data/wow/achievement-category/index"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_achievement_category(
        self, region: str, locale: str, achievement_category_id: int
    ) -> custom_types.AchievementCategory:
        """
        Return an achievement category by ID.

        Args:
            region (RegionType): The region of the data to retrieve.
            locale (str): The locale to use for the request.
            achievement_category_id (int): The ID of the achievement to retrieve.

        Returns:
            AchievementCategory: An AchievementCategory dictionary containing the achievement category data.
            _links: Links
            id: int
            name: str
            achievements: List[KeyValue]
            subcategories: List[KeyValue]
            is_guild_category: bool
            aggregates_by_faction: AggregatesByFaction
            display_order: int
        """
        resource = f"/data/wow/achievement-category/{achievement_category_id}"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    # Auction House API

    def get_auction_house_index(
        self, region: str, locale: str, connected_realm_id: int
    ):
        """*CLASSIC ONLY*
        Returns an index of auction houses for a connected realm.
        """
        resource = f"/data/wow/connected-realm/{connected_realm_id}/auctions/index"

        return self._get_data(
            resource, region, locale, namespace=f"dynamic-classic-{region}"
        )

    def get_auctions_for_auction_house(
        self, region: str, locale: str, connected_realm_id: int, auction_house_id: int
    ):
        """*CLASSIC ONLY*
        Returns all active auctions for a specific auction house on a connected realm.
        """
        resource = f"/data/wow/connected-realm/{connected_realm_id}/auctions/{auction_house_id}"

        return self._get_data(
            resource, region, locale, namespace=f"dynamic-classic-{region}"
        )

    def get_auctions(
        self, region: str, locale: str, connected_realm_id: int
    ) -> custom_types.Auctions:
        """
        This method fetches the current auction house data for the specified
        connected realm in the given region.

        Args:
            region (RegionType): The region of the connected realm. Valid values are
                'us', 'eu', 'kr', and 'tw'.
            locale (str): The locale to use for the request. For example, 'en_US',
                'es_MX', 'fr_FR'.
            connected_realm_id (int): The ID of the connected realm.

        Returns:
            Auctions: A dictionary containing the auction house data. The
            structure of this dictionary depends on the Blizzard API response.
            These fields could be present:
                id: int
                item: Item
                quantity: int
                unit_price: Optional[int]
                time_left: str
                bid: Optional[int]
                buyout: Optional[int]
                pet: Optional[Pet]
        """
        resource = f"/data/wow/connected-realm/{connected_realm_id}/auctions"

        return self._get_data(resource, region, locale, namespace=f"dynamic-{region}")

    def get_commodities(self, region: str, locale: str) -> custom_types.Auctions:
        """Returns all active auctions for commodity items for the entire game region.

        Args:
            region (RegionType): The region of the connected realm. Valid values are
                'us', 'eu', 'kr', and 'tw'.
            locale (str): The locale to use for the request. For example, 'en_US',
                'es_MX', 'fr_FR'.

        Returns:
            Auctions: A dictionary containing the auction house data. The
            structure of this dictionary depends on the Blizzard API response.
            These fields could be present:
                id: int
                item: Item
                quantity: int
                unit_price: Optional[int]
                time_left: str
                bid: Optional[int]
                buyout: Optional[int]
        """
        resource = f"/data/wow/auctions/commodities"

        return self._get_data(resource, region, locale, namespace=f"dynamic-{region}")

    # Azerite Essence API

    def get_azerite_essences_index(
        self, region: str, locale: str
    ) -> custom_types.AzeriteEssencesIndex:
        """Returns an index of azerite essences.

        Args:
            region (RegionType): The region of the connected realm. Valid values are
                'us', 'eu', 'kr', and 'tw'.
            locale (str): The locale to use for the request. For example, 'en_US',
                'es_MX', 'fr_FR'.

        Returns:
            AzeriteEssencesIndex: A dictionary containing Azertie Essences data.
            _links: Links
            azerite_essences: List[KeyValue]
        """
        resource = "/data/wow/azerite-essence/index"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_azerite_essence_media(
        self, region: str, locale: str, azerite_essence_id: int
    ) -> custom_types.GenericMedia:
        """Returns an Azerite essence's media information by ID.

        Args:
            region (RegionType): The region of the connected realm. Valid values are
                'us', 'eu', 'kr', and 'tw'.
            locale (str): The locale to use for the request. For example, 'en_US',
                'es_MX', 'fr_FR'.
            azerite_essence_id (int): The ID of the Azerite essence.

        Returns:
            GenericMedia: A dictionary containing Azerite Essence media data.
            _links: Links
            assets: List[Asset]
            id: int
        """
        resource = f"/data/wow/media/azerite-essence/{azerite_essence_id}"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_connected_realms_index(
        self, region: str, locale: str, is_classic: bool = False
    ) -> custom_types.ConnectedRealmsIndex:
        """Returns an index of connected realms.

        Args:
            region (RegionType): The region of the connected realm. Valid values are
                'us', 'eu', 'kr', and 'tw'.
            locale (str): The locale to use for the request. For example, 'en_US',
                'es_MX', 'fr_FR'.

        Returns:
            ConnectedRealmsIndex: A dictionary containing a list of connected realm links.
            _links: Links
            connected_realms: List[Link]
        """
        resource = "/data/wow/connected-realm/index"
        namespace = f"dynamic-classic-{region}" if is_classic else f"dynamic-{region}"

        return self._get_data(resource, region, locale, namespace=namespace)

    def get_connected_realm(
        self,
        region: str,
        locale: str,
        connected_realm_id: int,
        is_classic: bool = False,
    ) -> custom_types.ConnectedRealm:
        """Returns a connected realm by ID.

        Args:
            region (RegionType): The region of the connected realm. Valid values are
                'us', 'eu', 'kr', and 'tw'.
            locale (str): The locale to use for the request. For example, 'en_US',
                'es_MX', 'fr_FR'.
            connected_realm_id (int): The ID of the connected realm.

        Returns:
            ConnectedRealm: A dictionary containing Azertie Essence media data.
            id: int
            region: KeyValue
            connected_realm: Link
            name: str
            category: str
            locale: str
            timezone: str
            type: ConnectedRealmType
            is_tournament: bool
            slug: str
        """
        resource = f"/data/wow/connected-realm/{connected_realm_id}"
        namespace = f"dynamic-classic-{region}" if is_classic else f"dynamic-{region}"

        return self._get_data(resource, region, locale, namespace=namespace)

    # Covenant API

    def get_covenant_index(
        self, region: str, locale: str
    ) -> custom_types.CovenantIndex:
        """
        Return an index of covenants.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.

        Returns:
            Dict[str, Any]: An index of covenants.
            _links: Links
            covenants: List[KeyValue]
        """
        resource = "/data/wow/covenant/index"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_covenant(
        self, region: str, locale: str, covenant_id: int
    ) -> custom_types.Covenant:
        """
        Return a covenant by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            covenant_id (int): The ID of the covenant.

        Returns:
            Dict[str, Any]: The covenant data.
            _links: dict
            id: int
            name: str
            description: str
            signature_ability: CovenantSignatureAbility
            class_abilities: List[CovenantClassAbility]
            soulbinds: List[KeyValue]
            renown_rewards: List[CovenantRenownReward]
            media: Media
        """
        resource = f"/data/wow/covenant/{covenant_id}"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_covenant_media(
        self, region: str, locale: str, covenant_id: int
    ) -> custom_types.GenericMedia:
        """
        Return media for a covenant by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            covenant_id (int): The ID of the covenant.

        Returns:
            GenericMedia: A dictionary containing the covenant media data.
            key: Link
            id: int
        """
        resource = f"/data/wow/media/covenant/{covenant_id}"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_soulbind_index(
        self, region: str, locale: str
    ) -> custom_types.SoulbindIndex:
        """
        Return an index of soulbinds.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.

        Returns:
            SoulbindIndex: An index of soulbinds.
            _links: Links
            soulbinds: List[KeyValue]
        """
        resource = "/data/wow/covenant/soulbind/index"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_soulbind(
        self, region: str, locale: str, soulbind_id: int
    ) -> custom_types.Soulbind:
        """
        Return a soulbind by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            soulbind_id (int): The ID of the soulbind.

        Returns:
            Soulbind: A dictionary containing the soulbind data.
            _links: Links
            id: int
            name: str
            covenant: SoulbindCovenant
            creature: KeyValue
            follower: SoulbindFollower
            talent_tree: SoulbindTalentTree
        """
        resource = f"/data/wow/covenant/soulbind/{soulbind_id}"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_conduit_index(self, region: str, locale: str) -> custom_types.ConduitIndex:
        """
        Return an index of conduits.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.

        Returns:
            ConduitIndex: A dictionary containing the index of conduits.
            _links: Links
            conduits: List[KeyValue]
        """
        resource = "/data/wow/covenant/conduit/index"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_conduit(
        self, region: str, locale: str, conduit_id: int
    ) -> custom_types.Conduit:
        """
        Return a conduit by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            conduit_id (int): The ID of the conduit.

        Returns:
            Conduit: A dict mapping conduit data.
            _links: Links
            id: int
            name: str
            item: KeyValue
            socket_type: ConduitSocketType
            ranks: List[ConduitRanks]
        """
        resource = f"/data/wow/covenant/conduit/{conduit_id}"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    # Creature API

    def get_creature(
        self, region: str, locale: str, creature_id: int, is_classic: bool = False
    ) -> custom_types.Creature:
        """
        Return a creature by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            creature_id (int): The ID of the creature.

        Returns:
            Creature: A dictionary containing the creature data.
            _links: Links
            id: int
            name: str
            type: KeyValue
            family: KeyValue
            display: list[CreatureDisplays]
        """
        resource = f"/data/wow/creature/{creature_id}"
        namespace = f"static-classic-{region}" if is_classic else f"static-{region}"

        return self._get_data(resource, region, locale, namespace=namespace)

    def get_creature_display_media(
        self,
        region: str,
        locale: str,
        creature_display_id: int,
        is_classic: bool = False,
    ) -> custom_types.GenericMedia:
        """
        Return a creature's media data by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            creature_id (int): The ID of the creature.

        Returns:
            GenericMedia: A dictionary containing the media data.
            key: Link
            id: int
            assets: List[Asset]
        """
        resource = f"/data/wow/media/creature-display/{creature_display_id}"
        return self.api.get(resource, region, locale, namespace=f"static-{region}")

    def get_creature_families_index(
        self, region: str, locale: str, is_classic: bool = False
    ) -> custom_types.CreatureFamilyIndex:
        """
        Return the creature families index.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.

        Returns:
            CreatureFamiliesIndex: A dictionary containing the creature family index.
            _links: Links
            creature_families: List[CreatureFamily]
        """
        resource = "/data/wow/creature-family/index"
        namespace = f"static-classic-{region}" if is_classic else f"static-{region}"

        return self._get_data(resource, region, locale, namespace=namespace)

    def get_creature_family(
        self,
        region: str,
        locale: str,
        creature_family_id: int,
        is_classic: bool = False,
    ) -> custom_types.CreatureFamily:
        """
        Return the creature family by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            creature_family_id (int): The ID of the creature family.

        Returns:
            CreatureFamily: A dictionary containing the creature family data.
            _links: Links
            id: int
            name: str
            specialization: CreatureSpecialization
            media: Media
        """
        resource = f"/data/wow/creature-family/{creature_family_id}"
        namespace = f"static-classic-{region}" if is_classic else f"static-{region}"

        return self._get_data(resource, region, locale, namespace=namespace)

    def get_creature_family_media(
        self,
        region: str,
        locale: str,
        creature_family_id: int,
        is_classic: bool = False,
    ) -> custom_types.GenericMedia:
        """
        Return the creature family media by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            creature_family_id (int): The ID of the creature family.

        Returns:
            GenericMedia: A dictionary containing the creature family media data.
            key: Link
            id: int
            assets: List[Asset]
        """
        resource = f"/data/wow/media/creature-family/{creature_family_id}"
        namespace = f"static-classic-{region}" if is_classic else f"static-{region}"

        return self._get_data(resource, region, locale, namespace=namespace)

    def get_creature_types_index(
        self, region: str, locale: str, is_classic: bool = False
    ) -> custom_types.CreatureTypeIndex:
        """
        Return the creature type index.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.

        Returns:
            CreatureTypeIndex: A dictionary containing the creature family media data.
            _links: Links
            creature_types: List[KeyValue]
        """
        resource = "/data/wow/creature-type/index"
        namespace = f"static-classic-{region}" if is_classic else f"static-{region}"

        return self._get_data(resource, region, locale, namespace=namespace)

    def get_creature_type(
        self, region: str, locale: str, creature_type_id: int, is_classic: bool = False
    ) -> custom_types.KeyValue:
        """
        Return the creature type by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            creature_type_id (int): The ID of the creature type.

        Returns:
            CreatureType: A dictionary containing the creature type data.
            key: Link
            name: str
            id: int
        """
        resource = f"/data/wow/creature-type/{creature_type_id}"
        namespace = f"static-classic-{region}" if is_classic else f"static-{region}"

        return self._get_data(resource, region, locale, namespace=namespace)

    # Guild Crest API

    def get_guild_crest_components_index(
        self, region: str, locale: str, is_classic: bool = False
    ) -> custom_types.GuildCrestComponentsIndex:
        """
        Return the guild crest components index.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.

        Returns:
            GuildCrestComponentsIndex: A dictionary containing the guild crest component data.
            _links: Links
            emblems: List[Emblem]
            borders: List[GuildCrestBorder]
            colors: GuildCrestColors
        """
        resource = "/data/wow/guild-crest/index"
        namespace = f"static-classic-{region}" if is_classic else f"static-{region}"

        return self._get_data(resource, region, locale, namespace=namespace)

    def get_guild_crest_border_media(
        self, region: str, locale: str, border_id: int, is_classic: bool = False
    ) -> custom_types.GenericMedia:
        """
        Return the guild crest border media by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            border_id (int): The ID of the guild crest border.

        Returns:
            GenericMedia: A dictionary containing the guild crest component media data.
            _links: Links
            emblems: List[GuildCrestEmblem]
            borders: List[GuildCrestBorder]
            colors: GuildCrestColors
        """
        resource = f"/data/wow/media/guild-crest/border/{border_id}"
        namespace = f"static-classic-{region}" if is_classic else f"static-{region}"

        return self._get_data(resource, region, locale, namespace=namespace)

    def get_guild_crest_emblem_media(
        self, region: str, locale: str, emblem_id: int, is_classic: bool = False
    ) -> custom_types.GenericMedia:
        """
        Return the guild crest border media by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            border_id (int): The ID of the guild crest border.

        Returns:
            GenericMedia: A dictionary containing the guild crest emblem media.
            _links: Links
            assets: List[Asset]
            id: int
        """
        resource = f"/data/wow/media/guild-crest/emblem/{emblem_id}"
        namespace = f"static-classic-{region}" if is_classic else f"static-{region}"

        return self._get_data(resource, region, locale, namespace=namespace)

    # Heirloom API

    def get_heirloom_index(
        self, region: str, locale: str
    ) -> custom_types.HeirloomIndex:
        """
        Return the heirloom index.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.

        Returns:
            HeirloomIndex: A dictionary containing the heirloom index.
            _links: Links
            heirlooms: List[KeyValue]
        """
        resource = "/data/wow/heirloom/index"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_heirloom(
        self, region: str, locale: str, heirloom_id: int
    ) -> custom_types.Heirloom:
        """
        Return an heirloom by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            heirloom_id (int): The ID of the heirloom.

        Returns:
            Heirloom: A dictionary containing the heirloom data.
            _links: Links
            id: int
            item: KeyValue
            source: HeirloomSource
            source_description: str
            upgrades: List[HeirloomUpgrade]
            media: KeyValue
        """
        resource = f"/data/wow/heirloom/{heirloom_id}"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    # Item API

    def get_item(
        self, region: str, locale: str, item_id: int, is_classic: bool = False
    ) -> custom_types.Item:
        """
        Return an item by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            item_id (int): The ID of the item.

        Returns:
            Item: A dictionary containing the item data.
            _links: Links
            id: int
            name: str
            quality: ItemQuality
            level: int
            required_level: int
            media: KeyValue
            item_class: ItemClass
            item_subclass: ItemSubclass
            inventory_type: InventoryType
            purchase_price: int
            sell_price: int
            max_count: int
            is_equippable: bool
            is_stackable: bool
            preview_item: ItemPreview
            purchase_quantity: int
            appearances: List[ItemAppearance]
        """
        resource = f"/data/wow/item/{item_id}"
        namespace = f"static-classic-{region}" if is_classic else f"static-{region}"

        return self._get_data(resource, region, locale, namespace=namespace)

    def get_item_media(
        self, region: str, locale: str, item_id: int, is_classic: bool = False
    ) -> custom_types.GenericMedia:
        """
        Return item media by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            item_id (int): The ID of the item.

        Returns:
            GenericMedia: A dictionary containing the item media data.
            _links: Links
            assets: List[Asset]
            id: int
        """
        resource = f"/data/wow/media/item/{item_id}"
        namespace = f"static-classic-{region}" if is_classic else f"static-{region}"

        return self._get_data(resource, region, locale, namespace=namespace)

    def get_item_classes_index(
        self, region: str, locale: str, is_classic: bool = False
    ) -> custom_types.ItemClassesIndex:
        """
        Return the item classes index.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.

        Returns:
            ItemClassesIndex: A dictionary containing the item index data.
            _links: Links
            item_classes: List[KeyValue]
        """
        resource = "/data/wow/item-class/index"
        namespace = f"static-classic-{region}" if is_classic else f"static-{region}"

        return self._get_data(resource, region, locale, namespace=namespace)

    def get_item_class(
        self, region: str, locale: str, item_class_id: int, is_classic: bool = False
    ) -> custom_types.ItemClass:
        """
        Return an item class by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            item_class_id (int): The ID of the item class.

        Returns:
            ItemClass: A dictionary containing the item class data.
            _links: Links
            id: int
            name: str
            subclasses: List[KeyValue]
        """
        resource = f"/data/wow/item-class/{item_class_id}"
        namespace = f"static-classic-{region}" if is_classic else f"static-{region}"

        return self._get_data(resource, region, locale, namespace=namespace)

    def get_item_sets_index(
        self, region: str, locale: str, is_classic: bool = False
    ) -> custom_types.ItemSetsIndex:
        """
        Return the item sets index.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.

        Returns:
            ItemSetsIndex: A dictionary containing the item sets index.
            _links: Links
            item_sets: List[KeyValue]
        """
        resource = "/data/wow/item-set/index"
        namespace = f"static-classic-{region}" if is_classic else f"static-{region}"

        return self._get_data(resource, region, locale, namespace=namespace)

    def get_item_set(
        self, region: str, locale: str, item_set_id: int, is_classic: bool = False
    ) -> custom_types.ItemSet:
        """
        Return an item set by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            item_set_id (int): The ID of the item set.

        Returns:
            ItemSet: A dictionary containing the item set data.
            _links: Links
            id: int
            name: str
            items: List[KeyValue]
            effects: List[ItemSetEffect]
            is_effect_active: bool
        """
        resource = f"/data/wow/item-set/{item_set_id}"
        namespace = f"static-classic-{region}" if is_classic else f"static-{region}"

        return self._get_data(resource, region, locale, namespace=namespace)

    def get_item_subclass(
        self,
        region: str,
        locale: str,
        item_class_id: int,
        item_subclass_id: int,
        is_classic: bool = False,
    ) -> custom_types.ItemSubclass:
        """
        Return an item subclass by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            item_set_id (int): The ID of the item set.
            item_subclass_id (int): The ID of the item subclass.

        Returns:
        ItemSubclass: A dictionary containing the item subclass data.
        _links: Links
        class_id: int
        subclass_id: int
        display_name: str
        hide_subclass_in_tooltips: bool
        """
        resource = (
            f"/data/wow/item-class/{item_class_id}/item-subclass/{item_subclass_id}"
        )
        namespace = f"static-classic-{region}" if is_classic else f"static-{region}"

        return self._get_data(resource, region, locale, namespace=namespace)

    # Item Appearance API

    def get_item_appearance(
        self, region: str, locale: str, appearance_id: int, is_classic: bool = False
    ) -> custom_types.ItemAppearance:
        """
        Return an item appearamce by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            appearance_id (int): The ID of the item appearance.

        Returns:
            ItemAppearance: A dictionary containing the item appearance data.
            _links: Links
            id: int
            slot: Item
            item_class: KeyValue
            item_subclass: KeyValue
            item_display_info_id: int
            items: List[KeyValue]
            media: GenericMedia
        """
        resource = f"/data/wow/item-appearance/{appearance_id}"
        namespace = f"static-classic-{region}" if is_classic else f"static-{region}"

        return self._get_data(resource, region, locale, namespace=namespace)

    def get_item_appearance_sets_index(
        self, region: str, locale: str, is_classic: bool = False
    ) -> custom_types.IteamAppearanceSetsIndex:
        """
        Return an item appearamce by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.

        Returns:
            ItemAppearanceSetsIndex: A dictionary containing the item appearance set index.
            _links: Links
            appearance_sets: List[KeyValue]
        """
        resource = f"/data/wow/item-appearance/set/index"
        namespace = f"static-classic-{region}" if is_classic else f"static-{region}"

        return self._get_data(resource, region, locale, namespace=namespace)

    def get_item_appearance_set(
        self, region: str, locale: str, appearance_set_id: int, is_classic: bool = False
    ) -> custom_types.ItemAppearanceSet:
        """
        Return an item appearance set by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            appearance_set_id (int): The ID of the item appearance set.

        Returns:
            ItemAppearanceSet: A dictionary containing the item appearance set data.
            _links: Links
            id: int
            set_name: str
            appearances: List[GenericID]
        """
        resource = f"/data/wow/item-appearance/set/{appearance_set_id}"
        namespace = f"static-classic-{region}" if is_classic else f"static-{region}"

        return self._get_data(resource, region, locale, namespace=namespace)

    def get_item_appearance_slot_index(self, region: str, locale: str) -> List[str]:
        """
        Return the item appearance slot index.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.

        Returns:
            List[str]: A list of item appearance slots.
        """
        item_appearance_slot_index = [
            "HEAD",
            "SHOULDER",
            "CHEST",
            "BODY",
            "WAIST",
            "LEGS",
            "FEET",
            "WRIST",
            "HAND",
            "BACK",
            "WEAPON",
            "SHIELD",
            "RANGED",
            "CLOAK",
            "TWOHWEAPON",
            "TABARD",
            "ROBE",
            "WEAPONMAINHAND",
            "EQUIPABLESPELL_WEAPON",
            "WEAPONOFFHAND",
            "HOLDABLE",
            "AMMO",
            "RANGEDRIGHT",
            "PROFESSION_TOOL",
            "PROFESSION_GEAR",
        ]
        return item_appearance_slot_index

    def get_item_appearance_slot(
        self, region: str, locale: str, slot_type: str, is_classic: bool = False
    ) -> custom_types.ItemAppearanceSlot:
        """
        Return the item appearance slot by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            slot_type (str): The type of the item appearance slot.
            Must be in list of item_appearance_slot_index.

        Returns:
            ItemAppearanceSlotIndex: A dictionary containing the item appearance slot index.
            _links: Links
            slots: List[ItemAppearaceSlotIndexReference]
        """
        resource = f"/data/wow/item-appearance/slot/{slot_type.upper()}"
        namespace = f"static-classic-{region}" if is_classic else f"static-{region}"

        return self._get_data(resource, region, locale, namespace=namespace)

    # Journal API

    def get_journal_expansions_index(
        self, region: str, locale: str
    ) -> custom_types.JournalExpansionsIndex:
        """
        Return the journal expansions index.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.

        Returns:
            JournalExpasionsIndex: A dictionary containing the item appearance slot index.
            _links: Links
            tiers: List[KeyValue]
        """
        resource = "/data/wow/journal-expansion/index"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_journal_expansion(
        self, region: str, locale: str, journal_expansion_id: int
    ) -> custom_types.JournalExpansion:
        """
        Return the journal expansions index.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            journal_expansion_id (int): The ID of the journal expansion.

        Returns:
            JournalExpansion: A dictionary containing the item appearance slot index.
            _links: Links
            id: int
            name: str
            dungeons: List[KeyValue]
            raids: List[KeyValue]
        """
        resource = f"/data/wow/journal-expansion/{journal_expansion_id}"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_journal_encounters_index(
        self, region: str, locale: str
    ) -> custom_types.JournalEncountersIndex:
        """
        Return the journal encounters index.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.

        Returns:
            JournalEncountersIndex: A dictionary containing the journal encounters index.
            _links: Links
            name: str
            id: int
            encounters: List[KeyValue]
        """
        resource = "/data/wow/journal-encounter/index"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_journal_encounter(
        self, region: str, locale: str, journal_encounter_id: int
    ) -> custom_types.JournalEncounter:
        """
        Return a journal encounter by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            journal_encounter_id (int): The ID of the journal encounter.

        Returns:
            JournalEncounter: A dictionary containing the journal encounter data.
            _links: Links
            id: int
            name: str
            description: str
            creatures: List[Creature]
            items: List[GenericID]
            sections: List[Section]
            instance: KeyValue
            category: GenericType
            modes: List[GenericType]
        """
        resource = f"/data/wow/journal-encounter/{journal_encounter_id}"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_journal_instances_index(
        self, region: str, locale: str
    ) -> custom_types.JournalInstancesIndex:
        """
        Return the journal instances index.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.

        Returns:
            _links: Links
            instances: List[KeyValue]
        """
        resource = "/data/wow/journal-instance/index"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_journal_instance(
        self, region: str, locale: str, journal_instance_id: int
    ) -> custom_types.JournalInstance:
        """
        Return the journal instances data by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            journal_instance_id (int): The ID of the journal instance.

        Returns:
            JournalInstance: A dictionary containing the journal instance data.
            _links: Links
            id: int
            name: str
            map: GenericID
            area: GenericID
            description: str
            encounters: List[GenericID]
            expansion: KeyValue
            location: KeyValue
            modes: list[JournalInstanceMode]
            media: GenericID
            minimum_level: int
            category: Dict[str, str]
            order_index: int
        """
        resource = f"/data/wow/journal-instance/{journal_instance_id}"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_journal_instance_media(
        self, region: str, locale: str, journal_instance_id: int
    ) -> custom_types.JournalInstanceMedia:
        """
        Return the journal instance media data by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            journal_instance_id (int): The ID of the journal instance.

        Returns:
            JournalInstanceMedia: A dictionary containing the journal instance media data.
            _links: Links
            assets: List[JournalInstanceMediaAsset]
        """
        resource = f"/data/wow/media/journal-instance/{journal_instance_id}"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    # Modified Cradting API

    def get_modified_crafting_index(
        self, region: str, locale: str
    ) -> custom_types.ModifiedCraftingIndex:
        """
        Return the modified crafting index.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.

        Returns:
            ModifiedCraftingIndex: A dictionary containing the modified crafting index.
            _links: Links
            categories: Link
            slot_types: Link
        """
        resource = "/data/wow/modified-crafting/index"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_modified_crafting_category_index(
        self, region: str, locale: str
    ) -> custom_types.ModifiedCraftingCategoryIndex:
        """
        Return the modified crafting category index.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.

        Returns:
            ModifiedCraftingCategoryIndex: A dictionary containing the modified crafting category index.
            _links: Links
            categories: list[KeyValue]
        """
        resource = "/data/wow/modified-crafting/category/index"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_modified_crafting_category(
        self, region: str, locale: str, category_id: int
    ) -> custom_types.ModifiedCraftingCategory:
        """
        Return the modified crafting category index.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            category_id (int): The ID of the modified crafting category.

        Returns:
            ModifiedCraftingCategory: A dictionary containing the modified crafting category data.
            _links: Links
            id: int
            name: str
        """
        resource = f"/data/wow/modified-crafting/category/{category_id}"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_modified_crafting_reagent_slot_type_index(
        self, region: str, locale: str
    ) -> custom_types.ModifiedCraftingSlotTypeIndex:
        """
        Return the modified crafting category index.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            category_id (int): The ID of the modified crafting category.

        Returns:
            ModifiedCraftingReagentSlotTypeIndex: A dictionary containing the modified crafting category reagent slot type idex.
            _links: Links
            slot_types: list[KeyValue]
        """
        resource = "/data/wow/modified-crafting/reagent-slot-type/index"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_modified_crafting_reagent_slot_type(
        self, region: str, locale: str, slot_type_id: int
    ) -> Dict[str, Any]:
        """
        Return the modified crafting reagent slot type by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            slot_type_id (int): The ID of the modified reagent slot type.

        Returns:
            ModifiedCraftingReagentSlotTypex: A dictionary containing the modified crafting category reagent slot type data.
            _links: Links
            id: int
            description: str
            compatible_categories: list[KeyValue]
        """
        resource = f"/data/wow/modified-crafting/reagent-slot-type/{slot_type_id}"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    # Mount API

    def get_mounts_index(self, region: str, locale: str) -> custom_types.MountsIndex:
        """
        Return the mounts index.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.

        Returns:
            MountsIndex: A dictionary containing the mounts index.
            _links: Links
            mounts: List[KeyValue]
        """
        resource = "/data/wow/mount/index"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_mount(self, region: str, locale: str, mount_id: int) -> custom_types.Mount:
        """
        Return a mount by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            mount_id (int): The ID of the mount.

        Returns:
            Mount: A dictionary containing the mount data.
            _links: Links
            id: int
            name: str
            creature_displays: List[GenericID]
            description: str
            source: GenericType
            faction: FactionType
            requirements: Requirements
        """
        resource = f"/data/wow/mount/{mount_id}"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    # Mythic Keystone Affix API

    def get_mythic_keystone_affixes_index(
        self, region: str, locale: str
    ) -> custom_types.MythicKeystoneAffixesIndex:
        """
        Return the mythic keystone affixes index.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.

        Returns:
            MythicKeystoneAffixesIndex: A dictionary containing the affix index.
            _links: Links
            affixes: List[KeyValue]
        """
        resource = "/data/wow/keystone-affix/index"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_mythic_keystone_affix(
        self, region: str, locale: str, keystone_affix_id: int
    ) -> custom_types.MythicKeystoneAffix:
        """
        Return a mythic keystone affixes by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            keystone_affix_id (int): The ID of the keystone affix.

        Returns:
            MythicKeystoneAffix: A dictionary containing the affix data.
            _links: Links
            id: int
            name: str
            description: str
            media: GenericID
        """
        resource = f"/data/wow/keystone-affix/{keystone_affix_id}"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_mythic_keystone_affix_media(
        self, region: str, locale: str, keystone_affix_id: int
    ) -> custom_types.MythicKeyStoneAffixMedia:
        """
        Return mythic keystone affix media by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            keystone_affix_id (int): The ID of the keystone affix.

        Returns:
            MythicKeystoneAffixMedia: A dictionary containing the affix data.
            _links: Links
            assets: List[Asset]

        """
        resource = f"/data/wow/media/keystone-affix/{keystone_affix_id}"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    # Mythic Keystone Dungeon API

    def get_mythic_keystone_dungeons_index(
        self, region: str, locale: str
    ) -> custom_types.MythicKeystoneIndex:
        """
        Return the mythic keystone index.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.

        Returns:
            MythicKeystoneIndex: A dictionary containing the mythic keystone index.
            _links: Links
            seasons: Link
            dungeons: Link
        """
        resource = "/data/wow/mythic-keystone/dungeon/index"

        return self._get_data(resource, region, locale, namespace=f"dynamic-{region}")

    def get_mythic_keystone_dungeon(
        self, region: str, locale: str, dungeon_id: int
    ) -> custom_types.MythicKeystoneDungeon:
        """
        Return a mythic keystone dungeon by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            dungeon_id (int): The ID of the dungeon.

        Returns:
            MythicKeystoneDungeon: A dictionary containing the mythic keystone dungeon data.
            _links: Links
            id: int
            name: str
            map: GenericID
            zone: Zone
            dungeon: KeyValue
            keystone_upgrades: List[KeystoneUpgrade]
            is_tracked: bool
        """
        resource = f"/data/wow/mythic-keystone/dungeon/{dungeon_id}"

        return self._get_data(resource, region, locale, namespace=f"dynamic-{region}")

    def get_mythic_keystone_periods_index(
        self, region: str, locale: str
    ) -> custom_types.MythicKeystonePeriodsIndex:
        """
        Return the mythic keystone periods index.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.

        Returns:
            MythicKeystonePeriodsIndex: A dictionary containing the mythic keystone periods index.
            _links: Links
            periods: List[KeyValue]
        """
        resource = "/data/wow/mythic-keystone/period/index"

        return self._get_data(resource, region, locale, namespace=f"dynamic-{region}")

    def get_mythic_keystone_period(
        self, region: str, locale: str, period_id: int
    ) -> custom_types.MythicKeystonePeriod:
        """
        Return a mythic keystone dungeon by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            period_id (int): The ID of the period.

        Returns:
            MythicKeystoneDungeon: A dictionary containing the mythic keystone dungeon data.
            _links: Links
            id: int
            start_timestamp: int (unix timestamp)
            end_timestamp: int (unix timestamp)
        """
        resource = f"/data/wow/mythic-keystone/period/{period_id}"

        return self._get_data(resource, region, locale, namespace=f"dynamic-{region}")

    def get_mythic_keystone_seasons_index(
        self, region: str, locale: str
    ) -> custom_types.MythicKeystoneSeasonsIndex:
        """
        Returns the mythic keystone seasons index.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            period_id (int): The ID of the period.

        Returns:
            MythicKeystoneSeasonsIndex: A dictionary containing the mythic keystone seasons index.
            _links: Links
            seasons: List[KeyValue]
        """
        resource = "/data/wow/mythic-keystone/season/index"

        return self._get_data(resource, region, locale, namespace=f"dynamic-{region}")

    def get_mythic_keystone_season(
        self, region: str, locale: str, season_id: int
    ) -> custom_types.MythicKeystoneSeason:
        """
        Returns the mythic keystone seasons index.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            season_id (int): The ID of the season.

        Returns:
            MythicKeystoneSeason: A dictionary containing the mythic keystone season data.
            _links: Links
            id: int
            start_timestamp: int (unix timestamp)
            end_timestamp: int (unix timestamp)
            periods: list[KeyValue]
            season_name: str
        """
        resource = f"/data/wow/mythic-keystone/season/{season_id}"

        return self._get_data(resource, region, locale, namespace=f"dynamic-{region}")

    # Mythic Keystone Leaderboard API

    def get_mythic_keystone_leaderboards_index(
        self, region: str, locale: str, connected_realm_id: int
    ) -> custom_types.MythicKeystoneLeaderboardsIndex:
        """
        Returns an index of Mythic Keystone Leaderboard dungeon instances for a connected realm.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            connected_realm_id (int): The ID of the connected realm.

        Returns:
            MythicKeystoneLeaderboardsIndex: A dictionary containing the mythic keystone leaderboards index.
            _links: Links
            current_leaderboards: list[KeyValue]
        """
        resource = (
            f"/data/wow/connected-realm/{connected_realm_id}/mythic-leaderboard/index"
        )

        return self._get_data(resource, region, locale, namespace=f"dynamic-{region}")

    def get_mythic_keystone_leaderboard(
        self,
        region: str,
        locale: str,
        connected_realm_id: int,
        dungeon_id: int,
        period_id: int,
    ) -> custom_types.MythicKeystoneLeaderboard:
        """
        Returns a weekly Mythic Keystone Leaderboard by period.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            connected_realm_id (int): The ID of the connected realm.
            dungeon_id (int): The ID of the dungeon.
            period_id (int): The ID of the period.

        Returns:
            MythicKeystoneLeaderboard: A dictionary containing the mythic keystone leaderboard weekly data.
            _links: Links
            map: MythicKeystoneLeaderboardMap
            period: int
            period_start_timestamp: int
            period_end_timestamp: int
            connected_realm: ConnectedRealm
            leading_groups: List[MythicKeystoneLeaderboardLeadingGroup]
            keystone_affixes: List[MythicKeystoneLeaderboardAffixDetail]
            map_challenge_mode_id: int
            name: str
        """
        resource = f"/data/wow/connected-realm/{connected_realm_id}/mythic-leaderboard/{dungeon_id}/period/{period_id}"

        return self._get_data(resource, region, locale, namespace=f"dynamic-{region}")

    # Mythic Raid Leaderboard API

    def get_mythic_raid_leaderboard(
        self, region: str, locale: str, raid: str, faction: str
    ) -> custom_types.MythicRaidLeaderboard:
        """
        Returns a weekly Mythic Keystone Leaderboard by period.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            raid (str): The raid name. Only raids from Battle for Azeroth and newer are supported.
                example: "nyalotha-the-waking-city", "castle-nathria", "sanctum-of-domination",
            faction (str): The faction name ("horde" or "alliance").

        Returns:
            MythicRaidLeaderboard: A dictionary containing the mythic keystone leaderboard weekly data.
            _links: Links
            map: MythicKeystoneLeaderboardMap
            period: int
            period_start_timestamp: int
            period_end_timestamp: int
            connected_realm: ConnectedRealm
            leading_groups: List[MythicKeystoneLeaderboardLeadingGroup]
            keystone_affixes: List[MythicKeystoneLeaderboardAffixDetail]
            map_challenge_mode_id: int
            name: str
        """
        resource = f"/data/wow/leaderboard/hall-of-fame/{raid}/{faction.lower()}"

        return self._get_data(resource, region, locale, namespace=f"dynamic-{region}")

    # Pet API

    def get_pets_index(self, region: str, locale: str) -> custom_types.PetsIndex:
        """
        Returns the battle pets index.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.

        Returns:
            PetsIndex: A dictionary containing the pets index.
            _links: Links
            pets: List[KeyValue]
        """
        resource = "/data/wow/pet/index"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_pet(self, region: str, locale: str, pet_id: int) -> custom_types.Pet:
        """
        Returns a battle pet by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            pet_id (int): The ID of the pet.

        Returns:
            Pet: A dictionary containing the pet data.
            _links: Links
            id: int
            name: str
            battle_pet_type: BattlePetType
            description: str
            is_capturable: bool
            is_tradable: bool
            is_battlepet: bool
            is_alliance_only: bool
            is_horde_only: bool
            abilities: List[BattlePetAbility]
            source: GenericType
            icon: str
            creature: Creature
            is_random_creature_display: bool
            media: GenericID
        """
        resource = f"/data/wow/pet/{pet_id}"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_pet_media(
        self, region: str, locale: str, pet_id: int
    ) -> custom_types.GenericMedia:
        """
        Returns media for a battle pet by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            pet_id (int): The ID of the pet.

        Returns:
            GenericMedia: A dictionary containing the pet media data.
            _links: Links
            assets: List[Asset]
            id: int
        """
        resource = f"/data/wow/media/pet/{pet_id}"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_pet_abilities_index(
        self, region: str, locale: str
    ) -> custom_types.PetAbilitiesIndex:
        """
        Returns an index of pet abilities.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.

        Returns:
            PetAbilitiesIndex: A dictionary containing the pet abilities index.
            _links: Links
            abilities: List[KeyValue]
        """
        resource = "/data/wow/pet-ability/index"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_pet_ability(
        self, region: str, locale: str, pet_ability_id: int
    ) -> custom_types.PetAbility:
        """
        Returns a pet ability by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            pet_ability_id (int): The ID of the pet ability.

        Returns:
            PetAbility: A dictionary containing the pet ability data.
            _links: Links
            id: int
            name: str
            battle_pet_type: BattlePetType
            rounds: int
            media: GenericID
        """
        resource = f"/data/wow/pet-ability/{pet_ability_id}"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_pet_ability_media(
        self, region: str, locale: str, pet_ability_id: int
    ) -> custom_types.GenericMedia:
        """
        Returns media for a pet ability by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            pet_ability_id (int): The ID of the pet ability.

        Returns:
            GenericMedia: A dictionary containing the pet ability media data.
            _links: Links
            assets: List[Asset]
            id: int
        """
        resource = f"/data/wow/media/pet-ability/{pet_ability_id}"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    # Playable Class API

    def get_playable_classes_index(
        self, region: str, locale: str, is_classic: bool = False
    ) -> custom_types.PlayableClassesIndex:
        """
        Returns an index of playable classes.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.

        Returns:
            PlayableClassesIndex: A dictionary containing the playable class index.
            _links: Links
            classes: List[KeyValue]
        """
        resource = "/data/wow/playable-class/index"
        namespace = f"static-classic-{region}" if is_classic else f"static-{region}"

        return self._get_data(resource, region, locale, namespace=namespace)

    def get_playable_class(
        self, region: str, locale: str, class_id: int, is_classic: bool = False
    ) -> custom_types.PlayableClass:
        """
        Return a playable class by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            class_id (int): The ID of the playable class.

        Returns:
            PlayableClass: A dictionary containing the playable class data.
            _links: Links
            id: int
            name: str
            gender: PlayableClassGender
            power_type: KeyValue
            specializations: List[KeyValue]
            media: GenericID
            pvp_talent_slots: Link
            playable_races: List[KeyValue]
            additional_power_types: List[KeyValue]
        """
        resource = f"/data/wow/playable-class/{class_id}"
        namespace = f"static-classic-{region}" if is_classic else f"static-{region}"

        return self._get_data(resource, region, locale, namespace=namespace)

    def get_playable_class_media(
        self,
        region: str,
        locale: str,
        class_id: int,
        is_classic: bool = False,
    ) -> custom_types.GenericMedia:
        """
        Return media for a playable class by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            class_id (int): The ID of the playable class.

        Returns:
            GenericMeida: A dictionary containing the playable class data.
            _links: Links
            id: int
            name: str
            gender: PlayableClassGender
            power_type: KeyValue
            specializations: List[KeyValue]
            media: GenericID
            pvp_talent_slots: Link
            playable_races: List[KeyValue]
            additional_power_types: List[KeyValue]
        """
        resource = f"/data/wow/media/playable-class/{class_id}"
        namespace = f"static-classic-{region}" if is_classic else f"static-{region}"

        return self._get_data(resource, region, locale, namespace=namespace)

    def get_pvp_talent_slots(
        self, region: str, locale: str, class_id: int
    ) -> custom_types.PvPTalentSlots:
        """
        Return the PvP talent slots for a playable class by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            class_id (int): The ID of the playable class.

        Returns:
            PvPTalentSlots: A dictionary containing the PvP talent slots for a given class.
            _links: Links
            id: int
            talent_slots: List[PvPTalentSlotReference]
        """
        resource = f"/data/wow/playable-class/{class_id}/pvp-talent-slots"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    # Playable Race API

    def get_playable_races_index(
        self, region: str, locale: str, is_classic: bool = False
    ) -> custom_types.PlayableRacesIndex:
        """
        Return an index of playable races.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.

        Returns:
            PlayableRacesIndex: A dictionary containing the playable races index.
            _links: Links
            races: List[KeyValue]
            id: int
            name: str
        """
        resource = "/data/wow/playable-race/index"
        namespace = f"static-classic-{region}" if is_classic else f"static-{region}"

        return self._get_data(resource, region, locale, namespace=namespace)

    def get_playable_race(
        self, region: str, locale: str, playable_race_id: int, is_classic: bool = False
    ) -> custom_types.PlayableRace:
        """
        Return a playable race by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            playable_race_id: The ID of the playable race.

        Returns:
            PlayableRaces: A dictionary containing the playable race data.
            _links: Links
            id: int
            name: str
            gender_name: PlayableClassGender
            is_selectable: bool
            is_allied_race: bool
            playable_classes: List[KeyValue]
        """
        resource = f"/data/wow/playable-race/{playable_race_id}"
        namespace = f"static-classic-{region}" if is_classic else f"static-{region}"

        return self._get_data(resource, region, locale, namespace=namespace)

    # Playable Specialization API

    def get_playable_specializations_index(
        self, region: str, locale: str
    ) -> custom_types.PlayableSpecializationsIndex:
        """
        Return an index of playable specializations.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.

        Returns:
            PlayableRaces: A dictionary containing the playable race data.
            _links: Links
            id: int
            name: str
            gender_name: PlayableClassGender
            is_selectable: bool
            is_allied_race: bool
            playable_classes: List[KeyValue]
        """
        resource = "/data/wow/playable-specialization/index"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_playable_specialization(
        self, region: str, locale: str, spec_id: int
    ) -> custom_types.PlayableSpecialization:
        """
        Return a playable specialization by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            spec_id: The ID of the playable specialization.

        Returns:
            GenericMedia: A dictionary containing the playable spec data.
            _links: Links
            id: int
            playable_class: KeyValue
            name: str
            gender_description: PlayableClassGender
            media: GenericID
            role: GenericType
            pvp_talents: list[PvPTalent]
            spec_talent_tree: GenericType
            power_type: KeyValue
            primary_stat_type: GenericType
            hero_talent_trees: List[KeyValue]
        """
        resource = f"/data/wow/playable-specialization/{spec_id}"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_playable_specialization_media(
        self, region: str, locale: str, spec_id: int
    ) -> custom_types.GenericMedia:
        """
        Return media for a playable specialization by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            spec_id: The ID of the playable specialization.

        Returns:
            GenericMedia: A dictionary containing the playable spec data.
            _links: Links
            assets: List[Asset]
            id: int
        """
        resource = f"/data/wow/media/playable-specialization/{spec_id}"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    # Power Type API

    def get_power_types_index(
        self, region: str, locale: str, is_classic: bool = False
    ) -> custom_types.PowerTypesIndex:
        """
        Return an index of power types.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.

        Returns:
            PowerTypesIndex: A dictionary containing the power types index.
            _links: Links
            power_types: List[KeyValue]
        """
        resource = "/data/wow/power-type/index"
        namespace = f"static-classic-{region}" if is_classic else f"static-{region}"

        return self._get_data(resource, region, locale, namespace=namespace)

    def get_power_type(
        self, region: str, locale: str, power_type_id: int, is_classic: bool = False
    ) -> custom_types.PowerType:
        """
        Return a power type by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            power_type_id: The ID of the power type.

        Returns:
            PowerTypes: A dictionary containing the power type data.
            _links: Links
            power_types: List[KeyValue]
        """
        resource = f"/data/wow/power-type/{power_type_id}"
        namespace = f"static-classic-{region}" if is_classic else f"static-{region}"

        return self._get_data(resource, region, locale, namespace=namespace)

    # Profession API

    def get_professions_index(
        self, region: str, locale: str
    ) -> custom_types.ProfessionsIndex:
        """
        Return an index of professions.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.

        Returns:
            ProfessionsIndex: A dictionary containing the professions index.
            _links: Links
            professions: List[KeyValue]
        """
        resource = "/data/wow/profession/index"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_profession(
        self, region: str, locale: str, profession_id: int
    ) -> custom_types.Profession:
        """
        Return a profession by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            profession_id (int): The ID of the profession.

        Returns:
            Profession: A dictionary containing the profession data.
            _links: Links
            id: int
            name: str
            description: str
            type: GenericType
            media: GenericID
            skill_tiers: List[KeyValue]
        """
        resource = f"/data/wow/profession/{profession_id}"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_profession_media(
        self, region: str, locale: str, profession_id: int
    ) -> custom_types.GenericMedia:
        """
        Return media for a profession by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            profession_id (int): The ID of the profession.

        Returns:
            GenericMedia: A dictionary containing the profession media data.
            _links: Links
            assets: List[Asset]
            id: int
        """
        resource = f"/data/wow/media/profession/{profession_id}"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_profession_skill_tier(
        self, region: str, locale: str, profession_id: int, skill_tier_id: int
    ) -> custom_types.ProfessionSkillTier:
        """
        Return a skill tier for a profession by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            profession_id (int): The ID of the profession.

        Returns:
            ProfessionSkillTier: A dictionary containing the profession skill data.
            _links: Links
            id: int
            name: str
            minimum_skill_level: int
            maximum_skill_level: int
            categories: List[ProfessionSkillTierCategories]
        """
        resource = f"/data/wow/profession/{profession_id}/skill-tier/{skill_tier_id}"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_recipe(
        self, region: str, locale: str, recipe_id: int
    ) -> custom_types.Recipe:
        """
        Return a recipe by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            recipe_id (int): The ID of the recipe.

        Returns:
            Recipe: A dictionary containing the recipe data.
            _links: Links
            id: int
            name: str
            media: GenericID
            crafted_item: KeyValue
            reagents: List[KeyValue]
            crafted_quantity: Dict[str, int]

        """
        resource = f"/data/wow/recipe/{recipe_id}"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_recipe_media(
        self, region: str, locale: str, recipe_id: int
    ) -> custom_types.GenericMedia:
        """
        Return media for a recipe by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            recipe_id (int): The ID of the recipe.

        Returns:
            GenericMedia: A dictionary containing the recipe media data.
            _links: Links
            assets: List[Asset]
            id: int
        """
        resource = f"/data/wow/media/recipe/{recipe_id}"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    # Pvp Season API

    def get_pvp_seasons_index(
        self, region: str, locale: str
    ) -> custom_types.PvPSeasonsIndex:
        """
        Return an index of PvP seasons.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.

        Returns:
            PvPSeasonsIndex: A dictionary containing the PvP seasons index.
            _links: Links
            seasons: List[GenericID]
            current_season: GenericID
        """
        resource = "/data/wow/pvp-season/index"

        return self._get_data(resource, region, locale, namespace=f"dynamic-{region}")

    def get_pvp_season(
        self, region: str, locale: str, pvp_season_id: int
    ) -> custom_types.PvPSeason:
        """
        Return a Pvp season by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            pvp_season_id (int): The ID of the Pvp season.

        Returns:
            PvPSeason: A dictionary containing the PvP season data.
            _links: Links
            id: int
            leaderboards: Link
            rewards: Link
            start_timestamp: int
            end_timestamp: int
        """
        resource = f"/data/wow/pvp-season/{pvp_season_id}"

        return self._get_data(resource, region, locale, namespace=f"dynamic-{region}")

    def get_pvp_leaderboards_index(
        self, region: str, locale: str, pvp_season_id: int
    ) -> custom_types.PvPSeasonLeaderboardsIndex:
        """
        Return an index of Pvp leaderboards for a Pvp season.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.

        Returns:
            PvPSeasonLeaderboardsIndex: A dictionary containing the PvP season leaderboards index.
            _links: Links
            season: GenericID
            leaderboards: List[KeyValue]
        """
        resource = f"/data/wow/pvp-season/{pvp_season_id}/pvp-leaderboard/index"

        return self._get_data(resource, region, locale, namespace=f"dynamic-{region}")

    def get_pvp_leaderboard(
        self, region: str, locale: str, pvp_season_id: int, pvp_bracket: str
    ) -> custom_types.PvPSeasonLeaderboard:
        """
        Return the Pvp leaderboard of a specific Pvp bracket for a Pvp season.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            pvp_season_id (int): The ID of the Pvp season.
            pvp_bracket (str): The Pvp bracket. Example: "2v2", "3v3", "rbg".

        Returns:
            PvPSeasonLeaderboard: A dictionary containing the PvP season leaderboard data.
            _links: Links
            season: GenericID
            leaderboards: List[KeyValue]
        """
        resource = f"/data/wow/pvp-season/{pvp_season_id}/pvp-leaderboard/{pvp_bracket}"

        return self._get_data(resource, region, locale, namespace=f"dynamic-{region}")

    def get_pvp_rewards_index(
        self, region: str, locale: str, pvp_season_id: int
    ) -> custom_types.PvPRewardsIndex:
        """
        Return an index of Pvp rewards for a Pvp season.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.

        Returns:
            PvPRewardsIndex: A dictionary containing the PvP season rewards index.
            _links: Links
            season: GenericID
            rewards: List[PvPSeasonRewardsIndexRewards]
        """
        resource = f"/data/wow/pvp-season/{pvp_season_id}/pvp-reward/index"

        return self._get_data(resource, region, locale, namespace=f"dynamic-{region}")

    # Pvp Tier API

    def get_pvp_tiers_index(
        self, region: str, locale: str
    ) -> custom_types.PvPTiersIndex:
        """
        Return an index of Pvp tiers.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.

        Returns:
            PvPTiersIndex: A dictionary containing the PvP tiers index.
            _links: Links
            tiers: List[KeyValue]
        """
        resource = "/data/wow/pvp-tier/index"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_pvp_tier(
        self, region: str, locale: str, pvp_tier_id: int
    ) -> custom_types.PvPTier:
        """
        Return a Pvp tier by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.

        Returns:
            PvPTier: A dictionary containing the PvP tier data.
            _links: Links
            id: int
            name: str
            min_rating: int
            max_rating: int
            media: GenericID
            bracket: GenericType
            rating_type: int
        """
        resource = f"/data/wow/pvp-tier/{pvp_tier_id}"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_pvp_tier_media(
        self, region: str, locale: str, pvp_tier_id: int
    ) -> custom_types.GenericMedia:
        """
        Return media for a Pvp tier by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            pvp_tier_id (int): The ID of the Pvp tier.

        Returns:
            GenericMedia: A dictionary containing the Pvp tier media data.
            _links: Links
            assets: List[Asset]
            id: int
        """
        resource = f"/data/wow/media/pvp-tier/{pvp_tier_id}"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    # Quest API

    def get_quests_index(self, region: str, locale: str) -> custom_types.QuestsIndex:
        """
        Return the parent index for quests.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.

        Returns:
            QuestsIndex: A dictionary containing the quests index.
            _links: Links
            categories: Link
            areas: Link
            types: Link
        """
        resource = "/data/wow/quest/index"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_quest(self, region: str, locale: str, quest_id: int) -> custom_types.Quest:
        """
        Return a quest by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            quest_id (int): The ID of the quest.

        Returns:
            Quest: A dictionary containing the quest data.
            _links: Links
            id: int
            title: str
            area: KeyValue
            description: str
            requirements: QuestRequirements
            rewards: QuestRewards
        """
        resource = f"/data/wow/quest/{quest_id}"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_quest_categories_index(
        self, region: str, locale: str
    ) -> custom_types.QuestCategoriesIndex:
        """
        Return an index of quest categories (such as quests for a specific class, profession, or storyline).

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.

        Returns:
            QuestCategoriesIndex: A dictionary containing the quest categories index.
            _links: Links
            categories: List[KeyValue]
        """
        resource = "/data/wow/quest/category/index"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_quest_category(
        self, region: str, locale: str, quest_category_id: int
    ) -> custom_types.QuestCategory:
        """
        Return a quest category by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            quest_category_id (int): The ID of the quest category.

        Returns:
            QuestCategory: A dictionary containing the quest category data.
            _links: Links
            id: int
            category: str
            quests: List[KeyValue]
        """
        resource = f"/data/wow/quest/category/{quest_category_id}"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_quest_areas_index(
        self, region: str, locale: str
    ) -> custom_types.QuestAreasIndex:
        """
        Return an index of quest areas.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.

        Returns:
            QuestAreasIndex: A dictionary containing the quest areas index.
            _links: Links
            areas: List[KeyValue]
        """
        resource = "/data/wow/quest/area/index"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_quest_area(
        self, region: str, locale: str, quest_area_id: int
    ) -> custom_types.QuestArea:
        """
        Return a quest area by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            quest_area_id (int): The ID of the quest area.

        Returns:
            QuestArea: A dictionary containing the quest area data.
            _links: Links
            id: int
            area: str
            quests: List[KeyValue]
        """
        resource = f"/data/wow/quest/area/{quest_area_id}"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_quest_types_index(
        self, region: str, locale: str
    ) -> custom_types.QuestTypesIndex:
        """
        Return an index of quest types (such as Pvp quests, raid quests, or account quests).

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.

        Returns:
            QuestTypesIndex: A dictionary containing the quest types index.
            _links: Links
            types: List[KeyValue]
        """
        resource = "/data/wow/quest/type/index"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_quest_type(
        self, region: str, locale: str, quest_type_id: int
    ) -> custom_types.QuestType:
        """
        Return a quest type by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.

        Returns:
            QuestType: A dictionary containing the quest type data.
            _links: Links
            id: int
            type: str
            quests: List[KeyValue]
        """
        resource = f"/data/wow/quest/type/{quest_type_id}"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    # Realm API

    def get_realms_index(
        self, region: str, locale: str, is_classic: bool = False
    ) -> custom_types.RealmsIndex:
        """
        Return an index of realms.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.

        Returns:
            RealmsIndex: A dictionary containing the realms index.
            _links: Links
            realms: List[Link]
        """
        resource = "/data/wow/realm/index"
        namespace = f"dynamic-classic-{region}" if is_classic else f"dynamic-{region}"

        return self._get_data(resource, region, locale, namespace=namespace)

    def get_realm(
        self, region: str, locale: str, realm_slug: str, is_classic: bool = False
    ) -> custom_types.Realm:
        """
        Return a single realm by slug or ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            realm_slug (str): The slug of the realm. Example: "tichondrius", "grizzly-hills", "lightnings-blade"

        Returns:
            Realm: A dictionary containing the realm data.
            _links: Links
            id: int
            region: KeyValue
            connected_realm: Link
            name: str
            category: str
            locale: str
            timezone: str
            type: GenericType
            is_tournament: bool
            slug: str
        """
        resource = f"/data/wow/realm/{realm_slug}"
        namespace = f"dynamic-classic-{region}" if is_classic else f"dynamic-{region}"

        return self._get_data(resource, region, locale, namespace=namespace)

    # Region API

    def get_regions_index(
        self, region: str, locale: str, is_classic: bool = False
    ) -> custom_types.RegionsIndex:
        """
        Return an index of regions.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.

        Returns:
            RegionsIndex: A dictionary containing the regions index.
            _links: Links
            regions: List[Link]
        """
        resource = "/data/wow/region/index"
        namespace = f"dynamic-classic-{region}" if is_classic else f"dynamic-{region}"

        return self._get_data(resource, region, locale, namespace=namespace)

    def get_region(
        self, region: str, locale: str, region_id: int, is_classic: bool = False
    ) -> custom_types.Region:
        """
        Return a region by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            region_id (int): The ID of the region.

        Returns:
            Region: A dictionary containing the region data.
            _links: Links
            id: int
            tag: str
            patch_string: str
        """
        resource = f"/data/wow/region/{region_id}"
        namespace = f"dynamic-classic-{region}" if is_classic else f"dynamic-{region}"

        return self._get_data(resource, region, locale, namespace=namespace)

    # Reputations API

    def get_reputation_factions_index(
        self, region: str, locale: str
    ) -> custom_types.ReputationFactionsIndex:
        """
        Return an index of reputation factions.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.

        Returns:
            ReputationFactionsIndex: A dictionary containing the reputation factions index.
            _links: Links
            factions: List[KeyValue]
        """
        resource = "/data/wow/reputation-faction/index"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_reputation_faction(
        self, region: str, locale: str, reputation_faction_id: int
    ) -> custom_types.ReputationFaction:
        """
        Return a single reputation faction by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            reputation_faction_id (int): The ID of the reputation faction.

        Returns:
            ReputationFaction: A dictionary containing the reputation faction data.
            _links: Links
            id: int
            name: str
            description: str
            reputation_tiers: KeyValue
        """
        resource = f"/data/wow/reputation-faction/{reputation_faction_id}"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_reputation_tiers_index(
        self, region: str, locale: str
    ) -> custom_types.ReputationTiersIndex:
        """
        Return an index of reputation tiers.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.

        Returns:
            ReputationTiersIndex: A dictionary containing the reputation tiers index.
            _links: Links
            reputation_tiers: List[KeyValue]
        """
        resource = "/data/wow/reputation-tiers/index"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_reputation_tier(
        self, region: str, locale: str, reputation_tiers_id: int
    ) -> custom_types.ReputationTier:
        """
        Return a single set of reputation tiers by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            reputation_tiers_id (int): The ID of the reputation tiers.

        Returns:
            ReputationTier: A dictionary containing the reputation tiers data.
            _links: Links
            id: int
            tiers: List[ReputationTierReference]
            faction: KeyValue
        """
        resource = f"/data/wow/reputation-tiers/{reputation_tiers_id}"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    # Spell API

    def get_spell(self, region: str, locale: str, spell_id: int) -> custom_types.Spell:
        """
        Return a spell by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            spell_id (int): The ID of the spell.

        Returns:
            Spell: A dictionary containing the spell data.
            _links: Links
            id: int
            name: str
            description: str
            media: CovenantMedia
        """
        resource = f"/data/wow/spell/{spell_id}"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_spell_media(
        self, region: str, locale: str, spell_id: int
    ) -> custom_types.GenericMedia:
        """
        Return media for a spell by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            spell_id (int): The ID of the spell.

        Returns:
            GenericMedia: A dictionary containing the spell media data.
            _links: Links
            assets: List[Asset]
        """
        resource = f"/data/wow/media/spell/{spell_id}"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    # Talent API

    def get_talents_index(
        self, region: str, locale: str
    ) -> custom_types.TalentTreeIndex:
        """
        Return an index of talents.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.

        Returns:
            TalentTreeIndex: A dictionary containing the talents index.
            _links: Links
            spec_talent_trees: List[KeyValue]
        """
        resource = "/data/wow/talent-tree/index"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_talent_tree(
        self, region: str, locale: str, talent_tree_id: int, spec_id: int
    ) -> custom_types.TalentTree:
        """
        Returns a talent tree by specialization ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            talent_tree_id: The ID of the talent tree.
            spec_id: The ID of the playable specialization.

        Returns:
            TalentTree: A dictionary containing the talent tree data.
            _links: Links
            id: int
            playable_class: KeyValue
            playable_specialization: KeyValue
            name: str
            media: Link
            restriction_lines: List[TalentTreeRestrictionLines]
            class_talent_nodes: List[TalentTreeClassTalentNodes]
            spec_talent_nodes: List[TalentTreeSpecTalentNodes]
            hero_talent_trees: List[TalentTreeHeroTalentTrees]

        """
        resource = (
            f"/data/wow/talent-tree/{talent_tree_id}/playable-specialization/{spec_id}"
        )

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_talent_tree_nodes(
        self, region: str, locale: str, talent_tree_id: int
    ) -> custom_types.TalentTreeNodes:
        """
        Returns all talent tree nodes as well as links to associated playable specializations given a talent tree id.
        This is useful to generate loadout export codes.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            talent_tree_id: The ID of the talent tree.

        Returns:
            TalentTreeNodes: A dictionary containing the talent tree nodes data.
            _links: Links
            id: int
            spec_talent_trees: List[TalentTreeNodesSpecTalentTrees]
            talent_nodes: List[TalentTreeClassTalentNodes]
        """
        resource = f"/data/wow/talent-tree/{talent_tree_id}"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_talents_index(self, region: str, locale: str) -> custom_types.TalentsIndex:
        """
        Return an index of talents.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.

        Returns:
            TalentsIndex: A dictionary containing the talents index.
            _links: Links
            talents: List[KeyValue]
        """
        resource = "/data/wow/talent/index"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_talent(
        self, region: str, locale: str, talent_id: int
    ) -> custom_types.Talent:
        """
        Return a talent by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            talent_id: The ID of the talent.

        Returns:
            Talent: A dictionary containing the Pvp talent data.
            _links: Links
            id: int
            rank_descriptions: List[TalentRankDescriptions]
            spell: KeyValue
            playable_class: KeyValue
            playable_specialization: KeyValue
        """
        resource = f"/data/wow/talent/{talent_id}"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_pvp_talents_index(
        self, region: str, locale: str
    ) -> custom_types.PvPTalentsIndex:
        """
        Returns an index of PvP talents.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.

        Returns:
            PvPTalentsIndex: A dictionary containing the Pvp talents index.
            _links: Links
            talents: List[KeyValue]
        """
        resource = f"/data/wow/pvp-talent/index"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_pvp_talent(
        self, region: str, locale: str, pvp_talent_id: int
    ) -> custom_types.PvPTalent:
        """
        Return a PvP talent by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            pvp_talent_id: The ID of the PvP talent.

        Returns:
            PvPTalent: A dictionary containing the PvP talent data.
            _links: Links
            id: int
            spell: KeyValue
            playable_specialization: KeyValue
            description: str
            unlock_player_level: int
            compatible_slots: list[int]
        """
        resource = f"/data/wow/pvp-talent/{pvp_talent_id}"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    # Tech Talent API

    def get_tech_talent_tree_index(
        self, region: str, locale: str
    ) -> custom_types.TechTalentTreeIndex:
        """
        Returns an index of tech talent trees.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.

        Returns:
            TechTalentTreeIndex: A dictionary containing the tech talent trees index.
            _links: Links
            talent_trees: List[KeyValue]
        """
        resource = "/data/wow/tech-talent-tree/index"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_tech_talent_tree(
        self, region: str, locale: str, tech_talent_tree_id: int
    ) -> custom_types.TechTalentTree:
        """
        Return a tech talent tree by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            tech_talent_tree_id: The ID of the tech talent tree.

        Returns:
            TechTalentTree: A dictionary containing the tech talent tree data.
            _links: Links
            id: int
            max_tiers: int
            talents: List[KeyValue]
        """
        resource = f"/data/wow/tech-talent-tree/{tech_talent_tree_id}"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_tech_talent_index(
        self, region: str, locale: str
    ) -> custom_types.TechTalentIndex:
        """
        Return an index of tech talents.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.

        Returns:
            TechTalentIndex: A dictionary containing the tech talents index.
            _links: Links
            talents: List[KeyValue]
        """
        resource = f"/data/wow/tech-talent/index"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_tech_talent(
        self, region: str, locale: str, tech_talent_id: int
    ) -> custom_types.TechTalent:
        """
        Return a tech talent by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            tech_talent_id: The ID of the tech talent.

        Returns:
            TechTalent: A dictionary containing the tech talent data.
            _links: Links
            id: int
            talent_tree: KeyValue
            name: str
            description: str
            spell_tooltip: TechTalentSpellTooltip
            tier: int
            display_order: int
            prerequisite_talent: KeyValue
            media: GenericID
        """
        resource = f"/data/wow/tech-talent/{tech_talent_id}"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_tech_talent_media(
        self, region: str, locale: str, tech_talent_id: int
    ) -> custom_types.GenericMedia:
        """
        Return media for a tech talent by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            tech_talent_id: The ID of the tech talent.

        Returns:
            GenericMedia: A dictionary containing the tech talent media data.
            _links: Links
            assets: List[Asset]
        """
        resource = f"/data/wow/media/tech-talent/{tech_talent_id}"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    # Title API

    def get_titles_index(self, region: str, locale: str) -> custom_types.TitlesIndex:
        """
        Return an index of titles.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.

        Returns:
            TitlesIndex: A dictionary containing the titles index.
            _links: Links
            titles: List[KeyValue]
        """
        resource = "/data/wow/title/index"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_title(self, region: str, locale: str, title_id: int) -> custom_types.Title:
        """
        Return a title by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            title_id: The ID of the title.

        Returns:
            Title: A dictionary containing the title data.
            _links: Links
            id: int
            name: str
            gender_name: PlayableClassGender
        """
        resource = f"/data/wow/title/{title_id}"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    # Toy API

    def get_toy_index(self, region: str, locale: str) -> custom_types.ToyIndex:
        """
        Return an index of toys.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.

        Returns:
            ToyIndex: A dictionary containing the toys index.
            _links: Links
            toys: List[KeyValue]
        """
        resource = "/data/wow/toy/index"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    def get_toy(self, region: str, locale: str, toy_id: int) -> custom_types.Toy:
        """
        Return a toy by ID.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.

        Returns:
            Toy: A dictionary containing the toy data.
            _links: Links
            id: int
            item: KeyValue
            source: GenericType
            should_exclude_if_uncollected: bool
            media: GenericID
        """
        resource = f"/data/wow/toy/{toy_id}"

        return self._get_data(resource, region, locale, namespace=f"static-{region}")

    # Wow Token API

    def get_token_index(
        self, region: str, locale: str, is_classic: bool = False
    ) -> custom_types.WoWTokenIndex:
        """
        Return the Wow Token index.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.

        Returns:
            WoWTokenIndex: A dictionary containing the Wow Token index.
            _links: Links
            last_updated_timestamp: int (unix timestamp)
            price: int
        """
        resource = "/data/wow/token/index"
        namespace = f"dynamic-classic-{region}" if is_classic else f"dynamic-{region}"

        return self._get_data(resource, region, locale, namespace=namespace)


    def get_token_price(
        self, region: str, locale: str, is_classic: bool = False
    ) -> Dict[str, Optional[str]]:
        """
        Returns the value of a WoW token in a readable format.

        Args:
            region (RegionType): The region of the data to retrieve.
            locale (str): The locale to use for the request.

        Returns:
            Dict[str, Optional[str]]: A dictionary containing the value of the token.
                                      Keys are 'gold', 'silver', and 'copper'.
                                      Values are the corresponding URLs or None if not found.
        """
        token_object = self.get_token_index(region, locale)

        token_price = token_object.get("price")
        
        # Convert token price to gold, silver, and copper
        gold = token_price // 10000
        silver = (token_price % 10000) // 100
        copper = token_price % 100
        
        return {"gold": gold, "silver": silver, "copper": copper}

    # Search Functionality

    # Usage example:
    # api = WowGameDataApi(client_id, client_secret)
    # query = SearchQuery()
    # query.add_field("has_queue", True)
    # query.add_field("realms.timezone", "America/New_York")
    # query.set_page(1).set_page_size(100)
    # query.set_order("id:asc", "name:desc")
    # results = api.search("us", "en_US", "connected-realm", query)
    
    def search(
        self, 
        region: str, 
        locale: str, 
        document_type: str,
        query: SearchQuery,
        namespace_type: Literal["static", "dynamic", "profile"] = "dynamic"
    ) -> Dict[str, Any]:
        """
        Perform a search query on the specified document type.

        Args:
            region (str): The region of the data to retrieve.
            locale (str): The locale to reflect in localized data.
            document_type (str): The type of document to search (e.g., 'connected-realm').
            query (SearchQuery): A SearchQuery object containing the search parameters.
            namespace_type (str): The type of namespace to use. Can be 'static', 'dynamic', or 'profile'.

        Returns:
            Dict[str, Any]: A dictionary containing the search results.
        """
        resource = f"/data/wow/search/{document_type}"
        
        # Ensure the namespace is included in the query parameters
        namespace = f"{namespace_type}-{region}"
        query.add_field("namespace", namespace)
        
        # Always include the locale
        query.add_field("locale", locale)
        
        query_string = query.build()
        
        full_url = f"{resource}?{query_string}"
        return self._get_data(full_url, region, locale)