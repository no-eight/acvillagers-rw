#! /usr/bin/python
# bimdl.py - downloads full res of all images for a given set of earch terms
# usage: /path/to/folder/ search terms -here 'with(parentheses'

import sys
import os
import re
import bs4
import requests
import logging
import requests
import csv

file_start = '<?xml version="1.0" encoding="utf-8" ?><Defs>\n'
file_end = '</Defs>'

rule_pack_body = ['<RulePackDef><defName>NamerPersonAC','</defName><rulePack><rulesStrings><li>name->[',']</li></rulesStrings><rulesRaw><li Class="Rule_File"><keyword>','</keyword><path>ACNames/','</path></li></rulesRaw></rulePack></RulePackDef>\n']

script_dir = os.path.dirname(__file__)
string_defs = 'Defs'
string_namegen = 'NameGen'
string_thingdefraces = 'ThingDefs_Races'
string_pawnkinddefs = 'PawnKindDefs'
string_pawnkinds_filename_front = 'PawnKinds_AC'
string_pawnkinds_filename_end = '.xml'
string_backstorydefs = 'BackstoryDefs'
string_backstorydefs_filename= 'ACBackstoryDefs'
string_race_filename_front = 'AC'
string_race_filename_end = '_Race.xml'
string_name_folder = os.path.join('Languages', 'English', "Strings", "ACNames")
string_namegen_filename = 'RulePacks_NameMakers_AC.xml'
string_txt = ".txt"
string_mod_folder_path_linux = '/home/thomas/.steam/steam/steamapps/common/RimWorld/Mods'

