class Position:
   def __init__(self, start, length, type="String", ignore=None):
       self.start = start
       self.end = length
       self.type = type
       self.ignore = ignore

class TaxRecord:

    def __init__(self, tokens):
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
        self.tax_rate = 0.00
        self.land_rate = 0.00

        if self.tax > 0 and self.assessment_value > 0:
            self.tax_rate = self.tax / self.assessment_value * 100

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
        buff = buff + "\n\tTax Rate = {}".format(self.tax_rate)
        buff = buff + "\n\tLand Rate = {}".format(self.land_rate)

        return buff

    def csv(self):
        buff = "{}".format(self.account_num)
        buff = buff + ", {}".format(self.name)
        buff = buff + ", {}".format(self.land_value)
        buff = buff + ", {}".format(self.bulding_value)
        buff = buff + ", {}".format(self.excemption_value)
        buff = buff + ", {}".format(self.assessment_value)
        buff = buff + ", {}".format(self.tax)
        buff = buff + ", {}".format(self.acres)
        buff = buff + ", {}".format(self.map)
        buff = buff + ", {}".format(self.tree_growth)
        buff = buff + ", {}".format(self.homestead)
        buff = buff + ", {}".format(self.tax_rate)
        buff = buff + ", {}".format(self.land_rate)

        return buff

    def update(self, tokens):
        token_count = len(tokens)
        if token_count == 1:
            value = tokens[0].group(0)
            prefix = value[0:2]
            if prefix == "R-" or prefix == "U-":
                self.map = value

        for index in range(token_count):
            value = tokens[index].group(0)
            if value == "Acres":
                self.acres = float(tokens[index+1].group(0))
                if self.tax > 0 and self.acres > 0:
                    self.land_rate = self.tax / self.acres
            if value == "*TREE":
                self.tree_growth = True
            if value == "Homestead":
                self.homestead = True


