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
_, INDEX_TO_POKEMON_NAME = attribute_dict_setup(POKEMON_NAME_TO_INDEX)

# OLD MOVE_NAME_TO_INDEX = {}
'''
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
# See PokemonMoves.csv
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