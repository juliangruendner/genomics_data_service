import sys


def to_upper(in_file, out_file):
    with open(in_file, "rt") as fin:
        with open(out_file, "wt") as fout:
            for line in fin:
                if line.startswith(">"):
                    fout.write(line)
                else:
                    fout.write(line.upper())


def chrX_to_X(in_file, out_file):
    with open(in_file, "rt") as fin:
        with open(out_file, "wt") as fout:
            for line in fin:
                if line.startswith(">chrX"):
                    fout.write(">X\n")
                elif line.startswith('>'):
                    fout.write(line)
                else:
                    fout.write(line.upper())


if __name__ == '__main__':
    # to_upper(in_file=sys.argv[1], out_file=sys.argv[2])
    chrX_to_X(in_file=sys.argv[1], out_file=sys.argv[2])
