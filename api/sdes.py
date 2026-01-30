from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        # Get user inputs
        plaintext = data.get('plaintext', '10111101')
        key = data.get('key', '1010000010')
        P10 = data.get('P10', [3,5,2,7,4,10,1,9,8,6])
        P8 = data.get('P8', [6,3,7,4,8,5,10,9])
        IP = data.get('IP', [2,6,3,1,4,8,5,7])
        EP = data.get('EP', [4,1,2,3,2,3,4,1])
        P4 = data.get('P4', [2,4,3,1])
        S0 = data.get('S0', [
            ["01","00","11","10"],
            ["11","10","01","00"],
            ["00","10","01","11"],
            ["11","01","11","10"]
        ])
        S1 = data.get('S1', [
            ["00","01","10","11"],
            ["10","00","01","11"],
            ["11","00","01","00"],
            ["10","01","00","11"]
        ])

        # Calculate IP inverse from IP
        IP_INV = calculate_ip_inverse(IP)

        # Run encryption with detailed step tracking
        result = encrypt_with_detailed_steps(plaintext, key, P10, P8, IP, IP_INV, EP, P4, S0, S1)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode('utf-8'))

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write('S-DES API Endpoint - Use POST to encrypt'.encode('utf-8'))


def calculate_ip_inverse(IP):
    """Calculate the inverse permutation of IP"""
    IP_INV = [0] * len(IP)
    for i, pos in enumerate(IP):
        IP_INV[pos - 1] = i + 1
    return IP_INV


def permute(bits, table):
    return ''.join(bits[i-1] for i in table)


def left_shift(bits, n):
    return bits[n:] + bits[:n]


def xor(a, b):
    return ''.join('0' if i == j else '1' for i, j in zip(a, b))


def sbox_lookup(bits, box):
    row = int(bits[0] + bits[3], 2)
    col = int(bits[1] + bits[2], 2)
    out = box[row][col]
    return out, row, col


def format_bits(bits):
    """Format bits with spaces for readability"""
    return ' '.join(bits)


def generate_permutation_detail(input_bits, table, table_name):
    """Generate detailed permutation explanation"""
    lines = []
    lines.append(f"Apply {table_name} Rule: {' '.join(map(str, table))}")
    lines.append(f"Input: {format_bits(input_bits)}")
    lines.append("")
    for i, pos in enumerate(table):
        lines.append(f"  Position {i+1}: Take bit {pos} → '{input_bits[pos-1]}'")
    output = permute(input_bits, table)
    lines.append("")
    lines.append(f"Result: {format_bits(output)}")
    return output, '\n'.join(lines)


def generate_xor_detail(a, b, label_a, label_b):
    """Generate detailed XOR explanation"""
    lines = []
    lines.append(f"{format_bits(a)}  ({label_a})")
    lines.append(f"{format_bits(b)}  ({label_b})")
    lines.append("-" * (len(a) * 2 + 10) + " (XOR)")
    result = xor(a, b)
    lines.append(f"{format_bits(result)}")
    return result, '\n'.join(lines)


def generate_sbox_detail(bits, box, box_name):
    """Generate detailed S-box lookup explanation"""
    lines = []
    row_bits = bits[0] + bits[3]
    col_bits = bits[1] + bits[2]
    row = int(row_bits, 2)
    col = int(col_bits, 2)
    output = box[row][col]
    
    lines.append(f"{box_name} Input: {format_bits(bits)}")
    lines.append(f"  Outer bits (1,4): {row_bits} → Row {row}")
    lines.append(f"  Inner bits (2,3): {col_bits} → Col {col}")
    lines.append(f"  Look up [{box_name}][Row {row}][Col {col}] → {output} (decimal {int(output, 2)})")
    
    return output, '\n'.join(lines)


def generate_keys_detailed(key, P10, P8):
    """Generate keys with detailed step-by-step explanation"""
    steps = []
    
    # Step: Show input key
    steps.append({
        "title": "Input Key",
        "content": f"Key (K): {format_bits(key)} (10 bits)"
    })
    
    # Step: Apply P10
    p10_result, p10_detail = generate_permutation_detail(key, P10, "P10")
    steps.append({
        "title": "Apply P10 Permutation",
        "content": p10_detail
    })
    
    # Step: Split
    left = p10_result[:5]
    right = p10_result[5:]
    steps.append({
        "title": "Split into Two Halves",
        "content": f"Left half:  {format_bits(left)}\nRight half: {format_bits(right)}"
    })
    
    # Step: LS-1
    left_ls1 = left_shift(left, 1)
    right_ls1 = left_shift(right, 1)
    steps.append({
        "title": "Left Shift by 1 (LS-1)",
        "content": f"Left:  {format_bits(left)} → {format_bits(left_ls1)} (shift left by 1)\nRight: {format_bits(right)} → {format_bits(right_ls1)} (shift left by 1)"
    })
    
    # Step: Combine and apply P8 for K1
    combined_k1 = left_ls1 + right_ls1
    K1, k1_detail = generate_permutation_detail(combined_k1, P8, "P8")
    steps.append({
        "title": "Generate K₁ (Apply P8)",
        "content": f"Combined: {format_bits(combined_k1)}\n\n{k1_detail}\n\n★ K₁ = {format_bits(K1)}"
    })
    
    # Step: LS-2
    left_ls2 = left_shift(left_ls1, 2)
    right_ls2 = left_shift(right_ls1, 2)
    steps.append({
        "title": "Left Shift by 2 (LS-2)",
        "content": f"Left:  {format_bits(left_ls1)} → {format_bits(left_ls2)} (shift left by 2)\nRight: {format_bits(right_ls1)} → {format_bits(right_ls2)} (shift left by 2)"
    })
    
    # Step: Combine and apply P8 for K2
    combined_k2 = left_ls2 + right_ls2
    K2, k2_detail = generate_permutation_detail(combined_k2, P8, "P8")
    steps.append({
        "title": "Generate K₂ (Apply P8)",
        "content": f"Combined: {format_bits(combined_k2)}\n\n{k2_detail}\n\n★ K₂ = {format_bits(K2)}"
    })
    
    return K1, K2, steps


