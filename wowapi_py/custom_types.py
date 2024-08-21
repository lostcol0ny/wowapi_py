from typing import TypedDict, Optional, List, Dict, Literal

RegionType = Literal["us", "eu", "tw", "kr", "cn"]


class Link(TypedDict):
    href: str


class Links(TypedDict):
    self: Link


class KeyValue(TypedDict):
    key: Link
    name: Optional[str]
    id: int


class Asset(TypedDict):
    key: str
    value: str
    file_data_id: int


class GenericID(TypedDict):
    key: Link
    id: int


class GenericMedia(TypedDict):
    _links: Links
    assets: List[Asset]
    id: int


class GenericType(TypedDict):
    type: str
    name: str


class GenericDisplayString(TypedDict):
    value: int
    display_string: str


class Criteria(TypedDict):
    id: int
    description: str
    amount: int


class AchievementMedia(TypedDict):
    key: Link
    id: int
    assets: List[Asset]


class Achievement(TypedDict):
    _links: Links
    id: int
    category: KeyValue
    name: str
    description: str
    points: int
    is_account_wide: bool
    criteria: Criteria
    media: AchievementMedia
    display_order: int


class AchievementIndex(TypedDict):
    _links: Links
    achievements: List[KeyValue]


class FactionAggregate(TypedDict):
    quantity: int
    points: int


class AggregatesByFaction(TypedDict):
    alliance: FactionAggregate
    horde: FactionAggregate


class AchievementCategory(TypedDict):
    _links: Links
    id: int
    name: str
    achievements: List[KeyValue]
    subcategories: List[KeyValue]
    is_guild_category: bool
    aggregates_by_faction: AggregatesByFaction
    display_order: int


class AchievementCategoriesIndex(TypedDict):
    _links: Links
    categories: List[KeyValue]
    root_categories: List[KeyValue]
    guild_categories: List[KeyValue]


class ConnectedRealm(TypedDict):
    href: str


class ItemModifier(TypedDict):
    type: int
    value: int


class Item(TypedDict):
    id: int
    context: Optional[int]
    bonus_lists: Optional[List[int]]
    modifiers: Optional[List[ItemModifier]]


class AuctionHousePet(TypedDict, total=False):
    breed_id: int
    level: int
    quality_id: int
    species_id: int


class AuctionItem(TypedDict):
    id: int
    item: Item
    quantity: int
    unit_price: Optional[int]
    time_left: str
    bid: Optional[int]
    buyout: Optional[int]
    pet: Optional[AuctionHousePet]


class Auctions(TypedDict):
    _links: Links
    connected_realm: ConnectedRealm
    auctions: List[AuctionItem]


class AzeriteEssencesIndex(TypedDict):
    _links: Links
    azerite_essences: List[KeyValue]


class ConnectedRealmsIndex(TypedDict):
    _links: Links
    connected_realms: List[Link]


class ConnectedRealmType(TypedDict):
    type: str
    name: str


class ConnectedRealm(TypedDict):
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


class CovenantIndex(TypedDict):
    _links: Links
    covenants: List[KeyValue]


class CovenantSpellTooltip(TypedDict):
    spell: str
    description: str
    cast_time: str
    power_cost: Optional[str] = None
    range: Optional[str] = None
    cooldown: Optional[str] = None


class CovenantSignatureAbility(TypedDict):
    id: int
    spell_tooltip: CovenantSpellTooltip


class CovenantClassAbility(TypedDict):
    id: int
    playable_class: str
    spell_tooltip: CovenantSpellTooltip


class CovenantRenownReward(TypedDict):
    level: int
    reward: KeyValue


class CovenantMedia(TypedDict):
    key: Link
    id: int


class Covenant(TypedDict):
    _links: Links
    id: int
    name: str
    description: str
    signature_ability: CovenantSignatureAbility
    class_abilities: List[CovenantClassAbility]
    soulbinds: List[KeyValue]
    renown_rewards: List[CovenantRenownReward]
    media: GenericMedia


class SoulbindIndex(TypedDict):
    _links: Links
    soulbinds: List[KeyValue]


class SoulbindTalentTree(TypedDict):
    key: Link
    id: int
    spell_tooltip: CovenantSpellTooltip


class SoulbindFollower(TypedDict):
    id: int
    name: str


class Soulbind(TypedDict):
    _links: Links
    id: int
    name: str
    covenant: KeyValue
    creature: KeyValue
    follower: SoulbindFollower
    talent_tree: SoulbindTalentTree


class ConduitIndex(TypedDict):
    _links: Links
    conduits: List[KeyValue]


class ConduitSpellTooltip(TypedDict):
    spell: KeyValue
    description: str
    cast_time: str


class ConduitRanks(TypedDict):
    id: int
    tier: int
    spell_tooltip: ConduitSpellTooltip


class Conduit(TypedDict):
    _links: Links
    id: int
    name: str
    item: KeyValue
    socket_type: GenericType
    ranks: List[ConduitRanks]


class CreatureDisplays(TypedDict):
    id: int
    key: Link
    is_tameable: bool


class CreatureFamily(TypedDict):
    _links: Links
    id: int
    name: str
    specialization: KeyValue
    media: GenericMedia


class CreatureFamilyIndex(TypedDict):
    _links: Links
    creature_families: List[CreatureFamily]


class Creature(TypedDict):
    _links: Links
    id: int
    name: str
    type: KeyValue
    family: KeyValue
    display: list[CreatureDisplays]


class CreatureTypeIndex(TypedDict):
    _links: Links
    creature_types: List[KeyValue]


class GuildCrestEmblem(TypedDict):
    id: int
    media: GenericMedia


class GuildCrestBorder(TypedDict):
    id: int
    media: GenericMedia


class GuildCrestRGBA(TypedDict):
    r: int
    g: int
    b: int
    a: float


class GuildCrestColor(TypedDict):
    id: int
    rgba: GuildCrestRGBA


class GuildCrestColors(TypedDict):
    emblems: List[GuildCrestColor]
    borders: List[GuildCrestColor]
    backgrounds: List[GuildCrestColor]


class GuildCrestComponentsIndex(TypedDict):
    _links: Links
    emblems: List[GuildCrestEmblem]
    borders: List[GuildCrestBorder]
    colors: GuildCrestColors


class HeirloomIndex(TypedDict):
    _links: Links
    heirlooms: List[KeyValue]


