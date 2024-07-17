In addr, r3
in data,r1
OUT addr, r0
out data, r2

halt

swap r0, r2

jc 3

data r0,0x30 
DATA r1, 0b00001111
DaTA r3, 255

dAta r2,0b00001000
  data r3,0xff 

shr R0,R1    
shl   r3,r2
not r3, r0
and r0,R1
or  r2,r1
xor  r2,r1
Add r2,r0

ld r0,r1
st r3,r1

clf     
cmp r1,r2

jmpr r3
jmp  0xf0


ja 0x02
 je 0b00001111
jz    0x01
jca 0x01
jce 0x01
jcz 0x01
jcae 0x10
jcaz 0x10
jcez 0x10
jcaez 0x10
jae 0x02
jaz 0x02
jaez 0x02
jez 0x33

halt 

in data ,r0


clf 