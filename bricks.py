from collections import defaultdict
import sys

MAX_BOX_BLOCKS = 10000000  # Maksymalna liczba klocków w pudełku
MAX_INSTRUCTIONS = 1000     # Maksymalna liczba instrukcji
MAX_BLOCKS_PER_INSTRUCTION = 5000  # Maksymalna liczba klocków wymaganych przez jedną instrukcję

def is_valid_block_code(code):
    valid_chars = 'ABCDEFGHIJKLMNO'
    return all(char in valid_chars for char in code)

def parse_input():
    instructions = {}   # Słownik przechowujący instrukcje
    box_blocks = []     # Lista przechowująca klocki w pudełku

    for line in sys.stdin:
        line = line.strip()

        if line:
            parts = line.split(':')
            instruction_number = int(parts[0])
            block_code = parts[1]

            if instruction_number == 0:
                if is_valid_block_code(block_code):
                    box_blocks.append(block_code)
            else:
                if instruction_number not in instructions:
                    instructions[instruction_number] = []
                if is_valid_block_code(block_code):
                    instructions[instruction_number].append(block_code)

    return instructions, box_blocks

def count_blocks(blocks):
    count = defaultdict(int)    # Licznik klocków

    for block in blocks:
        count[block] += 1

    return count

def execute_instructions(instructions, box_blocks):
    used_blocks_stage1_count = 0                     # Licznik użytych klocków w etapie I
    used_blocks_stage2_count = 0                     # Licznik użytych klocków w etapie II
    remaining_blocks_count = count_blocks(box_blocks)# Licznik klocków w pudełku
    missing_blocks_count = defaultdict(int)          # Licznik brakujących klocków
    successful_buildings = 0                         # Licznik udanych budowli
    failed_buildings = 0                             # Licznik nieudanych budowli

    # Sprawdzenie ograniczeń dotyczących liczby klocków w pudełku
    if len(box_blocks) > MAX_BOX_BLOCKS:
        print("klops")
        sys.exit(0)

    # Sprawdzenie ograniczeń dotyczących liczby instrukcji
    if len(instructions) > MAX_INSTRUCTIONS:
        print("klops")
        sys.exit(0)

    # Sprawdzenie ograniczeń dotyczących liczby klocków w pojedynczej instrukcji
    for instruction_blocks in instructions.values():
        if len(instruction_blocks) > MAX_BLOCKS_PER_INSTRUCTION:
            print("klops")
            sys.exit(0)

    # Etap I - Instrukcje jeżyka Bolka
    for instruction_number in sorted(instructions.keys()):
        if instruction_number % 3 == 0:
            for block in instructions[instruction_number]:
                if block in remaining_blocks_count and remaining_blocks_count[block] > 0:
                    # Użyj klocka z pudełka
                    used_blocks_stage1_count += 1
                    remaining_blocks_count[block] -= 1
                else:
                    # Klocek nie jest dostępny w pudełku
                    failed_buildings += 1
                    missing_blocks_count[block] += 1

    # Etap II - Pozostałe instrukcje
    for instruction_number in sorted(instructions.keys()):
        if instruction_number % 3 != 0:
            for block in instructions[instruction_number]:
                if block in remaining_blocks_count and remaining_blocks_count[block] > 0:
                    # Użyj klocka z pudełka
                    used_blocks_stage2_count += 1
                    remaining_blocks_count[block] -= 1
                else:
                    # Klocek nie jest dostępny w pudełku
                    failed_buildings += 1
                    missing_blocks_count[block] += 1

    successful_buildings = len(instructions) - failed_buildings

    return used_blocks_stage1_count, used_blocks_stage2_count, len(box_blocks) - used_blocks_stage1_count, sum(missing_blocks_count.values()), successful_buildings, failed_buildings

def main():
    instructions, box_blocks = parse_input()
    results = execute_instructions(instructions, box_blocks)

    # Wyświetlanie wyników
    for result in results:
        print(result)

    sys.exit(0)  # Zakończenie programu z kodem 0

if __name__ == '__main__':
    main()