class Damage(TypedDict):
    min_value: int
    max_value: int
    display_string: str
    damage_class: GenericType


class DPS(TypedDict):
    value: float
    display_string: str


class Weapon(TypedDict):
    damage: Damage
    attack_speed: GenericDisplayString
    dps: DPS


class StatDisplay(TypedDict):
    display_string: str
    color: Dict[str, int]


class Stat(TypedDict):
    type: GenericType
    value: int
    display: StatDisplay
    is_equip_bonus: Optional[bool]


class Upgrades(TypedDict):
    value: int
    max_value: int
    display_string: str


class Requirements(TypedDict):
    level: Dict[str, str]


class HeirloomUpgradeItem(TypedDict):
    item: KeyValue
    context: int
    bonus_list: List[int]
    quality: GenericType
    name: str
    media: GenericMedia
    item_class: KeyValue
    item_subclass: KeyValue
    inventory_type: GenericType
    binding: GenericType
    weapon: Weapon
    stats: List[Stat]
    upgrades: Upgrades
    requirements: Requirements
    level: GenericDisplayString


class HeirloomUpgrade(TypedDict):
    item: HeirloomUpgradeItem
    level: int


class Heirloom(TypedDict):
    _links: Links
    id: int
    item: KeyValue
    source: GenericType
    source_description: str
    upgrades: List[HeirloomUpgrade]
    media: GenericMedia


class Damage(TypedDict):
    min_value: int
    max_value: int
    display_string: str
    damage_class: GenericType


class Weapon(TypedDict):
    damage: Damage
    attack_speed: GenericDisplayString
    dps: GenericDisplayString


class StatDisplay(TypedDict):
    display_string: str
    color: Dict[str, int]


class Stat(TypedDict):
    type: GenericType
    value: int
    is_negated: Optional[bool]
    display: StatDisplay


class Spell(TypedDict):
    key: KeyValue
    name: str
    id: int


class SpellInfo(TypedDict):
    spell: Spell
    description: str


class Requirements(TypedDict):
    level: GenericDisplayString


class Level(TypedDict):
    value: int
    display_string: str


class Durability(TypedDict):
    value: int
    display_string: str


class PreviewItem(TypedDict):
    item: KeyValue
    context: int
    bonus_list: List[int]
    quality: GenericType
    name: str
    media: GenericMedia
    item_class: KeyValue
    item_subclass: KeyValue
    inventory_type: GenericType
    binding: GenericType
    unique_equipped: str
    weapon: Weapon
    stats: List[Stat]
    spells: List[SpellInfo]
    requirements: Requirements
    level: Level
    durability: Durability


class Appearance(TypedDict):
    key: KeyValue
    id: int


class Item(TypedDict):
    _links: Links
    id: int
    name: str
    quality: GenericType
    level: int
    required_level: int
    media: GenericMedia
    item_class: KeyValue
    item_subclass: KeyValue
    inventory_type: GenericType
    purchase_price: int
    sell_price: int
    max_count: int
    is_equippable: bool
    is_stackable: bool
    preview_item: PreviewItem
    purchase_quantity: int
    appearances: List[Appearance]


class ItemClassesIndex(TypedDict):
    _links: Links
    item_classes: List[KeyValue]


class ItemClass(TypedDict):
    _links: Links
    id: int
    name: str
    subclasses: List[KeyValue]


class ItemSetsIndex(TypedDict):
    _links: Links
    item_sets: List[KeyValue]


class ItemSetEffect(TypedDict):
    display_string: str
    required_count: int


class ItemSet(TypedDict):
    _links: Links
    id: int
    name: str
    items: List[KeyValue]
    effects: List[ItemSetEffect]
    is_effect_active: bool


class ItemSubclass(TypedDict):
    _links: Links
    class_id: int
    subclass_id: int
    display_name: str
    hide_subclass_in_tooltips: bool


class ItemAppearance(TypedDict):
    _links: Links
    id: int
    slot: Item
    item_class: KeyValue
    item_subclass: KeyValue
    item_display_info_id: int
    items: List[KeyValue]
    media: GenericMedia


class IteamAppearanceSetsIndex(TypedDict):
    _links: Links
    appearance_sets: List[KeyValue]


class ItemAppearanceSet(TypedDict):
    _links: Links
    id: int
    set_name: str
    appearances: List[GenericID]


class ItemAppearanceSlotIndexReference(TypedDict):
    key: Link


class ItemAppearanceSlotIndex(TypedDict):
    _links: Links
    slots: List[ItemAppearanceSlotIndexReference]


class ItemAppearanceSlot(TypedDict):
    _links: Links
    appearances: List[GenericID]


class JournalExpansionsIndex(TypedDict):
    _links: Links
    tiers: List[KeyValue]


class JournalExpansion(TypedDict):
    _links: Links
    id: int
    name: str
    dungeons: List[KeyValue]
    raids: List[KeyValue]


class JournalEncountersIndex(TypedDict):
    _links: Links
    name: str
    id: int
    encounters: List[KeyValue]


class Creature(TypedDict):
    id: int
    name: str
    creature_display: GenericID


class Section(TypedDict):
    id: int
    title: str
    body_text: Optional[str]
    sections: Optional[List["Section"]]
    creature_display: Optional[GenericID]


class JournalEncounter(TypedDict):
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


class JournalInstancesIndex(TypedDict):
    _links: Links
    instances: List[KeyValue]


class JournalInstanceMode(TypedDict):
    mode: GenericType
    players: int
    is_tracked: bool


class JournalInstance(TypedDict):
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


class JournalInstanceMediaAsset(TypedDict):
    key: str
    value: str


class JournalInstanceMedia(TypedDict):
    _links: Links
    assets: List[JournalInstanceMediaAsset]


class ModifiedCraftingIndex(TypedDict):
    _links: Links
    categories: Link
    slot_types: Link


class ModifiedCraftingCategoryIndex(TypedDict):
    _links: Links
    categories: list[KeyValue]


class ModifiedCraftingCategory(TypedDict):
    _links: Links
    id: int
    name: str


class ModifiedCraftingSlotTypeIndex(TypedDict):
    _links: Links
    slot_types: list[KeyValue]


class ModifiedCraftingReagentSlotType(TypedDict):
    _links: Links
    id: int
    description: str
    compatible_categories: list[KeyValue]


class MountsIndex(TypedDict):
    _links: Links
    mounts: List[KeyValue]