def fk_detailed(bits, key, EP, P4, S0, S1, round_num, key_name):
    """Perform fk function with detailed steps"""
    steps = []
    
    left = bits[:4]
    right = bits[4:]
    
    # Step: Show input and split
    steps.append({
        "title": f"Round {round_num}: Input",
        "content": f"Input: {format_bits(bits)}\nSplit:\n  L{round_num-1} (Left 4 bits):  {format_bits(left)}\n  R{round_num-1} (Right 4 bits): {format_bits(right)}"
    })
    
    # Step: E/P Expansion
    ep_result, ep_detail = generate_permutation_detail(right, EP, "E/P")
    steps.append({
        "title": f"Expansion/Permutation (E/P) on R{round_num-1}",
        "content": ep_detail
    })
    
    # Step: XOR with key
    xor_result, xor_detail = generate_xor_detail(ep_result, key, "E/P Output", key_name)
    steps.append({
        "title": f"XOR with {key_name}",
        "content": xor_detail
    })
    
    # Step: Split for S-boxes
    left_sbox = xor_result[:4]
    right_sbox = xor_result[4:]
    steps.append({
        "title": "Split for S-Boxes",
        "content": f"Left 4 bits → S0: {format_bits(left_sbox)}\nRight 4 bits → S1: {format_bits(right_sbox)}"
    })
    
    # Step: S0 lookup
    s0_out, s0_detail = generate_sbox_detail(left_sbox, S0, "S0")
    steps.append({
        "title": "S0 Box Lookup",
        "content": s0_detail
    })
    
    # Step: S1 lookup
    s1_out, s1_detail = generate_sbox_detail(right_sbox, S1, "S1")
    steps.append({
        "title": "S1 Box Lookup",
        "content": s1_detail
    })
    
    # Step: Combine S-box outputs
    sbox_combined = s0_out + s1_out
    steps.append({
        "title": "Combine S-Box Outputs",
        "content": f"S0 output: {s0_out}\nS1 output: {s1_out}\nCombined: {format_bits(sbox_combined)}"
    })
    
    # Step: P4 Permutation
    p4_result, p4_detail = generate_permutation_detail(sbox_combined, P4, "P4")
    steps.append({
        "title": "P4 Permutation",
        "content": p4_detail
    })
    
    # Step: XOR with Left half
    new_left, final_xor_detail = generate_xor_detail(p4_result, left, "P4 Output", f"L{round_num-1}")
    steps.append({
        "title": f"XOR P4 result with L{round_num-1}",
        "content": f"{final_xor_detail}\n\nThis becomes the new value for the round."
    })
    
    # Final output of round
    result = new_left + right
    steps.append({
        "title": f"Round {round_num} Output",
        "content": f"New Left:  {format_bits(new_left)} (result of XOR)\nRight:     {format_bits(right)} (unchanged R{round_num-1})\nCombined:  {format_bits(result)}"
    })
    
    return result, steps


