#!/usr/bin/env python3
import unittest
from math import ceil
from typing import List


class CheckUndiagonalize(unittest.TestCase):
    def test_undiag_1(self) -> None:
        result = undiag("HOREL,OL!LWD", 3)
        self.assertEqual(
            result,
            "Hello,World!".upper()
        )
        print(result)

    def test_undiag_2(self) -> None:
        result = undiag("M NWIT'EOF GHRH AEOEW O RVL HLSH  FO PPNETEEMTESVHBNEBHH1VNILLSEE TOT  TIEE   P   UOA'K.YTA5EATEEI AN BSANHHQVO,GSWNSOY S  - L8LCEM. SMAFSEHIESUENKI HOHIAF EWD,E1 IR  KAHROEUAA  OR CAEA IVGFLHIIR  BR NTOISR SQBTWGD MINTLTPEEOETKACOINYEHAHOLIAES ,PHN,RODTIEA'R  G IIK SA MEMEBO TVIE AAI OB  H HSPBT TPD; AR RIVCLFYWT IAE", 10)
        self.assertEqual(
            result,
            "Moby-Dick; or, The Whale is an 1851 novel by American writer Herman Melville. The book is the sailor Ishmael's narrative of the obsessive quest of Ahab, captain of the whaling ship Pequod, for revenge on Moby Dick, the giant white sperm whale that on the ship's previous voyage bit off Ahab's leg at the knee. Wikipedia".upper()
        )
        print(result)


def calc_row_lens(str_len: int, key: int) -> List[int]:
    """Calculate lengths of each row in `mainArray`
    The `mainArray` repeats horizontally in groups of `2*(key-1)`

    E.g., for `key == 4`: (`x` marks start of repeat)
    ```
    x           x           x           x           x
    ---------------------------------------------------
    A * * * * * G * * * * * M * * * * * S * * * * * Y *
    * B * * * F * H * * * L * N * * * R * T * * * X * Z
    * * C * E * * * I * K * * * O * Q * * * U * W * * *
    * * * D * * * * * J * * * * * P * * * * * V * * * *
    ```

    The length of each row can be calculated as:
        First row   [0]          : ceil(length / group_width)
        Last row    [key-1]      : ceil((length-half_group_width) / group_width)
        Middle rows [1] - [key-2]: More complicated; see implementation

    Args:
        str_len (int): length of the string
        key     (int): height of the matrix

    Returns:
        lengths (list[int]): a list of lengths for each row
    """
    # Width of repeating unit
    half_group_width = key - 1
    group_width = 2 * half_group_width
    # Initialize length list
    lengths = [0 for _ in range(key)]
    # Get first and last lengths
    lengths[0] = ceil(str_len / group_width)
    lengths[-1] = ceil((str_len - half_group_width) / group_width)
    # Width of the last block, which may not be complete
    last_block_width = str_len % group_width
    # Get middle rows' lengths
    for i in range(1, key-1):
        # Get the full blocks first; each block has 2 letters in these rows
        length = str_len // group_width * 2
        # Deal with the last block
        if last_block_width <= half_group_width:
            # Letters going down
            # There's 1 more letter on this row if width is strictly greater
            #   than row number, because the first row is also counted
            length += int(last_block_width > i)
        else:
            # Letters going up
            # There's at least 1 more letter on this row. There's a second
            #   letter if the distance to a full block is strictly smaller
            #   than row number, becuase the first row is not counted
            length += 1 + int(group_width - last_block_width < i)
        # Assign number to list
        lengths[i] = length
    # Check the sum of the lengths is the same as the length of the original
    #   string, just for a good measure
    assert sum(lengths) == str_len, (sum(lengths), str_len)
    return lengths


def split_str_by_len(s: str, lengths: List[int]) -> List[List[str]]:
    """Split the string at given indices
    Note that each slice is reverse for better popping performance

    Args:
        s       (str)      : string to be split
        lengths (List[int]): indices to split at

    Returns:
        s_split (list[list[str]]): split chars
    """
    s_split: List[List[str]] = []
    pointer = 0
    for length in lengths:
        # Here the string is reversed because popping from last element gives
        #   better performance, if the list is very large
        s_split.append(list(s[pointer:pointer+length][::-1]))
        pointer += length
    return s_split


def reconstruct_input(out_split: List[List[str]], str_len: int, key: int) -> str:
    """Construct original string

    Args:
        out_split (list[list[str]]): split chars of output string

    Returns:
        original (str): reconstructed original string
    """
    original: str = ""
    row = 0
    row_direction = 1
    for _ in range(str_len):
        original += out_split[row].pop()
        if row == 0:
            row_direction = 1
        elif row == key - 1:
            row_direction = -1
        row += row_direction
    return original


def undiag(out: str, key: int) -> str:
    # Calculate length of each row in `mainArray`
    # The length of the original string is the same as that of the output
    str_len = len(out)
    lengths = calc_row_lens(str_len, key)
    # Split the string according to the lengths
    out_split = split_str_by_len(out, lengths)
    # Reconstruct the string by zig-zagging
    original = reconstruct_input(out_split, str_len, key)
    return original


if __name__ == "__main__":
    unittest.main(verbosity=2)
