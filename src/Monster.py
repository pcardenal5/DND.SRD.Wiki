import re

class Monster():
    def __init__(self, fileName: str) -> None:
        self.fileName = fileName
        self.read()

    def __dict__(self)-> dict:
        return {
            'Name' : self.Name,
            'Class' : self.Class,
            'Challenge' : self.Challenge,
            'AC' : self.AC,
            'HP' : self.HP,
            'Speed' : self.Speed,
            'Stats' : self.Stats,
            'DamageResistances' : self.DamageResistances,
            'DamageImmunities' : self.DamageImmunities,
            'ConditionImmunities' : self.ConditionImmunities,
            'Senses' : self.Senses,
            'Languages' : self.Languages,
            'Properties' : self.Properties,
            'Actions' : self.Actions
        }

    def read(self) -> None:
        with open(self.fileName, 'r') as inputFile:
            self.lines = inputFile.readlines()
        # Remove empty lines and \n characters
        self.lines = [re.sub(r"\*\*[\w\s]+?:\*\*\s*", '', line.replace('\n', '')) for line in self.lines if line != '\n']
        self.parseLines()

    def parseLines(self) -> None:
        self.Name = re.sub(r'[^\w\s]', '', self.lines[0]).strip()
        self.Class = self.lines[1]
        self.Stats = self.parseStats(self.lines[7], self.lines[8])
        self.findStringElement('**Saving Throws**')
        self.AC = self.findStringElement('**Armor Class**')
        self.HP = self.findStringElement('**Hit Points**')
        self.Speed = self.findStringElement('**Speed**')
        self.DamageResistances = self.findStringElement('**Damage Resistances**')
        self.DamageImmunities = self.findStringElement('**Damage Immunities**')
        self.ConditionImmunities = self.findStringElement('**Condition Immunities**')
        self.Skills = self.findStringElement('**Skills**')
        self.Senses = self.findStringElement('**Senses**')
        self.Languages = self.findStringElement('**Languages**')
        self.Challenge = self.findStringElement('**Challenge**')

        # Detect Action section
        index = 0
        for i in self.lines:
            if i == '###### Actions':
                break
            index += 1
        self.Properties = self.lines[5:index]
        self.parseProperties()
        self.Actions = self.lines[index+1:]
        self.parseActions()

    def parseStats(self, statTable : str, saves : str) -> dict:
        statDict = {}
        statsGroup = [match for match in re.finditer(r'(\d+) \(([-\+]\d+)\)', statTable)]
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
                statDict[stat]['Save'] = saveValue.group(1)
            else:
                statDict[stat]['Save'] = statDict[stat]['Modifier']

        return statDict


    def findStringElement(self, searchString: str) -> str:
        for element in self.lines:
            if element.startswith(searchString):
                self.lines.remove(element)
                return element.replace(searchString, '').strip().capitalize()

        return ''


    def parseProperties(self) -> None:
        self.PropertiesText = ''
        for p in self.Properties:
            p = re.sub(r'^\*{2,3}([\s\w/\(\)]+?)\*{2,3}\.?\s', r'### \1 \n\n', p)
            self.PropertiesText += p + '\n\n'


    def parseActions(self) -> None:
        self.ActionsText = ''
        for p in self.Actions:
            if p.endswith('Legendary Actions'):
                p = '## Legendary Actions'
            p = re.sub(r'^\*{2,3}([\s\w/\(\)]+?)\*{2,3}\.?\s', r'### \1 \n\n', p)
            self.ActionsText += p + '\n\n'

if __name__ == '__main__':
    # mon = Monster('/data/DND.SRD.Wiki/Monsters/Acolyte (NPC).md')
    # print(mon.PropertiesText)
    mon = Monster('/data/DND.SRD.Wiki/Monsters/Aboleth.md')
    print(mon.__dict__())
