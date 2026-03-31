#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 20:55:49 2026

@author: josiahjones
"""


#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import itertools

#input 

def generate_inputs(n):
    return list(itertools.product([0,1], repeat=n))

def validate_table(inputs, outputs):
    if len(inputs) != 2**len(inputs[0]):
        return False, "Incorrect number of rows"
    if len(set(inputs)) != len(inputs):
        return False, "Duplicate input combinations"
    if any(o not in [0,1] for o in outputs):
        return False, "Outputs must be 0 or 1"
    return True, "Valid"

#minterm/maxterm computation

def get_minterms(outputs):
    return [i for i, val in enumerate(outputs) if val == 1]

def get_maxterms(outputs):
    return [i for i, val in enumerate(outputs) if val == 0]

def to_binary_str(index, n):
    return format(index, f'0{n}b')

#SOp/POS expressions

def sop_expression(minterms, n):
    terms = []
    for m in minterms:
        bits = to_binary_str(m, n)
        term = []
        for i, bit in enumerate(bits):
            var = chr(65 + i)
            term.append(var if bit == '1' else var + "'")
        terms.append(''.join(term))
    return " + ".join(terms)

def pos_expression(maxterms, n):
    terms = []
    for m in maxterms:
        bits = to_binary_str(m, n)
        term = []
        for i, bit in enumerate(bits):
            var = chr(65 + i)
            term.append(var + "'" if bit == '1' else var)
        terms.append("(" + " + ".join(term) + ")")
    return " ".join(terms)

#K-Map functions

def gray_code(n):
    if n == 1:
        return ['0', '1']
    prev = gray_code(n-1)
    return ['0'+x for x in prev] + ['1'+x for x in reversed(prev)]

def build_kmap(minterms, n):
    if n == 2:
        rows = gray_code(1)
        cols = gray_code(1)
    elif n == 3:
        rows = gray_code(1)
        cols = gray_code(2)
    elif n == 4:
        rows = gray_code(2)
        cols = gray_code(2)
    else:
        raise ValueError("K-map only supported for 2–4 variables")

    kmap = [[0 for _ in cols] for _ in rows]

    for m in minterms:
        bits = format(m, f'0{n}b')
        r = bits[:len(rows[0])]
        c = bits[len(rows[0]):]
        i = rows.index(r)
        j = cols.index(c)
        kmap[i][j] = 1

    return kmap, rows, cols

def print_kmap(kmap, rows, cols):
    print("\nK-Map:")
    print("    " + " ".join(cols))
    for i, row in enumerate(kmap):
        print(rows[i], " ", row)

#K Map grouping code block

def find_groups(kmap):
    rows = len(kmap)
    cols = len(kmap[0])
    groups = []

    #singles
    for i in range(rows):
        for j in range(cols):
            if kmap[i][j] == 1:
                groups.append([(i, j)])

    #horizontal pairs
    for i in range(rows):
        for j in range(cols):
            if kmap[i][j] == 1 and kmap[i][(j+1)%cols] == 1:
                groups.append([(i,j),(i,(j+1)%cols)])

    #vertical pairs
    for i in range(rows):
        for j in range(cols):
            if kmap[i][j] == 1 and kmap[(i+1)%rows][j] == 1:
                groups.append([(i,j),((i+1)%rows,j)])

    return groups

def group_to_term(group, rows, cols, n):
    bits_list = []
    for (i, j) in group:
        bits = rows[i] + cols[j]
        bits_list.append(bits)

    term = ""
    for i in range(n):
        column_bits = [b[i] for b in bits_list]
        if all(b == '1' for b in column_bits):
            term += chr(65+i)
        elif all(b == '0' for b in column_bits):
            term += chr(65+i) + "'"

    return term if term else "1"

def simplify_kmap(minterms, n):
    kmap, rows, cols = build_kmap(minterms, n)
    print_kmap(kmap, rows, cols)

    groups = find_groups(kmap)

    print("\nGroups:")
    for g in groups:
        print(g)

    terms = set()
    for g in groups:
        terms.add(group_to_term(g, rows, cols, n))

    return " + ".join(sorted(terms))

#expression evaluation

def evaluate_expr(expr, inputs):
    results = []

    for row in inputs:
        temp = expr

        for i, val in enumerate(row):
            var = chr(65+i)
            temp = temp.replace(var + "'", str(1 - val))
            temp = temp.replace(var, str(val))

        new_temp = ""
        for i in range(len(temp)):
            new_temp += temp[i]
            if i < len(temp)-1:
                if temp[i] in "01" and temp[i+1] in "01":
                    new_temp += " and "

        temp = new_temp
        temp = temp.replace("+", " or ")

        results.append(int(eval(temp)))

    return results


#main program

def main():
    n = int(input("Enter number of variables (2-4): "))
    inputs = generate_inputs(n)

    print("\nTruth Table:")
    outputs = []
    for row in inputs:
        val = int(input(f"{row}: "))
        outputs.append(val)

    valid, msg = validate_table(inputs, outputs)
    if not valid:
        print("Error:", msg)
        return

    choice = input("Choose form (SOP/POS): ").upper()

    if choice == "SOP":
        minterms = get_minterms(outputs)
        expr = sop_expression(minterms, n)
        print("\nMinterms:", minterms)
    else:
        maxterms = get_maxterms(outputs)
        expr = pos_expression(maxterms, n)
        print("\nMaxterms:", maxterms)

    print("\nCanonical Expression:")
    print(expr)

    #simplification
    if choice == "SOP":
        simplified = simplify_kmap(minterms, n)
    else:
        print("\nK-map simplification implemented for SOP only.")
        simplified = expr

    print("\nSimplified Expression:")
    print(simplified)

    #validation block
    result = evaluate_expr(simplified, inputs)

    if result == outputs:
        print("\nValidation: PASS")
    else:
        print("\nValidation: FAIL")

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
