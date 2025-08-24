# notes

here you can read natalie's autistic ramblings about implementing a RISC-V emulator in RIC.

**you will need to be familiar with the RISC-V ISA or something similar to understand most of this. you have been warned.**

## overview

the basic flow of the program is as follows:

- `rv.init` initializes the registers, pc and memory.
- `rv.exec` reads and executes the next instruction.

### variables

binary data is stored as continuous hex strings, so 2 characters are needed for 1 byte.

- `x`: registers, including x0. see [registers.msw](src/registers.msw).
- `mem.*`: 32K-long "pages" of memory. this "paging" exists to avoid running into the 64K variable size limit. they're not memory pages in the real sense. see [memory.msw](src/memory.msw)
- `cache.*`: 64 byte-long cache lines.

## memory cache

writing to memory is very expensive. due to the way RIC works, you can't set a substring in a variable. if you want to write to a piece of memory, you need to copy the entire thing and write it back in with the relevant bytes replaced. for example, with a 64K-long memory chunk variable, it can take up to **100ms to store a single word**.

an obvious fix is to split the memory up into chunks smaller than 64K. the problem is that they need to be smaller than 4K or so for this to be effective. since the chunks need to be stored tightly for , this doesn't scale well

to evade writing to the main memory too often, a system of cache lines is used. (hardware people will probably find this familiar.) these are temporary 64-byte buffers (`cache.*`) that the CPU reads/writes instead of the main memory. the emulator allocates up to 128 cache lines at a time. when it can't allocate any more, it flushes the oldest one that was allocated and discards it.

it's a half-assed imitation of real hardware, but it works. after adding this, a ~512-byte memset went from 7s down to 200ms.