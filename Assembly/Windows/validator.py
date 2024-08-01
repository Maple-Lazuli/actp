import re
import sys
import os
import argparse

lab_start_tag = re.compile("GLOBAL _lab(\d+)_(\d+)")
code_start_tag = re.compile(";+ YOUR CODE BELOW")
code_end_tag = re.compile(";+ YOUR CODE ABOVE")
lab_end_tag = re.compile("_labSize(\d+)_(\d+) dd")

opcode_list = ["int3", "mov", "add", "extern"]		# default acceptables opcodes
load_store = ["lodsb", "lodsw", "lodsd", "lodsq", \
			  "stosb", "stosw", "stosd", "stosq"]
def add_opcodes(level, lab, valid_opcodes):
	"""Build the list of valid opcodes based on the level and lab number"""
	if (level == 1 and lab == 3):
		valid_opcodes.append("xchg")
	elif (level == 2 and lab == 1):
		valid_opcodes.extend(["cmp", "jmp", "je", "jz", "jne", "jnz"])
	elif (level == 3 and lab == 1):
		valid_opcodes.extend(["shl", "shr", "ror", "rol", "movzx", "inc", "dec", "sub", "xor", \
							  "loop", "loope", "loopz", "loopne", "loopnz"])
	elif (level == 4 and lab == 1): 
		valid_opcodes.append("lea")
	elif (level == 5 and lab == 1):
		valid_opcodes.extend(["pop", "push", "popad", "pushad"])
	elif (level == 6 and lab == 1):
		valid_opcodes.extend(["call", "ret"])
	elif (level == 6 and lab == 5):
		valid_opcodes.extend(["db"])
	elif (level == 7 and lab == 1):
		valid_opcodes.extend(["resb", "resd", "resw", "struc", "endstruc"])
		valid_opcodes.remove("db") # needed for the printf bonus lab but not after
	elif (level == 7 and lab == 3):
		valid_opcodes.extend(["enter", "leave"])
	elif (level == 8 and lab == 1):
		valid_opcodes.extend([	"cmpsb", "cmpsw", "cmpsd", "cmpsq", \
								"scasb", "scasw", "scasd", "scasq", \
								"std", "cld"])
		valid_opcodes.extend(load_store)
	elif (level == 8 and lab == 2):
		valid_opcodes.extend(["rep", "repe", "repz", "repne", "repnz", \
							  "movsb", "movsw", "movsd", "movsq"])
		for op in load_store:
			valid_opcodes.remove(op)
	elif (level == 8 and lab == 3):
		valid_opcodes.extend(load_store)
	elif (level == 9 and lab == 1):
		valid_opcodes.extend(["and", "or", "test", "neg", \
								"popf", "pushf", "stc", "clc", "cmc", "movsx", \
								"jg", "jnle", "jge", "jnl", "jl", "jnge", "jle", "jng", "jecxz" \
								"ja", "jae", "jb", "jbe"])
	elif (level == 10 and lab == 1):
		valid_opcodes.extend(["bswap", "xadd", "cmpxchg", "imul", "mul", "idiv", "div", "adc", "sbb", "not", \
								"cmovg", "cmovnle", "cmovge", "cmovnl", "cmovl", "cmovnge", "cmovle", "cmovng", \
								"setg", "setnle", "setge", "setnl", "setl", "setnge", "setle", "setng", "setc", \
								"bt", "bts", "btr", "btc", "jc", "jnc", "loopz", "loope", "loopnz", "loopne", \
								"int", "iret", "nop", "ud2"])
								
def validate_registers(invalid_registers, line, line_no):
	"""Ensure the code uses only the allowed registers"""
	words = line.split()
	if len(words) > 1:
		operands = words[1].split(",")
		for operand in operands:
			if operand in invalid_registers:
				print("[!] %s is a forbidden register (line %d)" % (operand, line_no))
				return False
	return True
	
def validate(valid_opcodes, line,  level, lab, line_no):
	"""Determine if the op code on 'line' is within the list of 'valid opcodes'"""
	if valid_opcodes == None:		# do not validate
		return True
	if not line.startswith(";") and not line.startswith(".") \
			and not line.startswith("%") and not ":" in line:			# ignore comments, labels, and defines
		words = line.split()
		if len(words) > 0 and words[0] not in valid_opcodes:
				print("[!] %s not a valid opcode (line %d)" % (words[0], line_no))
				return False
		
		if level == 6 and lab == 1:
			return validate_registers(["ebp", "esi", "edi"], line, line_no)
		elif level == 7 and lab == 3:
			return validate_registers(["ebx", "esi", "edi"], line, line_no)
	return True
	
	
def parse_nasm(file_path):
	"""Read and validate the nasm file"""
	global opcode_list
	code_validates = True
	lab_validates = True
	validate_line = False
	line_no = 0
	valid_opcodes_list = opcode_list
	with open(file_path) as fh:
		for line in fh.readlines():
			line_no += 1
			if validate_line:
				if not validate(valid_opcodes_list, line.lower().strip(), level, lab, line_no):
					lab_validates = False
					code_validates = False
			match = lab_start_tag.match(line)
			if match:
				level = int(match.group(1))
				lab =  int(match.group(2))
				#print("Validating lab %d %d" % (level, lab))
				add_opcodes(int(level), int(lab), opcode_list)
				# some labs have specific opcodes to use
				if level == 0:			# do not validate level 0 labs
					valid_opcodes_list = None
				elif level == 4 and lab == 1:
					valid_opcodes_list += ["mov"]
				elif level == 5 and lab == 1:
					valid_opcodes_list += ["push", "pop"]
				elif level == 5 and lab == 2:
					valid_opcodes_list += ["pushad", "pop"]
				else:
					valid_opcodes_list = opcode_list
			elif code_start_tag.match(line):
				validate_line = True
				lab_validates = True
			elif code_end_tag.match(line):
				validate_line = False
			elif lab_end_tag.match(line):
				if not lab_validates:
					print("[!] lab %d.%d failed validation" % (level, lab))

	return code_validates
	
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Validate nasm files to ensure students are using the correct opcodes.")
	parser.add_argument("-f", "--file", dest="file_path", help="path to nasm file to validate", action="store", 
						default=os.path.join(os.getcwd(),"student.nasm"))
	parser.add_argument("-w", "--warn", dest="warn_only", help="print the warning messages, but always return true", 					action="store_true", default=False)
	args = parser.parse_args()
	
	print("Validating opcodes...")
	if parse_nasm(args.file_path) or args.warn_only:
		print("Opcodes are valid")
		sys.exit(0)
	else:
		sys.exit(1)