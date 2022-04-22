from lib.Secure import Secure
import os

sec = Secure()

def main():
	while True:
		inp = int(input("""
1. Secure File
2. Decrypt File
3. Generate RSA Keys
4. Exit
Choice: """))
		
		if inp == 1:
			fName = input('File to be secured: ')
			coverImg = input("Cover image location [default-lib/images/cover.img]: ")
			if coverImg != "":
				if os.path.isfile(coverImg):
					sec.secure_file(fName, coverImg)
				else:
					print(f"Cover Image [{coverImg}] does not exists...")
					sec.secure_file(fName)
			else:
				sec.secure_file(fName)
		elif inp == 2:
			stegoImg = input("Stego image: ")
			fName = input('Output file name [default-lib/output/decrypted.txt]: ')
			if fName == "":
				sec.desecure_file(stegoImg)
			else:
				sec.desecure_file(stegoImg, fName)
		elif inp == 3:
			sec.generate_key()
		elif inp == 4:
			exit()
		else:
			print("Invalid Input...")


if __name__ == "__main__":
	main()
