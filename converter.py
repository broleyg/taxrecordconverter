import re
from taxrecord import TaxRecord

def extract_field(start, length, buffer):
    value = buffer[start:length].strip()
    print('value={}'.format(value))
    return value

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
    if first_match.start() == 0:
        return False

    first_string = first_match.group(0)
    if first_string == "Land":
        return False

    if first_string == "Paris":
        return False

    return True

def is_first_record_line(tokens):
    first_match = tokens[0]
    if first_match.start() < 8:
        return True
    else:
        return False

def is_empty_line(tokens):
    return len(tokens) == 0

def convert():
    in_record = False
    tokens = None
    tax_record = None
    records = {}
    i = 0
    line_type = '?'
    num = 0
    with open('tax-records.txt', 'r') as infile:
        for line in infile:
            i = i + 1
            line_type = '?'
            tokens = parse_line(line)
            if not is_empty_line(tokens):
                if is_record_line(tokens):
                    if is_first_record_line(tokens):
                        line_type = 'F'
                        in_record = True
                        #dump_tokens(tokens)
                        tax_record = TaxRecord(tokens)
                        records[tax_record.account_num] = tax_record
                    else:
                        line_type = '-'
                        tax_record.update(tokens)
                else:
                    line_type = 'x'
                    if in_record:
                        in_record = False
            else:
                line_type = '.'

            if line_type == 'F':
                num = num + 1
                #print('{} {} {} {}'.format(num, i, line_type, line[:-1]))

    print('*'*75)
    for key, value in records.items():
        print(value.csv())
    print('*'*75)
    print(len(records))



def main():
    convert()

if __name__ == "__main__":
    main()
