# coding: utf-8
from __future__ import annotations

__all__ = ["GadaTestCase"]
import sys
from typing import Any
import unittest


class GadaTestCase(unittest.TestCase):
    def _check_len(self, array: Any, value: int) -> None:
        self.assertEqual(len(array), value, "length should be {}".format(value))

    def _check_index(self, io: binaryiotools.IO, value: int) -> None:
        self.assertEqual(io.index, value, "index should be {}".format(value))

    def _create_io(
        self, *, data: Any = None, littleEndian: bool = False, boolSize: int = 8
    ) -> binaryiotools.IO:
        """Create a **new binaryiotools.IO** and check initial state.

        :return: new binaryiotools.IO
        """
        io = binaryiotools.IO(data=data, littleEndian=littleEndian, boolSize=boolSize)
        self._check_len(io, len(data) if data is not None else 0)
        self._check_index(io, 0)

        return io

    def test_write_byte(self):
        """Test writing and reading a single byte."""
        io = self._create_io()

        # Write one byte
        io.byte = 1
        self._check_len(io, 1)
        self._check_index(io, 1)

        # Access byte by index
        self.assertEqual(io[0], 1, "incorrect value")

        # Rewind and read one byte
        io.index = 0
        self._check_index(io, 0)
        self.assertEqual(io.byte, 1, "incorrect value")
        self._check_index(io, 1)

    def test_context(self):
        """Test using beginContext and endContext."""
        io = self._create_io()

        # Begin a context at current index
        io.beginContext(0)
        self._check_index(io, 0)

        # Write one byte
        io.byte = 1
        self._check_index(io, 1)

        # End context to reset index position
        io.endContext()
        self._check_index(io, 0)

        # Read one byte
        self.assertEqual(io.byte, 1, "incorrect value")
        self._check_index(io, 1)

    def test_get_data(self):
        """Test getting data buffer."""
        io = self._create_io()

        # Check buffer is empty
        data = io.data
        self._check_len(data, 0)

        # Write byte 1 via IO
        io.byte = 1
        self._check_len(io, 1)
        self._check_len(data, 1)

        # Read byte 1 via buffer
        self.assertEqual(data[0], 1, "incorrect value")

        # Write byte 2 via buffer
        data[0] = bytes([2])[0]

        # Read byte 2 via buffer
        io.index = 0
        self.assertEqual(io.byte, 2, "incorrect value")

    def test_set_data(self):
        """Test setting data buffer."""
        io = self._create_io()

        # Invalid because it requires a bytes array
        with self.assertRaises(Exception):
            io.data = 1

        # Set data buffer manually
        io.data = bytes([1, 2])
        io.index = 0
        data = io.data
        self._check_len(io, 2)
        self._check_len(data, 2)

        # Read content
        self.assertEqual(io.byte, 1, "incorrect value")
        self.assertEqual(io.byte, 2, "incorrect value")

    def test_boolean(self):
        """Test reading/writing booleans of various size."""

        def check_boolean(size: int):
            io = self._create_io(boolSize=size)

            io.boolean = True
            io.boolean = False

            io.index = 0
            self.assertEqual(io.boolean, True, "incorrect value")
            self.assertEqual(io.boolean, False, "incorrect value")

        check_boolean(8)
        check_boolean(16)
        check_boolean(32)
        check_boolean(64)

        # Invalid boolean size
        io = self._create_io(boolSize=128)

        # Can't write boolean with invalid size
        with self.assertRaises(Exception):
            io.boolean = True

        # Can't read boolean with invalid size
        with self.assertRaises(Exception):
            b = io.boolean

    def test_get_bytes(self):
        """Test the bytes methods."""
        io = self._create_io()

        # Write some bytes
        io.byte = 1
        io.byte = 2

        # Read bytes
        io.index = 0
        buffer = io.getBytes(len(io))
        self._check_len(buffer, 2)
        self.assertEqual(buffer, bytes([1, 2]), "incorrect value")

    def test_add_bytes_array(self):
        """Test addBytes with a bytes array."""
        io = self._create_io()

        # Write some bytes
        io.addBytes([1, 2])
        io.setBytes([3, 4])

        # Read bytes
        io.index = 0
        buffer = io.getBytes(len(io))
        self._check_len(buffer, 4)
        self.assertEqual(buffer, bytes([1, 2, 3, 4]), "incorrect value")

    def test_add_bytes_io(self):
        """Test addBytes with another **binaryiotools.IO** instance."""
        io = self._create_io()

        # Write some bytes from another binaryiotools.IO instance
        io2 = self._create_io(data=bytes([1, 2]))
        io.addBytes(io2)

        # Read bytes
        io.index = 0
        buffer = io.getBytes(len(io))
        self._check_len(buffer, 2)
        self.assertEqual(buffer, bytes([1, 2]), "incorrect value")

    def test_add_bytes_str(self):
        """Test addBytes with a string."""
        io = self._create_io()

        # Write some bytes from string
        io.addBytes("hello")

        # Read bytes
        io.index = 0
        buffer = io.getBytes(len(io))
        self._check_len(buffer, 5)
        self.assertEqual(buffer, "hello".encode("utf8"), "incorrect value")

        # Override a part
        io.index = 4
        io.addBytes("o_world")

        # Read bytes
        io.index = 0
        buffer = io.getBytes(len(io))
        self._check_len(buffer, 11)
        self.assertEqual(buffer, "hello_world".encode("utf8"), "incorrect value")

    def test_write_data(self):
        """Test writing and reading data"""

        def exactly_equal(a, b):
            self.assertEqual(a, b, "incorrect value")

        def float_equal(eps):
            def wrap(a, b):
                self.assertTrue(abs(a - b) <= eps, "incorrect value")

            return wrap

        def check_method(name, value, binary, littleEndian, test=exactly_equal):
            io = self._create_io(littleEndian=littleEndian)

            # Try write a value
            setattr(io, name, value)
            print(io.data)
            self._check_len(io, len(binary))
            self._check_index(io, len(io))
            self.assertEqual(io.data, binary, "incorrect binary representation")

            # Try read the same value
            io.index = 0
            test(getattr(io, name), value)
            self._check_index(io, len(binary))

        # There is two naming for each data type word <=> i16
        for _ in (
            ("byte", "i8", -128, b"\x80", b"\x80"),
            ("unsignedByte", "u8", 255, b"\xff", b"\xff"),
            ("word", "i16", -32768, b"\x00\x80", b"\x80\x00"),
            ("unsignedWord", "u16", 65280, b"\x00\xff", b"\xff\x00"),
            ("dword", "i32", -2147483648, b"\x00\x00\x00\x80", b"\x80\x00\x00\x00"),
            (
                "unsignedDword",
                "u32",
                4278190080,
                b"\x00\x00\x00\xff",
                b"\xff\x00\x00\x00",
            ),
            (
                "qword",
                "i64",
                -9223372036854775808,
                b"\x00\x00\x00\x00\x00\x00\x00\x80",
                b"\x80\x00\x00\x00\x00\x00\x00\x00",
            ),
            (
                "unsignedQword",
                "u64",
                18374686479671623680,
                b"\x00\x00\x00\x00\x00\x00\x00\xff",
                b"\xff\x00\x00\x00\x00\x00\x00\x00",
            ),
        ):
            # First naming
            check_method(name=_[0], value=_[2], binary=_[3], littleEndian=True)
            check_method(name=_[0], value=_[2], binary=_[4], littleEndian=False)
            # Second naming
            check_method(name=_[1], value=_[2], binary=_[3], littleEndian=True)
            check_method(name=_[1], value=_[2], binary=_[4], littleEndian=False)

        # For float we need to check if values are almost equal
        check_method(
            "floating",
            3.40282346639e38,
            b"\xff\xff\x7f\x7f",
            True,
            float_equal(0.00001e38),
        )
        check_method(
            "floating",
            3.40282346639e38,
            b"\x7f\x7f\xff\xff",
            False,
            float_equal(0.00001e38),
        )
        check_method(
            "double",
            1.7976931348623157e308,
            b"\xff\xff\xff\xff\xff\xff\xef\x7f",
            True,
            float_equal(0.00001e38),
        )
        check_method(
            "double",
            1.7976931348623157e308,
            b"\x7f\xef\xff\xff\xff\xff\xff\xff",
            False,
            float_equal(0.00001e38),
        )

        check_method("sz754", "hello", b"\x05\x00\x00\x00hello\x00", True)
        check_method("sz754", "hello", b"\x00\x00\x00\x05hello\x00", False)

        # cString methods
        for _ in ["cString", "cStringA", "cStringU"]:
            check_method(_, "hello", b"hello\x00", False)

        # textLine methods
        for _ in ["textLine", "textLineA", "textLineU"]:
            check_method(_, "hello", b"hello\n", False)

    def test_sz754(self):
        """Test reading/writing sz754."""
        io = self._create_io()

        # Write hello => b'\x00\x00\x00\x05hello\x00'
        io.sz754 = "hello"
        self._check_len(io, 10)
        self._check_index(io, 10)

        # Write world => b'\x00\x00\x00\x05world\x00'
        io.sz754 = "world"
        self._check_len(io, 20)
        self._check_index(io, 20)

        # Read hello
        io.index = 0
        self.assertEqual(io.sz754, "hello", "incorrect value")
        self._check_index(io, 10)

        # Read world
        self.assertEqual(io.sz754, "world", "incorrect value")
        self._check_index(io, 20)


if __name__ == "__main__":
    unittest.main()
