decompintf = ghidra.app.decompiler.DecompInterface()
decompintf.openProgram(currentProgram)

asm = ghidra.app.plugin.assembler.Assemblers.getAssembler(currentProgram)

"""

def get_afl_maybe_log():
	fm = currentProgram.getFunctionManager()
	funcs = fm.getFunctions(True)
	filtered_funcs = filter(lambda f: f.getName() == "__afl_maybe_log", funcs)

	assert len(filtered_funcs) == 1

	return filtered_funcs[0]

#afl_maybe_log_func = get_afl_maybe_log()

#def find_previous_afl_maybe_log_calls(addr): # param 'addr' is the address of the current call to __afl_maybe_log . type(addr) == Address 

#def handle_bb(bb):
#	for op in bb.getIterator():
#		if op.opcode == op.CALL:	

#def handle_highfunc(hf):
#	for bb in hf.getBasicBlocks():
#		handle_bb(bb)
def find_func_by_name(name):
	fm = currentProgram.getFunctionManager()
	funcs = fm.getFunctions(True)
	filtered_funcs = filter(lambda f: f.getName() == name, funcs)

	assert len(filtered_funcs) == 1

	return filtered_funcs[0]

def get_func_possible_bitmap_locations(func):
	firstBB = func.getBasicBlocks()[0]

	for op in firstBB.getIterator():
		print(op)

	return	

"""

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

def do_stuff(input_format):
	"""
	@param input_format for now is a dictionary with keys being the function names and values being their weights

	@returns list of tuples in format of (func_name, bitmap_offset, weight)
			 where bitmap_offset is unique and no two function names should have the same bitmap offset otherwise we error
	"""

	result = []

	for func_name in input_format:
		func = getFunction(func_name)
		weight = input_format[func_name]

		f_bitmap_weight_caller_tuple = get_callers_with_bitmap_offsets_and_weights_recursive(func, weight)

		result += unroll_func_weight_bitmap_caller_tuple_recursive(f_bitmap_weight_caller_tuple)

	# TODO make sure that all tuples with the same function also have the same bitmap offset

	# TODO handle multiple occurences of the same function . e.g. A calls B and A calls C . Do we assign more weight to this function? Average? What is smart?

	

	return result

#print(get_bitmap_offsets())

# execfile("C:\\Users\\mans\\Desktop\\uni\\PST-FUZZ\\ghidra_scripts\\get_bitmap_offsets.py")
