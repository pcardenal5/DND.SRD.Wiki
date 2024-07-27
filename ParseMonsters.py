import os
import json
from src.Monster import Monster

monsterDir = './Monsters'

monsterList = [monster for monster in os.listdir(monsterDir) if not monster.startswith('#')]

monsterDict = {}
for monster in monsterList:
    try:
        mon = Monster(os.path.join(monsterDir, monster))
    except Exception as e:
        print(e)
        print('###'*30)
        print(monster)
        continue
    monsterDict[mon.Name] = mon.__dict__()
    outputFileName = os.path.join(os.path.expanduser('~/ObsiDnD/PlayersHandbook/'), 'MonsterClean', mon.Name + '.md')
    monsterText = f'''# {mon.Name}

*{mon.Class}*

**CR:**
	- {mon.Challenge}


**AC:** {mon.AC}
**HP:** {mon.HP}
**Speed:** {mon.Speed}

---


|       |              STR               |              DEX               |              CON               |              INT               |              WIS               |              CHA               |
|:-----:|:------------------------------:|:------------------------------:|:------------------------------:|:------------------------------:|:------------------------------:|:------------------------------:|
| Value |  {mon.Stats['STR']['Value']}   |  {mon.Stats['DEX']['Value']}   |  {mon.Stats['CON']['Value']}   |  {mon.Stats['INT']['Value']}   |  {mon.Stats['WIS']['Value']}   |  {mon.Stats['CHA']['Value']}   |
|  Mod  | {mon.Stats['STR']['Modifier']} | {mon.Stats['DEX']['Modifier']} | {mon.Stats['CON']['Modifier']} | {mon.Stats['INT']['Modifier']} | {mon.Stats['WIS']['Modifier']} | {mon.Stats['CHA']['Modifier']} |
| Save  |   {mon.Stats['STR']['Save']}   |   {mon.Stats['DEX']['Save']}   |   {mon.Stats['CON']['Save']}   |   {mon.Stats['INT']['Save']}   |   {mon.Stats['WIS']['Save']}   |   {mon.Stats['CHA']['Save']}   |



**Skills:**
	- {mon.Skills}

**Damage Resistances:**
	- {mon.DamageResistances}

**Damage Immunities:**
	- {mon.DamageImmunities}

**Condition Immunities:**
	- {mon.ConditionImmunities}

**Sences:**
	- {mon.Senses}

**Languages:**
	- {mon.Languages}

**Abilities:**
	- {mon.Properties}
---

**ACTIONS:**

{mon.Actions}

'''        

    with open(outputFileName, 'w') as outputFile:
        outputFile.write(monsterText)

with open('./monsters.json', 'w') as outputfile:
    json.dump(monsterDict, outputfile)

