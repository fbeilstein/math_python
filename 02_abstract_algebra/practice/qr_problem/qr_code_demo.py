import numpy as np
import cv2
import qr_code as qr
import implementation_tasks as tasks
import algebra_utils as utils

# =====================================================================
# 1. SPECIFICATIONS
# =====================================================================

QR_SPECS = {
    1: (16, 1, 16, 10),
    2: (28, 1, 28, 16),
    3: (44, 1, 44, 26),
    4: (64, 2, 32, 18),
    5: (86, 2, 43, 24),
    6: (108, 4, 27, 16)
}

def determine_version(text):
    required_bits = 4 + 8 + len(text) * 8
    required_bytes = (required_bits + 7) // 8
    for version, specs in QR_SPECS.items():
        if required_bytes <= specs[0]:
            return version, specs
    raise ValueError(f"Message too long! Max capacity is {QR_SPECS[6][0]} characters.")

# =====================================================================
# 2. DATA ENCODING & ISO COMPLIANCE
# =====================================================================

def encode_data(text, capacity_bytes):
    bitstream = "0100"
    bitstream += f"{len(text):08b}"
    for char in text: bitstream += f"{ord(char):08b}"
    bitstream += "0000"[:min(4, capacity_bytes * 8 - len(bitstream))]
    
    while len(bitstream) % 8 != 0: bitstream += "0"
    padding = ["11101100", "00010001"]
    pad_idx = 0
    while len(bitstream) < capacity_bytes * 8:
        bitstream += padding[pad_idx % 2]
        pad_idx += 1
        
    return [int(bitstream[i:i+8], 2) for i in range(0, len(bitstream), 8)]

# =====================================================================
# 3. INTERLEAVING & REED-SOLOMON
# =====================================================================

def interleave_blocks(data_bytes, version_specs, gf):
    total_data, num_blocks, data_per_block, ec_per_block = version_specs
    
    data_blocks = []
    ec_blocks = []
    
    gen_poly = tasks.get_generator_poly(ec_per_block, gf)
    
    for i in range(num_blocks):
        start = i * data_per_block
        end = start + data_per_block
        block_data = data_bytes[start:end]
        
        # Calculate EC Remainder using Unified OOP
        msg_padded = [utils.int_to_ext(c, gf) for c in block_data] + [gf.zero] * ec_per_block
        msg_poly = tasks.Polynomial(msg_padded)
        
        q, rem = divmod(msg_poly, gen_poly)
        diff = ec_per_block - len(rem.coeffs)
        rem_padded = [0]*diff + [utils.ext_to_int(c) for c in rem.coeffs]
            
        data_blocks.append(block_data)
        ec_blocks.append(rem_padded)
        
    interleaved_data = []
    for i in range(data_per_block):
        for block in data_blocks:
            if i < len(block): interleaved_data.append(block[i])
            
    interleaved_ec = []
    for i in range(ec_per_block):
        for block in ec_blocks:
            if i < len(block): interleaved_ec.append(block[i])
            
    return interleaved_data, interleaved_ec

# =====================================================================
# EXECUTION
# =====================================================================

def main():
    print("--- Unified OOP Abstract Algebra QR Generator ---")
    
    # 1. Abstract Algebra Setup: GF(2^8) with QR standard polynomial
    p, n = 2, 8
    qr_prim_poly = [1, 0, 0, 0, 1, 1, 1, 0, 1] # x^8 + x^4 + x^3 + x^2 + 1
    print(f"Constructing GF({p}^{n}) with primitive poly {qr_prim_poly}...")
    qr_prim_poly_obj = utils.make_poly(qr_prim_poly, p)
    gf = tasks.ExtensionField(qr_prim_poly_obj)
    
    message = "hello world from Python math! This uses GF(p^n) generalized math."
    print(f"\nEncoding Message: '{message}'")
    
    version, specs = determine_version(message)
    print(f"-> Selected Version {version} (Capacity: {specs[0]} bytes)")
    
    # 2. ISO Byte Mode Encoding
    raw_data_bytes = encode_data(message, specs[0])
    
    # 3. RS Encoding over Generalized GF(p^n)
    interleaved_data, interleaved_ec = interleave_blocks(raw_data_bytes, specs, gf)
    
    # 4. Routing via generalized module
    data_bits = [int(b) for byte in interleaved_data for b in f"{byte:08b}"]
    ec_bits = [int(b) for byte in interleaved_ec for b in f"{byte:08b}"]
    
    print(f"Routing {len(data_bits) + len(ec_bits)} bits through the matrix...")
    matrix = qr.build_qr_matrix(version, data_bits, ec_bits)
    
    # Rendering
    img = np.where(matrix == 1, 0, 255).astype(np.uint8)
    img_padded = cv2.copyMakeBorder(img, 4, 4, 4, 4, cv2.BORDER_CONSTANT, value=255)
    
    scale = 15
    final_img = cv2.resize(img_padded, (img_padded.shape[1] * scale, img_padded.shape[0] * scale), interpolation=cv2.INTER_NEAREST)
    
    filename = f"dynamic_scratch_qr_v{version}.png"
    cv2.imwrite(filename, final_img)
    print(f"\nSUCCESS! Saved as '{filename}'. Scan it with your phone!")

if __name__ == "__main__":
    main()
