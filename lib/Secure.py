from lib.Crypt import Crypt
from lib.Stego import Stego
from lib.RSA import Rsa
from multipledispatch import dispatch

class Secure:

	def __init__(self):
		self.crypt = Crypt()
		self.stego = Stego()
		self.rs = Rsa()
	
	@dispatch(str)
	def secure_file(self, f):
		f = self.crypt.encrypt_file(f)
		self.stego.stego(f)
	
	@dispatch(str, str)
	def secure_file(self, f, coverImg):
		f = self.crypt.encrypt_file(f)
		self.stego.stego(f, coverImg)
	
	def desecure_file(self, stegoImgFile, outputFile="lib/output/decrypted.txt"):
		outputFile += ".enc"
		self.stego.unStego(stegoImgFile, outputFile)
		self.crypt.decrypt_file(outputFile)
	
	def generate_key(self):
		self.rs.generate_keys()
		
