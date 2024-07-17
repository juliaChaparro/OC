import sys



# dicionario das operaçoes
opereacao = {
    'add': '1000',
    'shr': '1001',
    'shl': '1010',
    'not': '1011',
    'and': '1100',
    'or': '1101',
    'xor': '1110',
    'cmp': '1111',
    'ld': '0000',
    'st': '0001',
    'data': '0010 00',
    'jmpr': '0011 00',
    'jmp': '0100 0000',
    'clf': '0110 0000',
    'in':'0111 0',
    'out': '0111 1',
    'swap' : '',
    'halt': ''
}

#dicionario das operacoes do JCAEZ
jcaez={
    'jc': '0101 1000',
    'ja': '0101 0100',
    'je': '0101 0010',
    'jz': '0101 0001',
    'jca': '0101 1100',
    'jce': '0101 1010',
    'jcz': '0101 1001',
    'jae': '0101 0110',
    'jaz': '0101 0101',
    'jez': '0101 0011',
    'jcae': '0101 1110',
    'jcaz': '0101 1101',
    'jcez': '0101 1011',
    'jaez': '0101 0111',
    'jcaez': '0101 1111'
}

#dicionario dos registrador
register = {
    'r0':'00',
    'r1': '01',
    'r2': '10',
    'r3':'11'
}

#funcao que vai ler e tirar os erros, para ler melhor o programa
def read_source(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return [line.strip().lower() for line in lines if line.strip() and not line.startswith(';')]


#funçao que vai pegar uma linha e dividir em intrucao e operador 
def parse_line(line):
    parts = line.split()
    if len(parts) == 0:
        return None, None
    
    instruction = parts[0].lower()
    operands = []
    
    if len(parts) > 1:
        operands_str = ' '.join(parts[1:])
        operands = [op.strip() for op in operands_str.split(',')]
    
    return instruction, operands


# funçao que pega a intruçao e os operadores e faz o codigo indicado
# tranformando em um codigo binario 
def translate_to_machine_code(lines):
    machine_code = []
    for line in lines:
        instruction, operands = parse_line(line)
        if instruction in opereacao or instruction in jcaez:
            
            if instruction in 'clf':
                machine_code.append(opereacao['clf']) 

            if instruction == 'data':
                if (operands[1].startswith('0x')):
                    N = int(operands[1],16)
                elif(operands[1].startswith('0b')):
                    N = int (operands[1], 2)
                else:
                    N = int(operands[1])
                machine_code.append(opereacao['data']+register[operands[0]])
                machine_code.append(format(N,'08b')) 

            if instruction in ['and','or','xor','cmp','ld','st','not','shl','shr','add']:
                machine_code.append(opereacao[instruction]+register[operands[0]]+register[operands[1]])

            if instruction == 'jmpr':
                machine_code.append(opereacao[instruction]+register[operands[0]])

            if instruction == 'jmp':

                if (operands[0].startswith('0x')):
                    N = int(operands[0],16)
                elif(operands[0].startswith('0b')):
                    N = int (operands[0], 2)
                else:
                    N = int(operands[0])
                machine_code.append(opereacao['jmp'])    
                machine_code.append(format(N, '08b')) 
            
            if instruction in 'in':
                if (operands[0]== 'data'):
                    machine_code.append(opereacao[instruction]+'0'+register[operands[1]])
                elif(operands[0]=='address'):
                    machine_code.append(opereacao[instruction]+'1'+register[operands[1]])

            if instruction in 'out':
                if (operands[0]=='data'):
                    machine_code.append(opereacao[instruction]+'0'+register[operands[1]])
                elif(operands[0]=='address'):
                    machine_code.append(opereacao[instruction]+'1'+register[operands[1]])

            if instruction in 'swap':
                N1 = opereacao['xor']+register[operands[0]]+register[operands[1]]
                N2 = opereacao['xor']+register[operands[1]]+register[operands[0]]
                machine_code.append(N1)
                machine_code.append(N2)
                machine_code.append(N1)

            if instruction in 'halt':
                n = bin(len(machine_code))
                machine_code.append(opereacao['jmp'])
                machine_code.append(n)

            if instruction in jcaez:
                if (operands[0].startswith('0x')):
                    N = int(operands[0],16)
                elif(operands[0].startswith('0b')):
                    N = int (operands[0], 2)
                else:
                    N = int(operands[0])
                machine_code.append(jcaez[instruction])
                machine_code.append(format(N ,'08b'))

    return machine_code 

# funcao que vai pegar o numero binario e tratamento no codigo binario e fazer a converçao
def convert_binary_to_hexadecimal(codigo_binario):
    codigo_binario = codigo_binario.replace(' ', '')  
    return hex(int(codigo_binario, 2))[2:].upper().zfill(2)


# funcao que vai pegar o valor em binario vai transformar para hex e vai checar se ta apito ao sistema 
def convert_to_hex(machine_code):
    hex_words = []

    for code in machine_code:
        hex_word = convert_binary_to_hexadecimal(code)
        
        hex_words.append(hex_word)                                          

    return hex_words


#funcao que vai escrever no arquivo 
def output_file(memory, path):
    assert len(memory) <= 256
    
    while (len(memory) < 256):
        memory.append('00')
    with open(path, 'w') as output_file:
        output_file.write("v3.0 hex words addressed\n")
        for i in range(len(memory)):
            output_file.write(f'{i:02x}: ')
            output_file.write(memory[i] + "\n")



def assembler(source_file, output_file_path):

    lines = read_source(source_file)
    binary_code = translate_to_machine_code(lines)
    hex_code = convert_to_hex(binary_code)
    output_file(hex_code, output_file_path)


source_file = sys.argv[1]
output_file_path = sys.argv[2]
assembler(source_file, output_file_path)

