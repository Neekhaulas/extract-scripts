#!/usr/bin/env python

import binascii
import sys
import blowfish


DLL_HEADER_SIZE = 0x400


def decrypt(input_file, output_file):
	with open(input_file, "rb") as f:
		buf = f.read()

	if buf[0x80:0x84] == b"PE\0\0":
		print("File is not encrypted")
		write_decrypted_output(buf, output_file)
		return False

	print("Decrypting %r" % (input_file))

	key_offset = len(buf) - 0x38 - 5
	key = buf[key_offset:-5]
	print("Key:", binascii.hexlify(key))

	encrypted = buf[DLL_HEADER_SIZE:key_offset]

	cipher = blowfish.Cipher(key)
	decrypted = b"".join(cipher.decrypt_ecb(encrypted))
	clear_header = buf[:DLL_HEADER_SIZE]

	write_decrypted_output(clear_header + decrypted, output_file)

	return True


def write_decrypted_output(output, output_file):
	with open(output_file, "wb") as f:
		f.write(output)

		f.seek(0x80)
		f.write(b"PE\0\0")

	print("Written to %r" % (output_file))


def main():
	decrypt(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
	main()
