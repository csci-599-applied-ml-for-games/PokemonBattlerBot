'''
This class holds the game state
'''

from enum import IntEnum, auto

INDEX_TRACKER = 0
def increment_index():
	global INDEX_TRACKER
	INDEX_TRACKER += 1
	return INDEX_TRACKER

SHARED_INDEX_TRACKER = 0
def increment_shared_index():
	global SHARED_INDEX_TRACKER
	SHARED_INDEX_TRACKER += 1
	return SHARED_INDEX_TRACKER

TEAM_INDEX_TRACKER = 0
def increment_team_index():
	global TEAM_INDEX_TRACKER
	TEAM_INDEX_TRACKER += 1
	return TEAM_INDEX_TRACKER


def attribute_dict_setup(attribute_dict):
	reversed_dict = {v: k for k, v in attribute_dict.items()}
	our_min = min([v for k, v in attribute_dict.items()])
	attribute_dict['Count'] = len(attribute_dict)
	attribute_dict['Min'] = our_min
	return attribute_dict, reversed_dict 

WEATHER_NAME_TO_INDEX = {
	'RainDance': SHARED_INDEX_TRACKER,
	'PrimordialSea': increment_shared_index(),
	'SunnyDay': increment_shared_index(),
	'DesolateLand': increment_shared_index(),
	'Sandstorm': increment_shared_index(),
	'Hail': increment_shared_index(),
	'DeltaStream': increment_shared_index(),
	'NotFound': increment_shared_index()
}
_, INDEX_TO_WEATHER_NAME = attribute_dict_setup(WEATHER_NAME_TO_INDEX)

SHARED_ATTRIBUTES_COUNT = SHARED_INDEX_TRACKER + 1

MAX_BOOST = 12.0
MIN_BOOST = 0.0
ACTIVE_POKEMON_BOOST = {
	'atk': TEAM_INDEX_TRACKER,
	'def': increment_team_index(),
	'spa': increment_team_index(),
	'spd': increment_team_index(),
	'spe': increment_team_index(),
	'accuracy': increment_team_index(),
	'evasion': increment_team_index(), 
	'NotFound': increment_team_index()
}

ACTIVE_POKEMON_NAME_TO_INDEX = {
	'Pelipper': increment_team_index(),
	'Greninja': increment_team_index(), 
	'Swampert': increment_team_index(),
	'Manaphy': increment_team_index(),
	'Ferrothorn': increment_team_index(),
	'Tornadus': increment_team_index(),
	'Tornadus-Therian': increment_team_index(), 
	'NotFound': increment_team_index(), 
}
_, ACTIVE_INDEX_TO_POKEMON_NAME = attribute_dict_setup(ACTIVE_POKEMON_NAME_TO_INDEX)

ACTIVE_MOVE_NAME_TO_INDEX = {
	'knockoff': increment_team_index(),
	'uturn': increment_team_index(),
	'scald': increment_team_index(),
	'roost': increment_team_index(),
	'hydropump': increment_team_index(),  
	'darkpulse': increment_team_index(),
	'watershuriken': increment_team_index(),
	'spikes': increment_team_index(),
	'waterfall': increment_team_index(),
	'earthquake': increment_team_index(),
	'icepunch': increment_team_index(),
	'superpower': increment_team_index(),
	'tailglow': increment_team_index(),
	'surf': increment_team_index(),
	'icebeam': increment_team_index(),
	'rest': increment_team_index(), 
	'stealthrock': increment_team_index(),
	'toxic': increment_team_index(),
	'powerwhip': increment_team_index(),
	'hurricane': increment_team_index(),
	'defog': increment_team_index(),

	# Z-moves only below this comment
	'hydrovortex': increment_team_index(),
	'NotFound': increment_team_index(),
}
_, ACTIVE_INDEX_TO_MOVE_NAME = attribute_dict_setup(ACTIVE_MOVE_NAME_TO_INDEX)

ACTIVE_TYPE_NAME_TO_INDEX = {
	'Normal': increment_team_index(),
	'Fire': increment_team_index(),
	'Water': increment_team_index(),
	'Grass': increment_team_index(),
	'Electric': increment_team_index(),
	'Ice': increment_team_index(),
	'Fighting': increment_team_index(),
	'Poison': increment_team_index(),
	'Ground': increment_team_index(),
	'Flying': increment_team_index(),
	'Psychic': increment_team_index(),
	'Bug': increment_team_index(),
	'Ghost': increment_team_index(),
	'Dark': increment_team_index(),
	'Dragon': increment_team_index(),
	'Steel': increment_team_index(),
	'Fairy': increment_team_index(),
	'NotFound': increment_team_index(),
}
_, ACTIVE_INDEX_TO_TYPE_NAME = attribute_dict_setup(ACTIVE_TYPE_NAME_TO_INDEX)

ACTIVE_STATUS_NAME_TO_INDEX = {
	'brn': increment_team_index(),
	'par': increment_team_index(),
	'slp': increment_team_index(),
	'frz': increment_team_index(),
	'psn': increment_team_index(),
	'tox': increment_team_index(),
	'confusion': increment_team_index(),
	'curse': increment_team_index(),
	'flinch': increment_team_index(),
	'trapped': increment_team_index(),
	'trapper': increment_team_index(),
	'partiallytrapped': increment_team_index(),
	'lockedmove': increment_team_index(),
	'twoturnmove': increment_team_index(),
	'choicelock': increment_team_index(),
	'mustrecharge': increment_team_index(),
	'futuremove': increment_team_index(),
	'healreplacement': increment_team_index(),
	'stall': increment_team_index(),
	'gem': increment_team_index(),
	'raindance': increment_team_index(),
	'primordialsea': increment_team_index(),
	'sunnyday': increment_team_index(),
	'desolateland': increment_team_index(),
	'sandstorm': increment_team_index(),
	'hail': increment_team_index(),
	'deltastream': increment_team_index(),
	'arceus': increment_team_index(),
	'silvally': increment_team_index(),
	'NotFound': increment_team_index(),
}
_, ACTIVE_INDEX_TO_STATUS_NAME = attribute_dict_setup(ACTIVE_STATUS_NAME_TO_INDEX)

# Magic number to normalize stat values for input vector
# For eg. 1245 spa => 1245/2000 = 0.6225 value in vector
STAT_NORMALIZER = 2000
ACTIVE_STAT_NAME_TO_INDEX = {
	'atk': increment_team_index(),
	'def': increment_team_index(),
	'spa': increment_team_index(),
	'spd': increment_team_index(),
	'spe': increment_team_index(),
	'NotFound': increment_team_index(),
}
_, INDEX_TO_STAT_NAME = attribute_dict_setup(ACTIVE_STAT_NAME_TO_INDEX)

ACTIVE_NORMALIZED_HEALTH = increment_team_index()

# Magic number to normalize the quantity of an entry hazard for 
# input vactor. For eg. 3 spikes => 3/10 = 0.3 value in vector
MAX_ENTRY_HAZARD_COUNT = 10
ENTRY_HAZARD_TO_INDEX = {
	'Spikes': increment_team_index(),
	'Stealth Rock': increment_team_index(),
	'Toxic Spikes': increment_team_index(),
	'Sticky Web': increment_team_index(),
	'NotFound': increment_team_index(),
}
_, INDEX_TO_ENTRY_HAZARD = attribute_dict_setup(ENTRY_HAZARD_TO_INDEX)