def encrypt_with_detailed_steps(plaintext, key, P10, P8, IP, IP_INV, EP, P4, S0, S1):
    all_sections = []
    
    # Section 1: Inputs & Parameters
    inputs_content = f"""Plaintext (P): {format_bits(plaintext)} (8 bits)
Key (K): {format_bits(key)} (10 bits)

Standard Tables:
• IP (Initial Permutation): {' '.join(map(str, IP))}
• IP⁻¹ (Inverse Permutation): {' '.join(map(str, IP_INV))}
• E/P (Expansion/Permutation): {' '.join(map(str, EP))}
• P4 (Permutation 4): {' '.join(map(str, P4))}
• P10 (Key Permutation): {' '.join(map(str, P10))}
• P8 (Subkey Permutation): {' '.join(map(str, P8))}"""
    
    all_sections.append({
        "section": "1. The Inputs & Parameters",
        "subsections": [{
            "title": "Given Values & Standard Tables",
            "content": inputs_content
        }]
    })
    
    # Section 2: S-Boxes
    s0_table = "S-Box 0 (S0)\n"
    s0_table += "         Col 0(00)  Col 1(01)  Col 2(10)  Col 3(11)\n"
    for i, row in enumerate(S0):
        row_bits = format(i, '02b')
        s0_table += f"Row {i}({row_bits}):    {row[0]}        {row[1]}        {row[2]}        {row[3]}\n"
    
    s1_table = "S-Box 1 (S1)\n"
    s1_table += "         Col 0(00)  Col 1(01)  Col 2(10)  Col 3(11)\n"
    for i, row in enumerate(S1):
        row_bits = format(i, '02b')
        s1_table += f"Row {i}({row_bits}):    {row[0]}        {row[1]}        {row[2]}        {row[3]}\n"
    
    sbox_content = f"""{s0_table}
{s1_table}
Row Selection: Use bits 1 and 4 (outer bits)
Column Selection: Use bits 2 and 3 (inner bits)"""
    
    all_sections.append({
        "section": "2. The S-Boxes (Lookup Tables)",
        "subsections": [{
            "title": "S0 and S1 Boxes",
            "content": sbox_content
        }]
    })
    
    # Section 3: Key Generation
    K1, K2, key_steps = generate_keys_detailed(key, P10, P8)
    all_sections.append({
        "section": "Phase A: Key Generation",
        "subsections": key_steps
    })
    
    # Section 4: Initial Permutation
    ip_result, ip_detail = generate_permutation_detail(plaintext, IP, "IP")
    L0 = ip_result[:4]
    R0 = ip_result[4:]
    
    ip_subsections = [{
        "title": "Apply Initial Permutation (IP)",
        "content": f"Input (Plaintext): {format_bits(plaintext)}\n\n{ip_detail}"
    }, {
        "title": "Split into Halves",
        "content": f"L₀ (Left 4 bits):  {format_bits(L0)}\nR₀ (Right 4 bits): {format_bits(R0)}"
    }]
    
    all_sections.append({
        "section": "Phase B: Encryption - Step 1: Initial Permutation",
        "subsections": ip_subsections
    })
    
    # Section 5: Round 1 (fk with K1)
    r1_result, r1_steps = fk_detailed(ip_result, K1, EP, P4, S0, S1, 1, "K₁")
    all_sections.append({
        "section": "Phase B: Encryption - Step 2: Function fₖ (Round 1 with K₁)",
        "subsections": r1_steps
    })
    
    # Section 6: Switch
    sw_result = r1_result[4:] + r1_result[:4]
    sw_content = f"""Before Switch: {format_bits(r1_result)}
  Left half:  {format_bits(r1_result[:4])}
  Right half: {format_bits(r1_result[4:])}

After Switch (SW): {format_bits(sw_result)}
  New Left (L₁):  {format_bits(sw_result[:4])} (was Right)
  New Right (R₁): {format_bits(sw_result[4:])} (was Left)

The left and right halves are swapped."""
    
    all_sections.append({
        "section": "Phase B: Encryption - Step 3: Switch (SW)",
        "subsections": [{
            "title": "Swap Left and Right Halves",
            "content": sw_content
        }]
    })
    
    # Section 7: Round 2 (fk with K2)
    r2_result, r2_steps = fk_detailed(sw_result, K2, EP, P4, S0, S1, 2, "K₂")
    all_sections.append({
        "section": "Phase B: Encryption - Step 4: Function fₖ (Round 2 with K₂)",
        "subsections": r2_steps
    })
    
    # Section 8: Final Permutation (IP inverse)
    # Note: No swap after final round in S-DES
    final_input = r2_result
    ciphertext, ipinv_detail = generate_permutation_detail(final_input, IP_INV, "IP⁻¹")
    
    final_content = f"""After Round 2: {format_bits(r2_result)}
  Left:  {format_bits(r2_result[:4])}
  Right: {format_bits(r2_result[4:])}

Combined Input for IP⁻¹: {format_bits(final_input)}

{ipinv_detail}"""
    
    all_sections.append({
        "section": "Phase B: Encryption - Step 5: Final Permutation (IP⁻¹)",
        "subsections": [{
            "title": "Apply Inverse Initial Permutation",
            "content": final_content
        }]
    })
    
    # Section 9: Final Result
    result_content = f"""ENCRYPTION COMPLETE

Plaintext:   {format_bits(plaintext)}
Key:         {format_bits(key)}
K₁:          {format_bits(K1)}
K₂:          {format_bits(K2)}

★ CIPHERTEXT: {format_bits(ciphertext)}"""
    
    all_sections.append({
        "section": "Final Result",
        "subsections": [{
            "title": "Summary",
            "content": result_content
        }]
    })
    
    return {
        "success": True,
        "plaintext": plaintext,
        "key": key,
        "ciphertext": ciphertext,
        "K1": K1,
        "K2": K2,
        "IP_INV": IP_INV,
        "sections": all_sections
    }