import hashlib

def pass_hashing(pwd):
	pwd = pwd.encode()
	h_pass= hashlib.sha512(pwd)
	return h_pass.hexdigest()

def pass_verify(clear_pass, pass_sha512):
	h_pass = pass_hashing(clear_pass)
	if (h_pass == pass_sha512):
		return True
	else:
		return False
