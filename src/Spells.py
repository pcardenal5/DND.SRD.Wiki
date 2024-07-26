import re
class Spell():
    def __init__(self) -> None:
        pass

    def read(self, fileName : str ) -> dict[str,str]:
        with open(fileName, 'r') as inputFile:
            spellLines = inputFile.readlines()
        # Remove empty lines and \n characters
        return self.parse([re.sub(r"\*\*[\w\s]+?:\*\*\s*", '', line.replace('\n', '')) for line in spellLines if line != '\n'])

    def parse(self, spellLines : list[str]) -> dict[str,str]:
        spellDict = {}
        spellDict['Name'] = self.cleanName(spellLines[0])
        spellDict['Level'], spellDict['School'] = self.cleanLevel(spellLines[1])
        spellDict['Time'] = spellLines[2]
        spellDict['Range'] = spellLines[3]
        spellDict['Components'] = spellLines[4]
        spellDict['Duration'] = spellLines[5]

        if spellLines[-1].startswith('***At Higher Levels***'):
            spellDict['Description'] = '\n'.join(spellLines[6:-1])
            spellDict['Higher'] = spellLines[-1].replace('***At Higher Levels***. ', '')
        else:
            spellDict['Description'] = '\n'.join(spellLines[6:])
            spellDict['Higher'] = ''
        return spellDict


    @staticmethod
    def cleanName(spellName: str) -> str:
        return re.sub(r'[^\w]', '', spellName)
    

    @staticmethod
    def cleanLevel(spellLevel: str) -> tuple[str, str]:
        levelRegex = re.compile(r'\*(\d)\w\w-level\s([\w]+)').search(spellLevel)
        isRutual = spellLevel.endswith('ritual)*')
        if levelRegex:
            return levelRegex.group(1), (levelRegex.group(2) + isRutual*'(ritual)').capitalize()
        
        cantipRegex = re.compile(r'\*([\w]+)\scantrip\*$').search(spellLevel)
        if cantipRegex:
            return '0', cantipRegex.group(1)
        raise ValueError('Spell level and school not found')

if __name__ == '__main__':
    s = Spell()
    spelllines = s.read('/data/DND.SRD.Wiki/Spells/Acid Arrow.md')
    print(spelllines)
