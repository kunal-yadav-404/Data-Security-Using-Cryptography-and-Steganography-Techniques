import os
import numpy as np
from imageio import imread, imwrite
from multipledispatch import dispatch


class Stego:
	
	def __init__(self, cover = "lib/images/cover.png"):
		self.img_path = cover
		self.output_path = "lib/output/secured.png"
		self.max_value = 255 # max uint value per pixel per channel
		self.header_len = 4*8 # uint32 bit length
	
	@dispatch(str)
	def stego(self, file_path):
		image, shape_orig = self.read_image(self.img_path)
		file = self.read_file(file_path)
		file_len = file.shape[0]
		len_array = np.array([file_len], dtype=np.uint32).view(np.uint8)
		len_array = np.unpackbits(len_array)
		img_len = image.shape[0]
        
		if file_len >= img_len - self.header_len:  # 4 bytes are used to store file length
			print("File size too large, trying a different cover image...")
			self.img_path = "images/coverLarge.png"
			image, shape_orig = self.read_image(self.img_path)
			img_len = image.shape[0]
			if file_len >= img_len - self.header_len:
				print("File size too large...")
				return
			else:			
				tmp = file
				file = np.random.randint(2, size=img_len, dtype=np.uint8)
				file[self.header_len:self.header_len+file_len] = tmp
		else:
			tmp = file
			file = np.random.randint(2, size=img_len, dtype=np.uint8)
			file[self.header_len:self.header_len+file_len] = tmp
		file[:self.header_len] = len_array
		encoded_data = self.encode_data(image, file)

		self.write_image(self.output_path, encoded_data, shape_orig)
		os.remove(file_path)
		print("File fully secured!!!")
		print(f"Output available at: {self.output_path}")
		self.img_path = "lib/images/cover.png"
		return
	
	@dispatch(str, str)
	def stego(self, f, coverImg):
		self.img_path = coverImg
		self.stego(f)
	
	def unStego(self, stegoImgFile, outputFile):
		img_path = stegoImgFile
		if not os.path.isfile(img_path):
			print("Image file does not exist")
			return
		file_path = outputFile
		encoded_data, shape_orig = self.read_image(img_path)
		data = self.decode_data(encoded_data)
		el_array = np.packbits(data[:self.header_len])
		extracted_len = el_array.view(np.uint32)[0]
		data = data[self.header_len:extracted_len+self.header_len]
		self.write_file(file_path, data)
		print("Stego image Decoded!")
		return

	def read_image(self, img_path):
		img = np.array(imread(img_path), dtype=np.uint8)
		orig_shape = img.shape
		return img.flatten(), orig_shape
	
	def write_image(self, img_path, img_data, shape):
		img_data = np.reshape(img_data, shape)
		imwrite(img_path, img_data)

	def bytes2array(self, byte_data):
		byte_array = np.frombuffer(byte_data, dtype=np.uint8)
		return np.unpackbits(byte_array)

	def array2bytes(self, bit_array):
		byte_array = np.packbits(bit_array)
		return byte_array.tobytes()

	def read_file(self, file_path):
		file_bytes = open(file_path, "rb").read()
		return self.bytes2array(file_bytes)

	def write_file(self, file_path, file_bit_array):
		bytes_data = self.array2bytes(file_bit_array)
		f = open(file_path, 'wb')
		f.write(bytes_data)
		f.close()

	def encode_data(self, image, file_data):
		or_mask = file_data
		and_mask = np.zeros_like(or_mask)
		and_mask = (and_mask + self.max_value - 1) + or_mask 
		res = np.bitwise_or(image, or_mask)
		res = np.bitwise_and(res, and_mask)
		return res

	def decode_data(self, encoded_data):
		out_mask = np.ones_like(encoded_data)
		output = np.bitwise_and(encoded_data, out_mask)
		return output
