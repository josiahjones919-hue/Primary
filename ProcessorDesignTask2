#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 20:55:49 2026

@author: josiahjones
"""

import itertools

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

def get_minterms(inputs, outputs):
    return [i for i, val in enumerate(outputs) if val == 1]

def get_maxterms(inputs, outputs):
    return [i for i, val in enumerate(outputs) if val == 0]

def to_binary_str(index, n):
    return format(index, f'0{n}b')

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

def evaluate_expr(expr, inputs):
    results = []

    for row in inputs:
        temp = expr

        #replace variables with values
        for i, val in enumerate(row):
            var = chr(65+i)
            temp = temp.replace(var + "'", str(1 - val))
            temp = temp.replace(var, str(val))

        #insert AND between adjacent digits
        new_temp = ""
        for i in range(len(temp)):
            new_temp += temp[i]
            if i < len(temp) - 1:
                if temp[i] in "01" and temp[i+1] in "01":
                    new_temp += " and "

        temp = new_temp

        #replace OR operator
        temp = temp.replace("+", " or ")

        results.append(int(eval(temp)))

    return results

def main():
    n = int(input("Enter number of variables: "))
    inputs = generate_inputs(n)

    print("Enter output values:")
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
        minterms = get_minterms(inputs, outputs)
        expr = sop_expression(minterms, n)
        print("Minterms:", minterms)
    else:
        maxterms = get_maxterms(inputs, outputs)
        expr = pos_expression(maxterms, n)
        print("Maxterms:", maxterms)

    print("Canonical Expression:")
    print(expr)

    
    simplified = expr  #replace with real K-map logic

    print("Simplified Expression:")
    print(simplified)

    #validation
    result = evaluate_expr(simplified, inputs)

    if result == outputs:
        print("Validation: PASS")
    else:
        print("Validation: FAIL")

if __name__ == "__main__":
    main()