class FactionType(TypedDict):
    type: str
    name: str


class Requirements(TypedDict):
    faction: FactionType


class Mount(TypedDict):
    _links: Links
    id: int
    name: str
    creature_displays: List[GenericID]
    description: str
    source: GenericType
    faction: FactionType
    requirements: Requirements


class MythicKeystoneAffixesIndex(TypedDict):
    _links: Links
    affixes: List[KeyValue]


class MythicKeystoneAffix(TypedDict):
    _links: Links
    id: int
    name: str
    description: str
    media: GenericID


class MythicKeyStoneAffixMedia(TypedDict):
    _links: Links
    assets: List[Asset]


class MythicKeystoneIndex(TypedDict):
    _links: Links
    seasons: Link
    dungeons: Link


class Zone(TypedDict):
    slug: str


class KeystoneUpgrade(TypedDict):
    upgrade_level: int
    qualifying_duration: int


class MythicKeystoneDungeon(TypedDict):
    _links: Links
    id: int
    name: str
    map: GenericID
    zone: Zone
    dungeon: KeyValue
    keystone_upgrades: List[KeystoneUpgrade]
    is_tracked: bool


class MythicKeystonePeriodsIndex(TypedDict):
    _links: Links
    periods: List[KeyValue]


class MythicKeystonePeriod(TypedDict):
    _links: Links
    id: int
    start_timestamp: int
    end_timestamp: int


class MythicKeystoneSeasonsIndex(TypedDict):
    _links: Links
    seasons: List[KeyValue]


class MythicKeystoneSeason(TypedDict):
    _links: Links
    id: int
    start_timestamp: int
    end_timestamp: int
    periods: list[KeyValue]
    season_name: str


class MythicKeystoneLeaderboardsIndex(TypedDict):
    _links: Links
    current_leaderboards: list[KeyValue]


class MythicKeystoneLeaderboardMap(TypedDict):
    name: str
    id: int


class MythicKeystoneLeaderboardConnectedRealm(TypedDict):
    href: str


class MythicKeystoneLeaderboardRealm(TypedDict):
    key: KeyValue
    id: int
    slug: str


class MythicKeystoneLeaderboardProfile(TypedDict):
    name: str
    id: int
    realm: MythicKeystoneLeaderboardRealm


class MythicKeystoneLeaderboardFaction(TypedDict):
    type: str


class MythicKeystoneLeaderboardSpecialization(TypedDict):
    key: KeyValue
    id: int


class MythicKeystoneLeaderboardMember(TypedDict):
    profile: MythicKeystoneLeaderboardProfile
    faction: MythicKeystoneLeaderboardFaction
    specialization: MythicKeystoneLeaderboardSpecialization


class MythicKeystoneLeaderboardLeadingGroup(TypedDict):
    ranking: int
    duration: int
    completed_timestamp: int
    keystone_level: int
    members: List[MythicKeystoneLeaderboardMember]


class MythicKeystoneLeaderboardKeystoneAffix(TypedDict):
    key: KeyValue
    name: str
    id: int


class MythicKeystoneLeaderboardAffixDetail(TypedDict):
    keystone_affix: MythicKeystoneLeaderboardKeystoneAffix
    starting_level: int


class MythicKeystoneLeaderboard(TypedDict):
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


class MythicRaidLeaderboardRealm(TypedDict):
    name: str
    id: int
    slug: str


class MythicRaidLeaderboardGuild(TypedDict):
    name: str
    id: int
    realm: MythicRaidLeaderboardRealm


class MythicRaidLeaderboardFaction(TypedDict):
    type: str


class MythicRaidLeaderboardEntry(TypedDict):
    guild: MythicRaidLeaderboardGuild
    faction: MythicRaidLeaderboardFaction
    timestamp: int
    region: str
    rank: int


class MythicRaidLeaderboard(TypedDict):
    _links: Links
    slug: str
    criteria_type: str
    entries: List[MythicRaidLeaderboardEntry]
    journal_instance: KeyValue


class PetsIndex(TypedDict):
    _links: Links
    pets: List[KeyValue]


class BattlePetType(TypedDict):
    id: int
    type: str
    name: str


class BattlePetAbility(TypedDict):
    ability: KeyValue
    slot: int
    required_level: int


class Pet(TypedDict):
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


class PetAbilitiesIndex(TypedDict):
    _links: Links
    abilities: List[KeyValue]


class BattlePetType(TypedDict):
    id: int
    type: str
    name: str


class PetAbility(TypedDict):
    _links: Links
    id: int
    name: str
    battle_pet_type: BattlePetType
    rounds: int
    media: GenericID


class PlayableClassesIndex(TypedDict):
    _links: Links
    classes: List[KeyValue]


class PlayableClassGender(TypedDict):
    male: str
    female: str


class PlayableClass(TypedDict):
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


class PvPTalentSlotReference(TypedDict):
    slot_number: int
    unlock_player_level: int


class PvPTalentSlots(TypedDict):
    _links: Links
    id: int
    talent_slots: List[PvPTalentSlotReference]


class PlayableRacesIndex(TypedDict):
    _links: Links
    races: List[KeyValue]
    id: int
    name: str


class PlayableRace(TypedDict):
    _links: Links
    id: int
    name: str
    gender_name: PlayableClassGender
    is_selectable: bool
    is_allied_race: bool
    playable_classes: List[KeyValue]


class PlayableSpecializationsIndex(TypedDict):
    _links: Links
    character_specializations: List[KeyValue]


class PvPTalentSpellTooltip(TypedDict):
    description: str
    cast_time: str
    range: str
    cooldown: str


class PvPTalent(TypedDict):
    talent: KeyValue


class PlayableSpecialization(TypedDict):
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


class PowerTypesIndex(TypedDict):
    _links: Links
    power_types: List[KeyValue]


class PowerType(TypedDict):
    _links: Links
    id: int
    name: str


class ProfessionsIndex(TypedDict):
    _links: Links
    professions: List[KeyValue]


class Profession(TypedDict):
    _links: Links
    id: int
    name: str
    description: str
    type: GenericType
    media: GenericID
    skill_tiers: List[KeyValue]


class ProfessionSkillTierCategories(TypedDict):
    name: str
    recipes: List[KeyValue]


class ProfessionSkillTier(TypedDict):
    _links: Links
    id: int
    name: str
    minimum_skill_level: int
    maximum_skill_level: int
    categories: List[ProfessionSkillTierCategories]