TEAM_ATTRIBUTES_COUNT = TEAM_INDEX_TRACKER + 1
'''
OLD POKEMON NAME TO INDEX

POKEMON_NAME_TO_INDEX = {
	'Pelipper': INDEX_TRACKER,
	'Greninja': increment_index(), 
	'Swampert': increment_index(),
	'Manaphy': increment_index(),
	'Ferrothorn': increment_index(),
	'Tornadus': increment_index(),
	'Tornadus-Therian': increment_index(), 
	'NotFound': increment_index(), 
}
'''
POKEMON_NAME_TO_INDEX = {
	'Pelipper' :  INDEX_TRACKER,
	'Bulbasaur' :  increment_index(),
	'Ivysaur' :  increment_index(),
	'Venusaur' :  increment_index(),
	'Charmander' :  increment_index(),
	'Charmeleon' :  increment_index(),
	'Charizard' :  increment_index(),
	'Squirtle' :  increment_index(),
	'Wartortle' :  increment_index(),
	'Blastoise' :  increment_index(),
	'Caterpie' :  increment_index(),
	'Metapod' :  increment_index(),
	'Butterfree' :  increment_index(),
	'Weedle' :  increment_index(),
	'Kakuna' :  increment_index(),
	'Beedrill' :  increment_index(),
	'Pidgey' :  increment_index(),
	'Pidgeotto' :  increment_index(),
	'Pidgeot' :  increment_index(),
	'Rattata' :  increment_index(),
	'Raticate' :  increment_index(),
	'Spearow' :  increment_index(),
	'Fearow' :  increment_index(),
	'Ekans' :  increment_index(),
	'Arbok' :  increment_index(),
	'Pikachu' :  increment_index(),
	'Raichu' :  increment_index(),
	'Sandshrew' :  increment_index(),
	'Sandslash' :  increment_index(),
	'Nidoran-F' :  increment_index(),
	'Nidorina' :  increment_index(),
	'Nidoqueen' :  increment_index(),
	'Nidoran-M' :  increment_index(),
	'Nidorino' :  increment_index(),
	'Nidoking' :  increment_index(),
	'Clefairy' :  increment_index(),
	'Clefable' :  increment_index(),
	'Vulpix' :  increment_index(),
	'Ninetales' :  increment_index(),
	'Jigglypuff' :  increment_index(),
	'Wigglytuff' :  increment_index(),
	'Zubat' :  increment_index(),
	'Golbat' :  increment_index(),
	'Oddish' :  increment_index(),
	'Gloom' :  increment_index(),
	'Vileplume' :  increment_index(),
	'Paras' :  increment_index(),
	'Parasect' :  increment_index(),
	'Venonat' :  increment_index(),
	'Venomoth' :  increment_index(),
	'Diglett' :  increment_index(),
	'Dugtrio' :  increment_index(),
	'Meowth' :  increment_index(),
	'Persian' :  increment_index(),
	'Psyduck' :  increment_index(),
	'Golduck' :  increment_index(),
	'Mankey' :  increment_index(),
	'Primeape' :  increment_index(),
	'Growlithe' :  increment_index(),
	'Arcanine' :  increment_index(),
	'Poliwag' :  increment_index(),
	'Poliwhirl' :  increment_index(),
	'Poliwrath' :  increment_index(),
	'Abra' :  increment_index(),
	'Kadabra' :  increment_index(),
	'Alakazam' :  increment_index(),
	'Machop' :  increment_index(),
	'Machoke' :  increment_index(),
	'Machamp' :  increment_index(),
	'Bellsprout' :  increment_index(),
	'Weepinbell' :  increment_index(),
	'Victreebel' :  increment_index(),
	'Tentacool' :  increment_index(),
	'Tentacruel' :  increment_index(),
	'Geodude' :  increment_index(),
	'Graveler' :  increment_index(),
	'Golem' :  increment_index(),
	'Ponyta' :  increment_index(),
	'Rapidash' :  increment_index(),
	'Slowpoke' :  increment_index(),
	'Slowbro' :  increment_index(),
	'Magnemite' :  increment_index(),
	'Magneton' :  increment_index(),
	'Farfetchd' :  increment_index(),
	'Doduo' :  increment_index(),
	'Dodrio' :  increment_index(),
	'Seel' :  increment_index(),
	'Dewgong' :  increment_index(),
	'Grimer' :  increment_index(),
	'Muk' :  increment_index(),
	'Shellder' :  increment_index(),
	'Cloyster' :  increment_index(),
	'Gastly' :  increment_index(),
	'Haunter' :  increment_index(),
	'Gengar' :  increment_index(),
	'Onix' :  increment_index(),
	'Drowzee' :  increment_index(),
	'Hypno' :  increment_index(),
	'Krabby' :  increment_index(),
	'Kingler' :  increment_index(),
	'Voltorb' :  increment_index(),
	'Electrode' :  increment_index(),
	'Exeggcute' :  increment_index(),
	'Exeggutor' :  increment_index(),
	'Cubone' :  increment_index(),
	'Marowak' :  increment_index(),
	'Hitmonlee' :  increment_index(),
	'Hitmonchan' :  increment_index(),
	'Lickitung' :  increment_index(),
	'Koffing' :  increment_index(),
	'Weezing' :  increment_index(),
	'Rhyhorn' :  increment_index(),
	'Rhydon' :  increment_index(),
	'Chansey' :  increment_index(),
	'Tangela' :  increment_index(),
	'Kangaskhan' :  increment_index(),
	'Horsea' :  increment_index(),
	'Seadra' :  increment_index(),
	'Goldeen' :  increment_index(),
	'Seaking' :  increment_index(),
	'Staryu' :  increment_index(),
	'Starmie' :  increment_index(),
	'Mr-Mime' :  increment_index(),
	'Scyther' :  increment_index(),
	'Jynx' :  increment_index(),
	'Electabuzz' :  increment_index(),
	'Magmar' :  increment_index(),
	'Pinsir' :  increment_index(),
	'Tauros' :  increment_index(),
	'Magikarp' :  increment_index(),
	'Gyarados' :  increment_index(),
	'Lapras' :  increment_index(),
	'Ditto' :  increment_index(),
	'Eevee' :  increment_index(),
	'Vaporeon' :  increment_index(),
	'Jolteon' :  increment_index(),
	'Flareon' :  increment_index(),
	'Porygon' :  increment_index(),
	'Omanyte' :  increment_index(),
	'Omastar' :  increment_index(),
	'Kabuto' :  increment_index(),
	'Kabutops' :  increment_index(),
	'Aerodactyl' :  increment_index(),
	'Snorlax' :  increment_index(),
	'Articuno' :  increment_index(),
	'Zapdos' :  increment_index(),
	'Moltres' :  increment_index(),
	'Dratini' :  increment_index(),
	'Dragonair' :  increment_index(),
	'Dragonite' :  increment_index(),
	'Mewtwo' :  increment_index(),
	'Mew' :  increment_index(),
	'Chikorita' :  increment_index(),
	'Bayleef' :  increment_index(),
	'Meganium' :  increment_index(),
	'Cyndaquil' :  increment_index(),
	'Quilava' :  increment_index(),
	'Typhlosion' :  increment_index(),
	'Totodile' :  increment_index(),
	'Croconaw' :  increment_index(),
	'Feraligatr' :  increment_index(),
	'Sentret' :  increment_index(),
	'Furret' :  increment_index(),
	'Hoothoot' :  increment_index(),
	'Noctowl' :  increment_index(),
	'Ledyba' :  increment_index(),
	'Ledian' :  increment_index(),
	'Spinarak' :  increment_index(),
	'Ariados' :  increment_index(),
	'Crobat' :  increment_index(),
	'Chinchou' :  increment_index(),
	'Lanturn' :  increment_index(),
	'Pichu' :  increment_index(),
	'Cleffa' :  increment_index(),
	'Igglybuff' :  increment_index(),
	'Togepi' :  increment_index(),
	'Togetic' :  increment_index(),
	'Natu' :  increment_index(),
	'Xatu' :  increment_index(),
	'Mareep' :  increment_index(),
	'Flaaffy' :  increment_index(),
	'Ampharos' :  increment_index(),
	'Bellossom' :  increment_index(),
	'Marill' :  increment_index(),
	'Azumarill' :  increment_index(),
	'Sudowoodo' :  increment_index(),
	'Politoed' :  increment_index(),
	'Hoppip' :  increment_index(),
	'Skiploom' :  increment_index(),
	'Jumpluff' :  increment_index(),
	'Aipom' :  increment_index(),
	'Sunkern' :  increment_index(),
	'Sunflora' :  increment_index(),
	'Yanma' :  increment_index(),
	'Wooper' :  increment_index(),
	'Quagsire' :  increment_index(),
	'Espeon' :  increment_index(),
	'Umbreon' :  increment_index(),
	'Murkrow' :  increment_index(),
	'Slowking' :  increment_index(),
	'Misdreavus' :  increment_index(),
	'Unown' :  increment_index(),
	'Wobbuffet' :  increment_index(),
	'Girafarig' :  increment_index(),
	'Pineco' :  increment_index(),
	'Forretress' :  increment_index(),
	'Dunsparce' :  increment_index(),
	'Gligar' :  increment_index(),
	'Steelix' :  increment_index(),
	'Snubbull' :  increment_index(),
	'Granbull' :  increment_index(),
	'Qwilfish' :  increment_index(),
	'Scizor' :  increment_index(),
	'Shuckle' :  increment_index(),
	'Heracross' :  increment_index(),
	'Sneasel' :  increment_index(),
	'Teddiursa' :  increment_index(),
	'Ursaring' :  increment_index(),
	'Slugma' :  increment_index(),
	'Magcargo' :  increment_index(),
	'Swinub' :  increment_index(),
	'Piloswine' :  increment_index(),
	'Corsola' :  increment_index(),
	'Remoraid' :  increment_index(),
	'Octillery' :  increment_index(),
	'Delibird' :  increment_index(),
	'Mantine' :  increment_index(),
	'Skarmory' :  increment_index(),
	'Houndour' :  increment_index(),
	'Houndoom' :  increment_index(),
	'Kingdra' :  increment_index(),
	'Phanpy' :  increment_index(),
	'Donphan' :  increment_index(),
	'Porygon2' :  increment_index(),
	'Stantler' :  increment_index(),
	'Smeargle' :  increment_index(),
	'Tyrogue' :  increment_index(),
	'Hitmontop' :  increment_index(),
	'Smoochum' :  increment_index(),
	'Elekid' :  increment_index(),
	'Magby' :  increment_index(),
	'Miltank' :  increment_index(),
	'Blissey' :  increment_index(),
	'Raikou' :  increment_index(),
	'Entei' :  increment_index(),
	'Suicune' :  increment_index(),
	'Larvitar' :  increment_index(),
	'Pupitar' :  increment_index(),
	'Tyranitar' :  increment_index(),
	'Lugia' :  increment_index(),
	'Ho-Oh' :  increment_index(),
	'Celebi' :  increment_index(),
	'Treecko' :  increment_index(),
	'Grovyle' :  increment_index(),
	'Sceptile' :  increment_index(),
	'Torchic' :  increment_index(),
	'Combusken' :  increment_index(),
	'Blaziken' :  increment_index(),
	'Mudkip' :  increment_index(),
	'Marshtomp' :  increment_index(),
	'Swampert' :  increment_index(),
	'Poochyena' :  increment_index(),
	'Mightyena' :  increment_index(),
	'Zigzagoon' :  increment_index(),
	'Linoone' :  increment_index(),
	'Wurmple' :  increment_index(),
	'Silcoon' :  increment_index(),
	'Beautifly' :  increment_index(),
	'Cascoon' :  increment_index(),
	'Dustox' :  increment_index(),
	'Lotad' :  increment_index(),
	'Lombre' :  increment_index(),
	'Ludicolo' :  increment_index(),
	'Seedot' :  increment_index(),
	'Nuzleaf' :  increment_index(),
	'Shiftry' :  increment_index(),
	'Taillow' :  increment_index(),
	'Swellow' :  increment_index(),
	'Wingull' :  increment_index(),
	'Ralts' :  increment_index(),
	'Kirlia' :  increment_index(),
	'Gardevoir' :  increment_index(),
	'Surskit' :  increment_index(),
	'Masquerain' :  increment_index(),
	'Shroomish' :  increment_index(),
	'Breloom' :  increment_index(),
	'Slakoth' :  increment_index(),
	'Vigoroth' :  increment_index(),
	'Slaking' :  increment_index(),
	'Nincada' :  increment_index(),
	'Ninjask' :  increment_index(),
	'Shedinja' :  increment_index(),
	'Whismur' :  increment_index(),
	'Loudred' :  increment_index(),
	'Exploud' :  increment_index(),
	'Makuhita' :  increment_index(),
	'Hariyama' :  increment_index(),
	'Azurill' :  increment_index(),
	'Nosepass' :  increment_index(),
	'Skitty' :  increment_index(),
	'Delcatty' :  increment_index(),
	'Sableye' :  increment_index(),
	'Mawile' :  increment_index(),
	'Aron' :  increment_index(),
	'Lairon' :  increment_index(),
	'Aggron' :  increment_index(),
	'Meditite' :  increment_index(),
	'Medicham' :  increment_index(),
	'Electrike' :  increment_index(),
	'Manectric' :  increment_index(),
	'Plusle' :  increment_index(),
	'Minun' :  increment_index(),
	'Volbeat' :  increment_index(),
	'Illumise' :  increment_index(),
	'Roselia' :  increment_index(),
	'Gulpin' :  increment_index(),
	'Swalot' :  increment_index(),
	'Carvanha' :  increment_index(),
	'Sharpedo' :  increment_index(),
	'Wailmer' :  increment_index(),
	'Wailord' :  increment_index(),
	'Numel' :  increment_index(),
	'Camerupt' :  increment_index(),
	'Torkoal' :  increment_index(),
	'Spoink' :  increment_index(),
	'Grumpig' :  increment_index(),
	'Spinda' :  increment_index(),
	'Trapinch' :  increment_index(),
	'Vibrava' :  increment_index(),
	'Flygon' :  increment_index(),
	'Cacnea' :  increment_index(),
	'Cacturne' :  increment_index(),
	'Swablu' :  increment_index(),
	'Altaria' :  increment_index(),
	'Zangoose' :  increment_index(),
	'Seviper' :  increment_index(),
	'Lunatone' :  increment_index(),
	'Solrock' :  increment_index(),
	'Barboach' :  increment_index(),
	'Whiscash' :  increment_index(),
	'Corphish' :  increment_index(),
	'Crawdaunt' :  increment_index(),
	'Baltoy' :  increment_index(),
	'Claydol' :  increment_index(),
	'Lileep' :  increment_index(),
	'Cradily' :  increment_index(),
	'Anorith' :  increment_index(),
	'Armaldo' :  increment_index(),
	'Feebas' :  increment_index(),
	'Milotic' :  increment_index(),
	'Castform' :  increment_index(),
	'Kecleon' :  increment_index(),
	'Shuppet' :  increment_index(),
	'Banette' :  increment_index(),
	'Duskull' :  increment_index(),
	'Dusclops' :  increment_index(),
	'Tropius' :  increment_index(),
	'Chimecho' :  increment_index(),
	'Absol' :  increment_index(),
	'Wynaut' :  increment_index(),
	'Snorunt' :  increment_index(),
	'Glalie' :  increment_index(),
	'Spheal' :  increment_index(),
	'Sealeo' :  increment_index(),
	'Walrein' :  increment_index(),
	'Clamperl' :  increment_index(),
	'Huntail' :  increment_index(),
	'Gorebyss' :  increment_index(),
	'Relicanth' :  increment_index(),
	'Luvdisc' :  increment_index(),
	'Bagon' :  increment_index(),
	'Shelgon' :  increment_index(),
	'Salamence' :  increment_index(),
	'Beldum' :  increment_index(),
	'Metang' :  increment_index(),
	'Metagross' :  increment_index(),
	'Regirock' :  increment_index(),
	'Regice' :  increment_index(),
	'Registeel' :  increment_index(),
	'Latias' :  increment_index(),
	'Latios' :  increment_index(),
	'Kyogre' :  increment_index(),
	'Groudon' :  increment_index(),
	'Rayquaza' :  increment_index(),
	'Jirachi' :  increment_index(),
	'Deoxys-Normal' :  increment_index(),
	'Turtwig' :  increment_index(),
	'Grotle' :  increment_index(),
	'Torterra' :  increment_index(),
	'Chimchar' :  increment_index(),
	'Monferno' :  increment_index(),
	'Infernape' :  increment_index(),
	'Piplup' :  increment_index(),
	'Prinplup' :  increment_index(),
	'Empoleon' :  increment_index(),
	'Starly' :  increment_index(),
	'Staravia' :  increment_index(),
	'Staraptor' :  increment_index(),
	'Bidoof' :  increment_index(),
	'Bibarel' :  increment_index(),
	'Kricketot' :  increment_index(),
	'Kricketune' :  increment_index(),
	'Shinx' :  increment_index(),
	'Luxio' :  increment_index(),
	'Luxray' :  increment_index(),
	'Budew' :  increment_index(),
	'Roserade' :  increment_index(),
	'Cranidos' :  increment_index(),
	'Rampardos' :  increment_index(),
	'Shieldon' :  increment_index(),
	'Bastiodon' :  increment_index(),
	'Burmy' :  increment_index(),
	'Wormadam-Plant' :  increment_index(),
	'Mothim' :  increment_index(),
	'Combee' :  increment_index(),
	'Vespiquen' :  increment_index(),
	'Pachirisu' :  increment_index(),
	'Buizel' :  increment_index(),
	'Floatzel' :  increment_index(),
	'Cherubi' :  increment_index(),
	'Cherrim' :  increment_index(),
	'Shellos' :  increment_index(),
	'Gastrodon' :  increment_index(),
	'Ambipom' :  increment_index(),
	'Drifloon' :  increment_index(),
	'Drifblim' :  increment_index(),
	'Buneary' :  increment_index(),
	'Lopunny' :  increment_index(),
	'Mismagius' :  increment_index(),
	'Honchkrow' :  increment_index(),
	'Glameow' :  increment_index(),
	'Purugly' :  increment_index(),
	'Chingling' :  increment_index(),
	'Stunky' :  increment_index(),
	'Skuntank' :  increment_index(),
	'Bronzor' :  increment_index(),
	'Bronzong' :  increment_index(),
	'Bonsly' :  increment_index(),
	'Mime-Jr' :  increment_index(),
	'Happiny' :  increment_index(),
	'Chatot' :  increment_index(),
	'Spiritomb' :  increment_index(),
	'Gible' :  increment_index(),
	'Gabite' :  increment_index(),
	'Garchomp' :  increment_index(),
	'Munchlax' :  increment_index(),
	'Riolu' :  increment_index(),
	'Lucario' :  increment_index(),
	'Hippopotas' :  increment_index(),
	'Hippowdon' :  increment_index(),
	'Skorupi' :  increment_index(),
	'Drapion' :  increment_index(),
	'Croagunk' :  increment_index(),
	'Toxicroak' :  increment_index(),
	'Carnivine' :  increment_index(),
	'Finneon' :  increment_index(),
	'Lumineon' :  increment_index(),
	'Mantyke' :  increment_index(),
	'Snover' :  increment_index(),
	'Abomasnow' :  increment_index(),
	'Weavile' :  increment_index(),
	'Magnezone' :  increment_index(),
	'Lickilicky' :  increment_index(),
	'Rhyperior' :  increment_index(),
	'Tangrowth' :  increment_index(),
	'Electivire' :  increment_index(),
	'Magmortar' :  increment_index(),
	'Togekiss' :  increment_index(),
	'Yanmega' :  increment_index(),
	'Leafeon' :  increment_index(),
	'Glaceon' :  increment_index(),
	'Gliscor' :  increment_index(),
	'Mamoswine' :  increment_index(),
	'Porygon-Z' :  increment_index(),
	'Gallade' :  increment_index(),
	'Probopass' :  increment_index(),
	'Dusknoir' :  increment_index(),
	'Froslass' :  increment_index(),
	'Rotom' :  increment_index(),
	'Uxie' :  increment_index(),
	'Mesprit' :  increment_index(),
	'Azelf' :  increment_index(),
	'Dialga' :  increment_index(),
	'Palkia' :  increment_index(),
	'Heatran' :  increment_index(),
	'Regigigas' :  increment_index(),
	'Giratina-Altered' :  increment_index(),
	'Cresselia' :  increment_index(),
	'Phione' :  increment_index(),
	'Manaphy' :  increment_index(),
	'Darkrai' :  increment_index(),
	'Shaymin-Land' :  increment_index(),
	'Arceus' :  increment_index(),
	'Victini' :  increment_index(),
	'Snivy' :  increment_index(),
	'Servine' :  increment_index(),
	'Serperior' :  increment_index(),
	'Tepig' :  increment_index(),
	'Pignite' :  increment_index(),
	'Emboar' :  increment_index(),
	'Oshawott' :  increment_index(),
	'Dewott' :  increment_index(),
	'Samurott' :  increment_index(),
	'Patrat' :  increment_index(),
	'Watchog' :  increment_index(),
	'Lillipup' :  increment_index(),
	'Herdier' :  increment_index(),
	'Stoutland' :  increment_index(),
	'Purrloin' :  increment_index(),
	'Liepard' :  increment_index(),
	'Pansage' :  increment_index(),
	'Simisage' :  increment_index(),
	'Pansear' :  increment_index(),
	'Simisear' :  increment_index(),
	'Panpour' :  increment_index(),
	'Simipour' :  increment_index(),
	'Munna' :  increment_index(),
	'Musharna' :  increment_index(),
	'Pidove' :  increment_index(),
	'Tranquill' :  increment_index(),
	'Unfezant' :  increment_index(),
	'Blitzle' :  increment_index(),
	'Zebstrika' :  increment_index(),
	'Roggenrola' :  increment_index(),
	'Boldore' :  increment_index(),
	'Gigalith' :  increment_index(),
	'Woobat' :  increment_index(),
	'Swoobat' :  increment_index(),
	'Drilbur' :  increment_index(),
	'Excadrill' :  increment_index(),
	'Audino' :  increment_index(),
	'Timburr' :  increment_index(),
	'Gurdurr' :  increment_index(),
	'Conkeldurr' :  increment_index(),
	'Tympole' :  increment_index(),
	'Palpitoad' :  increment_index(),
	'Seismitoad' :  increment_index(),
	'Throh' :  increment_index(),
	'Sawk' :  increment_index(),
	'Sewaddle' :  increment_index(),
	'Swadloon' :  increment_index(),
	'Leavanny' :  increment_index(),
	'Venipede' :  increment_index(),
	'Whirlipede' :  increment_index(),
	'Scolipede' :  increment_index(),
	'Cottonee' :  increment_index(),
	'Whimsicott' :  increment_index(),
	'Petilil' :  increment_index(),
	'Lilligant' :  increment_index(),
	'Basculin-Red-Striped' :  increment_index(),
	'Sandile' :  increment_index(),
	'Krokorok' :  increment_index(),
	'Krookodile' :  increment_index(),
	'Darumaka' :  increment_index(),
	'Darmanitan-Standard' :  increment_index(),
	'Maractus' :  increment_index(),
	'Dwebble' :  increment_index(),
	'Crustle' :  increment_index(),
	'Scraggy' :  increment_index(),
	'Scrafty' :  increment_index(),
	'Sigilyph' :  increment_index(),
	'Yamask' :  increment_index(),
	'Cofagrigus' :  increment_index(),
	'Tirtouga' :  increment_index(),
	'Carracosta' :  increment_index(),
	'Archen' :  increment_index(),
	'Archeops' :  increment_index(),
	'Trubbish' :  increment_index(),
	'Garbodor' :  increment_index(),
	'Zorua' :  increment_index(),
	'Zoroark' :  increment_index(),
	'Minccino' :  increment_index(),
	'Cinccino' :  increment_index(),
	'Gothita' :  increment_index(),
	'Gothorita' :  increment_index(),
	'Gothitelle' :  increment_index(),
	'Solosis' :  increment_index(),
	'Duosion' :  increment_index(),
	'Reuniclus' :  increment_index(),
	'Ducklett' :  increment_index(),
	'Swanna' :  increment_index(),
	'Vanillite' :  increment_index(),
	'Vanillish' :  increment_index(),
	'Vanilluxe' :  increment_index(),
	'Deerling' :  increment_index(),
	'Sawsbuck' :  increment_index(),
	'Emolga' :  increment_index(),
	'Karrablast' :  increment_index(),
	'Escavalier' :  increment_index(),
	'Foongus' :  increment_index(),
	'Amoonguss' :  increment_index(),
	'Frillish' :  increment_index(),
	'Jellicent' :  increment_index(),
	'Alomomola' :  increment_index(),
	'Joltik' :  increment_index(),
	'Galvantula' :  increment_index(),
	'Ferroseed' :  increment_index(),
	'Ferrothorn' :  increment_index(),
	'Klink' :  increment_index(),
	'Klang' :  increment_index(),
	'Klinklang' :  increment_index(),
	'Tynamo' :  increment_index(),
	'Eelektrik' :  increment_index(),
	'Eelektross' :  increment_index(),
	'Elgyem' :  increment_index(),
	'Beheeyem' :  increment_index(),
	'Litwick' :  increment_index(),
	'Lampent' :  increment_index(),
	'Chandelure' :  increment_index(),
	'Axew' :  increment_index(),
	'Fraxure' :  increment_index(),
	'Haxorus' :  increment_index(),
	'Cubchoo' :  increment_index(),
	'Beartic' :  increment_index(),
	'Cryogonal' :  increment_index(),
	'Shelmet' :  increment_index(),
	'Accelgor' :  increment_index(),
	'Stunfisk' :  increment_index(),
	'Mienfoo' :  increment_index(),
	'Mienshao' :  increment_index(),
	'Druddigon' :  increment_index(),
	'Golett' :  increment_index(),
	'Golurk' :  increment_index(),
	'Pawniard' :  increment_index(),
	'Bisharp' :  increment_index(),
	'Bouffalant' :  increment_index(),
	'Rufflet' :  increment_index(),
	'Braviary' :  increment_index(),
	'Vullaby' :  increment_index(),
	'Mandibuzz' :  increment_index(),
	'Heatmor' :  increment_index(),
	'Durant' :  increment_index(),
	'Deino' :  increment_index(),
	'Zweilous' :  increment_index(),
	'Hydreigon' :  increment_index(),
	'Larvesta' :  increment_index(),
	'Volcarona' :  increment_index(),
	'Cobalion' :  increment_index(),
	'Terrakion' :  increment_index(),
	'Virizion' :  increment_index(),
	'Tornadus-Incarnate' :  increment_index(),
	'Thundurus-Incarnate' :  increment_index(),
	'Reshiram' :  increment_index(),
	'Zekrom' :  increment_index(),
	'Landorus-Incarnate' :  increment_index(),
	'Kyurem' :  increment_index(),
	'Keldeo-Ordinary' :  increment_index(),
	'Meloetta-Aria' :  increment_index(),
	'Genesect' :  increment_index(),
	'Chespin' :  increment_index(),
	'Quilladin' :  increment_index(),
	'Chesnaught' :  increment_index(),
	'Fennekin' :  increment_index(),
	'Braixen' :  increment_index(),
	'Delphox' :  increment_index(),
	'Froakie' :  increment_index(),
	'Frogadier' :  increment_index(),
	'Greninja' :  increment_index(),
	'Bunnelby' :  increment_index(),
	'Diggersby' :  increment_index(),
	'Fletchling' :  increment_index(),
	'Fletchinder' :  increment_index(),
	'Talonflame' :  increment_index(),
	'Scatterbug' :  increment_index(),
	'Spewpa' :  increment_index(),
	'Vivillon' :  increment_index(),
	'Litleo' :  increment_index(),
	'Pyroar' :  increment_index(),
	'Flabebe' :  increment_index(),
	'Floette' :  increment_index(),
	'Florges' :  increment_index(),
	'Skiddo' :  increment_index(),
	'Gogoat' :  increment_index(),
	'Pancham' :  increment_index(),
	'Pangoro' :  increment_index(),
	'Furfrou' :  increment_index(),
	'Espurr' :  increment_index(),
	'Meowstic-Male' :  increment_index(),
	'Honedge' :  increment_index(),
	'Doublade' :  increment_index(),
	'Aegislash-Shield' :  increment_index(),
	'Spritzee' :  increment_index(),
	'Aromatisse' :  increment_index(),
	'Swirlix' :  increment_index(),
	'Slurpuff' :  increment_index(),
	'Inkay' :  increment_index(),
	'Malamar' :  increment_index(),
	'Binacle' :  increment_index(),
	'Barbaracle' :  increment_index(),
	'Skrelp' :  increment_index(),
	'Dragalge' :  increment_index(),
	'Clauncher' :  increment_index(),
	'Clawitzer' :  increment_index(),
	'Helioptile' :  increment_index(),
	'Heliolisk' :  increment_index(),
	'Tyrunt' :  increment_index(),
	'Tyrantrum' :  increment_index(),
	'Amaura' :  increment_index(),
	'Aurorus' :  increment_index(),
	'Sylveon' :  increment_index(),
	'Hawlucha' :  increment_index(),
	'Dedenne' :  increment_index(),
	'Carbink' :  increment_index(),
	'Goomy' :  increment_index(),
	'Sliggoo' :  increment_index(),
	'Goodra' :  increment_index(),
	'Klefki' :  increment_index(),
	'Phantump' :  increment_index(),
	'Trevenant' :  increment_index(),
	'Pumpkaboo-Average' :  increment_index(),
	'Gourgeist-Average' :  increment_index(),
	'Bergmite' :  increment_index(),
	'Avalugg' :  increment_index(),
	'Noibat' :  increment_index(),
	'Noivern' :  increment_index(),
	'Xerneas' :  increment_index(),
	'Yveltal' :  increment_index(),
	'Zygarde' :  increment_index(),
	'Diancie' :  increment_index(),
	'Hoopa' :  increment_index(),
	'Volcanion' :  increment_index(),
	'Rowlet' :  increment_index(),
	'Dartrix' :  increment_index(),
	'Decidueye' :  increment_index(),
	'Litten' :  increment_index(),
	'Torracat' :  increment_index(),
	'Incineroar' :  increment_index(),
	'Popplio' :  increment_index(),
	'Brionne' :  increment_index(),
	'Primarina' :  increment_index(),
	'Pikipek' :  increment_index(),
	'Trumbeak' :  increment_index(),
	'Toucannon' :  increment_index(),
	'Yungoos' :  increment_index(),
	'Gumshoos' :  increment_index(),
	'Grubbin' :  increment_index(),
	'Charjabug' :  increment_index(),
	'Vikavolt' :  increment_index(),
	'Crabrawler' :  increment_index(),
	'Crabominable' :  increment_index(),
	'Oricorio-Baile' :  increment_index(),
	'Cutiefly' :  increment_index(),
	'Ribombee' :  increment_index(),
	'Rockruff' :  increment_index(),
	'Lycanroc-Midday' :  increment_index(),
	'Wishiwashi-Solo' :  increment_index(),
	'Mareanie' :  increment_index(),
	'Toxapex' :  increment_index(),
	'Mudbray' :  increment_index(),
	'Mudsdale' :  increment_index(),
	'Dewpider' :  increment_index(),
	'Araquanid' :  increment_index(),
	'Fomantis' :  increment_index(),
	'Lurantis' :  increment_index(),
	'Morelull' :  increment_index(),
	'Shiinotic' :  increment_index(),
	'Salandit' :  increment_index(),
	'Salazzle' :  increment_index(),
	'Stufful' :  increment_index(),
	'Bewear' :  increment_index(),
	'Bounsweet' :  increment_index(),
	'Steenee' :  increment_index(),
	'Tsareena' :  increment_index(),
	'Comfey' :  increment_index(),
	'Oranguru' :  increment_index(),
	'Passimian' :  increment_index(),
	'Wimpod' :  increment_index(),
	'Golisopod' :  increment_index(),
	'Sandygast' :  increment_index(),
	'Palossand' :  increment_index(),
	'Pyukumuku' :  increment_index(),
	'Type-Null' :  increment_index(),
	'Silvally' :  increment_index(),
	'Minior-Red-Meteor' :  increment_index(),
	'Komala' :  increment_index(),
	'Turtonator' :  increment_index(),
	'Togedemaru' :  increment_index(),
	'Mimikyu-Disguised' :  increment_index(),
	'Bruxish' :  increment_index(),
	'Drampa' :  increment_index(),
	'Dhelmise' :  increment_index(),
	'Jangmo-O' :  increment_index(),
	'Hakamo-O' :  increment_index(),
	'Kommo-O' :  increment_index(),
	'Tapu-Koko' :  increment_index(),
	'Tapu-Lele' :  increment_index(),
	'Tapu-Bulu' :  increment_index(),
	'Tapu-Fini' :  increment_index(),
	'Cosmog' :  increment_index(),
	'Cosmoem' :  increment_index(),
	'Solgaleo' :  increment_index(),
	'Lunala' :  increment_index(),
	'Nihilego' :  increment_index(),
	'Buzzwole' :  increment_index(),
	'Pheromosa' :  increment_index(),
	'Xurkitree' :  increment_index(),
	'Celesteela' :  increment_index(),
	'Kartana' :  increment_index(),
	'Guzzlord' :  increment_index(),
	'Necrozma' :  increment_index(),
	'Magearna' :  increment_index(),
	'Marshadow' :  increment_index(),
	'Poipole' :  increment_index(),
	'Naganadel' :  increment_index(),
	'Stakataka' :  increment_index(),
	'Blacephalon' :  increment_index(),
	'Zeraora' :  increment_index(),
	'Deoxys-Attack' :  increment_index(),
	'Deoxys-Defense' :  increment_index(),
	'Deoxys-Speed' :  increment_index(),
	'Wormadam-Sandy' :  increment_index(),
	'Wormadam-Trash' :  increment_index(),
	'Shaymin-Sky' :  increment_index(),
	'Giratina-Origin' :  increment_index(),
	'Rotom-Heat' :  increment_index(),
	'Rotom-Wash' :  increment_index(),
	'Rotom-Frost' :  increment_index(),
	'Rotom-Fan' :  increment_index(),
	'Rotom-Mow' :  increment_index(),
	'Castform-Sunny' :  increment_index(),
	'Castform-Rainy' :  increment_index(),
	'Castform-Snowy' :  increment_index(),
	'Basculin-Blue-Striped' :  increment_index(),
	'Darmanitan-Zen' :  increment_index(),
	'Meloetta-Pirouette' :  increment_index(),
	'Tornadus-Therian' :  increment_index(),
	'Thundurus-Therian' :  increment_index(),
	'Landorus-Therian' :  increment_index(),
	'Kyurem-Black' :  increment_index(),
	'Kyurem-White' :  increment_index(),
	'Keldeo-Resolute' :  increment_index(),
	'Meowstic-Female' :  increment_index(),
	'Aegislash-Blade' :  increment_index(),
	'Pumpkaboo-Small' :  increment_index(),
	'Pumpkaboo-Large' :  increment_index(),
	'Pumpkaboo-Super' :  increment_index(),
	'Gourgeist-Small' :  increment_index(),
	'Gourgeist-Large' :  increment_index(),
	'Gourgeist-Super' :  increment_index(),
	'Venusaur-Mega' :  increment_index(),
	'Charizard-Mega-X' :  increment_index(),
	'Charizard-Mega-Y' :  increment_index(),
	'Blastoise-Mega' :  increment_index(),
	'Alakazam-Mega' :  increment_index(),
	'Gengar-Mega' :  increment_index(),
	'Kangaskhan-Mega' :  increment_index(),
	'Pinsir-Mega' :  increment_index(),
	'Gyarados-Mega' :  increment_index(),
	'Aerodactyl-Mega' :  increment_index(),
	'Mewtwo-Mega-X' :  increment_index(),
	'Mewtwo-Mega-Y' :  increment_index(),
	'Ampharos-Mega' :  increment_index(),
	'Scizor-Mega' :  increment_index(),
	'Heracross-Mega' :  increment_index(),
	'Houndoom-Mega' :  increment_index(),
	'Tyranitar-Mega' :  increment_index(),
	'Blaziken-Mega' :  increment_index(),
	'Gardevoir-Mega' :  increment_index(),
	'Mawile-Mega' :  increment_index(),
	'Aggron-Mega' :  increment_index(),
	'Medicham-Mega' :  increment_index(),
	'Manectric-Mega' :  increment_index(),
	'Banette-Mega' :  increment_index(),
	'Absol-Mega' :  increment_index(),
	'Garchomp-Mega' :  increment_index(),
	'Lucario-Mega' :  increment_index(),
	'Abomasnow-Mega' :  increment_index(),
	'Floette-Eternal' :  increment_index(),
	'Latias-Mega' :  increment_index(),
	'Latios-Mega' :  increment_index(),
	'Swampert-Mega' :  increment_index(),
	'Sceptile-Mega' :  increment_index(),
	'Sableye-Mega' :  increment_index(),
	'Altaria-Mega' :  increment_index(),
	'Gallade-Mega' :  increment_index(),
	'Audino-Mega' :  increment_index(),
	'Sharpedo-Mega' :  increment_index(),
	'Slowbro-Mega' :  increment_index(),
	'Steelix-Mega' :  increment_index(),
	'Pidgeot-Mega' :  increment_index(),
	'Glalie-Mega' :  increment_index(),
	'Diancie-Mega' :  increment_index(),
	'Metagross-Mega' :  increment_index(),
	'Kyogre-Primal' :  increment_index(),
	'Groudon-Primal' :  increment_index(),
	'Rayquaza-Mega' :  increment_index(),
	'Pikachu-Rock-Star' :  increment_index(),
	'Pikachu-Belle' :  increment_index(),
	'Pikachu-Pop-Star' :  increment_index(),
	'Pikachu-Phd' :  increment_index(),
	'Pikachu-Libre' :  increment_index(),
	'Pikachu-Cosplay' :  increment_index(),
	'Hoopa-Unbound' :  increment_index(),
	'Camerupt-Mega' :  increment_index(),
	'Lopunny-Mega' :  increment_index(),
	'Salamence-Mega' :  increment_index(),
	'Beedrill-Mega' :  increment_index(),
	'Rattata-Alola' :  increment_index(),
	'Raticate-Alola' :  increment_index(),
	'Raticate-Totem-Alola' :  increment_index(),
	'Pikachu-Original-Cap' :  increment_index(),
	'Pikachu-Hoenn-Cap' :  increment_index(),
	'Pikachu-Sinnoh-Cap' :  increment_index(),
	'Pikachu-Unova-Cap' :  increment_index(),
	'Pikachu-Kalos-Cap' :  increment_index(),
	'Pikachu-Alola-Cap' :  increment_index(),
	'Raichu-Alola' :  increment_index(),
	'Sandshrew-Alola' :  increment_index(),
	'Sandslash-Alola' :  increment_index(),
	'Vulpix-Alola' :  increment_index(),
	'Ninetales-Alola' :  increment_index(),
	'Diglett-Alola' :  increment_index(),
	'Dugtrio-Alola' :  increment_index(),
	'Meowth-Alola' :  increment_index(),
	'Persian-Alola' :  increment_index(),
	'Geodude-Alola' :  increment_index(),
	'Graveler-Alola' :  increment_index(),
	'Golem-Alola' :  increment_index(),
	'Grimer-Alola' :  increment_index(),
	'Muk-Alola' :  increment_index(),
	'Exeggutor-Alola' :  increment_index(),
	'Marowak-Alola' :  increment_index(),
	'Greninja-Battle-Bond' :  increment_index(),
	'Greninja-Ash' :  increment_index(),
	'Zygarde-10' :  increment_index(),
	'Zygarde-50' :  increment_index(),
	'Zygarde-Complete' :  increment_index(),
	'Gumshoos-Totem' :  increment_index(),
	'Vikavolt-Totem' :  increment_index(),
	'Oricorio-Pom-Pom' :  increment_index(),
	'Oricorio-Pau' :  increment_index(),
	'Oricorio-Sensu' :  increment_index(),
	'Lycanroc-Midnight' :  increment_index(),
	'Wishiwashi-School' :  increment_index(),
	'Lurantis-Totem' :  increment_index(),
	'Salazzle-Totem' :  increment_index(),
	'Minior-Orange-Meteor' :  increment_index(),
	'Minior-Yellow-Meteor' :  increment_index(),
	'Minior-Green-Meteor' :  increment_index(),
	'Minior-Blue-Meteor' :  increment_index(),
	'Minior-Indigo-Meteor' :  increment_index(),
	'Minior-Violet-Meteor' :  increment_index(),
	'Minior-Red' :  increment_index(),
	'Minior-Orange' :  increment_index(),
	'Minior-Yellow' :  increment_index(),
	'Minior-Green' :  increment_index(),
	'Minior-Blue' :  increment_index(),
	'Minior-Indigo' :  increment_index(),
	'Minior-Violet' :  increment_index(),
	'Mimikyu-Busted' :  increment_index(),
	'Mimikyu-Totem-Disguised' :  increment_index(),
	'Mimikyu-Totem-Busted' :  increment_index(),
	'Kommo-O-Totem' :  increment_index(),
	'Magearna-Original' :  increment_index(),
	'Pikachu-Partner-Cap' :  increment_index(),
	'Marowak-Totem' :  increment_index(),
	'Ribombee-Totem' :  increment_index(),
	'Rockruff-Own-Tempo' :  increment_index(),
	'Lycanroc-Dusk' :  increment_index(),
	'Araquanid-Totem' :  increment_index(),
	'Togedemaru-Totem' :  increment_index(),
	'Necrozma-Dusk' :  increment_index(),
	'Necrozma-Dawn' :  increment_index(),
	'Necrozma-Ultra' :  increment_index(),
	'NotFound': increment_index(),

}
_, INDEX_TO_POKEMON_NAME = attribute_dict_setup(POKEMON_NAME_TO_INDEX)

