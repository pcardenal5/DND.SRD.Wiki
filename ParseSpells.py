import os
import json
from src.Spells import Spell

spellDir = './Spells'

spellList = [spell for spell in os.listdir(spellDir) if not spell.startswith('#')]

spellDict = {}
for spell in spellList:
    sp = Spell(os.path.join(spellDir, spell))
    spellDict[sp.Name] = sp.__dict__()
    outputFileName = os.path.join(os.path.expanduser('~/ObsiDnD/PlayersHandbook/'), 'SpellClean', sp.Name + '.md')
    spellText = f'''# {sp.Name}

_Lv{sp.Level} {sp.School}_

| Casting Time | Range | Components | Duration |
| :----------: | :---: | :--------: | :------: |
| {sp.Time} | {sp.Range} | {sp.Components} | {sp.Duration} |

{sp.Description}
'''

    if sp.Higher != '':
        spellText = spellText + f'''
## At higher levels

{sp.Higher}
'''        

    with open(outputFileName, 'w') as outputFile:
        outputFile.write(spellText)

with open('./Spells.json', 'w') as outputfile:
    json.dump(spellDict, outputfile)

