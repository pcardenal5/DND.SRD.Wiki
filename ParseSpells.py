import os
import json
from src.Spells import Spell

spellDir = './Spells'

spellList = [spell for spell in os.listdir(spellDir) if not spell.startswith('#')]

spellDict = {}
sp = Spell()
for spell in spellList:

    spell = sp.read(os.path.join(spellDir, spell))
    spellDict[spell['Name']] = spell
    with open(f'./SpellClean/{spell["Name"]}.md', 'w') as outputFile:
        outputFile.write(f'''
_Lv{spell['Level']} {spell['School']}_ 

| {spell['Time']} | {spell['Range']} | {spell['Components']} | {spell['Duration']} |
| -------- | ---- | --- | -------- |

{spell['Description']}
{spell['Higher']}
''')

with open('./Spells.json', 'w') as outputfile:
    json.dump(spellDict, outputfile)

