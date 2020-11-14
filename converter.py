import re
from taxrecord import TaxRecord

RECORD_HEADER = 'H'
RECORD_DETAIL = 'D'
REPORT_LINE = 'X'
EMPTY_LINE = 'E'
UNIDENTIFIED_LINE = '?'

def parse_line(line):
    words = []
    tokens = re.finditer(r'[\,|\.|\-|\/|\(|\)|\:|\*|\w]+', line)
    for m in tokens:
        words.append(m)
    return words

def dump_tokens(tokens):
    for m in tokens:
        print('%02d-%02d: %s' % (m.start(), m.end(), m.group(0)))

def is_record_line(tokens):

    # All records have a least one field
    if len(tokens) == 0:
        return False

    # All records lines start with one or more spaces so the
    # start position of the first token must be greater than zero
    first_match = tokens[0]
    if first_match.start() <= 1:
        return False

    first_string = first_match.group(0)
    if first_string == "Land":
        return False

    if first_string == "Paris":
        return False

    return True

def is_first_record_line(tokens):
    first_match = tokens[0]

    # The first line of each record has the account id of variable length
    # but always left justified at the eight position in the line so if
    # the first token starts after that we know its NOT the first line of the record
    if first_match.start() < 8:
        return True
    else:
        return False

def is_empty_line(tokens):
    return len(tokens) == 0

def determine_line_type(tokens):
    if is_empty_line(tokens):
        return EMPTY_LINE

    if is_record_line(tokens):
        if is_first_record_line(tokens):
            return RECORD_HEADER
        else:
            return RECORD_DETAIL

    return REPORT_LINE

def process_file(filename):
    line_type = None
    tokens = None
    records = {}
    record = None


    with open(filename, 'r') as infile:
        record = None
        records = {}

        for line in infile:
            tokens = parse_line(line)
            line_type =  determine_line_type(tokens)

            if line_type == RECORD_HEADER:
                record = TaxRecord(tokens)
                records[record.account_num] = record
            elif line_type == RECORD_DETAIL:
                if record is None:
                    raise Exception
                record.update(tokens, line)
            elif line_type == EMPTY_LINE:
                None
            elif line_type == REPORT_LINE:
                None
            else:
                print('{} {}'.format(line_type, line))

        return records

def convert_to_csv(inputfile, outputfile):
    records = process_file(inputfile)

    file = open(outputfile, 'w')
    for key, value in records.items():
        file.write(value.csv())
        file.write('\n')

def main():
    convert_to_csv('oxford-tax-records.txt', 'oxford-tax-records.csv')
    convert_to_csv('tax-records.txt', 'paris-tax-records.csv')

if __name__ == "__main__":
    main()