race_file_body = ['<AlienRace.ThingDef_AlienRace ParentName="BasePawn">\n\t<defName>Alien_AC','</defName>\n<label>',' Villager</label>\n\t<description>A Nook Inc. clone of the ',' villager ',', an anthropomorphic ',' who originally lived on Earth in the early 21st century. Though genetically identical to the original ',' mind was copied imperfectly, creating a personality distinct from other ','s, ','.</description>\n\t<alienRace>\n\t<generalSettings>\n\t\t<factionRelations><li>\n\t\t\t<factions><li>AnimalVillager</li></factions>\n\t\t\t<goodwill><min>100</min><max>100</max></goodwill>\n\t\t</li></factionRelations>\n\t\t<maleGenderProbability>','</maleGenderProbability>\n\t\t<forcedRaceTraitEntries>\n\t\t\t<li><defName>Xenophobia</defName><degree>1</degree><chance>0</chance></li>\n\t\t\t<li><defName>Xenophobia</defName><degree>-1</degree><chance>0</chance></li>\n\t\t</forcedRaceTraitEntries>\n\t\t<maxDamageForSocialfight>','</maxDamageForSocialfight>\n\t\t<alienPartGenerator>\n\t\t\t<headOffset>(',', ',')</headOffset>\n\t\t\t<aliencrowntypes><li>Average_Normal</li></aliencrowntypes>\n\t\t\t<alienbodytypes><li>','</li></alienbodytypes>\n\t\t\t<useGenderedHeads>false</useGenderedHeads>\n\n\t\t\t<bodyAddons><li>\n\t\t\t\t<drawSize>','</drawSize>\n\t\t\t\t<path>','Villagers/','/Tail/Tail</path>\n\t\t\t\t<bodyPart>tail</bodyPart>\n\t\t\t\t<inFrontOfBody>false</inFrontOfBody>\n\t\t\t\t<useSkinColor>true</useSkinColor>\n\t\t\t\t<drawnInBed>false</drawnInBed>\n\t\t\t\t<offsets>\n\t\t\t\t\t<south><bodyTypes><','>(',', ',')</','></bodyTypes><crownTypes><Normal_Average>(0,0)</Normal_Average></crownTypes></south>\n\t\t\t\t\t<north><bodyTypes><','>(',', ',')</','></bodyTypes><crownTypes><Normal_Average>(0,0)</Normal_Average></crownTypes></north>\n\t\t\t\t\t<east><bodyTypes><','>(',', ',')</','></bodyTypes><crownTypes><Normal_Average>(0,0)</Normal_Average></crownTypes></east>\n\t\t\t\t</offsets>\n\t\t\t</li><li>\n\t\t\t\t<drawSize>','</drawSize>\n\t\t\t\t<path>','Villagers/','/Head/Overhead</path>\n\t\t\t\t<inFrontOfBody>false</inFrontOfBody>\n\t\t\t\t<useSkinColor>true</useSkinColor>\n\t\t\t\t<drawnInBed>true</drawnInBed>\n\t\t\t\t<offsets>\n\t\t\t\t\t<south><bodyTypes><','>(0.0, 0.0)</','></bodyTypes><crownTypes><Normal_Average>(0,0)</Normal_Average></crownTypes></south>\n\t\t\t\t\t<north><bodyTypes><','>(0.0, ',')</','></bodyTypes><crownTypes><Normal_Average>(0,0)</Normal_Average></crownTypes></north>\n\t\t\t\t\t<east><bodyTypes><','>(0.0, 0.0)</','></bodyTypes><crownTypes><Normal_Average>(0,0)</Normal_Average></crownTypes></east>\n\t\t\t\t</offsets>\n\t\t\t</li></bodyAddons>\n\n\t\t\t<alienskincolorgen Class="ColorGenerator_Options"><options><li><weight>10</weight><only>RGBA(1.0,1.0,1.0,1)</only></li></options></alienskincolorgen>\n\t\t\t<customDrawSize>(',', ',')</customDrawSize><customHeadDrawSize>(',', ',')</customHeadDrawSize><customPortraitDrawSize>(',', ',')</customPortraitDrawSize><customPortraitHeadDrawSize>(',', ',')</customPortraitHeadDrawSize>\n\t\t</alienPartGenerator>\n\t\t<humanRecipeImport>true</humanRecipeImport>\n\t</generalSettings>\n\n\t<graphicPaths><li>\n\t\t<head>','Villagers/','/Head/</head>\n\t\t<body>','Villagers/','/Body/</body>\n\t\t<skeleton>Things/Pawn/Humanlike/Bodies/Dessicated/Dessicated_Thin</skeleton>\n\t</li></graphicPaths>\n\t<hairSettings><hasHair>false</hasHair><getsGreyAt>50</getsGreyAt></hairSettings>\n\t\t<relationSettings>\n\t\t\t<relationChanceModifierChild>0</relationChanceModifierChild><relationChanceModifierParent>0</relationChanceModifierParent><relationChanceModifierSibling>0</relationChanceModifierSibling><relationChanceModifierExLover>0.5</relationChanceModifierExLover><relationChanceModifierExSpouse>0</relationChanceModifierExSpouse><relationChanceModifierLover>0</relationChanceModifierLover><relationChanceModifierSpouse>0</relationChanceModifierSpouse><relationChanceModifierFiance>0</relationChanceModifierFiance>\n\t\t</relationSettings>\n\t\t<raceRestriction>\n\t\t\t<apparelList></apparelList>\n\t\t\t<whiteApparelList>\n\t\t\t\t<li>Apparel_TribalA</li><li>Apparel_Parka</li><li>Apparel_Duster</li><li>Apparel_Jacket</li><li>Apparel_FlakJacket</li><li>Apparel_VestPlate</li><li>Apparel_PowerArmor</li>\n\t\t\t\t<!--<li>Apparel_CowboyHat</li><li>Apparel_BowlerHat</li><li>Apparel_TribalHeaddress</li><li>Apparel_Tuque</li><li>Apparel_WarMask</li><li>Apparel_WarVeil</li><li>Apparel_SimpleHelmet</li><li>Apparel_AdvancedHelmet</li><li>Apparel_PowerArmorHelmet</li><li>Apparel_PsychicFoilHelmet</li>-->\n\t\t\t\t<li>Apparel_ShieldBelt</li><li>SmokepopBelt</li>\n\t\t\t\t<!-- Glittertech Apparel --><li>Apparel_NanoSuit</li><li>Apparel_Reactive</li><li>Apparel_NanoSkin</li><li>Apparel_NanoSpeed</li><li>Apparel_OCCombatVest</li><li>Apparel_HC1Shield</li><li>Apparel_OCShield</li>\n\t\t\t\t<!-- Rimatomics Apparel --><li>Apparel_RadiationSuit</li><li>Apparel_MoppSuitDesert</li><li>Apparel_MoppSuitWoodland</li><li>Apparel_MoppSuitSnow</li>\n\t\t\t\t<!-- Advanced Shield Belts Apparel --><li>Apparel_QRShieldBelt</li><li>Apparel_HeavyShieldBelt</li><li>Apparel_RangedShieldBelt</li>\n\t\t\t\t<!-- Dubs Kits stuff --><li>MedicineBag</li><li>MedicalKit</li><li>UltraMedKit</li><li>DubsRepairKit</li></whiteApparelList>\n\t\t\t<onlyUseRaceRestrictedApparel>true</onlyUseRaceRestrictedApparel>\n\t\t</raceRestriction>\n\n\t</alienRace>\n\t<statBases>\n\t\t<MarketValue>1000</MarketValue><MoveSpeed>4.6</MoveSpeed><Flammability>1.0</Flammability><ComfyTemperatureMin>-10</ComfyTemperatureMin><ComfyTemperatureMax>32</ComfyTemperatureMax><CarryingCapacity>60</CarryingCapacity>\n\t\t<LeatherAmount>','</LeatherAmount>\n\t\t<ResearchSpeed>1.2</ResearchSpeed><MiningSpeed>1.0</MiningSpeed><SocialImpact>1.0</SocialImpact><PlantHarvestYield>1.0</PlantHarvestYield><ConstructionSpeed>1.0</ConstructionSpeed>\n\t\t<ArmorRating_Blunt>','</ArmorRating_Blunt><ArmorRating_Sharp>','</ArmorRating_Sharp>\n\t</statBases>\n\t<tools>\n\t\t<li><label>left ','</label>\n\t\t\t<capacities><li>Blunt</li></capacities>\n\t\t\t<power>','</power>\n\t\t\t<cooldownTime>2</cooldownTime><linkedBodyPartsGroup>LeftHand</linkedBodyPartsGroup><surpriseAttack><extraMeleeDamages><li>\n\t\t\t\t<def>Stun</def><amount>','</amount></li>\n\t\t\t</extraMeleeDamages></surpriseAttack></li>\n\t\t<li><label>right ','</label>\n\t\t\t<capacities><li>Blunt</li></capacities>\n\t\t\t<power>','</power>\n\t\t\t<cooldownTime>2</cooldownTime><linkedBodyPartsGroup>RightHand</linkedBodyPartsGroup><surpriseAttack><extraMeleeDamages><li>\n\t\t\t\t<def>Stun</def><amount>','</amount></li>\n\t\t</extraMeleeDamages></surpriseAttack></li>\n\t\t<li><label>','</label>\n\t\t\t<capacities><li>Bite</li></capacities>\n\t\t\t<power>','</power>\n\t\t\t<cooldownTime>1.6</cooldownTime><linkedBodyPartsGroup>','</linkedBodyPartsGroup><chanceFactor>0.7</chanceFactor></li>\n\t\t<li><label>head</label>\n\t\t\t<capacities><li>Blunt</li></capacities>\n\t\t\t<power>','</power>\n\t\t\t<cooldownTime>2</cooldownTime><linkedBodyPartsGroup>HeadAttackTool</linkedBodyPartsGroup><ensureLinkedBodyPartsGroupAlwaysUsable>true</ensureLinkedBodyPartsGroupAlwaysUsable><chanceFactor>0.2</chanceFactor></li>\n\t</tools>\n\n\t<race>\n\t\t<thinkTreeMain>Humanlike</thinkTreeMain>\n\t\t<nameGenerator>NamerPersonAC','</nameGenerator>\n\t\t<thinkTreeConstant>HumanlikeConstant</thinkTreeConstant><intelligence>Humanlike</intelligence><makesFootprints>true</makesFootprints><lifeExpectancy>100</lifeExpectancy>\n\t\t<leatherDef>','</leatherDef>\n\t\t<nameCategory>HumanStandard</nameCategory><body>AC','</body>\n\t\t<baseBodySize>','</baseBodySize>\n\t\t<baseHealthScale>1.0</baseHealthScale><foodType>OmnivoreHuman</foodType><baseHungerRate>1.0</baseHungerRate>\n\n\t\t<gestationPeriodDays>32.5</gestationPeriodDays><litterSizeCurve><points><li>(0.5, 1.0)</li></points></litterSizeCurve><lifeStageAges><li><def>HumanlikeBaby</def><minAge>0</minAge></li><li><def>HumanlikeToddler</def><minAge>1.2</minAge></li><li><def>HumanlikeChild</def><minAge>4</minAge></li><li><def>HumanlikeTeenager</def><minAge>10</minAge></li><li><def>HumanlikeAdult</def><minAge>18</minAge></li></lifeStageAges>\n\t\t<soundMeleeHitPawn>Pawn_Melee_Punch_HitPawn</soundMeleeHitPawn><soundMeleeHitBuilding>Pawn_Melee_Punch_HitBuilding</soundMeleeHitBuilding><soundMeleeMiss>Pawn_Melee_Punch_Miss</soundMeleeMiss>\n\t\t<ageGenerationCurve><points><li>(14,0)</li><li>(16,100)</li><li>(50,100)</li><li>(60,30)</li><li>(70,18)</li><li>(80,10)</li><li>(90,3)</li><li>(100,0)</li></points></ageGenerationCurve>\n\t\t<hediffGiverSets><li>OrganicStandard</li></hediffGiverSets>\n\t</race>\n\t\t<recipes>','</recipes>\n</AlienRace.ThingDef_AlienRace>\n\n<AlienRace.RaceSettings><defName>','Settings</defName><pawnKindSettings>\n\t<startingColonists>\n\t\t<li><pawnKindEntries><li><kindDefs><li>AC','Villager</li></kindDefs><chance>100</chance></li></pawnKindEntries><factionDefs><li>Player_AnimalVillager</li></factionDefs></li>\n\t\t<li><pawnKindEntries><li><kindDefs><li>AC','Villager</li></kindDefs><chance>0.1</chance></li></pawnKindEntries><factionDefs><li>PlayerColony</li></factionDefs></li>\n\t</startingColonists>\n\t<alienrefugeekinds><li><kindDefs><li>AC','Villager</li></kindDefs><chance>10.0</chance></li></alienrefugeekinds>\n\t<alienslavekinds><li><kindDefs><li>AC','Villager</li></kindDefs><chance>10.0</chance></li></alienslavekinds>\n\t<alienwandererkinds><li><pawnKindEntries><li><kindDefs><li>AC','Villager</li></kindDefs><chance>5.0</chance></li></pawnKindEntries><factionDefs><li>PlayerColony</li></factionDefs></li></alienwandererkinds>\n</pawnKindSettings></AlienRace.RaceSettings>\n']

