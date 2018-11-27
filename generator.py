import re

def gen_output(outfile, old_state, new_state, i, reading_table, writing_table, performing_table):
    if i == len(reading_table):
        print(file=outfile)
        print('{},{}'.format(old_state, ','.join(reading_table)), file=outfile)
        print('{},{},{}'.format(new_state, ','.join(writing_table), ','.join(performing_table)), file=outfile)
    else:
        if reading_table[i] == '?':
            reading_table[i] = '_'
            writing_table[i] = '_'
            gen_output(outfile, old_state, new_state, i+1, list(reading_table), list(writing_table), performing_table)
            reading_table[i] = '1'
            writing_table[i] = '1'
        gen_output(outfile, old_state, new_state, i+1, list(reading_table), list(writing_table), performing_table)

def reduce_output(outfile):
    with open(outfile, 'r') as machine:
        code = machine.read()
        code = re.sub(r'\n+$|^\n+', '', code)
        lines = re.split(r'\n+', code)

    out = open(outfile, 'w')

    trans = set()
    i = 0
    while i < len(lines):
        if re.match(r'(name|init|accept): ', lines[i]):
            print(lines[i], file=out)
        elif re.match(r'fitas: ', lines[i]):
            tapes = re.sub(r'fitas: ', '', lines[i]).split(',')
            tapes = {v: k for k, v in enumerate(tapes)}
        elif not re.match(r'//--', lines[i]):
            trans.add('\n'+'\n'.join(lines[i:i+2]))
            i+=1
        i+=1
    for t in trans:
        print(t, file=out)

    out.close()

if __name__ == '__main__':
    with open('in', 'r') as machine:
        code = machine.read()
        code = re.sub(r'\n+$|^\n+', '', code)
        lines = re.split(r'\n+', code)

    tapes = {}

    out = open('out', 'w')

    i = 0
    while i < len(lines):
        if re.match(r'(name|init|accept): ', lines[i]):
            print(lines[i], file=out)
        elif re.match(r'fitas: ', lines[i]):
            tapes = re.sub(r'fitas: ', '', lines[i]).split(',')
            tapes = {v: k for k, v in enumerate(tapes)}
        elif not re.match(r'//--', lines[i]):
            print(lines[i])
            active_tapes = re.sub(r'//', '', lines[i]).split(',')
            i += 1

            params = lines[i].split(',')
            old_state, reading = params[0], params[1:]
            i += 1

            params = lines[i].split(',')
            new_state, writing, performing = params[0], params[1:1+len(active_tapes)], params[1+len(active_tapes):]

            reading_table = ['?']*len(tapes)
            writing_table = ['?']*len(tapes)
            performing_table = ['-']*len(tapes)
            for key, tape in enumerate(active_tapes):
                reading_table[tapes[tape]] = reading[key]
                writing_table[tapes[tape]] = writing[key]
                performing_table[tapes[tape]] = performing[key]

            gen_output(out, old_state, new_state, 0, reading_table, writing_table, performing_table)

#            print(active_tapes)
#            print(old_state, reading)
#            print(new_state, writing, performing)
        i += 1

    out.close()
    reduce_output('out')