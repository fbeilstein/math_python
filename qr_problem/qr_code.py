import numpy as np
import cv2

# =====================================================================
# 1. SPECIFICATIONS & DYNAMIC SIZING (Versions 1-6, EC Level M)
# =====================================================================

# Format: { Version: (Total Data Bytes, Num Blocks, Data/Block, EC/Block) }
QR_SPECS = {
    1: (16, 1, 16, 10),
    2: (28, 1, 28, 16),
    3: (44, 1, 44, 26),
    4: (64, 2, 32, 18),
    5: (86, 2, 43, 24),
    6: (108, 4, 27, 16)
}

def determine_version(text):
    """Finds the smallest QR version that can hold the message."""
    required_bits = 4 + 8 + len(text) * 8
    required_bytes = (required_bits + 7) // 8
    for version, specs in QR_SPECS.items():
        if required_bytes <= specs[0]:
            return version, specs
    raise ValueError(f"Message too long! Max capacity is {QR_SPECS[6][0]} characters.")

# =====================================================================
# 2. GALOIS FIELD & REED-SOLOMON MATH (The Brains)
# =====================================================================

def generate_gf256_tables():
    exp_table = [0] * 256
    log_table = [0] * 256
    x = 1
    for i in range(255):
        exp_table[i] = x
        log_table[x] = i
        x <<= 1
        if x & 0x100:
            x ^= 0x011D
    exp_table[255] = exp_table[0]
    return exp_table, log_table

def gf_poly_multiply(p, q, log_table, exp_table):
    result = [0] * (len(p) + len(q) - 1)
    for j in range(len(q)):
        for i in range(len(p)):
            if p[i] != 0 and q[j] != 0:
                mult_val = exp_table[(log_table[p[i]] + log_table[q[j]]) % 255]
                result[i + j] ^= mult_val
    return result

def get_error_correction_bytes(message, num_ec_bytes, log_table, exp_table):
    gen_poly = [1]
    for i in range(num_ec_bytes):
        gen_poly = gf_poly_multiply(gen_poly, [1, exp_table[i]], log_table, exp_table)
        
    msg_poly = message + [0] * num_ec_bytes
    for i in range(len(message)):
        coef = msg_poly[i]
        if coef != 0:
            for j in range(len(gen_poly)):
                if gen_poly[j] != 0:
                    mult_val = exp_table[(log_table[gen_poly[j]] + log_table[coef]) % 255]
                    msg_poly[i + j] ^= mult_val
    return msg_poly[len(message):]

def interleave_blocks(data_bytes, version_specs, log_table, exp_table):
    """Slices data, calculates EC for each block, and deals them like cards."""
    total_data, num_blocks, data_per_block, ec_per_block = version_specs
    
    data_blocks = []
    ec_blocks = []
    
    # 1. Generate the Error Correction for each individual slice
    for i in range(num_blocks):
        start = i * data_per_block
        end = start + data_per_block
        block_data = data_bytes[start:end]
        
        block_ec = get_error_correction_bytes(block_data, ec_per_block, log_table, exp_table)
        data_blocks.append(block_data)
        ec_blocks.append(block_ec)
        
    # 2. Interleave Data
    interleaved_data = []
    for i in range(data_per_block):
        for block in data_blocks:
            if i < len(block): interleaved_data.append(block[i])
            
    # 3. Interleave Error Correction
    interleaved_ec = []
    for i in range(ec_per_block):
        for block in ec_blocks:
            if i < len(block): interleaved_ec.append(block[i])
            
    return interleaved_data, interleaved_ec

# =====================================================================
# 3. DATA ENCODING (Translating Text to the ISO Bitstream)
# =====================================================================

def encode_data(text, capacity_bytes):
    # Mode Indicator for Byte Mode: 0100
    bitstream = "0100"
    
    # Character Count Indicator (8 bits for Versions 1-9)
    bitstream += f"{len(text):08b}"
    
    # The actual data
    for char in text:
        bitstream += f"{ord(char):08b}"
        
    # Terminator
    bitstream += "0000"[:min(4, capacity_bytes * 8 - len(bitstream))]
    
    # Pad to make length a multiple of 8
    while len(bitstream) % 8 != 0:
        bitstream += "0"
        
    # Add Alternating ISO Padding Bytes until full
    padding = ["11101100", "00010001"]
    pad_idx = 0
    while len(bitstream) < capacity_bytes * 8:
        bitstream += padding[pad_idx % 2]
        pad_idx += 1
        
    return [int(bitstream[i:i+8], 2) for i in range(0, len(bitstream), 8)]

# =====================================================================
# 4. FORMAT STRING CALCULATION (BCH Metadata)
# =====================================================================

def get_format_string():
    # Error Level M (00) and Mask 0 (000) -> 00000
    data = 0 
    generator = 1335 
    
    val = data << 10
    for i in range(4, -1, -1):
        if val & (1 << (i + 10)):
            val ^= (generator << i)
            
    # XOR with the standard format mask
    format_info = ((data << 10) | val) ^ 21522 
    return f"{format_info:015b}"

# =====================================================================
# 5. MATRIX PLACEMENT (Corrected ISO Compliance)
# =====================================================================

