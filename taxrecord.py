import re

class Position:
   def __init__(self, start, length, type="String", ignore=None):
       self.start = start
       self.end = length
       self.type = type
       self.ignore = ignore

class TaxRecord:

    def __init__(self, tokens):
        try:
            self._tokens = tokens
            end = len(tokens) - 1
            self.account_num = tokens[0].group(0)
            self.name = tokens[1].group(0)
            index = 2
            while index < end - 4:
                self.name = self.name + ' ' + tokens[index].group(0)
                index = index + 1
            self.land_value = float(tokens[end-4].group(0).replace(',',''))
            self.bulding_value = float(tokens[end-3].group(0).replace(',',''))
            self.excemption_value = float(tokens[end-2].group(0).replace(',',''))
            self.assessment_value = float(tokens[end-1].group(0).replace(',',''))
            self.tax = float(tokens[end].group(0).replace(',',''))
            self.acres = 0
            self.map = None
            self.tree_growth = False
            self.homestead = False
            self.soft = 0.0
            self.hard = 0.0
            self.mixed = 0.0
            self.map_type = None
            self.map_page = None
            self.map_plot = None

            if self.tax > 0 and self.assessment_value > 0:
                self.tax_rate = self.tax / self.assessment_value * 100

        except Exception:
            print(tokens)

    def __str__(self):
        buff = "Account #{}".format(self.account_num)
        buff = buff + "\n\tName = {}".format(self.name)
        buff = buff + "\n\tLand = {}".format(self.land_value)
        buff = buff + "\n\tBuliding = {}".format(self.bulding_value)
        buff = buff + "\n\tExemption = {}".format(self.excemption_value)
        buff = buff + "\n\tAssessment = {}".format(self.assessment_value)
        buff = buff + "\n\tTax = {}".format(self.tax)
        buff = buff + "\n\tAcres = {}".format(self.acres)
        buff = buff + "\n\tMap = {}".format(self.map)
        buff = buff + "\n\tTree Growth = {}".format(self.tree_growth)
        buff = buff + "\n\tHomestead = {}".format(self.homestead)
        buff = buff + "\n\tSoft = {}".format(self.soft)
        buff = buff + "\n\tHard = {}".format(self.hard)
        buff = buff + "\n\tMixed = {}".format(self.mixed)
        buff = buff + "\n\tMap Type = {}".format(self.map_type)
        buff = buff + "\n\tMap Page = {}".format(self.map_page)
        buff = buff + "\n\tMap Plot= {}".format(self.map_plot)

        return buff

    def csv(self):
        try:
            buff = "{}".format(self.account_num)
            buff = buff + ', "{}"'.format(self.name)
            buff = buff + ", {}".format(self.land_value)
            buff = buff + ", {}".format(self.bulding_value)
            buff = buff + ", {}".format(self.excemption_value)
            buff = buff + ", {}".format(self.assessment_value)
            buff = buff + ", {}".format(self.tax)
            buff = buff + ", {}".format(self.acres)
            buff = buff + ", {}".format(self.map)
            buff = buff + ", {}".format(self.tree_growth)
            buff = buff + ", {}".format(self.homestead)
            buff = buff + ", {}".format(self.soft)
            buff = buff + ", {}".format(self.hard)
            buff = buff + ", {}".format(self.mixed)
            buff = buff + ", {}".format(self.map_type)
            buff = buff + ", {}".format(self.map_page)
            buff = buff + ", {}".format(self.map_plot)

            return buff
        except Exception:
            print("** ERR: csv ***")
            print (self._tokens)
            return ''

    def _get_value(self, key, line):
        pattern = r'{}\s*(?P<value>[0-9]*\.[0-9]*)'.format(key)
        match = re.search(pattern, line)
        return match

    def update(self, tokens, line):
        try:
            token_count = len(tokens)
            if token_count == 1:
                value = tokens[0].group(0)
                match = re.search(r'(?P<map_type>[UR])-?(?P<map_page>[0-9]{2})-(?P<map_plot>[0-9]{1,3}-?[0-9A-Z]{0,4})', value)
                if (match):
                    self.map = value
                    self.map_type = match.group('map_type')
                    self.map_page = match.group('map_page')
                    self.map_plot = match.group('map_plot')

            match = self._get_value('Acres', line)
            if match:
                self.acres = match.group('value')

            for index in range(token_count):
                value = tokens[index].group(0)
                #if value == "Acres":
                #    self.acres = float(tokens[index+1].group(0))
                #    if self.tax > 0 and self.acres > 0:
                #        self.land_rate = self.tax / self.acres
                if value == "Soft:":
                    self.soft= float(tokens[index+1].group(0))
                if value == "Hard:":
                    self.hard= float(tokens[index+1].group(0))
                if value == "Mixed:":
                    self.mixed= float(tokens[index+1].group(0))
                if value == "*TREE":
                    self.tree_growth = True
                if value == "Homestead":
                    self.homestead = True

        except Exception as e:
            print(e)
            print(tokens)