'''
OLD MOVE INDEX

MOVE_NAME_TO_INDEX = {
	'knockoff': increment_index(),
	'uturn': increment_index(),
	'scald': increment_index(),
	'roost': increment_index(),
	'hydropump': increment_index(),  
	'darkpulse': increment_index(),
	'watershuriken': increment_index(),
	'spikes': increment_index(),
	'waterfall': increment_index(),
	'earthquake': increment_index(),
	'icepunch': increment_index(),
	'superpower': increment_index(),
	'tailglow': increment_index(),
	'surf': increment_index(),
	'icebeam': increment_index(),
	'rest': increment_index(), 
	'stealthrock': increment_index(),
	'toxic': increment_index(),
	'powerwhip': increment_index(),
	'hurricane': increment_index(),
	'defog': increment_index(),

	# Z-moves only below this comment
	'hydrovortex': increment_index(),
	'NotFound': increment_index(),
}
'''

MOVE_NAME_TO_INDEX = {
	'pound' :  increment_index(),
	'karatechop' :  increment_index(),
	'doubleslap' :  increment_index(),
	'cometpunch' :  increment_index(),
	'megapunch' :  increment_index(),
	'payday' :  increment_index(),
	'firepunch' :  increment_index(),
	'icepunch' :  increment_index(),
	'thunderpunch' :  increment_index(),
	'scratch' :  increment_index(),
	'vicegrip' :  increment_index(),
	'guillotine' :  increment_index(),
	'razorwind' :  increment_index(),
	'swordsdance' :  increment_index(),
	'cut' :  increment_index(),
	'gust' :  increment_index(),
	'wingattack' :  increment_index(),
	'whirlwind' :  increment_index(),
	'fly' :  increment_index(),
	'bind' :  increment_index(),
	'slam' :  increment_index(),
	'vinewhip' :  increment_index(),
	'stomp' :  increment_index(),
	'doublekick' :  increment_index(),
	'megakick' :  increment_index(),
	'jumpkick' :  increment_index(),
	'rollingkick' :  increment_index(),
	'sandattack' :  increment_index(),
	'headbutt' :  increment_index(),
	'hornattack' :  increment_index(),
	'furyattack' :  increment_index(),
	'horndrill' :  increment_index(),
	'tackle' :  increment_index(),
	'bodyslam' :  increment_index(),
	'wrap' :  increment_index(),
	'takedown' :  increment_index(),
	'thrash' :  increment_index(),
	'doubleedge' :  increment_index(),
	'tailwhip' :  increment_index(),
	'poisonsting' :  increment_index(),
	'twineedle' :  increment_index(),
	'pinmissile' :  increment_index(),
	'leer' :  increment_index(),
	'bite' :  increment_index(),
	'growl' :  increment_index(),
	'roar' :  increment_index(),
	'sing' :  increment_index(),
	'supersonic' :  increment_index(),
	'sonicboom' :  increment_index(),
	'disable' :  increment_index(),
	'acid' :  increment_index(),
	'ember' :  increment_index(),
	'flamethrower' :  increment_index(),
	'mist' :  increment_index(),
	'watergun' :  increment_index(),
	'hydropump' :  increment_index(),
	'surf' :  increment_index(),
	'icebeam' :  increment_index(),
	'blizzard' :  increment_index(),
	'psybeam' :  increment_index(),
	'bubblebeam' :  increment_index(),
	'aurorabeam' :  increment_index(),
	'hyperbeam' :  increment_index(),
	'peck' :  increment_index(),
	'drillpeck' :  increment_index(),
	'submission' :  increment_index(),
	'lowkick' :  increment_index(),
	'counter' :  increment_index(),
	'seismictoss' :  increment_index(),
	'strength' :  increment_index(),
	'absorb' :  increment_index(),
	'megadrain' :  increment_index(),
	'leechseed' :  increment_index(),
	'growth' :  increment_index(),
	'razorleaf' :  increment_index(),
	'solarbeam' :  increment_index(),
	'poisonpowder' :  increment_index(),
	'stunspore' :  increment_index(),
	'sleeppowder' :  increment_index(),
	'petaldance' :  increment_index(),
	'stringshot' :  increment_index(),
	'dragonrage' :  increment_index(),
	'firespin' :  increment_index(),
	'thundershock' :  increment_index(),
	'thunderbolt' :  increment_index(),
	'thunderwave' :  increment_index(),
	'thunder' :  increment_index(),
	'rockthrow' :  increment_index(),
	'earthquake' :  increment_index(),
	'fissure' :  increment_index(),
	'dig' :  increment_index(),
	'toxic' :  increment_index(),
	'confusion' :  increment_index(),
	'psychic' :  increment_index(),
	'hypnosis' :  increment_index(),
	'meditate' :  increment_index(),
	'agility' :  increment_index(),
	'quickattack' :  increment_index(),
	'rage' :  increment_index(),
	'teleport' :  increment_index(),
	'nightshade' :  increment_index(),
	'mimic' :  increment_index(),
	'screech' :  increment_index(),
	'doubleteam' :  increment_index(),
	'recover' :  increment_index(),
	'harden' :  increment_index(),
	'minimize' :  increment_index(),
	'smokescreen' :  increment_index(),
	'confuseray' :  increment_index(),
	'withdraw' :  increment_index(),
	'defensecurl' :  increment_index(),
	'barrier' :  increment_index(),
	'lightscreen' :  increment_index(),
	'haze' :  increment_index(),
	'reflect' :  increment_index(),
	'focusenergy' :  increment_index(),
	'bide' :  increment_index(),
	'metronome' :  increment_index(),
	'mirrormove' :  increment_index(),
	'selfdestruct' :  increment_index(),
	'eggbomb' :  increment_index(),
	'lick' :  increment_index(),
	'smog' :  increment_index(),
	'sludge' :  increment_index(),
	'boneclub' :  increment_index(),
	'fireblast' :  increment_index(),
	'waterfall' :  increment_index(),
	'clamp' :  increment_index(),
	'swift' :  increment_index(),
	'skullbash' :  increment_index(),
	'spikecannon' :  increment_index(),
	'constrict' :  increment_index(),
	'amnesia' :  increment_index(),
	'kinesis' :  increment_index(),
	'softboiled' :  increment_index(),
	'highjumpkick' :  increment_index(),
	'glare' :  increment_index(),
	'dreameater' :  increment_index(),
	'poisongas' :  increment_index(),
	'barrage' :  increment_index(),
	'leechlife' :  increment_index(),
	'lovelykiss' :  increment_index(),
	'skyattack' :  increment_index(),
	'transform' :  increment_index(),
	'bubble' :  increment_index(),
	'dizzypunch' :  increment_index(),
	'spore' :  increment_index(),
	'flash' :  increment_index(),
	'psywave' :  increment_index(),
	'splash' :  increment_index(),
	'acidarmor' :  increment_index(),
	'crabhammer' :  increment_index(),
	'explosion' :  increment_index(),
	'furyswipes' :  increment_index(),
	'bonemerang' :  increment_index(),
	'rest' :  increment_index(),
	'rockslide' :  increment_index(),
	'hyperfang' :  increment_index(),
	'sharpen' :  increment_index(),
	'conversion' :  increment_index(),
	'triattack' :  increment_index(),
	'superfang' :  increment_index(),
	'slash' :  increment_index(),
	'substitute' :  increment_index(),
	'struggle' :  increment_index(),
	'sketch' :  increment_index(),
	'triplekick' :  increment_index(),
	'thief' :  increment_index(),
	'spiderweb' :  increment_index(),
	'mindreader' :  increment_index(),
	'nightmare' :  increment_index(),
	'flamewheel' :  increment_index(),
	'snore' :  increment_index(),
	'curse' :  increment_index(),
	'flail' :  increment_index(),
	'conversion2' :  increment_index(),
	'aeroblast' :  increment_index(),
	'cottonspore' :  increment_index(),
	'reversal' :  increment_index(),
	'spite' :  increment_index(),
	'powdersnow' :  increment_index(),
	'protect' :  increment_index(),
	'machpunch' :  increment_index(),
	'scaryface' :  increment_index(),
	'feintattack' :  increment_index(),
	'sweetkiss' :  increment_index(),
	'bellydrum' :  increment_index(),
	'sludgebomb' :  increment_index(),
	'mudslap' :  increment_index(),
	'octazooka' :  increment_index(),
	'spikes' :  increment_index(),
	'zapcannon' :  increment_index(),
	'foresight' :  increment_index(),
	'destinybond' :  increment_index(),
	'perishsong' :  increment_index(),
	'icywind' :  increment_index(),
	'detect' :  increment_index(),
	'bonerush' :  increment_index(),
	'lockon' :  increment_index(),
	'outrage' :  increment_index(),
	'sandstorm' :  increment_index(),
	'gigadrain' :  increment_index(),
	'endure' :  increment_index(),
	'charm' :  increment_index(),
	'rollout' :  increment_index(),
	'falseswipe' :  increment_index(),
	'swagger' :  increment_index(),
	'milkdrink' :  increment_index(),
	'spark' :  increment_index(),
	'furycutter' :  increment_index(),
	'steelwing' :  increment_index(),
	'meanlook' :  increment_index(),
	'attract' :  increment_index(),
	'sleeptalk' :  increment_index(),
	'healbell' :  increment_index(),
	'return' :  increment_index(),
	'present' :  increment_index(),
	'frustration' :  increment_index(),
	'safeguard' :  increment_index(),
	'painsplit' :  increment_index(),
	'sacredfire' :  increment_index(),
	'magnitude' :  increment_index(),
	'dynamicpunch' :  increment_index(),
	'megahorn' :  increment_index(),
	'dragonbreath' :  increment_index(),
	'batonpass' :  increment_index(),
	'encore' :  increment_index(),
	'pursuit' :  increment_index(),
	'rapidspin' :  increment_index(),
	'sweetscent' :  increment_index(),
	'irontail' :  increment_index(),
	'metalclaw' :  increment_index(),
	'vitalthrow' :  increment_index(),
	'morningsun' :  increment_index(),
	'synthesis' :  increment_index(),
	'moonlight' :  increment_index(),
	'hiddenpower' :  increment_index(),
	'crosschop' :  increment_index(),
	'twister' :  increment_index(),
	'raindance' :  increment_index(),
	'sunnyday' :  increment_index(),
	'crunch' :  increment_index(),
	'mirrorcoat' :  increment_index(),
	'psychup' :  increment_index(),
	'extremespeed' :  increment_index(),
	'ancientpower' :  increment_index(),
	'shadowball' :  increment_index(),
	'futuresight' :  increment_index(),
	'rocksmash' :  increment_index(),
	'whirlpool' :  increment_index(),
	'beatup' :  increment_index(),
	'fakeout' :  increment_index(),
	'uproar' :  increment_index(),
	'stockpile' :  increment_index(),
	'spitup' :  increment_index(),
	'swallow' :  increment_index(),
	'heatwave' :  increment_index(),
	'hail' :  increment_index(),
	'torment' :  increment_index(),
	'flatter' :  increment_index(),
	'willowisp' :  increment_index(),
	'memento' :  increment_index(),
	'facade' :  increment_index(),
	'focuspunch' :  increment_index(),
	'smellingsalts' :  increment_index(),
	'followme' :  increment_index(),
	'naturepower' :  increment_index(),
	'charge' :  increment_index(),
	'taunt' :  increment_index(),
	'helpinghand' :  increment_index(),
	'trick' :  increment_index(),
	'roleplay' :  increment_index(),
	'wish' :  increment_index(),
	'assist' :  increment_index(),
	'ingrain' :  increment_index(),
	'superpower' :  increment_index(),
	'magiccoat' :  increment_index(),
	'recycle' :  increment_index(),
	'revenge' :  increment_index(),
	'brickbreak' :  increment_index(),
	'yawn' :  increment_index(),
	'knockoff' :  increment_index(),
	'endeavor' :  increment_index(),
	'eruption' :  increment_index(),
	'skillswap' :  increment_index(),
	'imprison' :  increment_index(),
	'refresh' :  increment_index(),
	'grudge' :  increment_index(),
	'snatch' :  increment_index(),
	'secretpower' :  increment_index(),
	'dive' :  increment_index(),
	'armthrust' :  increment_index(),
	'camouflage' :  increment_index(),
	'tailglow' :  increment_index(),
	'lusterpurge' :  increment_index(),
	'mistball' :  increment_index(),
	'featherdance' :  increment_index(),
	'teeterdance' :  increment_index(),
	'blazekick' :  increment_index(),
	'mudsport' :  increment_index(),
	'iceball' :  increment_index(),
	'needlearm' :  increment_index(),
	'slackoff' :  increment_index(),
	'hypervoice' :  increment_index(),
	'poisonfang' :  increment_index(),
	'crushclaw' :  increment_index(),
	'blastburn' :  increment_index(),
	'hydrocannon' :  increment_index(),
	'meteormash' :  increment_index(),
	'astonish' :  increment_index(),
	'weatherball' :  increment_index(),
	'aromatherapy' :  increment_index(),
	'faketears' :  increment_index(),
	'aircutter' :  increment_index(),
	'overheat' :  increment_index(),
	'odorsleuth' :  increment_index(),
	'rocktomb' :  increment_index(),
	'silverwind' :  increment_index(),
	'metalsound' :  increment_index(),
	'grasswhistle' :  increment_index(),
	'tickle' :  increment_index(),
	'cosmicpower' :  increment_index(),
	'waterspout' :  increment_index(),
	'signalbeam' :  increment_index(),
	'shadowpunch' :  increment_index(),
	'extrasensory' :  increment_index(),
	'skyuppercut' :  increment_index(),
	'sandtomb' :  increment_index(),
	'sheercold' :  increment_index(),
	'muddywater' :  increment_index(),
	'bulletseed' :  increment_index(),
	'aerialace' :  increment_index(),
	'iciclespear' :  increment_index(),
	'irondefense' :  increment_index(),
	'block' :  increment_index(),
	'howl' :  increment_index(),
	'dragonclaw' :  increment_index(),
	'frenzyplant' :  increment_index(),
	'bulkup' :  increment_index(),
	'bounce' :  increment_index(),
	'mudshot' :  increment_index(),
	'poisontail' :  increment_index(),
	'covet' :  increment_index(),
	'volttackle' :  increment_index(),
	'magicalleaf' :  increment_index(),
	'watersport' :  increment_index(),
	'calmmind' :  increment_index(),
	'leafblade' :  increment_index(),
	'dragondance' :  increment_index(),
	'rockblast' :  increment_index(),
	'shockwave' :  increment_index(),
	'waterpulse' :  increment_index(),
	'doomdesire' :  increment_index(),
	'psychoboost' :  increment_index(),
	'roost' :  increment_index(),
	'gravity' :  increment_index(),
	'miracleeye' :  increment_index(),
	'wakeupslap' :  increment_index(),
	'hammerarm' :  increment_index(),
	'gyroball' :  increment_index(),
	'healingwish' :  increment_index(),
	'brine' :  increment_index(),
	'naturalgift' :  increment_index(),
	'feint' :  increment_index(),
	'pluck' :  increment_index(),
	'tailwind' :  increment_index(),
	'acupressure' :  increment_index(),
	'metalburst' :  increment_index(),
	'uturn' :  increment_index(),
	'closecombat' :  increment_index(),
	'payback' :  increment_index(),
	'assurance' :  increment_index(),
	'embargo' :  increment_index(),
	'fling' :  increment_index(),
	'psychoshift' :  increment_index(),
	'trumpcard' :  increment_index(),
	'healblock' :  increment_index(),
	'wringout' :  increment_index(),
	'powertrick' :  increment_index(),
	'gastroacid' :  increment_index(),
	'luckychant' :  increment_index(),
	'mefirst' :  increment_index(),
	'copycat' :  increment_index(),
	'powerswap' :  increment_index(),
	'guardswap' :  increment_index(),
	'punishment' :  increment_index(),
	'lastresort' :  increment_index(),
	'worryseed' :  increment_index(),
	'suckerpunch' :  increment_index(),
	'toxicspikes' :  increment_index(),
	'heartswap' :  increment_index(),
	'aquaring' :  increment_index(),
	'magnetrise' :  increment_index(),
	'flareblitz' :  increment_index(),
	'forcepalm' :  increment_index(),
	'aurasphere' :  increment_index(),
	'rockpolish' :  increment_index(),
	'poisonjab' :  increment_index(),
	'darkpulse' :  increment_index(),
	'nightslash' :  increment_index(),
	'aquatail' :  increment_index(),
	'seedbomb' :  increment_index(),
	'airslash' :  increment_index(),
	'xscissor' :  increment_index(),
	'bugbuzz' :  increment_index(),
	'dragonpulse' :  increment_index(),
	'dragonrush' :  increment_index(),
	'powergem' :  increment_index(),
	'drainpunch' :  increment_index(),
	'vacuumwave' :  increment_index(),
	'focusblast' :  increment_index(),
	'energyball' :  increment_index(),
	'bravebird' :  increment_index(),
	'earthpower' :  increment_index(),
	'switcheroo' :  increment_index(),
	'gigaimpact' :  increment_index(),
	'nastyplot' :  increment_index(),
	'bulletpunch' :  increment_index(),
	'avalanche' :  increment_index(),
	'iceshard' :  increment_index(),
	'shadowclaw' :  increment_index(),
	'thunderfang' :  increment_index(),
	'icefang' :  increment_index(),
	'firefang' :  increment_index(),
	'shadowsneak' :  increment_index(),
	'mudbomb' :  increment_index(),
	'psychocut' :  increment_index(),
	'zenheadbutt' :  increment_index(),
	'mirrorshot' :  increment_index(),
	'flashcannon' :  increment_index(),
	'rockclimb' :  increment_index(),
	'defog' :  increment_index(),
	'trickroom' :  increment_index(),
	'dracometeor' :  increment_index(),
	'discharge' :  increment_index(),
	'lavaplume' :  increment_index(),
	'leafstorm' :  increment_index(),
	'powerwhip' :  increment_index(),
	'rockwrecker' :  increment_index(),
	'crosspoison' :  increment_index(),
	'gunkshot' :  increment_index(),
	'ironhead' :  increment_index(),
	'magnetbomb' :  increment_index(),
	'stoneedge' :  increment_index(),
	'captivate' :  increment_index(),
	'stealthrock' :  increment_index(),
	'grassknot' :  increment_index(),
	'chatter' :  increment_index(),
	'judgment' :  increment_index(),
	'bugbite' :  increment_index(),
	'chargebeam' :  increment_index(),
	'woodhammer' :  increment_index(),
	'aquajet' :  increment_index(),
	'attackorder' :  increment_index(),
	'defendorder' :  increment_index(),
	'healorder' :  increment_index(),
	'headsmash' :  increment_index(),
	'doublehit' :  increment_index(),
	'roaroftime' :  increment_index(),
	'spacialrend' :  increment_index(),
	'lunardance' :  increment_index(),
	'crushgrip' :  increment_index(),
	'magmastorm' :  increment_index(),
	'darkvoid' :  increment_index(),
	'seedflare' :  increment_index(),
	'ominouswind' :  increment_index(),
	'shadowforce' :  increment_index(),
	'honeclaws' :  increment_index(),
	'wideguard' :  increment_index(),
	'guardsplit' :  increment_index(),
	'powersplit' :  increment_index(),
	'wonderroom' :  increment_index(),
	'psyshock' :  increment_index(),
	'venoshock' :  increment_index(),
	'autotomize' :  increment_index(),
	'ragepowder' :  increment_index(),
	'telekinesis' :  increment_index(),
	'magicroom' :  increment_index(),
	'smackdown' :  increment_index(),
	'stormthrow' :  increment_index(),
	'flameburst' :  increment_index(),
	'sludgewave' :  increment_index(),
	'quiverdance' :  increment_index(),
	'heavyslam' :  increment_index(),
	'synchronoise' :  increment_index(),
	'electroball' :  increment_index(),
	'soak' :  increment_index(),
	'flamecharge' :  increment_index(),
	'coil' :  increment_index(),
	'lowsweep' :  increment_index(),
	'acidspray' :  increment_index(),
	'foulplay' :  increment_index(),
	'simplebeam' :  increment_index(),
	'entrainment' :  increment_index(),
	'afteryou' :  increment_index(),
	'round' :  increment_index(),
	'echoedvoice' :  increment_index(),
	'chipaway' :  increment_index(),
	'clearsmog' :  increment_index(),
	'storedpower' :  increment_index(),
	'quickguard' :  increment_index(),
	'allyswitch' :  increment_index(),
	'scald' :  increment_index(),
	'shellsmash' :  increment_index(),
	'healpulse' :  increment_index(),
	'hex' :  increment_index(),
	'skydrop' :  increment_index(),
	'shiftgear' :  increment_index(),
	'circlethrow' :  increment_index(),
	'incinerate' :  increment_index(),
	'quash' :  increment_index(),
	'acrobatics' :  increment_index(),
	'reflecttype' :  increment_index(),
	'retaliate' :  increment_index(),
	'finalgambit' :  increment_index(),
	'bestow' :  increment_index(),
	'inferno' :  increment_index(),
	'waterpledge' :  increment_index(),
	'firepledge' :  increment_index(),
	'grasspledge' :  increment_index(),
	'voltswitch' :  increment_index(),
	'strugglebug' :  increment_index(),
	'bulldoze' :  increment_index(),
	'frostbreath' :  increment_index(),
	'dragontail' :  increment_index(),
	'workup' :  increment_index(),
	'electroweb' :  increment_index(),
	'wildcharge' :  increment_index(),
	'drillrun' :  increment_index(),
	'dualchop' :  increment_index(),
	'heartstamp' :  increment_index(),
	'hornleech' :  increment_index(),
	'sacredsword' :  increment_index(),
	'razorshell' :  increment_index(),
	'heatcrash' :  increment_index(),
	'leaftornado' :  increment_index(),
	'steamroller' :  increment_index(),
	'cottonguard' :  increment_index(),
	'nightdaze' :  increment_index(),
	'psystrike' :  increment_index(),
	'tailslap' :  increment_index(),
	'hurricane' :  increment_index(),
	'headcharge' :  increment_index(),
	'geargrind' :  increment_index(),
	'searingshot' :  increment_index(),
	'technoblast' :  increment_index(),
	'relicsong' :  increment_index(),
	'secretsword' :  increment_index(),
	'glaciate' :  increment_index(),
	'boltstrike' :  increment_index(),
	'blueflare' :  increment_index(),
	'fierydance' :  increment_index(),
	'freezeshock' :  increment_index(),
	'iceburn' :  increment_index(),
	'snarl' :  increment_index(),
	'iciclecrash' :  increment_index(),
	'vcreate' :  increment_index(),
	'fusionflare' :  increment_index(),
	'fusionbolt' :  increment_index(),
	'flyingpress' :  increment_index(),
	'matblock' :  increment_index(),
	'belch' :  increment_index(),
	'rototiller' :  increment_index(),
	'stickyweb' :  increment_index(),
	'fellstinger' :  increment_index(),
	'phantomforce' :  increment_index(),
	'trickortreat' :  increment_index(),
	'nobleroar' :  increment_index(),
	'iondeluge' :  increment_index(),
	'paraboliccharge' :  increment_index(),
	'forestscurse' :  increment_index(),
	'petalblizzard' :  increment_index(),
	'freezedry' :  increment_index(),
	'disarmingvoice' :  increment_index(),
	'partingshot' :  increment_index(),
	'topsyturvy' :  increment_index(),
	'drainingkiss' :  increment_index(),
	'craftyshield' :  increment_index(),
	'flowershield' :  increment_index(),
	'grassyterrain' :  increment_index(),
	'mistyterrain' :  increment_index(),
	'electrify' :  increment_index(),
	'playrough' :  increment_index(),
	'fairywind' :  increment_index(),
	'moonblast' :  increment_index(),
	'boomburst' :  increment_index(),
	'fairylock' :  increment_index(),
	'kingsshield' :  increment_index(),
	'playnice' :  increment_index(),
	'confide' :  increment_index(),
	'diamondstorm' :  increment_index(),
	'steameruption' :  increment_index(),
	'hyperspacehole' :  increment_index(),
	'watershuriken' :  increment_index(),
	'mysticalfire' :  increment_index(),
	'spikyshield' :  increment_index(),
	'aromaticmist' :  increment_index(),
	'eerieimpulse' :  increment_index(),
	'venomdrench' :  increment_index(),
	'powder' :  increment_index(),
	'geomancy' :  increment_index(),
	'magneticflux' :  increment_index(),
	'happyhour' :  increment_index(),
	'electricterrain' :  increment_index(),
	'dazzlinggleam' :  increment_index(),
	'celebrate' :  increment_index(),
	'holdhands' :  increment_index(),
	'babydolleyes' :  increment_index(),
	'nuzzle' :  increment_index(),
	'holdback' :  increment_index(),
	'infestation' :  increment_index(),
	'poweruppunch' :  increment_index(),
	'oblivionwing' :  increment_index(),
	'thousandarrows' :  increment_index(),
	'thousandwaves' :  increment_index(),
	'landswrath' :  increment_index(),
	'lightofruin' :  increment_index(),
	'originpulse' :  increment_index(),
	'precipiceblades' :  increment_index(),
	'dragonascent' :  increment_index(),
	'hyperspacefury' :  increment_index(),
	'breakneckblitz' :  increment_index(),
	'alloutpummeling' :  increment_index(),
	'supersonicskystrike' :  increment_index(),
	'aciddownpour' :  increment_index(),
	'tectonicrage' :  increment_index(),
	'continentalcrush' :  increment_index(),
	'savagespinout' :  increment_index(),
	'neverendingnightmare' :  increment_index(),
	'corkscrewcrash' :  increment_index(),
	'infernooverdrive' :  increment_index(),
	'hydrovortex' :  increment_index(),
	'bloomdoom' :  increment_index(),
	'gigavolthavoc' :  increment_index(),
	'shatteredpsyche' :  increment_index(),
	'subzeroslammer' :  increment_index(),
	'devastatingdrake' :  increment_index(),
	'blackholeeclipse' :  increment_index(),
	'twinkletackle' :  increment_index(),
	'catastropika' :  increment_index(),
	'shoreup' :  increment_index(),
	'firstimpression' :  increment_index(),
	'banefulbunker' :  increment_index(),
	'spiritshackle' :  increment_index(),
	'darkestlariat' :  increment_index(),
	'sparklingaria' :  increment_index(),
	'icehammer' :  increment_index(),
	'floralhealing' :  increment_index(),
	'highhorsepower' :  increment_index(),
	'strengthsap' :  increment_index(),
	'solarblade' :  increment_index(),
	'leafage' :  increment_index(),
	'spotlight' :  increment_index(),
	'toxicthread' :  increment_index(),
	'laserfocus' :  increment_index(),
	'gearup' :  increment_index(),
	'throatchop' :  increment_index(),
	'pollenpuff' :  increment_index(),
	'anchorshot' :  increment_index(),
	'psychicterrain' :  increment_index(),
	'lunge' :  increment_index(),
	'firelash' :  increment_index(),
	'powertrip' :  increment_index(),
	'burnup' :  increment_index(),
	'speedswap' :  increment_index(),
	'smartstrike' :  increment_index(),
	'purify' :  increment_index(),
	'revelationdance' :  increment_index(),
	'coreenforcer' :  increment_index(),
	'tropkick' :  increment_index(),
	'instruct' :  increment_index(),
	'beakblast' :  increment_index(),
	'clangingscales' :  increment_index(),
	'dragonhammer' :  increment_index(),
	'brutalswing' :  increment_index(),
	'auroraveil' :  increment_index(),
	'sinisterarrowraid' :  increment_index(),
	'maliciousmoonsault' :  increment_index(),
	'oceanicoperetta' :  increment_index(),
	'guardianofalola' :  increment_index(),
	'soulstealing7starstrike' :  increment_index(),
	'stokedsparksurfer' :  increment_index(),
	'pulverizingpancake' :  increment_index(),
	'extremeevoboost' :  increment_index(),
	'genesissupernova' :  increment_index(),
	'shelltrap' :  increment_index(),
	'fleurcannon' :  increment_index(),
	'psychicfangs' :  increment_index(),
	'stompingtantrum' :  increment_index(),
	'shadowbone' :  increment_index(),
	'accelerock' :  increment_index(),
	'liquidation' :  increment_index(),
	'prismaticlaser' :  increment_index(),
	'spectralthief' :  increment_index(),
	'sunsteelstrike' :  increment_index(),
	'moongeistbeam' :  increment_index(),
	'tearfullook' :  increment_index(),
	'zingzap' :  increment_index(),
	'naturesmadness' :  increment_index(),
	'multiattack' :  increment_index(),
	'10000000voltthunderbolt' :  increment_index(),
	'mindblown' :  increment_index(),
	'plasmafists' :  increment_index(),
	'photongeyser' :  increment_index(),
	'lightthatburnsthesky' :  increment_index(),
	'searingsunrazesmash' :  increment_index(),
	'menacingmoonrazemaelstrom' :  increment_index(),
	'letssnuggleforever' :  increment_index(),
	'splinteredstormshards' :  increment_index(),
	'clangoroussoulblaze' :  increment_index(),
	'shadowrush' :  increment_index(),
	'shadowblast' :  increment_index(),
	'shadowblitz' :  increment_index(),
	'shadowbolt' :  increment_index(),
	'shadowbreak' :  increment_index(),
	'shadowchill' :  increment_index(),
	'shadowend' :  increment_index(),
	'shadowfire' :  increment_index(),
	'shadowrave' :  increment_index(),
	'shadowstorm' :  increment_index(),
	'shadowwave' :  increment_index(),
	'shadowdown' :  increment_index(),
	'shadowhalf' :  increment_index(),
	'shadowhold' :  increment_index(),
	'shadowmist' :  increment_index(),
	'shadowpanic' :  increment_index(),
	'shadowshed' :  increment_index(),
	'shadowsky' :  increment_index(),
	'NotFound': increment_index(),
}
_, INDEX_TO_MOVE_NAME = attribute_dict_setup(MOVE_NAME_TO_INDEX)

