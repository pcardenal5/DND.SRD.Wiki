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
    outputFileName = os.path.join(os.path.expanduser('~/ObsiDnD/PlayersHandbook/'), 'SpellClean', spell["Name"] + '.md')
    spellText = f'''_Lv{spell['Level']} {spell['School']}_

| Casting Time | Range | Components | Duration |
| :----------: | :---: | :--------: | :------: |
| {spell['Time']} | {spell['Range']} | {spell['Components']} | {spell['Duration']} |

{spell['Description']}
'''
    if spell['Higher'] != '':
        spellText = spellText + f'''
## At higher levels

{spell['Higher']}
'''        

    with open(outputFileName, 'w') as outputFile:
        outputFile.write(spellText)

with open('./Spells.json', 'w') as outputfile:
    json.dump(spellDict, outputfile)