class Recipe(TypedDict):
    _links: Links
    id: int
    name: str
    media: GenericID
    crafted_item: KeyValue
    reagents: List[KeyValue]
    crafted_quantity: Dict[str, int]


class PvPSeasonsIndex(TypedDict):
    _links: Links
    seasons: List[GenericID]
    current_season: GenericID


class PvPSeason(TypedDict):
    _links: Links
    id: int
    leaderboards: Link
    rewards: Link
    start_timestamp: int
    end_timestamp: int


class PvPSeasonLeaderboardsIndex(TypedDict):
    _links: Links
    season: GenericID
    leaderboards: List[KeyValue]


class PvPSeasonLeaderboardEntriesSeasonMatchStats(TypedDict):
    played: int
    won: int
    lost: int


class PvPSeasonLeaderboardEntriesRealm(TypedDict):
    key: KeyValue
    id: int
    slug: str


class PvPSeasonLeaderboardEntriesCharacter(TypedDict):
    name: str
    id: int
    realm: PvPSeasonLeaderboardEntriesRealm


class PvPSeasonLeaderboardEntries(TypedDict):
    character: PvPSeasonLeaderboardEntriesCharacter
    faction: Dict[str, str]
    rank: int
    rating: int
    season_match_statistics: PvPSeasonLeaderboardEntriesSeasonMatchStats
    tier: GenericID


class PvPSeasonLeaderboardBracket(TypedDict):
    id: int
    type: str


class PvPSeasonLeaderboard(TypedDict):
    _links: Links
    season: GenericID
    name: str
    bracket: PvPSeasonLeaderboardBracket
    entries: List[PvPSeasonLeaderboardEntries]


class PvPSeasonRewardsIndexRewards(TypedDict):
    bracket: GenericType
    achievement: KeyValue
    rating_cutoffs: int
    faction: FactionType


class PvPRewardsIndex(TypedDict):
    _links: Links
    season: GenericID
    rewards: List[PvPSeasonRewardsIndexRewards]


class PvPTiersIndex(TypedDict):
    _links: Links
    tiers: List[KeyValue]


class PvPTier(TypedDict):
    _links: Links
    id: int
    name: str
    min_rating: int
    max_rating: int
    media: GenericID
    bracket: GenericType
    rating_type: int


class QuestsIndex(TypedDict):
    _links: Links
    categories: Link
    areas: Link
    types: Link


class QuestRequirements(TypedDict):
    min_character_level: int
    max_character_level: int
    faction: FactionType


class ReputationReward(TypedDict):
    reward: KeyValue
    value: int


class MoneyUnits(TypedDict):
    gold: int
    silver: int
    copper: int


class MoneyReward(TypedDict):
    value: int
    units: MoneyUnits


class QuestRewards(TypedDict):
    experience: int
    reputations: List[ReputationReward]
    money: MoneyReward


class Quest(TypedDict):
    _links: Links
    id: int
    title: str
    area: KeyValue
    description: str
    requirements: QuestRequirements
    rewards: QuestRewards


class QuestCategoriesIndex(TypedDict):
    _links: Links
    categories: List[KeyValue]


class QuestCategory(TypedDict):
    _links: Links
    id: int
    category: str
    quests: List[KeyValue]


class QuestAreasIndex(TypedDict):
    _links: Links
    areas: List[KeyValue]


class QuestArea(TypedDict):
    _links: Links
    id: int
    area: str
    quests: List[KeyValue]


class QuestTypesIndex(TypedDict):
    _links: Links
    types: List[KeyValue]


class QuestType(TypedDict):
    _links: Links
    id: int
    type: str
    quests: List[KeyValue]


class RealmsIndex(TypedDict):
    _links: Links
    realms: List[Link]


class Realm(TypedDict):
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


class RegionsIndex(TypedDict):
    _links: Links
    regions: List[Link]


class Region(TypedDict):
    _links: Links
    id: int
    tag: str
    patch_string: str


class ReputationFactionsIndex(TypedDict):
    _links: Links
    factions: List[KeyValue]


class ReputationFaction(TypedDict):
    _links: Links
    id: int
    name: str
    description: str
    reputation_tiers: KeyValue


class ReputationTiersIndex(TypedDict):
    _links: Links
    reputation_tiers: List[KeyValue]


class ReputationTierReference(TypedDict):
    name: str
    min_value: int
    max_value: int
    id: int


class ReputationTier(TypedDict):
    _links: Links
    id: int
    tiers: List[ReputationTierReference]
    faction: KeyValue


class Spell(TypedDict):
    _links: Links
    id: int
    name: str
    description: str
    media: CovenantMedia


class TalentTreeIndex(TypedDict):
    _links: Links
    spec_talent_trees: List[KeyValue]


class TalentTreeRestrictionLines(TypedDict):
    required_points: int
    restricted_row: float
    is_for_class: bool


class TalentTreeSpecTalentNodesRanksSpellTooltip(TypedDict):
    spell: KeyValue
    description: str
    cast_time: str


class TalentTreeSpecTalentNodesRanksToolip(TypedDict):
    talent: KeyValue
    spell_tooltip: TalentTreeSpecTalentNodesRanksSpellTooltip


class TalentTreeClassTalentNodesRanks(TypedDict):
    rank: int
    tooltip: TalentTreeSpecTalentNodesRanksToolip


class TalentTreeSpecTalentNodesRanksTooltip(TypedDict):
    spell_tooltip: TalentTreeSpecTalentNodesRanksSpellTooltip
    talent: KeyValue


class TalentTreeSpecTalentNodesRanks(TypedDict):
    rank: int
    tooltip: TalentTreeSpecTalentNodesRanksTooltip


class TalentTreeSpecTalentNodes(TypedDict):
    id: int
    unlocks: List[Dict[int, int]]
    node_type: GenericType
    ranks: list[TalentTreeSpecTalentNodesRanks]
    display_row: int
    display_col: int
    raw_position_x: int
    raw_position_y: int


class TalentTreeHeroTalentTreesHeroTalentNodesNodesRanksChoiceofTooltips(TypedDict):
    talent: KeyValue
    spell_tooltip: TalentTreeSpecTalentNodesRanksSpellTooltip


