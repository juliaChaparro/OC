endereco | instrucao     | codigo
-------------------------------------
00 01    | data r0, 0x30 | 0x20 0x30
02 03    | data r1, 0x06 | 0x21 0x06
04 05    | data r2, 0xaa | 0x22 0xaa
06 07    | data r3, 0xff | 0x23 0xff
08       | ld r0,r1      | 0x01
09       | st r3,r1      | 0x1d 
0a       | shr r0,r1     | 0x94
0b       | shl r3,r0     | 0xac
0c       | not r2,r3     | 0xb7
0d       | and r1,r2     | 0xc6
0e       | or  r3, r2    | 0xde
0f       | xor r2, r1    | 0xe9
10       | cmp r0, r1    | 0xf1
11       | jmpr r1       | 0x31
12       | jmp 0x34      | 0x40 0x34
13       | jcaez 0x54    | 0x03 0x54
14       | 