TYPE_NAME_TO_INDEX = {
	'Normal': increment_index(),
	'Fire': increment_index(),
	'Water': increment_index(),
	'Grass': increment_index(),
	'Electric': increment_index(),
	'Ice': increment_index(),
	'Fighting': increment_index(),
	'Poison': increment_index(),
	'Ground': increment_index(),
	'Flying': increment_index(),
	'Psychic': increment_index(),
	'Bug': increment_index(),
	'Ghost': increment_index(),
	'Dark': increment_index(),
	'Dragon': increment_index(),
	'Steel': increment_index(),
	'Fairy': increment_index(),
	'NotFound': increment_index(),
}
_, INDEX_TO_TYPE_NAME = attribute_dict_setup(TYPE_NAME_TO_INDEX)

STATUS_NAME_TO_INDEX = {
	'brn': increment_index(),
	'par': increment_index(),
	'slp': increment_index(),
	'frz': increment_index(),
	'psn': increment_index(),
	'tox': increment_index(),
	'confusion': increment_index(),
	'curse': increment_index(),
	'flinch': increment_index(),
	'trapped': increment_index(),
	'trapper': increment_index(),
	'partiallytrapped': increment_index(),
	'lockedmove': increment_index(),
	'twoturnmove': increment_index(),
	'choicelock': increment_index(),
	'mustrecharge': increment_index(),
	'futuremove': increment_index(),
	'healreplacement': increment_index(),
	'stall': increment_index(),
	'gem': increment_index(),
	'raindance': increment_index(),
	'primordialsea': increment_index(),
	'sunnyday': increment_index(),
	'desolateland': increment_index(),
	'sandstorm': increment_index(),
	'hail': increment_index(),
	'deltastream': increment_index(),
	'arceus': increment_index(),
	'silvally': increment_index(),
	'NotFound': increment_index(),
}
_, INDEX_TO_STATUS_NAME = attribute_dict_setup(STATUS_NAME_TO_INDEX)

