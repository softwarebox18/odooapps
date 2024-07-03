import random
from odoo.tools.translate import _

def generate_codabar_value(self):
    barcode = random.choice('ABCD')  # Start character (A, B, C, or D)
    for _ in range(10):  # Generate the 10 middle characters
        char = random.choice('0123456789')
        barcode += char
    barcode += random.choice('ABCD')  # Stop character (A, B, C, or D)

    return barcode


def generate_code11_value(self):
    """
    Generate a random Code 11 barcode value.

    Returns:
        str: The generated Code 11 barcode value.
    """
    # Code 11 characters (0-9 and the dash character)
    code11_chars = '0123456789-'

    # Generate random barcode value
    barcode_length = random.randint(6, 15)  # Random length for the barcode value
    barcode_value = ''.join(random.choices(code11_chars, k=barcode_length))

    return barcode_value


# def generate_code11_value(self):
#     """
#     Generate a Code 11 barcode value.
#
#     Returns:
#         str: The generated Code 11 barcode value.
#     """
#     length = random.randint(4, 10)  # Random length for the barcode value
#     # Code 11 characters: digits 0-9 and special characters '-' and '*'
#     code11_chars = '0123456789-'
#     # Start and end characters for Code 11
#     start_stop_chars = '-'
#     # Generate random barcode value
#     barcode_value = ''.join(random.choices(code11_chars, k=length))
#     # Add start and end characters
#     barcode_value = start_stop_chars + barcode_value + start_stop_chars
#
#     return barcode_value


def generate_code128_value(self):
    """
        Generate a Code 128 barcode value with alphanumeric characters in upper case.

        Returns:
            str: The generated Code 128 barcode value.
        """
    length = 10  # Length of the generated barcode value
    # Randomly choose 2 to 3 alphabets
    alphabets = random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=random.randint(2, 3))
    # Generate random barcode value with numeric values and chosen alphabets
    barcode_value = ''.join(random.choices('0123456789' + ''.join(alphabets), k=length))

    return barcode_value


def generate_ean5_value(self):
    """
    Generate a random EAN-5 barcode value.

    Returns:
        str: The generated EAN-5 barcode value.
    """
    # Generate a random 5-digit number
    random_number = ''.join(random.choices('0123456789', k=4))

    # Calculate the checksum
    even_sum = sum(int(digit) for digit in random_number[::2])  # Sum of even-position digits
    odd_sum = sum(int(digit) for digit in random_number[1::2])  # Sum of odd-position digits
    total_sum = even_sum + odd_sum * 3  # Multiply sum of odd-position digits by 3 and add to even-position digits sum
    checksum = (10 - (total_sum % 10)) % 10  # Take modulo 10 of the total sum and find the difference from 10

    # Construct the full EAN-5 barcode value
    ean5_value = random_number + str(checksum)

    return ean5_value


def generate_ean8_value(self):
    """
    Generate a random EAN-8 barcode value.

    Returns:
        str: The generated EAN-8 barcode value.
    """
    # Generate number system (first two digits)
    number_system = ''.join(random.choices('0123456789', k=2))
    # Generate manufacturing code (five digits)
    manufacturing_code = ''.join(random.choices('0123456789', k=5))
    # Generate product code (two digits)
    product_code = ''.join(random.choices('0123456789', k=2))
    # Combine all parts to form the initial EAN-8 code
    ean8_initial = number_system + manufacturing_code + product_code
    # Calculate the check digit
    sum_even = sum(int(ean8_initial[i]) for i in range(0, 7, 2))
    sum_odd = sum(int(ean8_initial[i]) for i in range(1, 7, 2))
    checksum = (sum_even + sum_odd * 3) % 10
    if checksum != 0:
        checksum = 10 - checksum
    # Construct the full EAN-8 barcode value
    ean8_value = ean8_initial + str(checksum)

    return ean8_value


def generate_ean13_value(self):
    """
    Generate a random EAN-13 barcode value.

    Returns:
        str: The generated EAN-13 barcode value.
    """
    # Generate country code (first two digits)
    country_code = '000'  # For demonstration, you may replace '00' with an appropriate country code
    if self.env.user.company_id.country_id.phone_code:
        country_code = str(self.env.user.company_id.country_id.phone_code)
    # Pad country code with zeros to ensure it's at least two digits long
    country_code = country_code.zfill(2)

    # Generate manufacturing code (five digits)
    manufacturing_code = ''.join(random.choices('0123456789', k=5))

    # Generate product code (five digits)
    product_code = ''.join(random.choices('0123456789', k=5))

    # Combine all parts to form the initial EAN-13 code
    ean13_initial = country_code + manufacturing_code + product_code

    # Calculate the check digit
    sum_even = sum(int(ean13_initial[i]) for i in range(0, 12, 2))
    sum_odd = sum(int(ean13_initial[i]) for i in range(1, 12, 2))
    checksum = (sum_even + sum_odd * 3) % 10
    if checksum != 0:
        checksum = 10 - checksum

    # Construct the full EAN-13 barcode value
    ean13_value = ean13_initial + str(checksum)

    return ean13_value


