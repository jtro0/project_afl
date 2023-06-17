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

def get_bitmap_offset(func):
	highfunc = func_to_highfunc(func)

	firstBB = highfunc.getBasicBlocks()[0]

	for op in firstBB.getIterator():
		if op.opcode == op.PTRADD:
			op_arg0_addr = op.getInput(0).getAddress()

			if currentProgram.getSymbolTable().getGlobalSymbol("__afl_area_ptr", op_arg0_addr):
				return op.getInput(1).getOffset()

	#assert "Couldnt find __afl_area_ptr in first basic block" == False

	return None

def get_bitmap_offsets():
	bitmap_offsets = []

	for f in currentProgram.getFunctionManager().getFunctionsNoStubs(False):
		#print(f)
		if not f.isThunk():
			func_name = f.getName()

			if func_name[0:len("__afl")] != "__afl" and func_name[0:len("__sanitizer")] != "__sanitizer":
				#print(func_name)

				bitmap_offset = get_bitmap_offset(f)

				if bitmap_offset != None:
					bitmap_offsets.append((f, bitmap_offset))

	return bitmap_offsets

def get_callers_with_bitmap_offsets_and_weights_recursive(func, weight, depth=0, max_depth=10):
	if depth >= max_depth:
		return []

	callers = []

	for caller in func.getCallingFunctions(None):
		caller_tuple = get_callers_with_bitmap_offsets_and_weights_recursive(caller, weight/2, depth=depth+1, max_depth=max_depth)

		callers.append(caller_tuple)

	return (func, get_bitmap_offset(func), weight, callers)

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
	"""
	This function handles duplicate functions.

	It also removes functions for which bitmap offset is None 

	For example lets say we want to reach functions B and C and both of them are called from A,
	then we speculate that A must be an interesting function to reach as it can reach both B and C.
	A will also by the logic of our tool be a duplicate in the list of functions that are interesting.

	Thus in this function we will check for duplicate functions, make sure they have the same bitmap offset,
	and merge them to have a higher weight.

	"""

	# TODO : This function seems a bit ugly / inefficient. However does it really matter as this tool is only executed once when preparing the target program for fuzzing.s

	seen = {} # Key: bitmap_offset ; Value: (func, weight) ; NOTE bitmap_offset is the key as we want to make sure this is unique
	result = []

	for t in x:
		func = t[0]
		bitmap_offset = t[1]
		weight = t[2]

		#print(t)

		if bitmap_offset == None:
			continue

		if bitmap_offset in seen:
			assert seen[bitmap_offset][0] == func

			seen[bitmap_offset] = (seen[bitmap_offset][0], seen[bitmap_offset][1] + weight) # TODO : maybe do something else than the sum
		else:
			seen[bitmap_offset] = (func, weight)

	for bo in seen:
		result.append((seen[bo][0], bo, seen[bo][1])) # Is there a better way to do this?

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
		weight = input_format[func_name]

		f_bitmap_weight_caller_tuple = get_callers_with_bitmap_offsets_and_weights_recursive(func, weight)

		pre_result += unroll_func_weight_bitmap_caller_tuple_recursive(f_bitmap_weight_caller_tuple)

	result = handle_duplicate_func_bitmap_weight_tuples(pre_result)

	return result

#print(get_bitmap_offsets())
