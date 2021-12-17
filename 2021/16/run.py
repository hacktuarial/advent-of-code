from dataclasses import dataclass
from enum import Enum

def binary_to_int(binary: str) -> int:
    n = len(binary)
    return sum([int(b) * 2 ** (n - i - 1) for i, b in enumerate(binary)])


def hexadecimal_to_binary(hexa: str) -> str:
    # ignore trailing 0s
    hexa = hexa.replace("0", "")
    lookup = dict([
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


def parse_packet(hexa: str):
    binary = hexadecimal_to_binary(hexa)
    version: int = binary_to_int(binary[:3])
    type_id: int = binary_to_int(binary[3:6])
    value = ""
    index = 6
    while binary[index] == "1":
        value = value + binary[index+1 : index+5]
        index += 5
    # add the last one
    value = value + binary[index+1 : index + 5]
    value = binary_to_int(value)
    return Packet(version=version, type_id=type_id, value=value)

def test_packet():
    hexadecimal = "D2FE28"
    expected = Packet(version=6, type_id=4, value=2021)
    actual = parse_packet(hexadecimal)
    assert actual == expected, actual

test_packet()