def generate_extended_39_value(self):
    """
    Generate a random Code 39 barcode value.

    Returns:
        str: The generated Code 39 barcode value.
    """
    # Code 39 characters (excluding start/stop characters)
    code39_chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # Generate random barcode value
    barcode_length = random.randint(6, 7)  # Random length for the barcode value
    barcode_value = ''.join(random.choices(code39_chars, k=barcode_length))

    # Calculate the optional Mod 43 check digit
    def calculate_mod43(barcode):
        mod43_dict = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
                      'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'I': 18,
                      'J': 19, 'K': 20, 'L': 21, 'M': 22, 'N': 23, 'O': 24, 'P': 25, 'Q': 26, 'R': 27,
                      'S': 28, 'T': 29, 'U': 30, 'V': 31, 'W': 32, 'X': 33, 'Y': 34, 'Z': 35}
        sum = 0
        for char in barcode:
            sum += mod43_dict[char]
        return sum % 43

    check_digit = calculate_mod43(barcode_value)
    # Construct the full Code 39 barcode value
    code39_value = barcode_value + code39_chars[check_digit]  # Add start and stop characters

    return code39_value


def generate_extended_93_value(self):
    """
    Generate a random Code 93 Extended barcode value.

    Returns:
        str: The generated Code 93 Extended barcode value.
    """
    # Code 93 Extended characters
    code93_extended_chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

    # Generate random barcode value
    barcode_length = random.randint(5, 6)  # Random length for the barcode value
    barcode_value = ''.join(random.choices(code93_extended_chars, k=barcode_length))

    # Calculate the check digits
    def calculate_check_digits(barcode):
        weights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        checksum1 = sum(weights[i] * (code93_extended_chars.index(char) + 1) for i, char in enumerate(barcode)) % 47
        checksum2 = sum(
            weights[i + 1] * (code93_extended_chars.index(char) + 1) for i, char in enumerate(barcode)) % 47
        return code93_extended_chars[checksum1], code93_extended_chars[checksum2]

    # Construct the full Code 93 Extended barcode value with start and stop characters
    checksum1, checksum2 = calculate_check_digits(barcode_value)
    code93_extended_value = barcode_value + checksum1 + checksum2

    return code93_extended_value


def generate_fim_value(self):
    """
    Generate a random FIM (Facing Identification Mark) barcode value.

    Returns:
        str: The generated FIM barcode value.
    """
    # FIM characters: A, D, or T
    fim_chars = 'ADT'

    # FIM patterns
    fim_patterns = {
        'A': ['A', 'D', 'A', 'D'],
        'D': ['D', 'A', 'D', 'A'],
        'T': ['D', 'D', 'A', 'A']
    }

    # Randomly choose a FIM type
    fim_type = random.choice(fim_chars)

    # Generate FIM barcode value based on the selected type
    fim_value = ''.join(random.choice(fim_patterns[fim_type]))

    return fim_value


def generate_isbn_value(self):
    """
    Generate a random ISBN (International Standard Book Number) barcode value.

    Returns:
        str: The generated ISBN barcode value.
    """
    # Fixed three-digit country code of 978
    country_code = '978'

    # Generate 9-digit ISBN number
    isbn_number = ''.join(random.choices('0123456789', k=9))

    # Calculate the check digit
    def calculate_check_digit(isbn):
        sum = 0
        for i in range(len(isbn)):
            digit = int(isbn[i])
            if i % 2 == 0:  # Even position
                sum += digit
            else:  # Odd position
                sum += digit * 3
        return str((10 - (sum % 10)) % 10)

    check_digit = calculate_check_digit(country_code + isbn_number)
    # Combine country code, ISBN number, and check digit
    isbn_barcode_value = country_code + isbn_number + check_digit

    return isbn_barcode_value


def generate_i2of5_value(self):
    # Interleaved 2 of 5 consists of even number of digits
    return ''.join(random.choices('02468', k=10))


def generate_msi_value(self):
    # MSI (Modified Plessey) consists of 10 digits
    return ''.join(random.choices('0123456789', k=10))


def generate_postnet_value(self):
    # POSTNET (Postal Numeric Encoding Technique) consists of 10 digits
    return ''.join(random.choices('0123456789', k=11))


def generate_upca_value(self):
    # UPC-A consists of 12 digits
    return ''.join(random.choices('0123456789', k=12))


def generate_usps_4state_value(self):
    """
    Generate a random USPS 4-State barcode value.

    Returns:
        str: The generated USPS 4-State barcode value.
    """
    # Generate random digits for the barcode value
    barcode_value = ''.join(random.choices('0123456789', k=11))  # 11-digit ZIP code
    # Ensure the sequence number is 9 digits long
    sequence_number = ''.join(random.choices('0123456789', k=9))

    # Calculate check digit
    def calculate_check_digit(value):
        total = sum(int(digit) for digit in value)
        return str((10 - (total % 10)) % 10)

    check_digit = calculate_check_digit(barcode_value + sequence_number)

    # Construct the USPS 4-State barcode value
    usps_4state_value = '0' + barcode_value + sequence_number + check_digit
    return usps_4state_value