has_tail_recipes ='<li>InstallClothVillagerTail</li><li>InstallBionicVillagerTail</li>'
has_beak_recipes ='<li>InstallWoodenVillagerBeak</li><li>InstallBionicVillagerBeak</li>'
has_horn_recipes = '<li>InstallGoldHorn</li>'

racedef_use_name = [0,3,6,15,30,47,49,63,68,69,70,71,72,73]
racedef_use_species = [1,4,14,29,46,48]
racedef_jock_dependent = [9,53,54,56,57,59,60]
racedef_use_species_param = [10,11,13,17,18,21,22,25,26,28,29,34,38,39,40,41,42,43,44,45,46,50,51,52,53,56,59,61,64,65,66,67]
racedef_use_species_bodytype = [12,16,19,20,23,24,27,31,32,33,35,36,37]

pawnkind_file_body = ['\t<PawnKindDef Name="AC','BasePlayer" Abstract="True"><race>Alien_AC','</race><defaultFactionType>Player_AnimalVillager</defaultFactionType>\n\t\t<backstoryFiltersOverride><li><categories><li>AC','Backstory</li></categories></li></backstoryFiltersOverride>\n\t\t<weaponMoney><min>150</min><max>450</max></weaponMoney>\n\t\t<gearHealthRange><min>0.7</min><max>2.3</max></gearHealthRange>\n\t\t<apparelTags><li>IndustrialBasic</li><li>IndustrialAdvanced</li></apparelTags>\n\t\t<chemicalAddictionChance>0.15</chemicalAddictionChance>\n\t\t<invNutrition>2.1</invNutrition><itemQuality>Normal</itemQuality>\n\t\t<backstoryCryptosleepCommonality>0.02</backstoryCryptosleepCommonality>\n\t\t<combatEnhancingDrugsChance>0.25</combatEnhancingDrugsChance><combatEnhancingDrugsCount><min>0</min><max>3</max></combatEnhancingDrugsCount>\n\t\t<minGenerationAge>','</minGenerationAge><maxGenerationAge>','</maxGenerationAge>\n\t</PawnKindDef>\n\n\t<PawnKindDef ParentName="AC','Base"><defName>AC','Villager</defName><label>','</label>\n\t\t<combatPower>35</combatPower><apparelAllowHeadgearChance>0</apparelAllowHeadgearChance><apparelTags><li>IndustrialBasic</li><li>IndustrialAdvanced</li></apparelTags><isFighter>false</isFighter>\n\t\t<weaponTags><li>ACSlingshot</li></weaponTags><weaponMoney><min>0</min><max>0</max></weaponMoney><apparelMoney><min>200</min><max>650</max></apparelMoney><itemQuality>Normal</itemQuality><chemicalAddictionChance>0.05</chemicalAddictionChance><combatEnhancingDrugsChance>0</combatEnhancingDrugsChance><backstoryCryptosleepCommonality>0.1</backstoryCryptosleepCommonality>\n\t</PawnKindDef>\n\n\t<!---<PawnKindDef ParentName="AC','BasePlayer"><defName>AC','VillagerEmbark</defName><label>','</label>\n\t\t<combatPower>35</combatPower><weaponTags><li>ACSlingshot</li></weaponTags><weaponMoney><min>0</min><max>0</max></weaponMoney><apparelAllowHeadgearChance>0</apparelAllowHeadgearChance><apparelTags><li>IndustrialBasic</li><li>IndustrialAdvanced</li></apparelTags><isFighter>false</isFighter>\n\t\t<apparelMoney><min>200</min><max>650</max></apparelMoney><itemQuality>Normal</itemQuality><chemicalAddictionChance>0.05</chemicalAddictionChance><combatEnhancingDrugsChance>0</combatEnhancingDrugsChance><backstoryCryptosleepCommonality>0.1</backstoryCryptosleepCommonality>\n\t</PawnKindDef>-->\n\n\t<PawnKindDef Name="AC','Base" Abstract="True"><race>Alien_AC','</race><defaultFactionType>AnimalColony</defaultFactionType>\n\t\t<baseRecruitDifficulty>0.75</baseRecruitDifficulty>\n\t\t<backstoryFiltersOverride><li><categories><li>AC','Backstory</li></categories></li></backstoryFiltersOverride>\n\t\t<weaponMoney><min>150</min><max>450</max></weaponMoney>\n\t\t<gearHealthRange><min>0.7</min><max>2.3</max></gearHealthRange><apparelTags><li>IndustrialBasic</li><li>IndustrialAdvanced</li></apparelTags>\n\t\t<chemicalAddictionChance>0.15</chemicalAddictionChance>\n\t\t<invNutrition>2.1</invNutrition>\n\t\t<itemQuality>Normal</itemQuality>\n\t\t<backstoryCryptosleepCommonality>0.02</backstoryCryptosleepCommonality>\n\t\t<minGenerationAge>','</minGenerationAge><maxGenerationAge>','</maxGenerationAge>\n\t\t<combatEnhancingDrugsChance>0.25</combatEnhancingDrugsChance><combatEnhancingDrugsCount><min>0</min><max>3</max></combatEnhancingDrugsCount>\n\t</PawnKindDef>\n\n\t<!--<PawnKindDef ParentName="AC','Base"><defName>AC','_Ranger</defName><label>','</label>\n\t\t<combatPower>50</combatPower><gearHealthRange><min>1.0</min><max>3.2</max></gearHealthRange>\n\t\t<apparelTags><li>IndustrialBasic</li><li>IndustrialAdvanced</li><li>BeltDefensePop</li></apparelTags>\n\t\t<apparelMoney><min>1100</min><max>1600</max></apparelMoney><apparelAllowHeadgearChance>0.0</apparelAllowHeadgearChance>\n\t\t<weaponMoney><min>400</min><max>700</max></weaponMoney>\n\t\t<weaponTags><li>ACSlingshot</li></weaponTags><combatEnhancingDrugsChance>0.1</combatEnhancingDrugsChance><combatEnhancingDrugsCount><min>0</min><max>3</max></combatEnhancingDrugsCount>\n\t\t<inventoryOptions><skipChance>0.85</skipChance><subOptionsChooseOne><li><thingDef>Silver</thingDef><countRange><min>50</min><max>150</max></countRange></li><li><thingDef>MedicineIndustrial</thingDef><countRange><min>1</min><max>1</max></countRange></li></subOptionsChooseOne>\n\t\t</inventoryOptions>\n\t</PawnKindDef>-->']

