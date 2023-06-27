#!/bin/bash
set -e

##
# Pre-requirements:
# - env FUZZER: path to fuzzer work dir
##

git clone https://github.com/jtro0/project_afl.git "$FUZZER/repo_temp"
# git -C "$FUZZER/repo" checkout 458eb0813a6f7d63eed97f18696bca8274533123
git -C "$FUZZER/repo_temp" checkout test_suite
# git clone
cp -r $FUZZER/repo_temp/AFLplusplus $FUZZER/repo

# Fix: CMake-based build systems fail with duplicate (of main) or undefined references (of LLVMFuzzerTestOneInput)
sed -i '{s/^int main/__attribute__((weak)) &/}' $FUZZER/repo/utils/aflpp_driver/aflpp_driver.c
sed -i '{s/^int LLVMFuzzerTestOneInput/__attribute__((weak)) &/}' $FUZZER/repo/utils/aflpp_driver/aflpp_driver.c
cat >> $FUZZER/repo/utils/aflpp_driver/aflpp_driver.c << EOF
__attribute__((weak))
int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size)
{
  // assert(0 && "LLVMFuzzerTestOneInput should not be implemented in afl_driver");
  return 0;
}
EOF

wget https://github.com/NationalSecurityAgency/ghidra/releases/download/Ghidra_10.3.1_build/ghidra_10.3.1_PUBLIC_20230614.zip -O $FUZZER/ghidra.zip &> /dev/null
unzip $FUZZER/ghidra.zip -d $FUZZER/ghidra &> /dev/null

# patch -p1 -d "$FUZZER/repo" << EOF
# --- a/utils/aflpp_driver/aflpp_driver.c
# +++ b/utils/aflpp_driver/aflpp_driver.c
# @@ -67,7 +67,7 @@
#  // AFL++ shared memory fuzz cases
# -int                   __afl_sharedmem_fuzzing = 1;
# +int                   __afl_sharedmem_fuzzing = 0;
#  extern unsigned int * __afl_fuzz_len;
#  extern unsigned char *__afl_fuzz_ptr;
 
# @@ -107,7 +107,8 @@ 
#  // Notify AFL about persistent mode.
# -static volatile char AFL_PERSISTENT[] = "##SIG_AFL_PERSISTENT##";
# +// DISABLED to avoid afl-showmap misbehavior
# +static volatile char AFL_PERSISTENT[] = "##SIG_AFL_NOT_PERSISTENT##";
#  int                  __afl_persistent_loop(unsigned int);
 
#  // Notify AFL about deferred forkserver.
# EOF