class TalentTreeHeroTalentTreesHeroTalentNodesRanks(TypedDict):
    choice_of_tooltips: List[
        TalentTreeHeroTalentTreesHeroTalentNodesNodesRanksChoiceofTooltips
    ]
    spell_tooltip: TalentTreeSpecTalentNodesRanksSpellTooltip


class TalentTreeHeroTalentTreesHeroTalentNodes(TypedDict):
    id: int
    locked_by: List[Dict[int, int]]
    unlocks: List[Dict[int, int]]
    node_type: GenericType
    ranks: List[TalentTreeHeroTalentTreesHeroTalentNodesRanks]
    display_row: int
    display_col: int
    raw_position_x: int
    raw_position_y: int


class TalentTreeHeroTalentTrees(TypedDict):
    id: int
    name: str
    media: GenericID
    hero_talent_nodes: list[TalentTreeHeroTalentTreesHeroTalentNodes]
    playable_class: KeyValue
    playable_specializations: List[KeyValue]


class TalentTreeClassTalentNodes(TypedDict):
    id: int
    node_type: GenericType
    ranks: List[TalentTreeClassTalentNodesRanks]
    display_row: int
    display_col: int
    raw_position_x: int
    raw_position_y: int


class TalentTree(TypedDict):
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


class TalentTreeNodesSpecTalentTrees(TypedDict):
    key: Link
    name: str


class TalentTreeNodes(TypedDict):
    _links: Links
    id: int
    spec_talent_trees: List[TalentTreeNodesSpecTalentTrees]
    talent_nodes: List[TalentTreeClassTalentNodes]


class TalentsIndex(TypedDict):
    _links: Links
    talents: List[KeyValue]


class TalentRankDescriptions(TypedDict):
    rank: int
    description: str


class Talent(TypedDict):
    _links: Links
    id: int
    rank_descriptions: List[TalentRankDescriptions]
    spell: KeyValue
    playable_class: KeyValue
    playable_specialization: KeyValue


class PvPTalentsIndex(TypedDict):
    _links: Links
    pvp_talents: List[KeyValue]


class PvPTalent(TypedDict):
    _links: Links
    id: int
    spell: KeyValue
    playable_specialization: KeyValue
    description: str
    unlock_player_level: int
    compatible_slots: list[int]


class TechTalentTreeIndex(TypedDict):
    _links: Links
    talent_trees: List[KeyValue]


class TechTalentTree(TypedDict):
    _links: Links
    id: int
    max_tiers: int
    talents: List[KeyValue]


class TechTalentIndex(TypedDict):
    _links: Links
    talents: List[KeyValue]


class TechTalentSpellTooltip(TypedDict):
    key: KeyValue
    name: str
    id: int


class TechTalent(TypedDict):
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


class TitlesIndex(TypedDict):
    _links: Links
    titles: List[KeyValue]


class Title(TypedDict):
    _links: Links
    id: int
    name: str
    gender_name: PlayableClassGender


class ToyIndex(TypedDict):
    _links: Links
    toys: List[KeyValue]


class Toy(TypedDict):
    _links: Links
    id: int
    item: KeyValue
    source: GenericType
    should_exclude_if_uncollected: bool
    media: GenericID


class WoWTokenIndex(TypedDict):
    _links: Links
    last_updated_timestamp: int
    price: int


class AccountProfileSummaryCharacterReferenceRealm(TypedDict):
    key: Link
    name: str
    id: int
    slug: str


class AccountProfileSummaryCharacterReference(TypedDict):
    character: Link
    protected_character: Link
    name: str
    id: int
    realm: AccountProfileSummaryCharacterReferenceRealm
    playable_class: KeyValue
    playable_race: KeyValue
    gender: GenericType
    faction: GenericType
    level: int


class AccountProfileSummaryCharacters(TypedDict):
    id: int
    characters: List[AccountProfileSummaryCharacterReference]


class AccountProfileSummaryWowAccounts(TypedDict):
    id: int
    characters: List[AccountProfileSummaryCharacters]


class AccountProfileSummary(TypedDict):
    _links: Links
    id: int
    wow_accounts: List[AccountProfileSummaryWowAccounts]
    collections: Link


class CharacterAchievementSummaryCriteria(TypedDict):
    id: int
    is_completed: bool


class CharacterAchievementSummaryAchievements(TypedDict):
    id: int
    achievement: KeyValue
    criteria: CharacterAchievementSummaryCriteria
    completed_timestamp: int


class CharacterAchievementSummary(TypedDict):
    _links: Links
    total_quantity: int
    total_points: int
    achievements: List[KeyValue]


class CharacterAchievementStatisticsCharacterRealmReference(TypedDict):
    key: Link
    name: str
    id: int
    slug: str


class CharacterAchievementStatisticsCharacterReference(TypedDict):
    key: Link
    name: str
    id: int
    realm: CharacterAchievementStatisticsCharacterRealmReference


class CharacterAchievementStatisticsStatistic(TypedDict):
    id: int
    name: str
    last_updated_timestamp: int
    quantity: float
    description: Optional[str]


class CharacterAchievementStatisticsSubCategory(TypedDict):
    id: int
    name: str
    statistics: List[CharacterAchievementStatisticsStatistic]


class CharacterAchievementStatisticsCategory(TypedDict):
    id: int
    name: str
    sub_categories: Optional[List[CharacterAchievementStatisticsSubCategory]]
    statistics: List[CharacterAchievementStatisticsStatistic]


class CharacterAchievementStatistics(TypedDict):
    _links: Links
    character: CharacterAchievementStatisticsCharacterReference
    categories: List[CharacterAchievementStatisticsCategory]


class CharacterAppearanceSummaryCharacterRealmReference(TypedDict):
    key: Link
    name: str
    id: int
    slug: str


class CharacterAppearanceSummaryCharacterReference(TypedDict):
    key: Link
    name: str
    id: int
    realm: CharacterAppearanceSummaryCharacterRealmReference


class CharacterAppearanceSummaryGuildCrestColor(TypedDict):
    id: int
    rgba: Dict[str, int]


class CharacterAppearanceSummaryGuildCrestEmblem(TypedDict):
    id: int
    media: KeyValue
    color: GuildCrestColor


class CharacterAppearanceSummaryGuildCrestBorder(TypedDict):
    id: int
    media: KeyValue
    color: GuildCrestColor


class CharacterAppearanceSummaryGuildCrestBackground(TypedDict):
    color: GuildCrestColor


