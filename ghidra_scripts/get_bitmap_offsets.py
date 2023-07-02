import ast
# import argparse
import json
import os
import struct
import ast

decompintf = ghidra.app.decompiler.DecompInterface()
decompintf.openProgram(currentProgram)

asm = ghidra.app.plugin.assembler.Assemblers.getAssembler(currentProgram)

num_const_bo = 0
num_var_bo = 0

it = currentProgram.getSymbolTable().getAllSymbols(False)
with open("all_sym.txt", "w") as f:
	for sym in it:
		f.write(str(sym)+'\n')
  
f = open("all_not_found.txt", "w")
fi = open("all_found.txt", "w")
def func_to_highfunc(func):
	results = decompintf.decompileFunction(func, 30, None)
	highfunc = results.getHighFunction()

	return highfunc

def get_highfunc_by_name(name):
	f = getFunction(name)

	return func_to_highfunc(f)

def get_all_bitmap_offsets_for_func(func):
	global num_const_bo
	global num_var_bo

	highfunc = func_to_highfunc(func)

	result = []
	if highfunc == None:
		print("highfunc is none")
		return result

	for bb in highfunc.getBasicBlocks():
		found_var_bitmap_offset = False

		for op in bb.getIterator():
			if op.opcode == op.PTRADD:
				op_arg0_addr = op.getInput(0).getAddress()

				if currentProgram.getSymbolTable().getGlobalSymbol("__afl_area_ptr", op_arg0_addr):
					if op.getInput(1).isConstant():
						num_const_bo += 1
						result.append(op.getInput(1).getOffset())

						if found_var_bitmap_offset:
							print("INTERESTING: variable and constant bitmap offset in same bb. Decrementing num_var_bo")

							num_var_bo -= 1

						break
					elif not found_var_bitmap_offset:
						print("WARNING: variable bitmap offset in bb @ {}".format(op.getParent()))
						num_var_bo += 1
						found_var_bitmap_offset = True

	#assert "Couldnt find __afl_area_ptr in first basic block" == False

	return result

def get_callers_with_bitmap_offsets_and_weights_recursive(func, weight, max_depth, depth=0): #IMPORTANT : we might want to modify the max depth
	if depth >= max_depth or weight == 0:
		return []

	callers = []

	for caller in func.getCallingFunctions(None):
		caller_tuple = get_callers_with_bitmap_offsets_and_weights_recursive(caller, weight/2, max_depth=max_depth, depth=depth+1)

		callers.append(caller_tuple)

	bitmap_offsets = get_all_bitmap_offsets_for_func(func)

	if len(bitmap_offsets) > 0:
		return [func, bitmap_offsets, weight/len(bitmap_offsets), callers]
	else:
		print("bitmap_offsets is 0? " +str(bitmap_offsets))
		return [func, bitmap_offsets, 0, callers]

def unroll_func_weight_bitmap_caller_tuple_recursive(func_tuple):
	result = []

	if func_tuple == None or len(func_tuple) != 4:
		print("WARNING: could not get callers with bitmap offset")
  		print(func_tuple)
		return result

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
		print("handle_duplicate_func_bitmap_weight_tuples {}".format(t))

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

	differing_duplicates = []

	for t in x:
		print("func_bitmap_weight_tuples_to_bitmap_weight_map {}".format(t))
		bitmap_offsets = t[1]
		weight = t[2]

		for o in bitmap_offsets:
			if o in result:
				if result[o] != weight:
					print("WARNING: result[{}] == {} failed ({} != {})".format(o, weight, result[o], weight))
					differing_duplicates.append(o)
			else:
				result[o] = weight

	print("REMOVING DIFFERING DUPLICATES ; # differing duplicates: {} | # total: {}".format(len(differing_duplicates), len(result)))

	for o in differing_duplicates:
		result.pop(o)

	return result

def remove_null_weights(x):
	result = {}

	for o in x:
		if x[o] != 0:
			result[o] = x[o]

	return result

def do_stuff(input_format, max_depth):
	"""
	@param input_format for now is a dictionary with keys being the function names and values being their weights

	@returns list of tuples in format of (func_name, bitmap_offset, weight)
			 where bitmap_offset is unique and no two function names should have the same bitmap offset otherwise we error
	"""

	pre_result = []

	for entry in input_format:
		func_name = entry[0]

		func = getFunction(func_name)

		if func == None:
			print("WARNING: could not find function '{}'".format(func_name))
			f.write(func_name + '\n')
			continue
		else:
			fi.write(func_name+'\n')

		print("FOUND FUNCTION {}".format(func_name))

		weight = entry[1]
		print("weight " + str(weight))

		f_bitmap_weight_caller_tuple = get_callers_with_bitmap_offsets_and_weights_recursive(func, weight, max_depth=max_depth)

		pre_result += unroll_func_weight_bitmap_caller_tuple_recursive(f_bitmap_weight_caller_tuple)
		print("pre-result " + str(pre_result[:1]))
	no_dups = handle_duplicate_func_bitmap_weight_tuples(pre_result)

	result_with_null_weights = func_bitmap_weight_tuples_to_bitmap_weight_map(no_dups)

	result = remove_null_weights(result_with_null_weights)

	return result

def parse_input_file(input_file):
	with open(input_file, "r") as f:
		data = f.read()
		return ast.literal_eval(data)

def output_data_to_binary(output_data):
	result = bytes()

	for bitmap_offset in output_data:
		result += struct.pack("<II", bitmap_offset, output_data[bitmap_offset])

	return result

def dump_output_file(output_data, output_file):
	with open(output_file, "wb") as f:
		print("Dumping bitmap weights: {}".format(output_data))
		f.write(output_data_to_binary(output_data))

def do_all_the_stuff(input_file, output_file, max_depth):
	dump_output_file(do_stuff(parse_input_file(input_file), max_depth), output_file)

args = getScriptArgs()

import sys
print(sys.version)

if len(args) != 3:
    print("Parameters: <weight map input file> <bitmap weight output file> <max depth for function calls>")
    exit(-1)

do_all_the_stuff(args[0], args[1], args[2])

print("num_var_bo: {} | num_const_bo: {}".format(num_var_bo, num_const_bo))