# Magic number to normalize stat values for input vector
# For eg. 1245 spa => 1245/2000 = 0.6225 value in vector
STAT_NORMALIZER = 2000
STAT_NAME_TO_INDEX = {
	'atk': increment_index(),
	'def': increment_index(),
	'spa': increment_index(),
	'spd': increment_index(),
	'spe': increment_index(),
	'NotFound': increment_index(),
}
_, INDEX_TO_STAT_NAME = attribute_dict_setup(STAT_NAME_TO_INDEX)

ITEM_NAME_TO_INDEX = {
	'damprock': increment_index(),
	'choicespecs': increment_index(),
	'swampertite': increment_index(),
	'wateriumz': increment_index(),
	'figyberry': increment_index(),
	'rockyhelmet': increment_index(),
	'NotFound': increment_index(),
}
_, INDEX_TO_ITEM_NAME = attribute_dict_setup(ITEM_NAME_TO_INDEX)

ACTIVE_STATE = increment_index()

FAINTED_STATE = increment_index()

NORMALIZED_HEALTH = increment_index()

ATTRIBUTES_PER_POKEMON = INDEX_TRACKER + 1

def clean_move_name(move_name):
	return move_name.lower().replace(' ', '')

def start_of_pokemon(player, team_position):
	return (SHARED_ATTRIBUTES_COUNT + 
		player * GameState.num_player_elements + 
		TEAM_ATTRIBUTES_COUNT +
		team_position * ATTRIBUTES_PER_POKEMON)

