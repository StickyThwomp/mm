#!/usr/bin/env python3
#
#   Message Table Parser
#
import argparse
from typing import Optional
import os
import struct

script_dir = os.path.dirname(os.path.realpath(__file__))
repo = os.path.join(script_dir, "..", "..")


class Message:
    """Message data
    
    Format TBD, but there's a pre-amble, the message itself (mostly ascii), 
    and '\xbf' identifies the end.
    
    """
    MSG_END = b'\xbf'

    def __init__(self, data: bytearray):
        self.data = data
    
    def dump(self, width: int=16):
        """Print HEX bytes and string representation to console."""
        remainder = self.data
        while len(remainder) > 0:
            line, remainder = remainder[:width], remainder[width:]
            bytedump = " ".join(f"{char:02X}" for char in line)
            asciidump = "".join(f"{chr(char) if (32 <= char <= 127) else '.'}" for char in line)
            print(f"  {bytedump:{3*width}} | {asciidump}")

    @property
    def size(self)->int:
        return len(self.data)
    
    def __repr__(self)->str:
        return f"Message({self.data})"


class MessageTableEntry:
    """Entry in the Message Table.

    Consists of an ID, a Position, and a segment pointer identifying the message itself.
    Note, text_ids are NOT indexes in the table.

    """
    def __init__(self, text_id: int, typepos: int, psegment: int):
        self.text_id = text_id
        self.typepos = typepos
        self.psegment = psegment
        self._message = None  # type: Optional[bytearray]

    @property
    def message(self):
        if self._message is None:
            with open(os.path.join("baserom", "message_data_static"), 'rb') as f:
                f.seek(self.psegment & ~0x0F000000)
                data = bytearray()
                ch = None
                while ch != Message.MSG_END:
                    ch = f.read(1)
                    data += ch
            self._message = Message(data)
        return self._message

    def __str__(self):
        return (f"Message Table Entry: TextId: 0x{self.text_id:X}, TypePosition:{self.typepos}, "
                f"Segment: 0x{self.psegment:08X}")

    def __repr__(self):
        return f"MessageTableEntry(0x{self.text_id:X}, {self.typepos}, 0x{self.psegment:08X})"


class MessageTable:
    """Table of MessageTableEntry objects"""
    FMT = ">HBxL"

    def __init__(self, addr, message_table_buffer: bytearray):
        self.addr = addr
        self.entries = [MessageTableEntry(*data) for data in struct.iter_unpack(MessageTable.FMT, message_table_buffer)]
        if len(self.entries) == 0:
            raise ValueError("No entries found")
    
    def __iter__(self):
        for e in self.entries:
            yield e

    def __len__(self):
        return len(self.entries)

    def __getitem__(self, idx):
        return self.entries[idx]

    def summary(self):
        return f"Found {len(self)} entries at 0x{self.addr:08X}..." + "\n  " + "\n  ".join(("0: "+str(self[0]), "1: "+str(self[1]), "...", f"{len(self)-1}: " + str(self[-1])))

    @staticmethod
    def make_from_address(address):
        """Extract the message table (in z_message.data.s) pointed to by the given address"""
        data = bytearray()
        with open(os.path.join(repo, "data", "code", "z_message.data.s"), "r") as f:
            do_capture = False
            for line in f.readlines():
                if f"glabel D_{address:08X}" in line:
                    do_capture = True
                    continue
                if do_capture:
                    if line == "\n":
                        break
                    data.extend(struct.pack(">L", int(line.split("0x")[1].rstrip(),16)))
        return MessageTable(address, data)

    def __str__(self):
        return f"Message Table at 0x{self.addr:08X} containing {len(self)} entries."

    def __repr__(self):
        return f"MessageTable(0x{self.addr:08X}, bytearray(...))"


def get_msgtable(address:str):
    try:
        msg_table = MessageTable.make_from_address(address)
    except ValueError:
        print(f"Error: Unable to parse MessageTable at 0x{address:08X}")
        exit(-1)
    return msg_table

ALL_KNOWN_MESSAGETABLES = (0x801C6B98, 0x801CED40, 0x801CFB08)
def main():
    parser = argparse.ArgumentParser(description="Parses message table")
    parser.add_argument('-a', '--address', help=f"VRAM or ROM address to parse ({', '.join(hex(a) for a in ALL_KNOWN_MESSAGETABLES)})", default=None, type=lambda s : int(s.replace("D_", "0x"), 16))
    parser.add_argument('-id', '--text_id', help="textId to print to the console", default=None, type=lambda s : int(s,0))
    args = parser.parse_args()
    
    # Parse specified table, or all known tables.
    print("Parsing Message Tables...")
    possible_msg_tables = list()
    if args.address is not None:
        possible_msg_tables.append(get_msgtable(args.address))
    else:
        for addr in ALL_KNOWN_MESSAGETABLES:
            possible_msg_tables.append(get_msgtable(addr))
    
    print(f"Message Table Candidates:")
    for msgtbl in possible_msg_tables:
        print(f"  {msgtbl}")
    

    if args.text_id != None:
        found = False
        errors = list()
        print(f"Searching for specified text_id: {args.text_id} (0x{args.text_id:X})...")
        for msg_table in possible_msg_tables:
            try:
                entry = next(filter(lambda x: x.text_id == args.text_id, msg_table))
            except StopIteration:
                errors.append(f"  Error: Unable to find TextId: 0x{args.text_id:X} in MessageTable at 0x{msg_table.addr:08X}")
            else:
                print(f"\n{entry}")
                entry.message.dump()
                found = True
                break;
        if not found:
            for err in errors:
                print(err)
    else:
        print(f"Printing all messages found...")
        for msg_table in possible_msg_tables:
            for entry in msg_table:
                print(f"\n{entry}")
                entry.message.dump()

if __name__ == "__main__":
    main()