pawnkind_use_name = [0,1,5,6,7,8,9,10,11,12,16,17,18]

male_personality = ['Jock', 'Smug', 'Cranky', 'Lazy']
species_is_avian = ['Eagle', 'Duck', 'Bird', 'Chicken', 'Penguin', 'Ostrich']
species_has_no_tail = ['Frog']
species_has_horns = ['Deer', 'Rhino', 'Cow', 'Bull', 'Sheep', 'Goat']

species_params_dict = {}
def name_file_writer (villager_name):
    path = os.path.join(script_dir, string_name_folder)
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, villager_name + string_txt), 'w') as name_file:
        name_file.write(villager_name)

def make_species_params_dict ():
    with open('species_params.csv', newline='') as params_list:
        species_params_dict = {}
        species_params_dict_reader =  csv.DictReader(params_list, delimiter=',', quotechar='|')
        for row in species_params_dict_reader:
            species_params_dict[row['species']] = row
        return species_params_dict

def gender_from_personality (personality):
    if personality in male_personality:
        return '1'
    else:
        return '0'

### Name Maker ###
species_params_dict = make_species_params_dict()
with open('villagers.csv', newline='') as villager_list:
    villager_list_reader = csv.reader(villager_list, delimiter=',', quotechar='|')
    name_maker_file = file_start + '\n'
    for row in villager_list_reader:
        for i in range(0, len(rule_pack_body)):
            villager_name = row[0]
            name_file_writer(villager_name)
            name_maker_file += rule_pack_body[i]
            if i < len(rule_pack_body) - 1:
                name_maker_file += villager_name
    name_maker_file += file_end
    path = os.path.join(script_dir, string_defs, string_namegen)
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, string_namegen_filename), 'w') as namegen_file:
        namegen_file.write(name_maker_file)
