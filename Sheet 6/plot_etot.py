#!/usr/bin/env python3
"""Parse a QE-like output file for total energies (Etot) per SCF iteration and plot Etot vs n.

Usage:
    python plot_etot.py diamond.out

It writes `etot_vs_n.png` in the same directory as the input file.
"""
import sys
import re
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def parse_etot_lines(text):
    """Return list of (n, etot) parsed from text.

    The function looks for lines that contain Etot or total energy and an iteration number.
    It supports common variants like:
      !    total energy              =   -10.12345678 Ry
      total energy              =   -10.12345678 Ry
      Etot = -10.12345678 Ry
    If no explicit iteration number is present, it will assign sequential n starting at 1.
    """
    etot_pattern = re.compile(r"(?P<iter>\biter(?:ation)?\s*=?\s*(?P<i>\d+))|(?P<bang>!\s*)?total energy\s*=?\s*(?P<val>[-+]?\d+\.\d+)|\bEtot\b\s*=?\s*(?P<et>[-+]?\d+\.\d+)", re.IGNORECASE)

    results = []
    seq_n = 0
    for line in text.splitlines():
        m = etot_pattern.search(line)
        if not m:
            continue
        # try different groups
        val = None
        if m.group('val'):
            val = float(m.group('val'))
        elif m.group('et'):
            val = float(m.group('et'))

        if val is None:
            continue

        # try to find an explicit iteration number on the same line
        itnum = None
        it_match = re.search(r"\b(iter(?:ation)?|n)\s*[:=]?\s*(\d+)", line, re.IGNORECASE)
        if it_match:
            try:
                itnum = int(it_match.group(2))
            except Exception:
                itnum = None

        if itnum is None:
            seq_n += 1
            itnum = seq_n
        else:
            # keep seq_n aligned if explicit iter found
            seq_n = itnum

        results.append((itnum, val))

    # sort by iteration number
    results.sort(key=lambda x: x[0])
    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: python plot_etot.py <path/to/diamond.out>")
        sys.exit(2)

    infile = Path(sys.argv[1])
    if not infile.exists():
        print(f"Input file not found: {infile}")
        sys.exit(1)

    text = infile.read_text(encoding='utf-8', errors='ignore')
    data = parse_etot_lines(text)
    if not data:
        print("No Etot/total energy lines found in the file.")
        sys.exit(1)

    ns, etots = zip(*data)

    # If energies are in Rydberg and are large negative numbers, keep as-is; user can convert later.
    plt.figure(figsize=(6,4))
    plt.plot(ns, etots, marker='o')
    plt.xlabel('SCF iteration n')
    plt.ylabel('Total energy (Ry)')
    plt.title(f'Total energy vs SCF iteration ({infile.name})')
    plt.grid(True)

    outpath = infile.with_name('etot_vs_n.png')
    plt.tight_layout()
    plt.savefig(outpath, dpi=150)
    print(f'Saved plot: {outpath}')


if __name__ == '__main__':
    main()