class CharacterAppearanceSummaryGuildCrest(TypedDict):
    emblem: GuildCrestEmblem
    border: GuildCrestBorder
    background: CharacterAppearanceSummaryGuildCrestBackground


class CharacterAppearanceSummaryCharacterItem(TypedDict):
    id: int
    slot: GenericType
    enchant: int
    item_appearance_modifier_id: int
    internal_slot_id: int
    subclass: int


class CharacterAppearanceSummaryCustomizationChoice(TypedDict):
    id: int
    name: Optional[str]
    display_order: int


class CharacterAppearanceSummaryCharacterCustomization(TypedDict):
    option: GenericID
    choice: CharacterAppearanceSummaryCustomizationChoice


class CharacterAppearanceSummary(TypedDict):
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


class CharacterCollectionsIndexCharacterRealm(TypedDict):
    key: Link
    name: str
    id: int
    slug: str


class CharacterCollectionsIndexCharacter(TypedDict):
    key: Link
    name: str
    id: int
    realm: CharacterCollectionsIndexCharacterRealm


class CharacterCollectionsIndex(TypedDict):
    _links: Links
    pets: Link
    mounts: Link
    heirlooms: Link
    toys: Link
    character: CharacterCollectionsIndexCharacter
    transmogs: Link


class CharacterHeirloomsCollectionSummaryHeirloomUpgrade(TypedDict):
    level: int


class CharacterHeirloomsCollectionSummaryHeirloom(TypedDict):
    heirloom: KeyValue
    upgrade: CharacterHeirloomsCollectionSummaryHeirloomUpgrade


class CharacterHeirloomsCollectionSummary(TypedDict):
    _links: Links
    heirlooms: List[CharacterHeirloomsCollectionSummaryHeirloom]


class CharacterMountsCollectionSummaryMounts(TypedDict):
    mount: KeyValue
    is_character_specific: Optional[bool]
    is_useable: Optional[bool]


class CharacterMountsCollectionSummary(TypedDict):
    _links: Links
    mounts: List[CharacterMountsCollectionSummaryMounts]


class CharacterPetsCollectionSummaryStats(TypedDict):
    breed_id: int
    health: int
    power: int
    speed: int


class CharacterPetsCollectionSummaryReference(TypedDict):
    species: KeyValue
    level: int
    quality: GenericType
    stats: CharacterPetsCollectionSummaryStats
    creature_display: GenericID


class CharacterPetsCollectionSummary(TypedDict):
    _links: Links
    pets: List[CharacterPetsCollectionSummaryReference]
    unlocked_battle_pet_slots: int


class CharacterToysCollectionSummaryReference(TypedDict):
    toy: KeyValue


class CharacterToysCollectionSummary(TypedDict):
    _links: Links
    toys: List[CharacterToysCollectionSummaryReference]


class CharacterTransmogsCollectionSummarySlots(TypedDict):
    slot: GenericType
    appearances: list[GenericID]


class CharacterTransmogsCollectionSummary(TypedDict):
    _links: Links
    appearance_sets: List[KeyValue]
    slots: list[CharacterTransmogsCollectionSummarySlots]


class CharacterEncountersSummary(TypedDict):
    _links: Links
    character: CharacterAchievementStatisticsCharacterReference
    dungeons: Link
    raids: Link


class CharacterDungeonsEncounter(TypedDict):
    encounter: KeyValue
    completed_count: int
    last_kill_timestamp: int


class CharacterDungeonsProgress(TypedDict):
    completed_count: int
    total_count: int
    encounters: List[CharacterDungeonsEncounter]


class CharacterDungeonsMode(TypedDict):
    difficulty: GenericType
    status: GenericType
    progress: CharacterDungeonsProgress


class CharacterDungeonsInstance(TypedDict):
    instance: KeyValue
    modes: List[CharacterDungeonsMode]


class CharacterDungeonsExpansion(TypedDict):
    expansion: KeyValue
    instances: List[CharacterDungeonsInstance]


class CharacterDungeons(TypedDict):
    _links: Links
    expansions: List[CharacterDungeonsExpansion]


class CharacterEquipmentSummaryCharacterReference(TypedDict):
    key: Link
    name: str
    id: int
    realm: KeyValue


class CharacterEquipmentSummaryItemReference(TypedDict):
    key: Link
    id: int


class CharacterEquipmentSummaryItemSlot(TypedDict):
    type: str
    name: str


class CharacterEquipmentSummaryEnchantmentSlot(TypedDict):
    id: int
    type: str


class CharacterEquipmentSummaryEnchantment(TypedDict):
    display_string: str
    source_item: Optional[KeyValue]
    enchantment_id: int
    enchantment_slot: CharacterEquipmentSummaryEnchantmentSlot


class CharacterEquipmentSummarySocketType(TypedDict):
    type: str
    name: str


class CharacterEquipmentSummarySocket(TypedDict):
    socket_type: CharacterEquipmentSummarySocketType
    item: KeyValue
    display_string: str
    media: KeyValue


class CharacterEquipmentSummaryStat(TypedDict):
    type: GenericType
    value: int
    display: GenericDisplayString
    is_equip_bonus: Optional[bool]
    is_negated: Optional[bool]


class CharacterEquipmentSummaryRequirements(TypedDict):
    level: GenericDisplayString
    playable_classes: Optional[Dict[str, List[KeyValue]]]


class CharacterEquipmentSummaryTransmog(TypedDict):
    item: KeyValue
    display_string: str
    item_modified_appearance_id: int


class CharacterEquipmentSummarySpell(TypedDict):
    spell: KeyValue
    description: str


class CharacterEquipmentSummaryEquippedItemSellPriceDisplayStrings(TypedDict):
    header: str
    gold: str
    silver: str
    coller: int


class CharacterEquipmentSummaryEquippedItemSellPrice(TypedDict):
    value: int
    display_strings: CharacterEquipmentSummaryEquippedItemSellPriceDisplayStrings


class ArmorDisplay(TypedDict):
    display_string: str
    color: Dict[str, int]


class Armor(TypedDict):
    value: int
    display: ArmorDisplay


class CharacterEquipmentSummaryColoredString(TypedDict):
    display_string: str
    color: Dict[str, int]


class CharacterEquipmentSummaryEquippedItemDamageClass(TypedDict):
    type: str
    name: str


class CharacterEquipmentSummaryEquippedItemWeaponDamage(TypedDict):
    min_value: int
    max_value: int
    display_string: str
    damage_class: CharacterEquipmentSummaryEquippedItemDamageClass


