from io import BufferedReader
import struct


def read_bool(buffer: BufferedReader) -> bool:
    return struct.unpack("<?", buffer.read(1))[0]

def read_ubyte(buffer: BufferedReader) -> int:
    return struct.unpack("<B", buffer.read(1))[0]

def read_ushort(buffer: BufferedReader) -> int:
    return struct.unpack("<H", buffer.read(2))[0]

def read_uint(buffer: BufferedReader) -> int:
    return struct.unpack("<I", buffer.read(4))[0]

def read_float(buffer: BufferedReader) -> float:
    return struct.unpack("<f", buffer.read(4))[0]

def read_double(buffer: BufferedReader) -> float:
    return struct.unpack("<d", buffer.read(8))[0]

def read_ulong(buffer: BufferedReader) -> int:
    return struct.unpack("<Q", buffer.read(8))[0]

def read_string(buffer: BufferedReader) -> str:
    strlen = 0
    strflag = read_ubyte(buffer)
    if (strflag == 0x0b):
        strlen = 0
        shift = 0
        # uleb128
        # https://en.wikipedia.org/wiki/LEB128
        while True:
            byte = read_ubyte(buffer)
            strlen |= ((byte & 0x7F) << shift)
            if (byte & (1 << 7)) == 0:
                break
            shift += 7
    return (struct.unpack("<" + str(strlen) + "s", buffer.read(strlen))[0]).decode("utf-8")

def read_int_double(buffer: BufferedReader):
    read_ubyte(buffer)
    integer = read_uint(buffer)
    read_ubyte(buffer)
    double = read_double(buffer)
    return (integer, double)

def read_int_float(buffer: BufferedReader):
    read_ubyte(buffer)
    integer = read_uint(buffer)
    read_ubyte(buffer)
    double = read_float(buffer)
    return (integer, double)

def read_timing_point(buffer: BufferedReader):
    bpm = read_double(buffer)
    offset = read_double(buffer)
    inherited = read_bool(buffer)
    return (bpm, offset, inherited)
