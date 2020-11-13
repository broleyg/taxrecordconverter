import re


def extract_field(start, length, buffer):
    value = buffer[start:length].strip()
    print('value={}'.format(value))
    return value

def categorize(line):

    if re.match("\ ", line):
        print('PARSE : {}'.format(line))
        account = line[0:10].strip()
        full_name = line[11:25]
        print('account={}'.format(account))
        for m in re.finditer(r'\w+', line):
            print('%02d-%02d: %s' % (m.start(), m.end(), m.group(0)))
    else:
        #print('IGNORE: {}'.format(line))
        None

def convert():
    with open('tax-records.txt', 'r') as infile:
        for line in infile:
            categorize(line)

def main():
    convert()

if __name__ == "__main__":
    main()
