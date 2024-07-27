import re
class Spell():
    def __init__(self, fileName: str) -> None:
        self.fileName = fileName
        self.read()
        self.spellDict = self.__dict__()

    def __dict__(self) -> dict[str,str]:
        d = {}
        d["Name"] =  self.Name
        d["Level"] =  self.Level
        d["School"] =  self.School
        d["Time"] =  self.Time
        d["Range"] =  self.Range
        d["Components"] =  self.Components
        d["Duration"] =  self.Duration
        d["Description"] =  self.Description
        d["Higher"] =  self.Higher
        return d


    def read(self) -> None:
        with open(self.fileName, 'r') as inputFile:
            spellLines = inputFile.readlines()
        # Remove empty lines and \n characters
        self.parse([re.sub(r"\*\*[\w\s]+?:\*\*\s*", '', line.replace('\n', '')) for line in spellLines if line != '\n'])

    def parse(self, spellLines : list[str]) -> None:
        
        self.Name = self.cleanName(spellLines[0])
        self.Level, self.School = self.cleanLevel(spellLines[1])
        self.Time = spellLines[2].capitalize()
        self.Range = spellLines[3].capitalize()
        self.Components = spellLines[4]
        self.Duration = spellLines[5]

        if spellLines[-1].startswith('***At Higher Levels***'):
            self.Description = '\n'.join(spellLines[6:-1])
            self.Higher = spellLines[-1].replace('***At Higher Levels***. ', '')
        else:
            self.Description = '\n\n'.join(spellLines[6:])
            self.Higher = ''


    @staticmethod
    def cleanName(spellName: str) -> str:
        return re.sub(r'[^\w\s]', '', spellName.strip())


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
    s = Spell('/data/DND.SRD.Wiki/Spells/Acid Arrow.md')
    print(s)