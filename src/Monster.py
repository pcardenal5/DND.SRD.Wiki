import re

class Monster():
    def __init__(self, fileName: str) -> None:
        self.fileName = fileName
        self.read()
        self.spellDict = self.__dict__()

    def __dict__(self)-> dict[str,str]:
        return {'' : ''}

    def read(self) -> None:
        with open(self.fileName, 'r') as inputFile:
            monsterLines = inputFile.readlines()
        # Remove empty lines and \n characters
        self.parse([re.sub(r"\*\*[\w\s]+?:\*\*\s*", '', line.replace('\n', '')) for line in monsterLines if line != '\n'])

    def parse(self, monsterLines: list[str]) -> None:
        self.Name = monsterLines[0]
        self.Class = monsterLines[1]
        self.AC = monsterLines[2]
        self.HP = monsterLines[3]
        self.Speed = monsterLines[4]
        self.Stats = self.parseStats(monsterLines[7], monsterLines[8])
        rest = monsterLines[9:]
        self.DamageResistances, rest = self.findStringElement('**Damage Resistances**', rest)
        self.DamageImmunities, rest = self.findStringElement('**Damage Immunities**', rest)
        self.ConditionImmunities, rest = self.findStringElement('**Condition Immunities**', rest)
        self.Senses, rest = self.findStringElement('**Senses**', rest)
        self.Languages, rest = self.findStringElement('**Languages**', rest)
        self.Challenge, rest = self.findStringElement('**Challenge**', rest)
        
        # Detect Action section
        index = 0
        for i in rest:
            if i == '###### Actions':
                break
            index += 1
        self.Properties = rest[0:index]
        self.Actions = rest[index+1:]

    @staticmethod
    def parseStats(statTable : str, saves : str) -> dict:
        statDict = {}
        statsGroup = [match for match in re.finditer(r'(\d+) \(([-\+]\d)\)', statTable)]
        statDict['STR'] = {
            'Value' : statsGroup[0].group(1),
            'Modifier': statsGroup[0].group(2)
        }

        statDict['DEX'] = {
            'Value' : statsGroup[1].group(1),
            'Modifier': statsGroup[1].group(2)
        }

        statDict['CON'] = {
            'Value' : statsGroup[2].group(1),
            'Modifier': statsGroup[2].group(2)
        }

        statDict['INT'] = {
            'Value' : statsGroup[3].group(1),
            'Modifier': statsGroup[3].group(2)
        }

        statDict['WIS'] = {
            'Value' : statsGroup[4].group(1),
            'Modifier': statsGroup[4].group(2)
        }

        statDict['CHA'] = {
            'Value' : statsGroup[5].group(1),
            'Modifier': statsGroup[5].group(2)
        }

        # Get saves value from string
        for stat in statDict.keys():
            saveValue = re.search(stat.capitalize() + r' [\+-](\d+)', saves)
            if saveValue:
                statDict[stat]['Save'] = saveValue.group(0)
            else:
                statDict[stat]['Save'] = statDict[stat]['Modifier']

        return statDict

    def findStringElement(self, searchString: str, searchList : list[str]) -> tuple[str, list[str]]:
        for element in searchList:
            if element.startswith(searchString):
                searchList.remove(element)
                return element.replace(searchString, '').strip().capitalize(), searchList
                
        return '', searchList

if __name__ == '__main__':
    Monster('/data/DND.SRD.Wiki/Monsters/Aboleth.md')