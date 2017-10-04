import collections
import itertools
import json

class LabAnalyzer:
  def __init__(self):
    self.rooms = []
    with open('section-presets.json') as file:
      self.presets = json.loads(file.read())

  def loadRooms(self, rooms):
    self.rooms = rooms

  def divideIntoSections(self):
    dividers = [i for i, room in enumerate(self.rooms) if room['name'] == 'Aspirant\'s Trial' or room['name'] == 'Aspirant\'s Plaza']

    def findSection(start):
      result = []
      visited = set([start])
      q = collections.deque([start])
      while q:
        x = q.popleft()
        result.append(x)
        for room in self.rooms[x]['exits']:
          if not room in dividers and not room in visited:
            q.append(room)
            visited.add(room)
      return result

    firstSection = sorted([*findSection(dividers[0]), dividers[1]])
    thirdSection = sorted([*findSection(dividers[3]), dividers[2]])
    secondSection = sorted([*(set(range(len(self.rooms))) - set(firstSection) - set(thirdSection)), dividers[1], dividers[2]])
    return (firstSection, secondSection, thirdSection)

  def sectionMatrix(self, section):
    return [[1 if to in self.rooms[frm]['exits'] and self.rooms[frm]['exits'][to] != 'C' else 0 for to in section]
            for frm in section]

  def sectionHasGoldenKey(self, section):
    return any('GK' in self.rooms[room]['contents'] for room in section)

  def findPreset(self, part, section):
    matrix = self.sectionMatrix(section)
    hasGoldenKey = self.sectionHasGoldenKey(section)
    for preset in self.presets[part]:
      order = self.sectionIsomorphism(matrix, preset['matrix'])
      if order:
        return [preset['coords'][i - 1] for i in order[1:-1]]

  def sectionIsomorphism(self, m1, m2):
    if len(m1) != len(m2):
      return None
    else:
      for p in itertools.permutations(range(1, len(m1) - 1)):
        order = [0, *p, len(m1) - 1]
        if [[m2[x][y] for y in order] for x in order] == m1:
          return order
      return None
