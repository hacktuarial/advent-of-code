from dataclasses import dataclass
from typing import List
from functools import reduce


def binary_to_int(binary: str) -> int:
    n = len(binary)
    return sum([int(b) * 2 ** (n - i - 1) for i, b in enumerate(binary)])


def hexadecimal_to_binary(hexa: str) -> str:
    # ignore trailing 0s
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


class Packet:
    pass


@dataclass
class LiteralPacket(Packet):
    version: int
    type_id: int
    value: int


@dataclass
class Operator(Packet):
    version: int
    type_id: int
    length_type_id: int
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


def parse_packets(string: str, packets: List) -> str:
    if len(string) == 0 or set(string) == {"0"}:
        return packets
    left, right = 0, 3
    version: int = binary_to_int(string[left:right])
    left, right = left + 3, right + 3
    type_id: int = binary_to_int(string[left:right])
    # right = right + 3
    if type_id == 4:
        # it's a literal-value packet
        value = ""
        while string[right] == "1":
            value += string[right + 1 : right + 5]
            right += 5
        # add the last one
        value += string[right + 1 : right + 5]
        right += 5
        value = binary_to_int(value)
        packet = LiteralPacket(version=version, type_id=type_id, value=value)
        packets.append(packet)
        return parse_packets(string[right:], packets)
    else:
        # it's an operator
        length_type_id = int(string[left])
        my_packets = []
        if length_type_id == 0:
            # then the next 15 bits are a number that represents the total length in bits of the sub-packets contained by this packet.
            right = left + 15
            n_bits = binary_to_int(string[left:right])
            left, right = right, right + n_bits
            # add these packets to this Operator packet
            parse_packets(string[left:right], my_packets)
            packet = Operator(
                version=version,
                type_id=type_id,
                length_type_id=length_type_id,
                packets=my_packets,
            )
            packets.append(packet)
            return parse_packets(string[right + n_bits :], packets)
        else:
            # then the next 11 bits are a number that represents the number of sub-packets immediately contained by this packet.
            right = left + 11
            n_packets = binary_to_int(string[left:right])
            while len(my_packets) < n_packets:
                string = parse_packets(string, my_packets)
            packet = Operator(
                version=version,
                type_id=type_id,
                length_type_id=length_type_id,
                packets=my_packets,
            )
            packets.append(packet)
            return parse_packets(string, packets)


def test_packet():
    hexadecimal = "D2FE28"
    expected = [
        LiteralPacket(version=6, type_id=4, value=2021),
    ]
    actual = []
    parse_packets(hexadecimal_to_binary(hexadecimal), actual)
    assert actual == expected, actual

    packets = []
    actual = parse_packets("110100010100101001000100100", packets)
    assert packets == [LiteralPacket(6, 4, 10), LiteralPacket(2, 4, 20)]


def test_operator():
    packets = []
    actual = parse_packets(hexadecimal_to_binary("38006F45291200"), packets)
    assert actual.version == 1
    assert actual.type_id == 6
    assert actual.length_type_id == 0
    assert len(actual.packets) == 2
    assert actual.packets[0].value == 10
    assert actual.packets[1].value == 20

    actual = parse_packets(hexadecimal_to_binary("EE00D40C823060"))
    assert [packet.value for packet in actual.packets] == [1, 2, 3]

    actual = parse_packets(hexadecimal_to_binary("8A004A801A8002F478"))
    assert actual.version == 4


def part1():
    string = """420D610055D273AF1630010092019207300B278BE5932551E703E608400C335003900AF0402905009923003880856201E95C00B60198D400B50034400E20101DC00E10024C00F1003C400B000212697140249D049F0F8952A8C6009780272D5D074B5741F3F37730056C0149658965E9AED7CA8401A5CC45BB801F0999FFFEEE0D67050C010C0036278A62D4D737F359993398027800BECFD8467E3109945C1008210C9C442690A6F719C48A351006E9359C1C5003E739087E80F27EC29A0030322BD2553983D272C67508E5C0804639D4BD004C401B8B918E3600021D1061D47A30053801C89EF2C4CCFF39204C53C212DABED04C015983A9766200ACE7F95C80D802B2F3499E5A700267838803029FC56203A009CE134C773A2D3005A77F4EDC6B401600043A35C56840200F4668A71580043D92D5A02535BAF7F9A89CF97C9F59A4F02C400C249A8CF1A49331004CDA00ACA46517E8732E8D2DB90F3005E92362194EF5E630CA5E5EEAD1803E200CC228E70700010A89D0BE3A08033146164177005A5AEEB1DA463BDC667600189C9F53A6FF6D6677954B27745CA00BCAE53A6EEDC60074C920001B93CFB05140289E8FA4812E071EE447218CBE1AA149008DBA00A497F9486262325FE521898BC9669B382015365715953C5FC01AA8002111721D4221007E13C448BA600B4F77F694CE6C01393519CE474D46009D802C00085C578A71E4001098F518639CC301802B400E7CDDF4B525C8E9CA2188032600E44B8F1094C0198CB16A29180351EA1DC3091F47A5CA0054C4234BDBC2F338A77B84F201232C01700042A0DC7A8A0200CC578B10A65A000601048B24B25C56995A30056C013927D927C91AB43005D127FDC610EF55273F76C96641002A4F0F8C01CCC579A8D68E52587F982996F537D600"""
    binary = hexadecimal_to_binary(string)
    raise ValueError(binary[:15])
    packets = parse_packets(binary)
    print(packets)


test_packet()
test_operator()
part1()
