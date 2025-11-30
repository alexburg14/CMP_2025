#!/usr/bin/env python3
"""Analyze `diamond.out` to print band indices and energies at Gamma and at k=(0,0.75,0).

Usage:
    python analyze_bands.py diamond.out
"""
import sys
from pathlib import Path
import re


def parse_band_blocks(text):
    # find k-point headers and following energy line(s)
    # header looks like: "k = 0.0000 0.0000 0.0000 (   893 PWs)   bands (ev):"
    lines = text.splitlines()
    blocks = []
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"\s*k\s*=\s*([-0-9.]+)\s+([-0-9.]+)\s+([-0-9.]+)", line)
        if m:
            k = (float(m.group(1)), float(m.group(2)), float(m.group(3)))
            # collect next non-empty lines that look like energy numbers
            energies = []
            j = i+1
            while j < len(lines) and (lines[j].strip() == '' or re.search(r"[-0-9\.]+", lines[j])):
                if lines[j].strip():
                    # parse floats from the line
                    parts = re.findall(r"[-+]?[0-9]*\.?[0-9]+", lines[j])
                    # convert to floats
                    try:
                        vals = [float(p) for p in parts]
                    except:
                        vals = []
                    energies.extend(vals)
                j += 1
            blocks.append((k, energies))
            i = j
        else:
            i += 1
    return blocks


def find_block_for_k(blocks, target):
    # match within rounding tolerance
    for k, energies in blocks:
        if all(abs(k[i] - target[i]) < 1e-6 for i in range(3)):
            return k, energies
    # try matching with some tolerance (like 1e-3) if exact match not found
    for k, energies in blocks:
        if all(abs(k[i] - target[i]) < 1e-3 for i in range(3)):
            return k, energies
    return None


def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_bands.py diamond.out")
        sys.exit(1)
    p = Path(sys.argv[1])
    if not p.exists():
        print('Input file not found')
        sys.exit(1)

    text = p.read_text(encoding='utf-8', errors='ignore')
    blocks = parse_band_blocks(text)

    # targets
    gamma = (0.0, 0.0, 0.0)
    k075 = (0.0, 0.75, 0.0)

    g = find_block_for_k(blocks, gamma)
    k7 = find_block_for_k(blocks, k075)

    if not g:
        print('Gamma block not found')
    else:
        kg, eg = g
        print(f'Gamma k = {kg}: found {len(eg)} band energies')
        for idx, e in enumerate(eg, start=1):
            print(f'  band {idx:3d}: {e:12.6f} eV')

    print('')
    if not k7:
        print('k=(0,0.75,0) block not found')
    else:
        kk, ek = k7
        print(f'k = {kk}: found {len(ek)} band energies')
        for idx, e in enumerate(ek, start=1):
            print(f'  band {idx:3d}: {e:12.6f} eV')

    # find global highest occupied and lowest unoccupied as reported in file
    m = re.search(r'highest occupied, lowest unoccupied level \(ev\):\s*([0-9\.\-]+)\s*([0-9\.\-]+)', text)
    if m:
        vbm = float(m.group(1))
        cbm = float(m.group(2))
        print('\nReported global edges:')
        print(f'  VBM = {vbm:.6f} eV, CBM = {cbm:.6f} eV, gap = {cbm-vbm:.6f} eV')


if __name__ == '__main__':
    main()