class CharacterEquipmentSummaryEquippedItemWeaponAttackSpeed(TypedDict):
    value: int
    display_string: str


class CharacterEquipmentSummaryEquippedItemWeaponDPS(TypedDict):
    value: float
    display_string: str


class CharacterEquipmentSummaryEquippedItemWeapon(TypedDict):
    damage: CharacterEquipmentSummaryEquippedItemWeaponDamage
    attack_speed: CharacterEquipmentSummaryEquippedItemWeaponAttackSpeed
    dps: CharacterEquipmentSummaryEquippedItemWeaponDPS


class CharacterEquipmentSummaryEquippedItem(TypedDict):
    item: GenericID
    slot: GenericType
    quantity: int
    context: int
    bonus_list: List[int]
    quality: GenericType
    name: str
    modified_appearance_id: int
    media: GenericID
    item_class: KeyValue
    item_subclass: KeyValue
    inventory_type: GenericType
    binding: GenericType
    armor: Optional[Armor]
    stats: List[Stat]
    sell_price: CharacterEquipmentSummaryEquippedItemSellPrice
    requirements: Requirements
    level: GenericDisplayString
    transmog: Optional[CharacterEquipmentSummaryTransmog]
    durability: Optional[GenericDisplayString]
    name_description: Optional[CharacterEquipmentSummaryColoredString]
    unique_equipped: Optional[str]
    limit_category: Optional[str]
    enchantments: Optional[List[CharacterEquipmentSummaryEnchantment]]
    sockets: Optional[List[CharacterEquipmentSummarySocket]]
    weapon: Optional[Weapon]  # This could be further defined if needed
    spells: Optional[List[Spell]]
    description: Optional[str]
    is_subclass_hidden: Optional[bool]
    modified_crafting_stat: Optional[List[GenericType]]


class CharacterEquipmentSummaryItemSetItem(TypedDict):
    item: KeyValue
    is_equipped: Optional[bool]


class CharacterEquipmentSummaryItemSetEffect(TypedDict):
    display_string: str
    required_count: int
    is_active: bool


class CharacterEquipmentSummaryEquippedItemSet(TypedDict):
    item_set: KeyValue
    items: List[CharacterEquipmentSummaryItemSetItem]
    effects: List[ItemSetEffect]
    display_string: str


class CharacterEquipmentSummary(TypedDict):
    _links: Links
    character: CharacterEquipmentSummaryCharacterReference
    equipped_items: List[CharacterEquipmentSummaryEquippedItem]
    equipped_item_sets: List[CharacterEquipmentSummaryEquippedItemSet]


class CharacterHunterPetsSummaryHunterPets(TypedDict):
    name: str
    level: int
    creature: KeyValue
    slot: int
    creature_display: GenericID


class CharacterHunterPetsSummary(TypedDict):
    _links: Links
    character: CharacterAchievementStatisticsCharacterReference
    hunter_pets: List[CharacterHunterPetsSummaryHunterPets]


class CharacterMediaSummary(TypedDict):
    _links: Links
    character: CharacterAchievementStatisticsCharacterReference
    assets: List[JournalInstanceMediaAsset]


class CharacterMythicKeystoneProfileIndexCurrentPeriod(TypedDict):
    period: GenericID


class CharacterMythicKeystoneProfileIndexRating(TypedDict):
    rating: float
    color: GuildCrestRGBA


class CharacterMythicKeystoneProfileIndex(TypedDict):
    _links: Links
    current_period: CharacterMythicKeystoneProfileIndexCurrentPeriod
    seasons: List[GenericID]
    character: KeyValue
    current_mythic_rating: CharacterMythicKeystoneProfileIndexRating


class Realm(TypedDict):
    key: Link
    id: int
    slug: str


class Character(TypedDict):
    name: str
    id: int
    realm: Realm


class Member(TypedDict):
    character: Character
    specialization: KeyValue
    race: KeyValue
    equipped_item_level: int


class Color(TypedDict):
    r: int
    g: int
    b: int
    a: float


class MythicRating(TypedDict):
    color: Color
    rating: float


class BestRun(TypedDict):
    completed_timestamp: int
    duration: int
    keystone_level: int
    keystone_affixes: List[KeyValue]
    members: List[Member]
    dungeon: KeyValue
    is_completed_within_time: bool
    mythic_rating: MythicRating


class CharacterReference(TypedDict):
    key: Link
    name: str
    id: int
    realm: Realm


class CharacterMythicKeystoneSeasonDetails(TypedDict):
    _links: Links
    season: GenericID
    best_runs: List[BestRun]
    character: CharacterReference
    mythic_rating: MythicRating


class CharacterProfessionsSummaryPrimariesTiers(TypedDict):
    skill_points: int
    max_skill_points: int
    tier: GenericID
    known_recipes: List[KeyValue]


class CharacterProfessionsSummaryPrimaries(TypedDict):
    profession: KeyValue
    tiers: List[CharacterProfessionsSummaryPrimariesTiers]


class CharacterProfessionsSummarySecondaries(TypedDict):
    profession: KeyValue
    skill_points: int
    max_skill_points: int


class CharacterProfessionsSummary(TypedDict):
    _links: Links
    character: CharacterAchievementStatisticsCharacterReference
    primaries: List[CharacterProfessionsSummaryPrimaries]
    secondaries: List[CharacterProfessionsSummarySecondaries]


class CharacterProfileSummaryGuild(TypedDict):
    key: Link
    name: str
    id: int
    realm: Realm
    faction: FactionType


class CharacterProfileSummaryTitle(TypedDict):
    key: Link
    name: str
    id: int
    display_string: str


class CharacterProfileSummaryCovenantProgress(TypedDict):
    chosen_covenant: KeyValue
    renown_level: int
    soulbinds: Link


class CharacterProfileSummary(TypedDict):
    _links: Links
    id: int
    name: str
    gender: GenericType
    faction: FactionType
    race: KeyValue
    character_class: KeyValue
    active_spec: KeyValue
    realm: Realm
    guild: Optional["CharacterProfileSummaryGuild"]
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
    active_title: Optional["CharacterProfileSummaryTitle"]
    reputations: Link
    quests: Link
    achievements_statistics: Link
    professions: Link
    covenant_progress: Optional["CharacterProfileSummaryCovenantProgress"]
    name_search: str


