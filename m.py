import sys

# Tabela de operações com seus códigos binários correspondentes
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
    'data': '0010',
    'jmpr': '0011',
    'jmp': '0100',
    'clf': '0101',
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

# Tabela de códigos binários para operações condicionais
jcaez = {
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

# Tabela de registradores com seus códigos binários correspondentes
register = {
    'r0': '00',
    'r1': '01',
    'r2': '10',
    'r3': '11'
}

def read_source(file_path):
    """Lê o arquivo de origem e retorna suas linhas, convertidas para minúsculas e sem linhas vazias ou comentários."""
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return [line.strip().lower() for line in lines if line.strip() and not line.startswith(';')]

def parse_line(line):
    """Analisa uma linha de código, dividindo-a em instrução e operandos."""
    parts = line.split()
    if len(parts) == 0:
        return None, None
    
    instruction = parts[0].lower()
    operands = []
    
    if len(parts) > 1:
        operands_str = ' '.join(parts[1:])
        operands = [op.strip() for op in operands_str.split(',')]
    
    return instruction, operands



def translate_to_machine_code(lines):
    """Converte linhas de código em assembly para código de máquina binário."""
    machine_code = []
    for line in lines:
        instruction, operands = parse_line(line)
        code = ''
        
        if instruction in opereacao:
            code = opereacao[instruction]
            
            if instruction == 'ld':
                if len(operands) == 2 and operands[0] in register:
                    if operands[1].startswith('0x'):
                        value = int(operands[1], 16)
                    elif operands[1].startswith('0b'):
                        value = int(operands[1], 2)
                    elif operands[1].isdigit():
                        value = int(operands[1])
                    else:
                        value = 0  
                    code += register[operands[0]] + format(value, '08b')
            
            elif instruction == 'add':
                if len(operands) == 3 and all(op in register for op in operands):
                    code += register[operands[0]] + register[operands[1]] + register[operands[2]]
                else:
                    print(f"Erro na linha: {line} - Operandos inválidos para 'add'")
                    continue
            
            elif instruction in ['shl', 'shr']:
                if len(operands) == 2 and operands[0] in register and operands[1].isdigit():
                    code += register[operands[0]] + format(int(operands[1]), '04b')
                else:
                    print(f"Erro na linha: {line} - Operandos inválidos para '{instruction}'")
                    continue

            elif instruction == 'not':
                if len(operands) == 1 and operands[0] in register:
                    code += register[operands[0]] + '0000'
                else:
                    print(f"Erro na linha: {line} - Operandos inválidos para 'not'")
                    continue
            
            elif instruction in ['and', 'or', 'xor', 'cmp', 'st']:
                if len(operands) == 2 and all(op in register for op in operands):
                    code += register[operands[0]] + register[operands[1]]
                else:
                    print(f"Erro na linha: {line} - Operandos inválidos para '{instruction}'")
                    continue
            
            elif instruction == 'jmp':
                if len(opereacao) == 1:
                    if operands[0].startswith('0x'):
                        address = int(operands[0], 16)
                    elif operands[0].startswith('0b'):
                        address = int(operands[0], 2)
                    else:
                        address = int(operands[0])
                    if 0 <= address <= 255:
                        code += format(address, '08b')
                    else:
                        print(f"Erro na linha: {line} - Endereço inválido para 'jmp'")
                        continue
                else:
                    print(f"Erro na linha: {line} - Operandos inválidos para 'jmp'")
                    continue
            
            elif instruction in jcaez:
                if len(operands) == 1:
                    if operands[0].startswith('0x'):
                        address = int(operands[0], 16)
                    elif operands[0].startswith('0b'):
                        address = int(operands[0], 2)
                    else:
                        address = int(operands[0])
                    if 0 <= address <= 255:
                        code += jcaez[instruction] + format(address, '08b')
                    else:
                        print(f"Erro na linha: {line} - Endereço inválido para '{instruction}'")
                        continue
                else:
                    print(f"Erro na linha: {line} - Operandos inválidos para '{instruction}'")
                    continue

        elif instruction == 'data':
            if len(operands) == 1:
                if operands[0].startswith('0x'):
                    value = int(operands[0], 16)
                elif operands[0].startswith('0b'):
                    value = int(operands[0], 2)
                else:
                    value = int(operands[0])
                code = format(value, '08b')
            else:
                print(f"Erro na linha: {line} - Operando inválido para 'data'")
                continue
        
        machine_code.append(code)
    
    return machine_code


def write_outputfile(output_file_path, machine_code):
    """Escreve o código de máquina binário em um arquivo de saída."""
    with open(output_file_path, "w") as file:
        for code in machine_code:
            file.write(f"{code}\n")

def convert_binary_to_hexadecimal(binary_code):
    """Converte código binário para hexadecimal."""
    binary_code = binary_code.replace(' ', '')  # Remove espaços
    return hex(int(binary_code, 2))[2:].upper().zfill(len(binary_code) // 4)

def convert_to_hex(machine_code):
    """Converte código de máquina binário em hexadecimal."""
    hex_words = []
    for code in machine_code:
        hex_word = convert_binary_to_hexadecimal(code)
        hex_words.append(hex_word)
    return hex_words

def assembler(source_file, output_file_path):
    """Função principal que monta o código assembly em código de máquina binário e gera o arquivo de saída em hexadecimal."""
    lines = read_source(source_file)
    print(lines)
    machine_code = translate_to_machine_code(lines)
    print(machine_code)

    hex_code = convert_to_hex(machine_code)
    write_outputfile(output_file_path, hex_code)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python assembler.py <arquivo_entrada.asm> <arquivo_saida.m>")
    else:
        source_file = sys.argv[1]
        output_file_path = sys.argv[2]
        assembler(source_file, output_file_path)
