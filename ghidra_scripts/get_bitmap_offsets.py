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

def get_highfunc_by_name(name):
	f = getFunction(name)

	results = decompintf.decompileFunction(f, 30, None)
	highfunc = results.getHighFunction()

	return highfunc

def get_bitmap_offset(funcname):
	hf = get_highfunc_by_name(funcname)

	firstBB = hf.getBasicBlocks()[0]

	for op in firstBB.getIterator():
		if op.opcode == op.PTRADD:
			op_arg0_addr = op.getInput(0).getAddress()

			if currentProgram.getSymbolTable().getGlobalSymbol("__afl_area_ptr", op_arg0_addr):
				return op.getInput(1).getOffset()

	#assert "Couldnt find __afl_area_ptr in first basic block" == False

	return None

def get_bitmap_offsets(funcnames):
	result = []

	for name in funcnames:
		bitmap_offset = get_bitmap_offset(name)

		if bitmap_offset != None:
			result.append((name, get_bitmap_offset(name)))

	return result

bitmap_offsets = []

for f in currentProgram.getFunctionManager().getFunctionsNoStubs(False):
	print(f)
	if not f.isThunk():
		func_name = f.getName()

		if func_name[0:len("__afl")] != "__afl" and func_name[0:len("__sanitizer")] != "__sanitizer":
			print(func_name)

			bitmap_offset = get_bitmap_offset(func_name)

			if bitmap_offset != None:
				bitmap_offsets.append((func_name, bitmap_offset))

print(bitmap_offsets)

# execfile("C:\\Users\\mans\\Desktop\\uni\\PST-FUZZ\\ghidra_scripts\\get_bitmap_offsets.py")