### Race File ###
with open('villagers.csv', newline='') as villager_list:
    villager_list_reader = csv.reader(villager_list, delimiter=',', quotechar='|')
    species_params_dict = make_species_params_dict()
    path = os.path.join(script_dir, string_defs, string_thingdefraces)
    os.makedirs(path, exist_ok=True)
    for row in villager_list_reader:
        race_file = file_start + '\n'
        villager_name = row[0]
        villager_species = row[1]
        villager_species_lower = villager_species.lower()
        villager_param_dict = species_params_dict[villager_species_lower]
        villager_personality = row[2]
        villager_catch = row[3]
        for i in range (0,len(race_file_body)):
            race_file += race_file_body[i]
            if i in racedef_use_name:
                race_file += villager_name
            elif i in racedef_use_species:
                if i == 4:
                    race_file += villager_species_lower
                else:
                    race_file += villager_species
            elif i in racedef_use_species_param:
                if i in [13, 28, 38, 39, 42, 43]:
                    race_file += villager_param_dict['draw_size']
                elif i in [40, 41, 44, 45]:
                    race_file += villager_param_dict['head_draw_size']
                elif i in [53, 56]:
                    race_file += villager_param_dict['label_fist']
                elif i == 10:
                    race_file += villager_param_dict['head_offset_x']
                elif i == 11:
                    race_file += villager_param_dict['head_offset_y']
                elif i == 17:
                    race_file += villager_param_dict['south_tail_offset_x']
                elif i == 34:
                    race_file += villager_param_dict['overhead_offset_y']
                elif i == 18:
                    race_file += villager_param_dict['south_tail_offset_y']
                elif i == 21:
                    race_file += villager_param_dict['north_tail_offset_x']
                elif i == 22:
                    race_file += villager_param_dict['north_tail_offset_y']
                elif i == 25:
                    race_file += villager_param_dict['east_tail_offset_x']
                elif i == 26:
                    race_file += villager_param_dict['east_tail_offset_y']
                elif i == 50:
                    race_file += villager_param_dict['leather_amount']
                elif i == 51:
                    race_file += villager_param_dict['armor_rating_blunt']
                elif i == 52:
                    race_file += villager_param_dict['armor_rating_sharp']
                elif i == 59:
                    race_file += villager_param_dict['label_teeth']
                elif i == 64:
                    race_file += villager_param_dict['leather_def']
                elif i == 61:
                    if villager_species in species_is_avian:
                        race_file += 'VillagerBeak'
                    else:
                        race_file += 'Teeth'
                elif i == 65:
                    if villager_species in species_is_avian:
                        race_file += 'Avian'
                    else:
                        race_file += 'Standard'
                elif i == 67:
                    if villager_species in species_is_avian:
                        race_file += has_beak_recipes
                    elif villager_species in species_has_no_tail:
                        race_file += has_jaw_recipes
                    elif villager_species in species_has_horns or villager_name == 'Julian':
                        if villager_species == 'Deer' and villager_personality not in male_personality:
                            race_file += has_tail_recipes
                        else:
                            race_file += has_horn_recipes + has_tail_recipes
                    else:
                        race_file += has_tail_recipes
                elif i == 66:
                    race_file += villager_param_dict['base_body_size']
            elif i in racedef_use_species_bodytype:
                race_file += villager_param_dict['body_type']
            elif i in racedef_jock_dependent:
                temp = ''
                if i in [54, 57]:
                    if villager_personality == 'Jock':
                        temp = '8.2'
                    else:
                        temp = '6.0'
                elif i in [55, 58]:
                    if villager_personality == 'Jock':
                        temp = '20.0'
                    else:
                        temp = '14.0'
                elif i == 9:
                    if villager_personality == 'Jock':
                        temp = '8.0'
                    else:
                        temp = '6.0'
                elif i == 60:
                    if villager_personality == 'Jock':
                        temp = '8.0'
                    else:
                        temp = '8.0'
                elif i == 62:
                    if villager_personality == 'Jock':
                        temp = '6.0'
                    else:
                        temp = '4.0'
                race_file += temp
            elif i == 2:
                personality_lower = villager_personality.lower()
                race_file += personality_lower
            elif i == 7:
                race_file += villager_catch
            elif i == 8:
                race_file += gender_from_personality(villager_personality)
            elif i == 5:
                if villager_personality in ['Jock', "Cranky", "Lazy", "Smug"]:
                    race_file += 'his'
                else:
                    race_file += 'her'
        race_file += file_end
        with open(os.path.join(path, string_race_filename_front + villager_name + string_race_filename_end),
                  'w') as open_file:
            open_file.write(race_file)
### PawnKind File ###
with open('villagers.csv', newline='') as villager_list:
    villager_list_reader = csv.reader(villager_list, delimiter=',', quotechar='|')
    species_params_dict = make_species_params_dict()
    path = os.path.join(script_dir, string_defs, string_pawnkinddefs)
    os.makedirs(path, exist_ok=True)
    for row in villager_list_reader:
        race_file = file_start + '\n'
        villager_name = row[0]
        villager_personality = row[2]
        for i in range (0,len(pawnkind_file_body)):
            race_file += pawnkind_file_body[i]
            if i in pawnkind_use_name:
                race_file += villager_name
            elif i in [2, 13]:
                race_file += villager_personality
            elif i in [3, 14]:
                if villager_personality != 'Cranky':
                    race_file += '20'
                else:
                    race_file += '55'
            elif i in [4, 15]:
                if villager_personality == 'Peppy':
                    race_file += '35'
                elif villager_personality == 'Cranky':
                    race_file += '85'
                else:
                    race_file += '45'
        race_file += file_end
        with open(os.path.join(path, string_pawnkinds_filename_front + villager_name + string_pawnkinds_filename_end),
                  'w') as open_file:
            open_file.write(race_file)