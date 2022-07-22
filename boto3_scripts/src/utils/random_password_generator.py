from random import choice

def generate_password(lenOfPassword=8):
		valid_chars_for_password="abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"

		return "".join(choice(valid_chars_for_password) for _ in range(lenOfPassword))
