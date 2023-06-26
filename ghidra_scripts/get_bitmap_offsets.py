import json
import struct

decompintf = ghidra.app.decompiler.DecompInterface()
decompintf.openProgram(currentProgram)

asm = ghidra.app.plugin.assembler.Assemblers.getAssembler(currentProgram)

def func_to_highfunc(func):
	results = decompintf.decompileFunction(func, 30, None)
	highfunc = results.getHighFunction()

	return highfunc

def get_highfunc_by_name(name):
	f = getFunction(name)

	return func_to_highfunc(f)

def get_bitmap_offset(func): # TODO : change this function to return list of all bitmap offsets in this function
	highfunc = func_to_highfunc(func)

	firstBB = highfunc.getBasicBlocks()[0]

	for op in firstBB.getIterator():
		if op.opcode == op.PTRADD:
			op_arg0_addr = op.getInput(0).getAddress()

			if currentProgram.getSymbolTable().getGlobalSymbol("__afl_area_ptr", op_arg0_addr):
				return op.getInput(1).getOffset()

	#assert "Couldnt find __afl_area_ptr in first basic block" == False

	return None

def get_all_bitmap_offsets_for_func(func):
	highfunc = func_to_highfunc(func)

	result = []

	for bb in highfunc.getBasicBlocks():
		for op in bb.getIterator():
			if op.opcode == op.PTRADD:
				op_arg0_addr = op.getInput(0).getAddress()

				if currentProgram.getSymbolTable().getGlobalSymbol("__afl_area_ptr", op_arg0_addr):
					result.append(op.getInput(1).getOffset())
					break

	#assert "Couldnt find __afl_area_ptr in first basic block" == False

	return result

def get_callers_with_bitmap_offsets_and_weights_recursive(func, weight, depth=0, max_depth=10): #IMPORTANT : we might want to modify the max depth
	if depth >= max_depth:
		return []

	callers = []

	for caller in func.getCallingFunctions(None):
		caller_tuple = get_callers_with_bitmap_offsets_and_weights_recursive(caller, weight/2, depth=depth+1, max_depth=max_depth)

		callers.append(caller_tuple)

	bitmap_offsets = get_all_bitmap_offsets_for_func(func)

	if len(bitmap_offsets) > 0:
		return (func, bitmap_offsets, weight/len(bitmap_offsets), callers)
	else:
		return (func, bitmap_offsets, 0, callers)

def unroll_func_weight_bitmap_caller_tuple_recursive(func_tuple):
	result = []

	func = func_tuple[0]
	bitmap_offset = func_tuple[1]
	weight = func_tuple[2]
	callers = func_tuple[3]

	result.append((func, bitmap_offset, weight))

	for caller_tuple in callers:
		result += unroll_func_weight_bitmap_caller_tuple_recursive(caller_tuple)

	return result

def handle_duplicate_func_bitmap_weight_tuples(x):
	seen = {} # Key : func ; Value : (bitmap_offsets, weight)

	for t in x:
		func = t[0]
		bitmap_offsets = t[1]
		weight = t[2]

		if bitmap_offsets == []:
			continue

		if func in seen:
			assert seen[func][0] == bitmap_offsets

			seen[func] = (bitmap_offsets, seen[func][1] + weight)
		else:
			seen[func] = (bitmap_offsets, weight)

	result = []

	for func in seen:
		result.append((func, seen[func][0], seen[func][1]))

	return result

def func_bitmap_weight_tuples_to_bitmap_weight_map(x):
	result = {}

	for t in x:
		bitmap_offsets = t[1]
		weight = t[2]

		for o in bitmap_offsets:
			if o in result:
				assert result[o] == weight
			else:
				result[o] = weight

	return result

def do_stuff(input_format):
	"""
	@param input_format for now is a dictionary with keys being the function names and values being their weights

	@returns list of tuples in format of (func_name, bitmap_offset, weight)
			 where bitmap_offset is unique and no two function names should have the same bitmap offset otherwise we error
	"""

	pre_result = []

	for func_name in input_format:
		func = getFunction(func_name)

		if func == None:
			print("WARNING: could not find function '{}'".format(func_name))
			continue

		weight = input_format[func_name]

		f_bitmap_weight_caller_tuple = get_callers_with_bitmap_offsets_and_weights_recursive(func, weight)

		pre_result += unroll_func_weight_bitmap_caller_tuple_recursive(f_bitmap_weight_caller_tuple)

	no_dups = handle_duplicate_func_bitmap_weight_tuples(pre_result)

	result = func_bitmap_weight_tuples_to_bitmap_weight_map(no_dups)

	return result

def parse_input_file(input_file):
	with open(input_file, "r") as f:
		return json.load(f)

def output_data_to_binary(output_data):
	result = bytes()

	for bitmap_offset in output_data:
		result += struct.pack("<II", bitmap_offset, output_data[bitmap_offset])

	return result

def dump_output_file(output_data, output_file):
	with open(output_file, "wb") as f:
		print("Dumping bitmap weights: {}".format(output_data))
		f.write(output_data_to_binary(output_data))

def do_all_the_stuff(input_file, output_file):
	dump_output_file(do_stuff(parse_input_file(input_file)), output_file)

args = getScriptArgs()

if len(args) != 2:
    print("Parameters: <weight map input file> <bitmap weight output file>")
    exit(-1)

do_all_the_stuff(args[0], args[1])
