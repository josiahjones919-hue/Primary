#!/usr/bin/env python3
#Josiah Jones




import sys
import unittest

#Processor Constants (FR2)

MIN_INT32 = -2**31              # -2147483648
MAX_INT32 = 2**31 - 1           #  2147483647
BIT_WIDTH = 32


#Core Conversion Logic is as follows

class DataSystem32Bit:

    #Parse decimal signed integer input
    @staticmethod
    def parse_decimal_input(value_str):
        return int(value_str)
    #Detect overflow condition
    @staticmethod
    def detect_overflow(x):
        return x < MIN_INT32 or x > MAX_INT32
    #Apply Saturation Clamping
    @staticmethod
    def apply_saturation(x):
        if x > MAX_INT32:
            return MAX_INT32, 1
        elif x < MIN_INT32:
            return MIN_INT32, 1
        return x, 0
    #Two's Conversion
    @staticmethod
    def decimal_to_binary_32bit(x):
        if x < 0:
            x = (1 << BIT_WIDTH) + x  
        return format(x, '032b')
    #Two's Binary to Decimal
    @staticmethod
    def binary_to_decimal(bin_str):
        if bin_str[0] == '1':  # negative number
            return int(bin_str, 2) - (1 << BIT_WIDTH)
        return int(bin_str, 2)
    #Binary to Hex
    @staticmethod
    def binary_to_hex(bin_str):
        hex_str = format(int(bin_str, 2), '08X')
        return f"0x{hex_str}"
    #This is the main processing function/Handles format selection and returns flags
    @staticmethod
    def process(value_str, output_format):


        #Parse input
        x = DataSystem32Bit.parse_decimal_input(value_str)

        #Overflow Detection
        overflow_flag = 1 if DataSystem32Bit.detect_overflow(x) else 0

        #Apply saturation
        x_clamped, saturated_flag = DataSystem32Bit.apply_saturation(x)

        #Convert to internal 32-bit binary
        bin_32 = DataSystem32Bit.decimal_to_binary_32bit(x_clamped)

        output_format = output_format.upper()

        if output_format == "DEC":
            value_out = DataSystem32Bit.binary_to_decimal(bin_32)
        elif output_format == "BIN":
            value_out = bin_32
        elif output_format == "HEX":
            value_out = DataSystem32Bit.binary_to_hex(bin_32)
        else:
            raise ValueError("Invalid output format. Use DEC, BIN, or HEX.")

        return value_out, overflow_flag, saturated_flag


#Command-Line Interface

if __name__ == "__main__" and len(sys.argv) > 1:
    if len(sys.argv) != 3:
        print("Usage: python data_system.py <decimal_value> <DEC|BIN|HEX>")
        sys.exit(1)

    value_input = sys.argv[1]
    format_selector = sys.argv[2]

    result, overflow, saturated = DataSystem32Bit.process(value_input, format_selector)

    print("Output:", result)
    print("Overflow:", overflow)
    print("Saturated:", saturated)


#Unit Tests for FR8

class TestDataSystem32Bit(unittest.TestCase):

    def test_positive_value(self):
        value, overflow, saturated = DataSystem32Bit.process("123", "DEC")
        self.assertEqual(value, 123)
        self.assertEqual(overflow, 0)
        self.assertEqual(saturated, 0)

    def test_zero(self):
        value, overflow, saturated = DataSystem32Bit.process("0", "BIN")
        self.assertEqual(value, "00000000000000000000000000000000")
        self.assertEqual(overflow, 0)
        self.assertEqual(saturated, 0)

    def test_negative_value(self):
        value, overflow, saturated = DataSystem32Bit.process("-123", "DEC")
        self.assertEqual(value, -123)
        self.assertEqual(overflow, 0)
        self.assertEqual(saturated, 0)

    def test_max_boundary(self):
        value, overflow, saturated = DataSystem32Bit.process(str(MAX_INT32), "DEC")
        self.assertEqual(value, MAX_INT32)
        self.assertEqual(overflow, 0)
        self.assertEqual(saturated, 0)

    def test_min_boundary(self):
        value, overflow, saturated = DataSystem32Bit.process(str(MIN_INT32), "DEC")
        self.assertEqual(value, MIN_INT32)
        self.assertEqual(overflow, 0)
        self.assertEqual(saturated, 0)

    def test_positive_overflow(self):
        value, overflow, saturated = DataSystem32Bit.process(str(MAX_INT32 + 1), "DEC")
        self.assertEqual(value, MAX_INT32)
        self.assertEqual(overflow, 1)
        self.assertEqual(saturated, 1)

    def test_negative_overflow(self):
        value, overflow, saturated = DataSystem32Bit.process(str(MIN_INT32 - 1), "DEC")
        self.assertEqual(value, MIN_INT32)
        self.assertEqual(overflow, 1)
        self.assertEqual(saturated, 1)