class CharacterProfileStatus(TypedDict):
    _links: Links
    id: int
    is_valid: bool


class CharacterPvPBracketStatisticsBreakdown(TypedDict):
    played: int
    won: int
    lost: int


class CharacterPvPBracketStatistics(TypedDict):
    _links: Links
    character: CharacterAchievementStatisticsCharacterReference
    faction: GenericType
    bracket: PvPSeasonLeaderboardBracket
    rating: int
    season: GenericID
    tier: GenericID
    season_match_statistics: CharacterPvPBracketStatisticsBreakdown
    weekly_match_statistics: CharacterPvPBracketStatisticsBreakdown


class CharacterPvPSummaryMapStatistics(TypedDict):
    world_map: SoulbindFollower
    match_statistics: CharacterPvPBracketStatisticsBreakdown


class CharacterPvPSummary(TypedDict):
    _links: Links
    honor_level: int
    pvp_map_statistics: List[CharacterPvPSummaryMapStatistics]
    honorable_kills: int
    character: CharacterAchievementStatisticsCharacterReference


class CharacterQuests(TypedDict):
    _links: Links
    character: CharacterAchievementStatisticsCharacterReference
    in_progress: List[KeyValue]
    completed: Link


class CharacterCompletedQuests(TypedDict):
    _links: Links
    character: CharacterAchievementStatisticsCharacterReference
    quests: List[KeyValue]


class CharacterReputationsStanding(TypedDict):
    raw: int
    value: int
    max: int
    tier: int
    name: str


class CharacterReputationsReference(TypedDict):
    faction: KeyValue
    standing: CharacterReputationsStanding


class CharacterReputations(TypedDict):
    _links: Links
    character: CharacterAchievementStatisticsCharacterReference
    reputations: List[CharacterReputationsReference]


class CharacterSoulbinds(TypedDict):
    _links: Links
    character: CharacterAchievementStatisticsCharacterReference
    chosen_covenant: KeyValue
    renown_level: int


class Specialization(TypedDict):
    specialization: KeyValue
    glyphs: List[KeyValue]
    pvp_talent_slots: List["PvPTalentSlot"]
    loadouts: List["Loadout"]


class PvPTalentSlot(TypedDict):
    selected: "PvPTalent"
    slot_number: int


class SpellTooltip(TypedDict):
    spell: KeyValue
    description: str
    cast_time: str
    power_cost: Optional[str]
    range: Optional[str]
    cooldown: Optional[str]


class PvPTalent(TypedDict):
    talent: KeyValue
    spell_tooltip: SpellTooltip


class Loadout(TypedDict):
    is_active: bool
    talent_loadout_code: str
    selected_class_talents: List["SelectedTalent"]
    selected_spec_talents: Optional[List["SelectedTalent"]]
    selected_class_talent_tree: KeyValue
    selected_spec_talent_tree: KeyValue


class SelectedTalent(TypedDict):
    id: int
    rank: int
    tooltip: "TalentTooltip"


class TalentTooltip(TypedDict):
    talent: KeyValue
    spell_tooltip: SpellTooltip


class CharacterSpecializationsSummary(TypedDict):
    _links: Links
    specializations: List["Specialization"]
    active_specialization: KeyValue
    character: CharacterReference
    active_hero_talent: Optional[dict]


class CharacterStatisticsSummaryValue(TypedDict):
    rating: int
    rating_bonus: float
    value: Optional[float]


class CharacterStatisticsSummaryEffective(TypedDict):
    base: int
    effective: int


class CharacterStatisticsSummary(TypedDict):
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


class CharacterTitlesSummary(TypedDict):
    _links: Links
    character: CharacterReference
    active_title: CharacterProfileSummaryTitle
    titles: List[KeyValue]


class GuildCrestComponent(TypedDict):
    id: int
    media: GenericID
    color: GuildCrestColor


class GuildCrest(TypedDict):
    emblem: GuildCrestComponent
    border: GuildCrestComponent
    background: GuildCrestColor


class GuildRealm(TypedDict):
    key: Link
    name: str
    id: int
    slug: str


class Guild(TypedDict):
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


class GuildActivitiesCharacterAchievement(TypedDict):
    character: KeyValue
    realm: GuildRealm


class GuildActivitiesActivity(TypedDict):
    type: str


class GuildActivities(TypedDict):
    character_achievement: GuildActivitiesCharacterAchievement
    activity: GuildActivitiesActivity
    timestamp: int


class GuildActivityGuild(TypedDict):
    key: Link
    name: str
    id: int
    realm: GuildRealm
    faction: FactionType


class GuildActivity(TypedDict):
    _links: Links
    guild: GuildActivityGuild
    activities: List[GuildActivities]


class GuildAchievementsGuild(TypedDict):
    key: Link
    name: str
    id: int
    realm: Realm
    faction: FactionType


class GuildAchievementsGuildAchievement(TypedDict):
    id: int
    achievement: KeyValue
    criteria: Optional["GuildAchievementsAchievementCriteria"]
    completed_timestamp: Optional[int]


class GuildAchievementsAchievementCriteria(TypedDict):
    id: int
    is_completed: bool
    child_criteria: Optional[List["GuildAchievementsChildCriteria"]]


class GuildAchievementsChildCriteria(TypedDict):
    id: int
    amount: int
    is_completed: bool


class GuildAchievementsCategoryProgress(TypedDict):
    category: KeyValue
    quantity: int
    points: int


class GuildAchievementsRecentEvent(TypedDict):
    achievement: KeyValue
    timestamp: int


class GuildAchievements(TypedDict):
    _links: Links
    guild: Guild
    total_quantity: int
    total_points: int
    achievements: List["GuildAchievementsGuildAchievement"]
    category_progress: List["GuildAchievementsCategoryProgress"]
    recent_events: List["GuildAchievementsRecentEvent"]


class GuildRosterMemberCharacter(TypedDict):
    key: Link
    name: str
    id: int
    realm: Realm
    level: int
    playable_class: GenericID
    playable_race: GenericID


class GuildRosterMember(TypedDict):
    character: GuildRosterMemberCharacter
    rank: int


class GuildRosterGuild(TypedDict):
    key: Link
    name: str
    id: int
    realm: Realm
    faction: FactionType


class GuildRoster(TypedDict):
    _links: Links
    guild: GuildRosterGuild
    members: List[GuildRosterMember]
