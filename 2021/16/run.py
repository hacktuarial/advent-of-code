from dataclasses import dataclass
from typing import List
from functools import reduce


def binary_to_int(binary: str) -> int:
    n = len(binary)
    return sum([int(b) * 2 ** (n - i - 1) for i, b in enumerate(binary)])


def hexadecimal_to_binary(hexa: str) -> str:
    # ignore trailing 0s
    hexa = hexa.replace("0", "")
    lookup = dict(
        [
            ("0", "0000"),
            ("1", "0001"),
            ("2", "0010"),
            ("3", "0011"),
            ("4", "0100"),
            ("5", "0101"),
            ("6", "0110"),
            ("7", "0111"),
            ("8", "1000"),
            ("9", "1001"),
            ("A", "1010"),
            ("B", "1011"),
            ("C", "1100"),
            ("D", "1101"),
            ("E", "1110"),
            ("F", "1111"),
        ]
    )
    return "".join([lookup[c] for c in hexa])


assert hexadecimal_to_binary("D2FE28") == "110100101111111000101000"


@dataclass
class Packet:
    version: int
    type_id: int
    value: int


@dataclass
class Operator:
    packets: List[Packet]


def read_number(string: str) -> (int, str):
    value = ""
    index = 0
    while string[index] == "1":
        value = value + string[index + 1 : index + 5]
        index += 5
    # add the last one
    value = value + string[index + 1 : index + 5]
    return binary_to_int(value), string[index + 5 :]


# assert read_number("11010001010") == 10, read_number("11010001010")
# assert read_number("0101001000100100") == 20
# assert read_numbers("110100010100101001000100100") == [10, 20]
# print(read_numbers("1101000101001010010001001000000000"))
# assert read_numbers("01010000001100100000100011000001100000") == [1, 2, 3]


def parse_packets(binary: str):
    if len(binary) == 0 or set(binary) == {"0"}:
        return []
    version: int = binary_to_int(binary[:3])
    type_id: int = binary_to_int(binary[3:6])
    if type_id == 4:
        # it's a packet
        value, binary = read_number(binary[6:])
        return [Packet(version=version, type_id=type_id, value=value)] + parse_packets(
            binary
        )
    else:
        # it's an operator
        length_type_id = int(binary[3])

        if length_type_id == 0:
            # then the next 15 bits are a number that represents the total length in bits of the sub-packets contained by this packet.
            start_of_packets = 4 + 15
            length_of_many_packets = binary_to_int(binary[4:start_of_packets])
        else:
            # then the next 11 bits are a number that represents the number of sub-packets immediately contained by this packet.
            start_of_packets = 4 + 11
            n_packets = binary_to_int(binary[4:start_of_packets])
        return None


def test_packet():
    hexadecimal = "D2FE28"
    expected = Packet(version=6, type_id=4, value=2021)
    actual = parse_packets(hexadecimal_to_binary(hexadecimal))[0]
    assert actual == expected, actual
    assert parse_packets("11010001010")[0].value == 10


test_packet()