def health_sum(vector_list, player):
	total = 0
	for position in range(GameState.max_team_size):
		total += vector_list[start_of_pokemon(player, position) + 
			NORMALIZED_HEALTH]
	return total

def ko_count(vector_list, player):
	total = 0
	for position in range(GameState.max_team_size):
		total += vector_list[start_of_pokemon(player, position) + FAINTED_STATE]
	return total

class GameState():
	class Player(IntEnum):
		'''
		player one corresponds to local player, not necessarily P1 as determined 
		by the client
		'''
		one = 0 
		two = auto()
		count = auto()

	max_team_size = 6

	num_player_elements = (TEAM_ATTRIBUTES_COUNT + 
		max_team_size * ATTRIBUTES_PER_POKEMON)

	@staticmethod
	def vector_dimension():
		return (SHARED_ATTRIBUTES_COUNT + 
			GameState.Player.count * GameState.num_player_elements)

	def __init__(self):
		self.vector_list = [0.0 for _ in range(GameState.vector_dimension())]

		#NOTE: for easy access to pokemon team position in the future
		self.name_to_position = [{}, {}] 
		self.team_abilities = [{}, {}] #TODO: remove and pack in vector_list
		self.team_mega = [{}, {}]

	def _set_weather(self, weather_name, value):
		position = WEATHER_NAME_TO_INDEX.get(weather_name, 
			WEATHER_NAME_TO_INDEX['NotFound'])
		self.vector_list[position] = value

	def set_player_attribute(self, player, attribute_index, value):
		self.vector_list[SHARED_ATTRIBUTES_COUNT + 
			player * GameState.num_player_elements + 
			attribute_index] = value

	def get_player_attribute(self, player, attribute_index):
		return self.vector_list[SHARED_ATTRIBUTES_COUNT + 
			player * GameState.num_player_elements + 
			attribute_index]

	def set_pokemon_attribute(self, player, team_position, attribute_index, 
		value):
		
		self.vector_list[start_of_pokemon(player, team_position) + 
			attribute_index] = value

	def get_pokemon_attribute(self, player, team_position, attribute_index):
		return self.vector_list[start_of_pokemon(player, team_position) 
			+ attribute_index]

	def set_weather(self, weather_name):
		self.clear_all_weather()
		self._set_weather(weather_name, 1.0)

	def clear_all_weather(self):
		for weather_name in WEATHER_NAME_TO_INDEX:
			if weather_name in ['Min', 'Count']:
				continue
			self._set_weather(weather_name, 0.0)

	def clear_weather(self, weather_name):
		self.vector_list[WEATHER_NAME_TO_INDEX[weather_name]] = 0.0

	def check_weather(self, weather_name):
		return self.vector_list[WEATHER_NAME_TO_INDEX[weather_name]] == 1.0

	def all_weather(self):
		weathers = []
		for weather_name in WEATHER_NAME_TO_INDEX:
			if weather_name == 'Min' or weather_name == 'Count':
				continue
			if self.check_weather(weather_name):
				weathers.append(weather_name)
		return weathers

	@staticmethod
	def pokemon_name_clean(pokemon_name):
		return pokemon_name.rstrip(', M').rstrip(', F')

	def set_team(self, player, team):
		'''
		player: member of Player enum
		team: list of pokemon names as strings. 
			If updating for some reason, don't change the order in which you 
			pass in the pokemon
		'''
		for team_position, pokemon_name in enumerate(team):
			pokemon_name = GameState.pokemon_name_clean(pokemon_name)
			
			self.name_to_position[player][pokemon_name] = team_position

			pokemon_index = POKEMON_NAME_TO_INDEX.get(pokemon_name, 
				POKEMON_NAME_TO_INDEX['NotFound'])
			self.set_pokemon_attribute(player, team_position, pokemon_index, 
				1.0)

	def _set_health(self, player, position, value):
		self.set_pokemon_attribute(player, position, NORMALIZED_HEALTH, value)

	def set_health(self, player, name, value):
		position = self.name_to_position[player][name]
		self._set_health(player, position, value)
		
		if self.check_active(player, name):
			self.set_player_attribute(player, ACTIVE_NORMALIZED_HEALTH, value)

	def init_health(self, player):
		for team_position in range(len(self.name_to_position[player])):
			self._set_health(player, team_position, 1.0)

	def check_health(self, player, name):
		name = GameState.pokemon_name_clean(name)
		position = self.name_to_position[player][name]
		return self.get_pokemon_attribute(player, position, NORMALIZED_HEALTH)

	def all_health(self, player):
		health_list = []
		team = self.name_to_position[player]
		for name in team:
			health_list.append((name, self.check_health(player, name)))
		return health_list 

	def check_team_position(self, player, position):
		'''
		Returns a string of the pokemon that's in the position passed in. 
		Probably only useful for debugging

		player: member of Player enum
		position: the position that the pokemon takes on the team. zero-indexed
		'''
		start_checking = start_of_pokemon(player, position) 
		end_checking = start_checking + POKEMON_NAME_TO_INDEX['Count']
		for pokemon_index in range(start_checking, end_checking):
			if self.vector_list[pokemon_index] == 1.0:
				return INDEX_TO_POKEMON_NAME[pokemon_index - start_checking]
		else:
			raise Exception('We somehow couldn\'t find the pokemon')

	def _set_active(self, player, position, value):
		'''
		Sets a pokemon in a position to a value 
		(0.0 for inactive and 1.0 for active)  
		Probably only useful for debugging

		player: member of Player enum
		position: the position that the pokemon takes on the team. zero-indexed
		value: float for value
		'''
		self.set_pokemon_attribute(player, position, ACTIVE_STATE, value)

	def set_active(self, player, name):
		'''
		Sets a pokemon with a name a position to a value 
		(0.0 for inactive and 1.0 for active)  
		Probably only useful for debugging

		player: member of Player enum
		name: string for the name of the pokemon
		'''
		name = GameState.pokemon_name_clean(name)
		for team_position in range(GameState.max_team_size):
			self._set_active(player, team_position, 0.0)

		team_position = self.name_to_position[player][name]
		self._set_active(player, team_position, 1.0)
		
		for set_pokemon_name in ACTIVE_POKEMON_NAME_TO_INDEX:
			if set_pokemon_name in ['Min', 'Count']:
				continue
			index = ACTIVE_POKEMON_NAME_TO_INDEX[set_pokemon_name]
			if set_pokemon_name == name:
				self.set_player_attribute(player, index, 1.0)
			else:
				self.set_player_attribute(player, index, 0.0)
		
		moves = self.check_moves(player, name)
		for set_move_name in ACTIVE_MOVE_NAME_TO_INDEX:
			if set_move_name in ['Min', 'Count']:
				continue
			index = ACTIVE_MOVE_NAME_TO_INDEX[set_move_name]
			if set_move_name in moves:
				self.set_player_attribute(player, index, 
					self._get_move(player, team_position, 
						MOVE_NAME_TO_INDEX[set_move_name]))
			else: 
				self.set_player_attribute(player, index, 0.0)

		types = self.check_types(player, name)
		for set_type_name in ACTIVE_TYPE_NAME_TO_INDEX:
			if set_type_name in ['Min', 'Count']:
				continue
			index = ACTIVE_TYPE_NAME_TO_INDEX[set_type_name]
			if set_type_name in types:
				self.set_player_attribute(player, index, 1.0)
			else:
				self.set_player_attribute(player, index, 0.0)

		statuses = self.check_status(player, name)
		for set_status_name in ACTIVE_STATUS_NAME_TO_INDEX:
			if set_status_name in ['Min', 'Count']:
				continue
			index = ACTIVE_STATUS_NAME_TO_INDEX[set_status_name]
			if set_status_name in statuses:
				self.set_player_attribute(player, index, 1.0)
			else:
				self.set_player_attribute(player, index, 0.0)

		self.set_player_attribute(player, ACTIVE_NORMALIZED_HEALTH, 
			self.check_health(player, name))

	def check_active_slot(self, player):
		pokemon_names = []
		for get_pokemon_name in ACTIVE_POKEMON_NAME_TO_INDEX:
			if get_pokemon_name in ['Min', 'Count']:
				continue
			index = ACTIVE_POKEMON_NAME_TO_INDEX[get_pokemon_name]
			if self.get_player_attribute(player, index) == 1.0:
				pokemon_names.append(get_pokemon_name)
		
		moves = []
		for get_move_name in ACTIVE_MOVE_NAME_TO_INDEX:
			if get_move_name in ['Min', 'Count']:
				continue
			index = ACTIVE_MOVE_NAME_TO_INDEX[get_move_name]
			value = self.get_player_attribute(player, index)
			if value > 0.0:
				moves.append((get_move_name, value))

		types = []
		for get_type_name in ACTIVE_TYPE_NAME_TO_INDEX:
			if get_type_name in ['Min', 'Count']:
				continue
			index = ACTIVE_TYPE_NAME_TO_INDEX[get_type_name]
			value = self.get_player_attribute(player, index)
			if value == 1.0:
				types.append(get_type_name)

		statuses = []
		for get_status_name in ACTIVE_STATUS_NAME_TO_INDEX:
			if get_status_name in ['Min', 'Count']:
				continue
			index = ACTIVE_STATUS_NAME_TO_INDEX[get_status_name]
			value = self.get_player_attribute(player, index)
			if value == 1.0:
				statuses.append((get_status_name, value))

		health = self.get_player_attribute(player, ACTIVE_NORMALIZED_HEALTH)

		return pokemon_names, moves, types, statuses, health

	def check_active(self, player, name):
		'''
		Returns a boolean for whether the pokemon is active

		player: member of Player enum
		name: string for the name of the pokemon
		'''
		name = GameState.pokemon_name_clean(name)
		position = self.name_to_position[player][name]
		return self.get_pokemon_attribute(player, position, ACTIVE_STATE)

	def all_active(self, player):
		active_pokemon = []
		team = self.name_to_position[player]
		for name in team:
			if self.check_active(player, name):
				active_pokemon.append(name)
		return active_pokemon

	def _set_fainted(self, player, position, value):
		self.set_pokemon_attribute(player, position, FAINTED_STATE, value)

	def set_fainted(self, player, name):
		team_position = self.name_to_position[player][name]
		self._set_active(player, team_position, 0.0)
		self._set_health(player, team_position, 0.0)
		self._set_fainted(player, team_position, 1.0)

	def check_fainted(self, player, name):
		name = GameState.pokemon_name_clean(name)
		position = self.name_to_position[player][name]
		return self.get_pokemon_attribute(player, position, FAINTED_STATE) == 1.0
	
	def all_fainted(self, player):
		'''
		Returns all of the fainted pokemon for player as a list of strings
		'''
		fainted = []
		team = self.name_to_position[player]
		for name in team:
			if self.check_fainted(player, name):
				fainted.append(name)
		return fainted

	def _set_move(self, player, team_position, move_position, value):
		self.set_pokemon_attribute(player, team_position, move_position, value)

	def _get_move(self, player, team_position, move_position):
		return self.get_pokemon_attribute(player, team_position, move_position)

	def set_move(self, player, pokemon_name, move_name, pp, max_pp):
		team_position = self.name_to_position[player][pokemon_name]
		move_position = MOVE_NAME_TO_INDEX.get(move_name, MOVE_NAME_TO_INDEX['NotFound'])
		value = float(pp) / float(max_pp)
		self._set_move(player, team_position, move_position, value)

		index = ACTIVE_MOVE_NAME_TO_INDEX[move_name]
		self.set_player_attribute(player, index, value)

	def check_moves(self, player, pokemon_name):
		pokemon_name = GameState.pokemon_name_clean(pokemon_name)
		moves = []
		team_position = self.name_to_position[player][pokemon_name]
		start_checking = (start_of_pokemon(player, team_position) + 
			MOVE_NAME_TO_INDEX['Min'])
		end_checking = start_checking + MOVE_NAME_TO_INDEX['Count']

		start_of_move_indices = start_of_pokemon(player, team_position)
		for move_index in range(start_checking, end_checking):
			if self.vector_list[move_index] > 0.0:
				moves.append(INDEX_TO_MOVE_NAME[move_index - 
					start_of_move_indices])
		return moves

	def all_moves(self, player):
		all_moves = []
		team = self.name_to_position[player]
		for name in team:
			all_moves.append((name, self.check_moves(player, name)))
		return all_moves

	def _set_type(self, player, position, type_position, value):
		self.set_pokemon_attribute(player, position, type_position, value)

	def set_type(self, player, name, type_name):
		team_position = self.name_to_position[player][name]
		type_position = TYPE_NAME_TO_INDEX.get(type_name, TYPE_NAME_TO_INDEX['NotFound'])
		self._set_type(player, team_position, type_position, 1.0)

	def set_types(self, player, name, type_names):
		for type_name in type_names:
			self.set_type(player, name, type_name)
			
	def check_types(self, player, name):
		name = GameState.pokemon_name_clean(name)
		types = []
		position = self.name_to_position[player][name]
		start_checking = (start_of_pokemon(player, position) + 
			TYPE_NAME_TO_INDEX['Min'])
		end_checking = start_checking + TYPE_NAME_TO_INDEX['Count']
		
		start_of_type_indices = start_of_pokemon(player, position)
		
		for type_index in range(start_checking, end_checking):
			if self.vector_list[type_index] == 1.0:
				types.append(INDEX_TO_TYPE_NAME[type_index - 
					start_of_type_indices])
		return types

	def all_types(self, player):
		all_types = []
		team = self.name_to_position[player]
		for name in team:
			all_types.append((name, self.check_types(player, name)))
		return all_types
	
	def _set_status(self, player, team_position, status_position, value):
		self.set_pokemon_attribute(player, team_position, status_position, value)

	def set_status(self, player, name, status_name):
		team_position = self.name_to_position[player][name]
		status_position = STATUS_NAME_TO_INDEX.get(status_name, STATUS_NAME_TO_INDEX['NotFound'])
		self._set_status(player, team_position, status_position, 1.0)

		if self.check_active(player, name):
			index = ACTIVE_STATUS_NAME_TO_INDEX.get(status_name, 
				ACTIVE_STATUS_NAME_TO_INDEX['NotFound'])
			self.set_player_attribute(player, index, 1.0)
	
	def remove_status(self, player, name, status_name):
		team_position = self.name_to_position[player][name]
		status_position = STATUS_NAME_TO_INDEX.get(status_name, STATUS_NAME_TO_INDEX['NotFound'])
		self._set_status(player, team_position, status_position, 0.0)
		
		if self.check_active(player, name):
			index = ACTIVE_STATUS_NAME_TO_INDEX.get(status_name, 
				ACTIVE_STATUS_NAME_TO_INDEX['NotFound'])
			self.set_player_attribute(player, index, 0.0)

	def check_status(self, player, name):
		name = GameState.pokemon_name_clean(name)
		statuses = []
		position = self.name_to_position[player][name]
		start_checking = (start_of_pokemon(player, position) + 
			STATUS_NAME_TO_INDEX['Min'])
		end_checking = start_checking + STATUS_NAME_TO_INDEX['Count']
		
		start_of_status_indices = start_of_pokemon(player, position)
		
		for status_index in range(start_checking, end_checking):
			if self.vector_list[status_index] == 1.0:
				statuses.append(INDEX_TO_STATUS_NAME[status_index - 
					start_of_status_indices])
		return statuses

	def all_statuses(self, player):
		statuses = []
		team = self.name_to_position[player]
		for name in team:
			statuses.append((name, self.check_status(player, name)))
		return statuses

	def reset_boosts(self, player):
		for boost_name in ACTIVE_POKEMON_BOOST:
			if boost_name in ['Min', 'Count']:
				continue
			self.set_boost(player, boost_name, 0.5)

	def _set_boost(self, player, boost_position, value):
		self.set_player_attribute(player, boost_position, value)

	def set_boost(self, player, boost_name, value):
		boost_position = ACTIVE_POKEMON_BOOST[boost_name]
		if value < 0.0:
			value = 0.0
		elif value > 1.0:
			value = 1.0
		self._set_boost(player, boost_position, value)

	def get_boost(self, player, boost_name):
		boost_position = ACTIVE_POKEMON_BOOST[boost_name]
		return self.get_player_attribute(player, boost_position)

	def add_boost(self, player, boost_name, delta):
		normalized_delta = delta / MAX_BOOST
		current_boost = self.get_boost(player, boost_name)
		self.set_boost(player, boost_name, normalized_delta + current_boost)

	def all_boosts(self, player):
		boosts = []
		for boost_name in ACTIVE_POKEMON_BOOST:
			if boost_name in ['Min', 'Count']:
				continue
			boosts.append((boost_name, self.get_boost(player, boost_name)))
		return boosts

	def _set_entry_hazard(self, player, entry_hazard_position, value):
		self.set_player_attribute(player, entry_hazard_position, value)

	def set_entry_hazard(self, player, entry_hazard, value):
		entry_hazard_position = ENTRY_HAZARD_TO_INDEX.get(entry_hazard, ENTRY_HAZARD_TO_INDEX['NotFound'])
		self._set_entry_hazard(player, entry_hazard_position, value)
	
	def get_entry_hazard(self, player, entry_hazard):
		entry_hazard_position = ENTRY_HAZARD_TO_INDEX.get(entry_hazard, ENTRY_HAZARD_TO_INDEX['NotFound'])
		return self.get_player_attribute(player, entry_hazard_position)

	def increment_entry_hazard(self, player, entry_hazard):
		current_entry_hazard = self.get_entry_hazard(player, entry_hazard)
		if (current_entry_hazard + 1.0/MAX_ENTRY_HAZARD_COUNT) > 1.0:
			self.set_entry_hazard(player, entry_hazard, 1.0)
		
		else:
			self.set_entry_hazard(player, entry_hazard, current_entry_hazard + 1.0/MAX_ENTRY_HAZARD_COUNT)

	def clear_entry_hazard(self, player, entry_hazard):
		self.set_entry_hazard(player, entry_hazard, 0.0)
	
	def all_entry_hazard(self, player):
		entry_hazards = []
		for entry_hazard in ENTRY_HAZARD_TO_INDEX:
			if entry_hazard not in ['Min', 'Count']:
				entry_hazards.append((entry_hazard, self.get_entry_hazard(player, entry_hazard)))

		return entry_hazards

	def _set_stat(self, player, team_position, stat_position, value):
		self.set_pokemon_attribute(player, team_position, stat_position, value)
	
	def set_stat(self, player, pokemon_name, stat_name, value):
		team_position = self.name_to_position[player][pokemon_name]
		stat_position = STAT_NAME_TO_INDEX.get(stat_name, STAT_NAME_TO_INDEX['NotFound'])
		value = value / STAT_NORMALIZER
		if value > 1.0:
			value = 1.0
		
		self._set_stat(player, team_position, stat_position, value)
	
	def get_stat(self, player, pokemon_name, stat_name):
		team_position = self.name_to_position[player][pokemon_name]
		stat_position = STAT_NAME_TO_INDEX.get(stat_name, STAT_NAME_TO_INDEX['NotFound'])
		return self.get_pokemon_attribute(player, team_position, stat_position)

	def all_stats(self, player):
		stats = []
		team = self.name_to_position[player]
		for pokemon_name in team:
			pokemon_stats = []
			for stat_name in STAT_NAME_TO_INDEX:
				if stat_name not in ['Min', 'Count']:
					pokemon_stats.append((stat_name, self.get_stat(player, pokemon_name, stat_name)))
			
			stats.append((pokemon_name, pokemon_stats))

		return stats
	
	def _set_item(self, player, team_position, item_position, value):
		self.set_pokemon_attribute(player, team_position, item_position, value)
	
	def set_item(self, player, pokemon_name, item_name):
		team_position = self.name_to_position[player][pokemon_name]
		item_position = ITEM_NAME_TO_INDEX.get(item_name, ITEM_NAME_TO_INDEX['NotFound'])
		self._set_item(player, team_position, item_position, 1.0)

	def get_item(self, player, pokemon_name, item_name):
		team_position = self.name_to_position[player][pokemon_name]
		item_position = ITEM_NAME_TO_INDEX.get(item_name, ITEM_NAME_TO_INDEX['NotFound'])
		return self.get_pokemon_attribute(player, team_position, item_position)

	def clear_all_items(self, player, pokemon_name):
		team_position = self.name_to_position[player][pokemon_name]
		for item_name in ITEM_NAME_TO_INDEX:
			if item_name not in ['Min', 'Count']:
				item_position = ITEM_NAME_TO_INDEX.get(item_name)
				self._set_item(player, team_position, item_position, 0.0)

	def all_items(self, player):
		items = []
		team = self.name_to_position[player]
		for pokemon_name in team:
			pokemon_items = []
			for item_name in ITEM_NAME_TO_INDEX:
				if self.get_item(player, pokemon_name, item_name) == 1.0 and item_name not in ['Min', 'Count']:
					pokemon_items.append(item_name)

			items.append((pokemon_name, pokemon_items))

		return items

	def update_abilities(self, player, pokemon, ability):
		#TODO: replace implementation with packing into vector list
		pokemon_name = GameState.pokemon_name_clean(str(pokemon))
		self.team_abilities[player][pokemon_name] = ability

	def update_team_mega(self, player, pokemon):
		# TODO: replace implementation with packing into vector list
		# TODO: Megas go inactive once the pokemon faints... add code to switch if pokemon faints
		pokemon_name = GameState.pokemon_name_clean(str(pokemon))
		self.team_mega[player][pokemon_name] = True
		
	def update_used_zpower(self, pokemon):
		# TODO: replace implementation with packing into vector list
		pokemon_name = GameState.pokemon_name_clean(str(pokemon))
		self.team_zpower[player][pokemon_name] = True