def build_qr_matrix(version, data_bits, ec_bits):
    size = 4 * version + 17
    matrix = np.full((size, size), -1, dtype=int)
    
    def draw_finder(r_start, c_start):
        for r in range(7):
            for c in range(7):
                is_edge = (r == 0 or r == 6 or c == 0 or c == 6)
                is_center = (2 <= r <= 4 and 2 <= c <= 4)
                matrix[r_start + r][c_start + c] = 1 if (is_edge or is_center) else 0
                
        # White borders
        for i in range(8):
            if r_start + 7 < size and c_start + i < size: matrix[r_start + 7][c_start + i] = 0
            if r_start + i < size and c_start + 7 < size: matrix[r_start + i][c_start + 7] = 0
            if r_start - 1 >= 0 and c_start + i < size: matrix[r_start - 1][c_start + i] = 0
            if r_start + i < size and c_start - 1 >= 0: matrix[r_start + i][c_start - 1] = 0

    # 1. Place Finders (The 3 corners)
    draw_finder(0, 0)
    draw_finder(0, size - 7)
    draw_finder(size - 7, 0)
    
    # 2. Place Alignment Pattern (Version 2+)
    # FIX: V2-V6 only have ONE alignment pattern at the bottom right.
    # Drawing any others will corrupt the main finders!
    if version >= 2:
        c = size - 7 # The mathematical center for the bottom-right pattern
        for r in range(-2, 3):
            for col in range(-2, 3):
                is_border = (r == -2 or r == 2 or col == -2 or col == 2)
                is_abs_center = (r == 0 and col == 0)
                matrix[c + r][c + col] = 1 if (is_border or is_abs_center) else 0
    
    # 3. Place Timing Patterns
    for i in range(8, size - 8):
        matrix[6][i] = matrix[i][6] = (i % 2) == 0
        
    # 4. Place Dark Module
    matrix[4 * version + 9][8] = 1
    
    # 5. Place Format String
    fmt = get_format_string()
    tl_x = [0, 1, 2, 3, 4, 5, 7, 8, 8, 8, 8, 8, 8, 8, 8]
    tl_y = [8, 8, 8, 8, 8, 8, 8, 8, 7, 5, 4, 3, 2, 1, 0]
    for i in range(15): matrix[tl_y[i]][tl_x[i]] = int(fmt[i])
    for i in range(7): matrix[size - 1 - i][8] = int(fmt[i])
    for i in range(8): matrix[8][size - 8 + i] = int(fmt[7 + i])

    # 6. DATA ROUTING (The Zigzag Snake)
    all_bits = data_bits + ec_bits
    bit_idx = 0
    direction = -1 
    col = size - 1
    row = size - 1
    
    while col > 0:
        if col == 6: col -= 1 # Skip timing column entirely
        for _ in range(size):
            for c_offset in range(2):
                if matrix[row][col - c_offset] == -1: 
                    
                    # FIX: Handle Remainder Bits safely
                    if bit_idx < len(all_bits):
                        pixel = all_bits[bit_idx]
                        bit_idx += 1
                    else:
                        pixel = 0 # ISO Spec: Pad leftover matrix modules with 0
                    
                    # Apply Mask 0: (row + col) % 2 == 0
                    if (row + (col - c_offset)) % 2 == 0:
                        pixel ^= 1
                        
                    matrix[row][col - c_offset] = pixel
            row += direction
        row -= direction 
        direction *= -1  
        col -= 2         

    return matrix
# =====================================================================
# EXECUTION
# =====================================================================

def main():
    print("--- Pure Python ISO QR Generator ---")
    print("Initializing Galois Field Tables...")
    exp_table, log_table = generate_gf256_tables()
    
    # The ultimate test: A long string that forces the script 
    # to dynamically promote to Version 3!
    message = "hello world from Python math! This dynamically scales to Version 3."
    
    print(f"\nEncoding Message: '{message}'")
    print(f"Message Length: {len(message)} characters.")
    
    # Dynamic Promotion
    version, specs = determine_version(message)
    print(f"-> Automatically selected Version {version} (Capacity: {specs[0]} bytes)")
    
    # Encoding & Math
    raw_data_bytes = encode_data(message, specs[0])
    interleaved_data, interleaved_ec = interleave_blocks(raw_data_bytes, specs, log_table, exp_table)
    
    print(f"-> Data broken into {specs[1]} Galois Field Blocks and interleaved.")
    
    # Convert bytes to individual bits
    data_bits = [int(b) for byte in interleaved_data for b in f"{byte:08b}"]
    ec_bits = [int(b) for byte in interleaved_ec for b in f"{byte:08b}"]
    
    # Matrix Routing
    print(f"Routing {len(data_bits) + len(ec_bits)} bits through the matrix...")
    matrix = build_qr_matrix(version, data_bits, ec_bits)
    
    # Rendering
    img = np.where(matrix == 1, 0, 255).astype(np.uint8)
    img_padded = cv2.copyMakeBorder(img, 4, 4, 4, 4, cv2.BORDER_CONSTANT, value=255)
    
    scale = 15
    final_img = cv2.resize(img_padded, (img_padded.shape[1] * scale, img_padded.shape[0] * scale), interpolation=cv2.INTER_NEAREST)
    
    filename = f"dynamic_scratch_qr_v{version}.png"
    cv2.imwrite(filename, final_img)
    
    print(f"\nSUCCESS! Grid size {matrix.shape[0]}x{matrix.shape[1]} saved as '{filename}'.")
    print("You can point your phone at your monitor right now to scan it.")

if __name__ == "__main__":
    main()