if __name__ == '__main__':
	#NOTE: tests for GameState data
	gs = GameState()
	team1 = ['Pelipper', 'Greninja', 'Swampert', 'Manaphy', 'Tornadus', 
			'Ferrothorn']
	gs.set_team(GameState.Player.one, team1)
	for position, expected_name in enumerate(team1):
		name = gs.check_team_position(GameState.Player.one, position)
		if name != expected_name:
			print(f'Incorrect pokemon {name} at position {position}. '
				f'Expected: {expected_name}')

	team2 = ['Pelipper', 'Greninja', 'Swampert', 'Manaphy', 'Ferrothorn',
			'Tornadus']
	gs.set_team(GameState.Player.two, team2)
	for position, expected_name in enumerate(team2):
		name = gs.check_team_position(GameState.Player.two, position)
		if name != expected_name:
			print(f'Incorrect pokemon {name} at position {position}. '
				f'Expected: {expected_name}')

	for expected_name in team1: 
		gs.set_active(GameState.Player.one, expected_name)
		for name in team1:
			result = gs.check_active(GameState.Player.one, name)
			if result:
				if name != expected_name:
					print(f'{GameState.Player.one}: '
						f'Pokemon {name} was unexpectedly active.')
			else:
				if name == expected_name:
					print(f'{GameState.Player.one}: ' 
						f'Pokemon {name} was unexpectedly inactive')

	for expected_name in team2: 
		gs.set_active(GameState.Player.two, expected_name)
		for name in team2:
			result = gs.check_active(GameState.Player.two, name)
			if result:
				if name != expected_name:
					print(f'{GameState.Player.two}: '
						f'Pokemon {name} was unexpectedly active.')
			else:
				if name == expected_name:
					print(f'{GameState.Player.two}: '
						f'Pokemon {name} was unexpectedly inactive')


	for expected_index, expected_name in enumerate(team1): 
		gs.set_fainted(GameState.Player.one, expected_name)
		for name_index, name in enumerate(team1):
			result = gs.check_fainted(GameState.Player.one, name)
			if result:
				if name_index > expected_index:
					print(f'{GameState.Player.one}: '
						f'Pokemon {name} was unexpectedly fainted.')
			else:
				if name_index <= expected_index:
					print(f'{GameState.Player.one}: ' 
						f'Pokemon {name} was unexpectedly alive')

	for expected_index, expected_name in enumerate(team2): 
		gs.set_fainted(GameState.Player.two, expected_name)
		for name_index, name in enumerate(team2):
			result = gs.check_fainted(GameState.Player.two, name)
			if result:
				if name_index > expected_index:
					print(f'{GameState.Player.two}: '
						f'Pokemon {name} was unexpectedly fainted.')
			else:
				if name_index <= expected_index:
					print(f'{GameState.Player.two}: ' 
						f'Pokemon {name} was unexpectedly alive')

	def check_moves(player, pokemon, move_names):
		has_moves = gs.check_moves(player, pokemon)
		if set(has_moves) != set(move_names):
			print(f'{pokemon} has moves {has_moves} instead of {move_names}')

	def test_moves(player, pokemon, move_names):
		for move_name in move_names:
			gs.set_move(player, pokemon, move_name, 1.0, 1.0)
		check_moves(player, pokemon, move_names)
	
	for player in GameState.Player:
		if player == GameState.Player.count:
			continue
			
		pokemon_moves = [
			('Pelipper', ['knockoff', 'uturn', 'scald', 'roost']),
			('Greninja', ['hydropump', 'darkpulse', 'watershuriken', 'spikes']),
			('Swampert', ['waterfall', 'earthquake', 'icepunch', 'superpower']),
			('Manaphy', ['tailglow', 'surf', 'icebeam', 'rest']),
			('Ferrothorn', ['stealthrock', 'knockoff', 'toxic', 'powerwhip']),
			('Tornadus', ['hurricane', 'knockoff', 'uturn', 'defog'])
		]
		for pokemon, move_names in pokemon_moves:
			test_moves(player, pokemon, move_names)
		for pokemon, move_names in pokemon_moves:
			check_moves(player, pokemon, move_names)

	def check_types(player, pokemon, type_names):
		has_types = gs.check_types(player, pokemon)
		if set(has_types) != set(type_names):
			print(f'{pokemon} has types {has_types} instead of {type_names}')

	def test_types(player, pokemon, type_names):
		for type_name in type_names:
			gs.set_type(player, pokemon, type_name)
		check_types(player, pokemon, type_names)
	
	for player in GameState.Player:
		if player == GameState.Player.count:
			continue

		pokemon_types = [
			('Pelipper', ['Water', 'Flying']),
			('Greninja', ['Water', 'Dark']),
			('Swampert', ['Water', 'Ground']),
			('Manaphy', ['Water']),
			('Ferrothorn', ['Grass', 'Steel']),
			('Tornadus', ['Flying'])
		]
		for pokemon, type_names in pokemon_types:
			test_types(player, pokemon, type_names)
		for pokemon, type_names in pokemon_types:
			check_types(player, pokemon, type_names)

	for player in GameState.Player:
		if player == GameState.Player.count:
			continue
		expected_health = [
			('Pelipper', 1.0),
			('Greninja', 1.0),
			('Swampert', 1.0),
			('Manaphy', 1.0),
			('Ferrothorn', 1.0),
			('Tornadus', 1.0)
		]
		gs.init_health(player)
		gs_health = gs.all_health(player)
		if set(gs_health) != set(expected_health):
			print(gs_health)
			print('gs_health had unexpected values when testing init_health')

		for (index, data) in enumerate(expected_health):
			pokemon, _ = data
			gs.set_health(player, pokemon, 0.0)
			new_expected = [element for element in expected_health]
			new_expected[index] = (pokemon, 0.0)
			gs_health = gs.all_health(player)
			if set(gs_health) != set(new_expected):
				print('gs_health had unexpected values when testing set_health')
				print(f'Got {gs_health}')
				print(f'Expected {new_expected}')
			gs.set_health(player, pokemon, 1.0)

	for player in GameState.Player:
		if player == GameState.Player.count:
			continue

		gs.init_health(player)
		player_health_sum = health_sum(gs.vector_list, player)
		if player_health_sum != 6.0:
			print(f'ERROR: unexpected health sum {player_health_sum} after init')
		for position in range(len(gs.name_to_position[player])):
			gs._set_health(player, position, 0.0)

			player_health_sum = health_sum(gs.vector_list, player)
			expected_sum = 6.0 - (position + 1)
			if player_health_sum != expected_sum:
				print('ERROR: unexpected health sum. ' 
					f'Expected {expected_sum} but had {player_health_sum}')


	for player in GameState.Player:
		if player == GameState.Player.count:
			continue

		for position in range(len(gs.name_to_position[player])):
			gs._set_fainted(player, position, 0.0)

		player_ko_count = ko_count(gs.vector_list, player)
		if player_ko_count != 0.0:
			print('ERROR: unexpected player_ko_count after setup')

		if player == GameState.Player.one: 
			team = team1 
		else:
			team = team2
		for expected_index, expected_name in enumerate(team): 
			gs.set_fainted(player, expected_name)		
			player_ko_count = ko_count(gs.vector_list, player)
			expected_ko_count = expected_index + 1
			if player_ko_count != expected_ko_count:
				print(f'ERROR: expected {expected_ko_count} KOs but had '
					f'{player_ko_count}')


	def check_statuses(player, pokemon, status_names):
		has_statuses = gs.check_status(player, pokemon)
		if set(has_statuses) != set(status_names):
			print(f'{pokemon} has types {has_statuses} instead of {status_names}')

	def test_statuses(player, pokemon, status_names):
		for status_name in status_names:
			gs.set_status(player, pokemon, status_name)
		check_statuses(player, pokemon, status_names)
	
	for player in GameState.Player:
		if player == GameState.Player.count:
			continue
		
		#Note: just a test input, such a combination of statuses is unlikely
		pokemon_statuses = [
			('Pelipper', ['brn', 'par', 'slp', 'frz', 'psn', 'tox']),
			('Greninja', ['confusion', 'flinch', 'trapped', 'trapper']),
			('Swampert', ['partiallytrapped', 'lockedmove', 'twoturnmove', 'choicelock']),
			('Manaphy', ['mustrecharge', 'futuremove', 'healreplacement', 'stall', 'gem']),
			('Ferrothorn', ['raindance', 'primordialsea', 'sunnyday', 'desolateland']),
			('Tornadus', ['sandstorm', 'hail', 'deltastream', 'arceus', 'silvally'])
		]
		for pokemon, status_names in pokemon_statuses:
			test_statuses(player, pokemon, status_names)
		for pokemon, status_names in pokemon_statuses:
			check_statuses(player, pokemon, status_names)

	weathers = gs.all_weather()
	if weathers != []:
		print(f'Weathers was {weathers} instead of []')
	gs.set_weather('RainDance')
	weathers = gs.all_weather()
	if len(weathers) > 1 or 'RainDance' not in weathers:
		print(f'Weathers was {weathers} not [\'RainDance\']')

	gs.set_weather('SunnyDay')
	weathers = gs.all_weather()
	if len(weathers) > 1 or 'SunnyDay' not in weathers:
		print(f'Weathers was {weathers} not [\'SunnyDay\']')

	gs.clear_all_weather()
	weathers = gs.all_weather()
	if weathers != []:
		print(f'Weathers was {weathers} instead of []')

	def reset_and_check(gs, player, expected_boosts):
		gs.reset_boosts(player)
		boosts = gs.all_boosts(player) 
		if set(boosts) != set(expected_boosts):
			print('Unexpected boost values')

	for player in GameState.Player:
		if player == GameState.Player.count:
			continue 

		expected_boosts = (('atk', 0.5),
			('def', 0.5), 
			('spa', 0.5), 
			('spd', 0.5), 
			('spe', 0.5), 
			('accuracy', 0.5), 
			('evasion', 0.5),
			('NotFound', 0.5)) 
		reset_and_check(gs, player, expected_boosts)

		for index, boost_name in enumerate(ACTIVE_POKEMON_BOOST):
			reset_and_check(gs, player, expected_boosts)

			new_expected_boosts = [old_boost for old_boost in expected_boosts]
			
			gs.add_boost(player, boost_name, 3)
			new_expected_boosts[index] = (boost_name, 0.75)
			boosts = gs.all_boosts(player)
			if set(new_expected_boosts) != set(boosts):
				print('Unexpected boost values')
				print(f'Expected {new_expected_boosts}')
				print(f'Got {boosts}')

			gs.add_boost(player, boost_name, 3)
			new_expected_boosts[index] = (boost_name, 1.0)
			boosts = gs.all_boosts(player)
			if set(new_expected_boosts) != set(boosts):
				print('Unexpected boost values')
				print(f'Expected {new_expected_boosts}')
				print(f'Got {boosts}')

			gs.add_boost(player, boost_name, 3)
			new_expected_boosts[index] = (boost_name, 1.0)
			boosts = gs.all_boosts(player)
			if set(new_expected_boosts) != set(boosts):
				print('Unexpected boost values')
				print(f'Expected {new_expected_boosts}')
				print(f'Got {boosts}')

			gs.add_boost(player, boost_name, -3)
			new_expected_boosts[index] = (boost_name, 0.75)
			boosts = gs.all_boosts(player)
			if set(new_expected_boosts) != set(boosts):
				print('Unexpected boost values')
				print(f'Expected {new_expected_boosts}')
				print(f'Got {boosts}')

			gs.add_boost(player, boost_name, -3)
			new_expected_boosts[index] = (boost_name, 0.5)
			boosts = gs.all_boosts(player)
			if set(new_expected_boosts) != set(boosts):
				print('Unexpected boost values')
				print(f'Expected {new_expected_boosts}')
				print(f'Got {boosts}')

			gs.add_boost(player, boost_name, -3)
			new_expected_boosts[index] = (boost_name, 0.25)
			boosts = gs.all_boosts(player)
			if set(new_expected_boosts) != set(boosts):
				print('Unexpected boost values')
				print(f'Expected {new_expected_boosts}')
				print(f'Got {boosts}')

			gs.add_boost(player, boost_name, -3)
			new_expected_boosts[index] = (boost_name, 0.0)
			boosts = gs.all_boosts(player)
			if set(new_expected_boosts) != set(boosts):
				print('Unexpected boost values')
				print(f'Expected {new_expected_boosts}')
				print(f'Got {boosts}')

			gs.add_boost(player, boost_name, -3)
			new_expected_boosts[index] = (boost_name, 0.0)
			boosts = gs.all_boosts(player)
			if set(new_expected_boosts) != set(boosts):
				print('Unexpected boost values')
				print(f'Expected {new_expected_boosts}')
				print(f'Got {boosts}')
			
			break
	
	# Test case for entry hazard names
	test_entry_hazards = ['Spikes', 'Toxic Spikes', 'Stealth Rock', 'Sticky Web']
	for entry_hazard in ENTRY_HAZARD_TO_INDEX.keys():
		if entry_hazard not in test_entry_hazards and entry_hazard not in ['Min', 'Count', 'NotFound']:
			print(f'Unexpected entry hazard: {entry_hazard}')

	# Test case entry hazard increment and decrement
	for player in GameState.Player:
		if player == GameState.Player.count:
			continue 

		# Increment entry hazard value once for all entry hazards
		for entry_hazard in test_entry_hazards:
			gs.increment_entry_hazard(player, entry_hazard)
		
		# Check incremented value with expected value
		for entry_hazard in test_entry_hazards:
			expected_entry_hazard_value = 1.0/MAX_ENTRY_HAZARD_COUNT
			actual_entry_hazard_value = gs.get_player_attribute(player, ENTRY_HAZARD_TO_INDEX[entry_hazard])
			if expected_entry_hazard_value != actual_entry_hazard_value:
				print(f'Unexpected entry_hazard_increment for player {player}')
				print(f'Expected: {expected_entry_hazard_value} value for {entry_hazard}')
				print(f'Got: {actual_entry_hazard_value} value for {entry_hazard}')
		
		# clear entry hazard value once for all entry hazards
		for entry_hazard in test_entry_hazards:
			gs.clear_entry_hazard(player, entry_hazard)
		
		# Check cleared value with expected value (= 0.0)
		for entry_hazard in test_entry_hazards:
			expected_entry_hazard_value = 0.0
			actual_entry_hazard_value = gs.get_player_attribute(player, ENTRY_HAZARD_TO_INDEX[entry_hazard])
			if expected_entry_hazard_value != actual_entry_hazard_value:
				print(f'Unexpected entry_hazard_clear for {player}')
				print(f'Expected: {expected_entry_hazard_value} value for player {entry_hazard}')
				print(f'Got: {actual_entry_hazard_value} value for {entry_hazard}')
				
		# Increment entry hazard value MAX_ENTRY_HAZARD_COUNT + 1 times to check entry hazard value can't exceed 1.0
		for entry_hazard in test_entry_hazards:
			for _ in range(MAX_ENTRY_HAZARD_COUNT + 1):
				gs.increment_entry_hazard(player, entry_hazard)	
		
		# Check max entry hazard value can be 1.0
		for entry_hazard in test_entry_hazards:
			expected_entry_hazard_value = 1.0
			actual_entry_hazard_value = gs.get_player_attribute(player, ENTRY_HAZARD_TO_INDEX[entry_hazard])
			if expected_entry_hazard_value != actual_entry_hazard_value:
				print(f'Unexpected entry_hazard_increment for player {player}, got > 1.0 value')
				print(f'Expected: {expected_entry_hazard_value} value for {entry_hazard}')
				print(f'Got: {actual_entry_hazard_value} value for {entry_hazard}')


	# Test case for item names
	test_items = ['damprock', 'choicespecs', 'swampertite', 'wateriumz',
		'figyberry', 'rockyhelmet']
	for item in ITEM_NAME_TO_INDEX.keys():
		if item not in test_items and item not in ['Min', 'Count', 'NotFound']:
			print(f'Unexpected item: {item}')

	# Test case for item set and clear_all
	for player in GameState.Player:
		if player == GameState.Player.count:
			continue 

		# set all items to 1.0
		for pokemon_name in team1:
			for item in test_items:
				gs.set_item(player, pokemon_name, item)
		
		# Check set value with expected value (= 1.0)
		for pokemon_name in team1:
			for item in test_items:
				expected_item_value = 1.0
				actual_item_value = gs.get_item(player, pokemon_name, item)
				if expected_item_value != actual_item_value:
					print(f'Unexpected set_item for player {player}')
					print(f'Expected: {expected_item_value} value for {item} for {pokemon_name}')
					print(f'Got: {actual_item_value} value for {item} for {pokemon_name}')
		
		# clear all items
		for pokemon_name in team1:
			gs.clear_all_items(player, pokemon_name)

		# Check clear value with expected value (= 0.0)
		for pokemon_name in team1:
			for item in test_items:
				expected_item_value = 0.0
				actual_item_value = gs.get_item(player, pokemon_name, item)
				if expected_item_value != actual_item_value:
					print(f'Unexpected set_item for player {player}')
					print(f'Expected: {expected_item_value} value for {item} for {pokemon_name}')
					print(f'Got: {actual_item_value} value for {item} for {pokemon_name}')


	# Test case for stats
	test_stats = ['atk', 'def', 'spa', 'spd',
		'spe']
	for stat in STAT_NAME_TO_INDEX.keys():
		if stat not in test_stats and stat not in ['Min', 'Count', 'NotFound']:
			print(f'Unexpected stat: {stat}')

	# Test case for set stat and get stat
	for player in GameState.Player:
		if player == GameState.Player.count:
			continue 

		test_stat_value = 1000
		# set all stat to test_stat_value
		for pokemon_name in team1:
			for stat in test_stats:
				gs.set_stat(player, pokemon_name, stat, test_stat_value)
		
		# Check set value with expected value (= test_stat_value / STAT_NORMALIZER)
		for pokemon_name in team1:
			for stat in test_stats:
				expected_stat_value = test_stat_value / STAT_NORMALIZER
				actual_stat_value = gs.get_stat(player, pokemon_name, stat)
				if expected_stat_value != actual_stat_value:
					print(f'Unexpected set_stat, get_stat for player {player}')
					print(f'Expected: {expected_stat_value} value for {stat} for {pokemon_name}')
					print(f'Got: {actual_stat_value} value for {stat} for {pokemon_name}')
		
		test_stat_value = 4000
		# set all stat to test_stat_value to check max stat value should be 1.0
		for pokemon_name in team1:
			for stat in test_stats:
				gs.set_stat(player, pokemon_name, stat, test_stat_value)
		
		# Check set value with expected value (= 1.0)
		for pokemon_name in team1:
			for stat in test_stats:
				expected_stat_value = 1.0
				actual_stat_value = gs.get_stat(player, pokemon_name, stat)
				if expected_stat_value != actual_stat_value:
					print(f'Unexpected set_stat, get_stat for player {player}')
					print(f'Expected: {expected_stat_value} value for {stat} for {pokemon_name}')
					print(f'Got: {actual_stat_value} value for {stat} for {pokemon_name}')