"""
Local development server for Cryptography Tools application.
Serves frontend static files and all API endpoints (S-DES, RSA, Hill).
Run: python dev_server.py
Open: http://localhost:8000
"""
import http.server
import socketserver
import json
import os
import sys
import math

# Add api folder to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'api'))

# ========== S-DES Functions ==========

def calculate_ip_inverse(IP):
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
    return ' '.join(bits)

def generate_permutation_detail(input_bits, table, table_name):
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
    lines = []
    lines.append(f"{format_bits(a)}  ({label_a})")
    lines.append(f"{format_bits(b)}  ({label_b})")
    lines.append("-" * (len(a) * 2 + 10) + " (XOR)")
    result = xor(a, b)
    lines.append(f"{format_bits(result)}")
    return result, '\n'.join(lines)

def generate_sbox_detail(bits, box, box_name):
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
    steps = []
    steps.append({"title": "Input Key", "content": f"Key (K): {format_bits(key)} (10 bits)"})
    p10_result, p10_detail = generate_permutation_detail(key, P10, "P10")
    steps.append({"title": "Apply P10 Permutation", "content": p10_detail})
    left = p10_result[:5]
    right = p10_result[5:]
    steps.append({"title": "Split into Two Halves", "content": f"Left half:  {format_bits(left)}\nRight half: {format_bits(right)}"})
    left_ls1 = left_shift(left, 1)
    right_ls1 = left_shift(right, 1)
    steps.append({"title": "Left Shift by 1 (LS-1)", "content": f"Left:  {format_bits(left)} → {format_bits(left_ls1)} (shift left by 1)\nRight: {format_bits(right)} → {format_bits(right_ls1)} (shift left by 1)"})
    combined_k1 = left_ls1 + right_ls1
    K1, k1_detail = generate_permutation_detail(combined_k1, P8, "P8")
    steps.append({"title": "Generate K₁ (Apply P8)", "content": f"Combined: {format_bits(combined_k1)}\n\n{k1_detail}\n\n★ K₁ = {format_bits(K1)}"})
    left_ls2 = left_shift(left_ls1, 2)
    right_ls2 = left_shift(right_ls1, 2)
    steps.append({"title": "Left Shift by 2 (LS-2)", "content": f"Left:  {format_bits(left_ls1)} → {format_bits(left_ls2)} (shift left by 2)\nRight: {format_bits(right_ls1)} → {format_bits(right_ls2)} (shift left by 2)"})
    combined_k2 = left_ls2 + right_ls2
    K2, k2_detail = generate_permutation_detail(combined_k2, P8, "P8")
    steps.append({"title": "Generate K₂ (Apply P8)", "content": f"Combined: {format_bits(combined_k2)}\n\n{k2_detail}\n\n★ K₂ = {format_bits(K2)}"})
    return K1, K2, steps

def fk_detailed(bits, key, EP, P4, S0, S1, round_num, key_name):
    steps = []
    left = bits[:4]
    right = bits[4:]
    steps.append({"title": f"Round {round_num}: Input", "content": f"Input: {format_bits(bits)}\nSplit:\n  L{round_num-1} (Left 4 bits):  {format_bits(left)}\n  R{round_num-1} (Right 4 bits): {format_bits(right)}"})
    ep_result, ep_detail = generate_permutation_detail(right, EP, "E/P")
    steps.append({"title": f"Expansion/Permutation (E/P) on R{round_num-1}", "content": ep_detail})
    xor_result, xor_detail = generate_xor_detail(ep_result, key, "E/P Output", key_name)
    steps.append({"title": f"XOR with {key_name}", "content": xor_detail})
    left_sbox = xor_result[:4]
    right_sbox = xor_result[4:]
    steps.append({"title": "Split for S-Boxes", "content": f"Left 4 bits → S0: {format_bits(left_sbox)}\nRight 4 bits → S1: {format_bits(right_sbox)}"})
    s0_out, s0_detail = generate_sbox_detail(left_sbox, S0, "S0")
    steps.append({"title": "S0 Box Lookup", "content": s0_detail})
    s1_out, s1_detail = generate_sbox_detail(right_sbox, S1, "S1")
    steps.append({"title": "S1 Box Lookup", "content": s1_detail})
    sbox_combined = s0_out + s1_out
    steps.append({"title": "Combine S-Box Outputs", "content": f"S0 output: {s0_out}\nS1 output: {s1_out}\nCombined: {format_bits(sbox_combined)}"})
    p4_result, p4_detail = generate_permutation_detail(sbox_combined, P4, "P4")
    steps.append({"title": "P4 Permutation", "content": p4_detail})
    new_left, final_xor_detail = generate_xor_detail(p4_result, left, "P4 Output", f"L{round_num-1}")
    steps.append({"title": f"XOR P4 result with L{round_num-1}", "content": f"{final_xor_detail}\n\nThis becomes the new value for the round."})
    result = new_left + right
    steps.append({"title": f"Round {round_num} Output", "content": f"New Left:  {format_bits(new_left)} (result of XOR)\nRight:     {format_bits(right)} (unchanged R{round_num-1})\nCombined:  {format_bits(result)}"})
    return result, steps

def encrypt_with_detailed_steps(plaintext, key, P10, P8, IP, IP_INV, EP, P4, S0, S1):
    all_sections = []
    inputs_content = f"""Plaintext (P): {format_bits(plaintext)} (8 bits)
Key (K): {format_bits(key)} (10 bits)

Standard Tables:
• IP (Initial Permutation): {' '.join(map(str, IP))}
• IP⁻¹ (Inverse Permutation): {' '.join(map(str, IP_INV))}
• E/P (Expansion/Permutation): {' '.join(map(str, EP))}
• P4 (Permutation 4): {' '.join(map(str, P4))}
• P10 (Key Permutation): {' '.join(map(str, P10))}
• P8 (Subkey Permutation): {' '.join(map(str, P8))}"""
    all_sections.append({"section": "1. The Inputs & Parameters", "subsections": [{"title": "Given Values & Standard Tables", "content": inputs_content}]})
    
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
    all_sections.append({"section": "2. The S-Boxes (Lookup Tables)", "subsections": [{"title": "S0 and S1 Boxes", "content": sbox_content}]})
    
    K1, K2, key_steps = generate_keys_detailed(key, P10, P8)
    all_sections.append({"section": "Phase A: Key Generation", "subsections": key_steps})
    
    ip_result, ip_detail = generate_permutation_detail(plaintext, IP, "IP")
    L0 = ip_result[:4]
    R0 = ip_result[4:]
    ip_subsections = [{"title": "Apply Initial Permutation (IP)", "content": f"Input (Plaintext): {format_bits(plaintext)}\n\n{ip_detail}"}, {"title": "Split into Halves", "content": f"L₀ (Left 4 bits):  {format_bits(L0)}\nR₀ (Right 4 bits): {format_bits(R0)}"}]
    all_sections.append({"section": "Phase B: Encryption - Step 1: Initial Permutation", "subsections": ip_subsections})
    
    r1_result, r1_steps = fk_detailed(ip_result, K1, EP, P4, S0, S1, 1, "K₁")
    all_sections.append({"section": "Phase B: Encryption - Step 2: Function fₖ (Round 1 with K₁)", "subsections": r1_steps})
    
    sw_result = r1_result[4:] + r1_result[:4]
    sw_content = f"""Before Switch: {format_bits(r1_result)}
  Left half:  {format_bits(r1_result[:4])}
  Right half: {format_bits(r1_result[4:])}

After Switch (SW): {format_bits(sw_result)}
  New Left (L₁):  {format_bits(sw_result[:4])} (was Right)
  New Right (R₁): {format_bits(sw_result[4:])} (was Left)

The left and right halves are swapped."""
    all_sections.append({"section": "Phase B: Encryption - Step 3: Switch (SW)", "subsections": [{"title": "Swap Left and Right Halves", "content": sw_content}]})
    
    r2_result, r2_steps = fk_detailed(sw_result, K2, EP, P4, S0, S1, 2, "K₂")
    all_sections.append({"section": "Phase B: Encryption - Step 4: Function fₖ (Round 2 with K₂)", "subsections": r2_steps})
    
    final_input = r2_result
    ciphertext, ipinv_detail = generate_permutation_detail(final_input, IP_INV, "IP⁻¹")
    final_content = f"""After Round 2: {format_bits(r2_result)}
  Left:  {format_bits(r2_result[:4])}
  Right: {format_bits(r2_result[4:])}

Combined Input for IP⁻¹: {format_bits(final_input)}

{ipinv_detail}"""
    all_sections.append({"section": "Phase B: Encryption - Step 5: Final Permutation (IP⁻¹)", "subsections": [{"title": "Apply Inverse Initial Permutation", "content": final_content}]})
    
    result_content = f"""ENCRYPTION COMPLETE

Plaintext:   {format_bits(plaintext)}
Key:         {format_bits(key)}
K₁:          {format_bits(K1)}
K₂:          {format_bits(K2)}

★ CIPHERTEXT: {format_bits(ciphertext)}"""
    all_sections.append({"section": "Final Result", "subsections": [{"title": "Summary", "content": result_content}]})
    
    return {"success": True, "plaintext": plaintext, "key": key, "ciphertext": ciphertext, "K1": K1, "K2": K2, "IP_INV": IP_INV, "sections": all_sections}


# ========== RSA Functions ==========

def gcd_func(a, b):
    while b:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd_val, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd_val, x, y

def mod_exp_detailed(base, exp, mod):
    steps = []
    steps.append(f"Computing {base}^{exp} mod {mod}")
    steps.append("")
    if exp == 0:
        steps.append("Result: 1 (any number to power 0 is 1)")
        return 1, '\n'.join(steps)
    exp_binary = bin(exp)[2:]
    steps.append(f"Step 1: Convert exponent to binary")
    steps.append(f"  {exp} in binary = {exp_binary}")
    steps.append("")
    steps.append("Step 2: Compute powers of 2 using repeated squaring")
    powers = {}
    current = base % mod
    power_of_2 = 1
    for i in range(len(exp_binary)):
        powers[power_of_2] = current
        steps.append(f"  {base}^{power_of_2} mod {mod} = {current}")
        if i < len(exp_binary) - 1:
            current = (current * current) % mod
            power_of_2 *= 2
    steps.append("")
    steps.append("Step 3: Combine powers based on binary representation")
    result = 1
    for i, bit in enumerate(reversed(exp_binary)):
        power_of_2 = 2**i
        if bit == '1':
            old_result = result
            result = (result * powers[power_of_2]) % mod
            steps.append(f"  Multiply by {base}^{power_of_2} = {powers[power_of_2]}")
            steps.append(f"    {old_result} × {powers[power_of_2]} mod {mod} = {result}")
    steps.append("")
    steps.append(f"Final Result: {base}^{exp} mod {mod} = {result}")
    return result, '\n'.join(steps)

def extended_euclidean_detailed(e, phi):
    """Extended Euclidean Algorithm with simple dividers for RSA"""
    lines = []
    
    # Header
    lines.append("═" * 55)
    lines.append("EXTENDED EUCLIDEAN ALGORITHM")
    lines.append(f"Finding d such that e × d ≡ 1 (mod φ(n))")
    lines.append(f"Where e = {e} and φ(n) = {phi}")
    lines.append("═" * 55)
    lines.append("")
    
    # Formulas
    lines.append("FORMULAS:")
    lines.append("─" * 40)
    lines.append("Recurrence Relations:")
    lines.append("  q = r1 ÷ r2  (integer division)")
    lines.append("  r = r1 - q × r2  (remainder)")
    lines.append("  s = s1 - q × s2")
    lines.append("  t = t1 - q × t2")
    lines.append("")
    lines.append("Init: s1=1, s2=0, t1=0, t2=1")
    lines.append("─" * 40)
    lines.append("")
    
    # Initialize values
    r1, r2 = phi, e
    s1, s2 = 1, 0
    t1, t2 = 0, 1
    
    # Computation table
    lines.append("COMPUTATION TABLE:")
    lines.append("─" * 45)
    lines.append("  q  │  r1  │  r2  │  r  │  s  │  t")
    lines.append("─────┼──────┼──────┼─────┼─────┼─────")
    lines.append(f"  -  │ {r1:>4} │ {r2:>4} │  -  │  -  │  -   ← Init")
    
    step = 1
    calculation_steps = []
    
    while r2 > 0:
        q = r1 // r2
        r = r1 % r2
        s = s1 - (q * s2)
        t = t1 - (q * t2)
        
        calc_detail = {
            'step': step, 'q': q, 'r1': r1, 'r2': r2, 'r': r,
            's1': s1, 's2': s2, 's': s, 't1': t1, 't2': t2, 't': t
        }
        calculation_steps.append(calc_detail)
        
        lines.append(f" {q:>2}  │ {r1:>4} │ {r2:>4} │ {r:>3} │ {s:>3} │ {t:>3}   Step {step}")
        
        r1, r2 = r2, r
        s1, s2 = s2, s
        t1, t2 = t2, t
        step += 1
    
    lines.append("─" * 45)
    lines.append(f"GCD({e}, {phi}) = {r1}")
    lines.append("")
    
    # Step-by-step calculations with simple dividers
    lines.append("DETAILED CALCULATIONS:")
    lines.append("═" * 55)
    
    for calc in calculation_steps:
        lines.append("")
        lines.append(f"STEP {calc['step']}")
        lines.append("─" * 55)
        lines.append(f"Given: r1={calc['r1']}, r2={calc['r2']}, s1={calc['s1']}, s2={calc['s2']}, t1={calc['t1']}, t2={calc['t2']}")
        lines.append("")
        lines.append("Calculate q (quotient):")
        lines.append(f"  q = r1 ÷ r2 = {calc['r1']} ÷ {calc['r2']} = {calc['q']}")
        lines.append("")
        lines.append("Calculate r (remainder):")
        lines.append(f"  r = r1 - q × r2")
        lines.append(f"  r = {calc['r1']} - {calc['q']} × {calc['r2']}")
        lines.append(f"  r = {calc['r1']} - {calc['q'] * calc['r2']} = {calc['r']}")
        lines.append("")
        lines.append("Calculate s:")
        lines.append(f"  s = s1 - q × s2")
        lines.append(f"  s = {calc['s1']} - {calc['q']} × {calc['s2']}")
        lines.append(f"  s = {calc['s1']} - ({calc['q'] * calc['s2']}) = {calc['s']}")
        lines.append("")
        lines.append("Calculate t:")
        lines.append(f"  t = t1 - q × t2")
        lines.append(f"  t = {calc['t1']} - {calc['q']} × {calc['t2']}")
        lines.append(f"  t = {calc['t1']} - ({calc['q'] * calc['t2']}) = {calc['t']}")
        lines.append("")
        lines.append("Update for next step:")
        lines.append(f"  r1 ← r2 = {calc['r2']},  r2 ← r = {calc['r']}")
        lines.append(f"  s1 ← s2 = {calc['s2']},  s2 ← s = {calc['s']}")
        lines.append(f"  t1 ← t2 = {calc['t2']},  t2 ← t = {calc['t']}")
        lines.append("─" * 55)
    
    lines.append("")
    
    if r1 != 1:
        lines.append("═" * 55)
        lines.append("RESULT: NO INVERSE EXISTS")
        lines.append(f"GCD({e}, {phi}) = {r1} ≠ 1")
        lines.append("═" * 55)
        return None, '\n'.join(lines)
    
    d = t1
    if d < 0:
        lines.append("ADJUSTMENT:")
        lines.append("─" * 40)
        lines.append(f"Coefficient t = {d} is negative")
        lines.append(f"Adjusting: {d} + {phi} = {d + phi}")
        lines.append("─" * 40)
        lines.append("")
        d = d + phi
    
    lines.append("═" * 55)
    lines.append("RESULT")
    lines.append("═" * 55)
    lines.append(f"GCD({e}, {phi}) = 1 ✓")
    lines.append("")
    lines.append(f"★ Private key d = {d}")
    lines.append("")
    lines.append("Verification:")
    lines.append(f"  {e} × {d} mod {phi} = {(e * d) % phi} ✓")
    lines.append("═" * 55)
    
    return d, '\n'.join(lines)

def rsa_encrypt_detailed(p, q, e, m):
    all_sections = []
    input_content = f"Given Parameters:\n  Prime p = {p}\n  Prime q = {q}\n  Public exponent e = {e}\n  Message m = {m}"
    all_sections.append({"section": "Input Parameters", "subsections": [{"title": "Given Values", "content": input_content}]})
    
    n = p * q
    n_content = f"n = p × q\nn = {p} × {q}\nn = {n}"
    all_sections.append({"section": "Calculate n (Modulus)", "subsections": [{"title": "Computation", "content": n_content}]})
    
    phi = (p - 1) * (q - 1)
    phi_content = f"φ(n) = (p - 1) × (q - 1)\nφ({n}) = ({p} - 1) × ({q} - 1)\nφ({n}) = {p-1} × {q-1}\nφ({n}) = {phi}"
    all_sections.append({"section": "Calculate φ(n) - Euler's Totient", "subsections": [{"title": "Computation", "content": phi_content}]})
    
    gcd_val = gcd_func(e, phi)
    gcd_content = f"gcd({e}, {phi}) = {gcd_val}\n\n{'✓ Valid: e and φ(n) are coprime' if gcd_val == 1 else '✗ Invalid'}"
    all_sections.append({"section": "Verify Public Exponent e", "subsections": [{"title": "GCD Check", "content": gcd_content}]})
    
    if gcd_val != 1:
        return {"success": False, "error": f"Invalid e: gcd({e}, {phi}) = {gcd_val}"}
    
    d, d_steps = extended_euclidean_detailed(e, phi)
    all_sections.append({"section": "Calculate Private Key d", "subsections": [{"title": "Extended Euclidean Algorithm", "content": d_steps}]})
    
    keys_content = f"PUBLIC KEY:\n  (e, n) = ({e}, {n})\n\nPRIVATE KEY:\n  (d, n) = ({d}, {n})"
    all_sections.append({"section": "Key Pair Generated", "subsections": [{"title": "Public and Private Keys", "content": keys_content}]})
    
    if m >= n:
        return {"success": False, "error": f"Message m ({m}) must be less than n ({n})"}
    
    c, enc_steps = mod_exp_detailed(m, e, n)
    enc_content = f"Encryption: c = m^e mod n\nc = {m}^{e} mod {n}\n\n{enc_steps}"
    all_sections.append({"section": "Encryption Process", "subsections": [{"title": "Modular Exponentiation", "content": enc_content}]})
    
    m_dec, dec_steps = mod_exp_detailed(c, d, n)
    dec_content = f"Decryption: m = c^d mod n\nm = {c}^{d} mod {n}\n\n{dec_steps}"
    all_sections.append({"section": "Decryption Process", "subsections": [{"title": "Modular Exponentiation", "content": dec_content}]})
    
    result_content = f"RSA COMPLETE\n\nOriginal Message:    m = {m}\nEncrypted Ciphertext: c = {c}\nDecrypted Message:   m = {m_dec}\n\nPublic Key:  (e, n) = ({e}, {n})\nPrivate Key: (d, n) = ({d}, {n})"
    all_sections.append({"section": "Final Result", "subsections": [{"title": "Summary", "content": result_content}]})
    
    return {"success": True, "p": p, "q": q, "n": n, "e": e, "d": d, "m": m, "c": c, "sections": all_sections}


# ========== Hill Cipher Functions ==========

def char_to_num(ch):
    return ord(ch.upper()) - ord('A')

def num_to_char(num):
    return chr((num % 26) + ord('A'))

def determinant(matrix, mod=26):
    n = len(matrix)
    if n == 2:
        return (matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]) % mod
    det = 0
    for j in range(n):
        minor = []
        for i in range(1, n):
            row = [matrix[i][k] for k in range(n) if k != j]
            minor.append(row)
        cofactor = ((-1) ** j) * matrix[0][j] * determinant(minor, mod)
        det += cofactor
    return det % mod

def mod_inverse_26(a, m=26):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def adjugate(matrix):
    n = len(matrix)
    adj = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            minor = []
            for mi in range(n):
                if mi == i:
                    continue
                row = [matrix[mi][mj] for mj in range(n) if mj != j]
                minor.append(row)
            if len(minor) == 1:
                cofactor = minor[0][0]
            elif len(minor) == 2:
                cofactor = minor[0][0] * minor[1][1] - minor[0][1] * minor[1][0]
            else:
                cofactor = determinant(minor)
            adj[j][i] = ((-1) ** (i + j)) * cofactor
    return adj

def format_matrix(matrix, indent=""):
    lines = []
    for row in matrix:
        lines.append(indent + "[ " + "  ".join(f"{x:3}" for x in row) + " ]")
    return '\n'.join(lines)

def hill_cipher_detailed(plaintext, key_matrix, m):
    all_sections = []
    mapping_content = "A=0  B=1  C=2  D=3  E=4  F=5  G=6  H=7  I=8  J=9\nK=10 L=11 M=12 N=13 O=14 P=15 Q=16 R=17 S=18 T=19\nU=20 V=21 W=22 X=23 Y=24 Z=25"
    all_sections.append({"section": "Alphabet Mapping", "subsections": [{"title": "A=0, B=1, ..., Z=25", "content": mapping_content}]})
    
    input_lines = [f"Plaintext: {plaintext}", f"Matrix Size: {m}×{m}", "", "Key Matrix K:", format_matrix(key_matrix, "  ")]
    all_sections.append({"section": "Input Parameters", "subsections": [{"title": "Given Values", "content": '\n'.join(input_lines)}]})
    
    plaintext_nums = [char_to_num(c) for c in plaintext]
    conv_lines = ["Converting each letter:"]
    for c in plaintext:
        conv_lines.append(f"  {c} → {char_to_num(c)}")
    conv_lines.append(f"\nPlaintext Vector P = [{', '.join(map(str, plaintext_nums))}]")
    all_sections.append({"section": "Convert Plaintext to Numbers", "subsections": [{"title": "Character to Number", "content": '\n'.join(conv_lines)}]})
    
    enc_lines = ["Encryption Formula: cᵢ = Σ(kⱼᵢ × pⱼ) mod 26", ""]
    enc_lines.append("For cᵢ, use COLUMN i of key matrix")
    enc_lines.append("")
    cipher_nums = []
    block_count = len(plaintext) // m
    for block in range(block_count):
        block_start = block * m
        P_block = plaintext_nums[block_start:block_start + m]
        enc_lines.append(f"Block {block + 1}: P = [{', '.join(map(str, P_block))}]")
        enc_lines.append("")
        C_block = []
        for i in range(m):
            # Use COLUMN i of key matrix
            products = [f"{key_matrix[j][i]}×{P_block[j]}" for j in range(m)]
            total = sum(key_matrix[j][i] * P_block[j] for j in range(m))
            result = total % 26
            C_block.append(result)
            enc_lines.append(f"  c{i+1} = ({' + '.join(products)}) = {total} mod 26 = {result}")
        cipher_nums.extend(C_block)
        enc_lines.append(f"  Cipher: [{', '.join(map(str, C_block))}]")
        enc_lines.append("")
    all_sections.append({"section": "Encryption", "subsections": [{"title": "Matrix Multiplication", "content": '\n'.join(enc_lines)}]})
    
    ciphertext = ''.join(num_to_char(n) for n in cipher_nums)
    cipher_conv = [f"Cipher numbers: [{', '.join(map(str, cipher_nums))}]", f"Ciphertext = {ciphertext}"]
    all_sections.append({"section": "Convert to Ciphertext", "subsections": [{"title": "Numbers to Letters", "content": '\n'.join(cipher_conv)}]})
    
    det = determinant(key_matrix)
    det = det % 26
    if det < 0:
        det += 26
    all_sections.append({"section": "Determinant", "subsections": [{"title": "det(K) mod 26", "content": f"det(K) mod 26 = {det}"}]})
    
    det_inv = mod_inverse_26(det)
    if det_inv:
        all_sections.append({"section": "Modular Inverse", "subsections": [{"title": f"det⁻¹ mod 26 = {det_inv}", "content": f"{det} × {det_inv} mod 26 = {(det * det_inv) % 26}"}]})
        adj = adjugate(key_matrix)
        K_inv = [[(det_inv * adj[i][j]) % 26 for j in range(m)] for i in range(m)]
        # Ensure positive values
        for i in range(m):
            for j in range(m):
                if K_inv[i][j] < 0:
                    K_inv[i][j] += 26
        
        # Detailed inverse calculation
        inv_lines = []
        inv_lines.append("Formula: [K⁻¹]ᵢⱼ = det⁻¹ × (-1)^(i+j) × Dⱼᵢ mod 26")
        inv_lines.append("")
        inv_lines.append("STEP 1: Calculate Cofactor Matrix C")
        inv_lines.append("─" * 45)
        inv_lines.append("Cᵢⱼ = (-1)^(i+j) × Mᵢⱼ")
        inv_lines.append("")
        
        cofactor_matrix = [[0] * m for _ in range(m)]
        for i in range(m):
            for j in range(m):
                minor = []
                for mi in range(m):
                    if mi == i:
                        continue
                    row = [key_matrix[mi][mj] for mj in range(m) if mj != j]
                    minor.append(row)
                
                inv_lines.append(f"─ M[{i+1},{j+1}] (delete row {i+1}, col {j+1}) ─")
                inv_lines.append("")
                # Display the minor matrix
                for row in minor:
                    inv_lines.append("  [ " + "  ".join(f"{x:3}" for x in row) + " ]")
                inv_lines.append("")
                
                if len(minor) == 1:
                    minor_det = minor[0][0]
                    inv_lines.append(f"  det(M[{i+1},{j+1}]) = {minor_det}")
                elif len(minor) == 2:
                    a, b = minor[0][0], minor[0][1]
                    c, d = minor[1][0], minor[1][1]
                    minor_det = a * d - b * c
                    inv_lines.append(f"  det(M[{i+1},{j+1}]) = ({a}×{d}) - ({b}×{c})")
                    inv_lines.append(f"                = {a*d} - {b*c} = {minor_det}")
                else:
                    minor_det = determinant(minor)
                    inv_lines.append(f"  det(M[{i+1},{j+1}]) = {minor_det}")
                
                sign = ((-1) ** (i + j))
                cofactor = sign * minor_det
                cofactor_matrix[i][j] = cofactor
                sign_str = "+" if sign == 1 else "-"
                inv_lines.append("")
                inv_lines.append(f"  C[{i+1},{j+1}] = (-1)^({i+1}+{j+1}) × det(M[{i+1},{j+1}])")
                inv_lines.append(f"        = ({sign_str}1) × {minor_det} = {cofactor}")
                inv_lines.append("")
        
        inv_lines.append("")
        inv_lines.append("Cofactor Matrix C:")
        inv_lines.append(format_matrix(cofactor_matrix))
        inv_lines.append("")
        inv_lines.append("STEP 2: Adjugate = Transpose of C")
        inv_lines.append("─" * 45)
        inv_lines.append(format_matrix(adj))
        inv_lines.append("")
        inv_lines.append("STEP 3: K⁻¹ = det⁻¹ × adj(K) mod 26")
        inv_lines.append("─" * 45)
        for i in range(m):
            for j in range(m):
                inv_lines.append(f"K⁻¹[{i+1},{j+1}] = {det_inv} × {adj[i][j]} mod 26 = {K_inv[i][j]}")
        inv_lines.append("")
        inv_lines.append("Inverse Matrix K⁻¹:")
        inv_lines.append(format_matrix(K_inv))
        
        all_sections.append({"section": "Inverse Matrix", "subsections": [{"title": "K⁻¹ mod 26", "content": '\n'.join(inv_lines)}]})
        
        dec_lines = ["Decryption Formula: pᵢ = Σ(k⁻¹ⱼᵢ × cⱼ) mod 26", ""]
        dec_lines.append("For pᵢ, use COLUMN i of K⁻¹")
        dec_lines.append("")
        decrypted_nums = []
        for block in range(block_count):
            block_start = block * m
            C_block = cipher_nums[block_start:block_start + m]
            dec_lines.append(f"Block {block + 1}: C = [{', '.join(map(str, C_block))}]")
            dec_lines.append("")
            P_block = []
            for i in range(m):
                # Use COLUMN i of K_inv
                products = [f"{K_inv[j][i]}×{C_block[j]}" for j in range(m)]
                total = sum(K_inv[j][i] * C_block[j] for j in range(m))
                result = total % 26
                P_block.append(result)
                dec_lines.append(f"  p{i+1} = ({' + '.join(products)}) = {total} mod 26 = {result}")
            decrypted_nums.extend(P_block)
            dec_lines.append(f"  Decrypted: [{', '.join(map(str, P_block))}]")
            dec_lines.append("")
        decrypted_text = ''.join(num_to_char(n) for n in decrypted_nums)
        dec_lines.append(f"Decrypted = {decrypted_text}")
        all_sections.append({"section": "Decryption", "subsections": [{"title": "Result", "content": '\n'.join(dec_lines)}]})
    else:
        decrypted_text = "N/A"
    
    result = f"HILL CIPHER COMPLETE\n\nPlaintext:  {plaintext}\nCiphertext: {ciphertext}\nDecrypted:  {decrypted_text}"
    all_sections.append({"section": "Final Result", "subsections": [{"title": "Summary", "content": result}]})
    
    return {"success": True, "plaintext": plaintext, "ciphertext": ciphertext, "sections": all_sections}


# ========== Request Handler ==========

class DevHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory='public', **kwargs)
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            if self.path == '/api/sdes':
                plaintext = data.get('plaintext', '10111101')
                key = data.get('key', '1010000010')
                P10 = data.get('P10', [3,5,2,7,4,10,1,9,8,6])
                P8 = data.get('P8', [6,3,7,4,8,5,10,9])
                IP = data.get('IP', [2,6,3,1,4,8,5,7])
                EP = data.get('EP', [4,1,2,3,2,3,4,1])
                P4 = data.get('P4', [2,4,3,1])
                S0 = data.get('S0', [["01","00","11","10"],["11","10","01","00"],["00","10","01","11"],["11","01","11","10"]])
                S1 = data.get('S1', [["00","01","10","11"],["10","00","01","11"],["11","00","01","00"],["10","01","00","11"]])
                IP_INV = calculate_ip_inverse(IP)
                result = encrypt_with_detailed_steps(plaintext, key, P10, P8, IP, IP_INV, EP, P4, S0, S1)
            
            elif self.path == '/api/rsa':
                p = data.get('p', 17)
                q = data.get('q', 13)
                e = data.get('e', 3)
                m = data.get('m', 9)
                result = rsa_encrypt_detailed(p, q, e, m)
            
            elif self.path == '/api/hill':
                plaintext = data.get('plaintext', 'ACT').upper()
                key_matrix = data.get('keyMatrix', [[6,24,1],[13,16,10],[20,17,15]])
                m = data.get('m', 3)
                result = hill_cipher_detailed(plaintext, key_matrix, m)
            
            elif self.path == '/api/playfair':
                from playfair import playfair_cipher_detailed
                plaintext = data.get('plaintext', 'instruments')
                keyword = data.get('keyword', 'monarchy')
                result = playfair_cipher_detailed(plaintext, keyword)
            
            elif self.path == '/api/monoalphabetic':
                from monoalphabetic import monoalphabetic_cipher_detailed
                plaintext = data.get('plaintext', 'hello')
                mode = data.get('mode', 'additive')
                operation = data.get('operation', 'encrypt')
                key_k = data.get('key_k', 3)
                key_a = data.get('key_a', 5)
                key_b = data.get('key_b', 8)
                result = monoalphabetic_cipher_detailed(plaintext, mode, key_k=key_k, key_a=key_a, key_b=key_b, operation=operation)
            
            elif self.path == '/api/adfgvx':
                from adfgvx import adfgvx_cipher_detailed
                plaintext = data.get('plaintext', 'attackat1200am')
                grid_key = data.get('grid_key', 'privacy')
                trans_key = data.get('trans_key', 'cipher')
                result = adfgvx_cipher_detailed(plaintext, grid_key, trans_key)
            
            elif self.path == '/api/extended-euclidean':
                # Import from the api module
                import importlib.util
                spec = importlib.util.spec_from_file_location("extended_euclidean", os.path.join(os.path.dirname(__file__), 'api', 'extended-euclidean.py'))
                ee_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(ee_module)
                a = int(data.get('a', 5))
                m = int(data.get('m', 192))
                result = ee_module.extended_euclidean_detailed(a, m)
            
            elif self.path == '/api/mod-exp':
                import importlib.util
                spec = importlib.util.spec_from_file_location("mod_exp", os.path.join(os.path.dirname(__file__), 'api', 'mod-exp.py'))
                me_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(me_module)
                a = int(data.get('a', 7))
                n = int(data.get('n', 256))
                m = int(data.get('m', 13))
                result = me_module.mod_exp_detailed(a, n, m)
            
            elif self.path == '/api/gcd':
                import importlib.util
                spec = importlib.util.spec_from_file_location("gcd", os.path.join(os.path.dirname(__file__), 'api', 'gcd.py'))
                gcd_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(gcd_module)
                a = int(data.get('a', 48))
                b = int(data.get('b', 18))
                result = gcd_module.gcd_detailed(a, b)
            
            elif self.path == '/api/euler':
                import importlib.util
                spec = importlib.util.spec_from_file_location("euler", os.path.join(os.path.dirname(__file__), 'api', 'euler.py'))
                euler_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(euler_module)
                base = int(data.get('base', 7))
                exponent = int(data.get('exponent', 256))
                modulus = int(data.get('modulus', 13))
                result = euler_module.euler_theorem_detailed(base, exponent, modulus)
            
            elif self.path == '/api/fermat':
                import importlib.util
                spec = importlib.util.spec_from_file_location("fermat", os.path.join(os.path.dirname(__file__), 'api', 'fermat.py'))
                fermat_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(fermat_module)
                base = int(data.get('base', 3))
                exponent = int(data.get('exponent', 100))
                modulus = int(data.get('modulus', 7))
                result = fermat_module.fermat_theorem_detailed(base, exponent, modulus)
            
            elif self.path == '/api/adfgvx':
                import importlib.util
                spec = importlib.util.spec_from_file_location("adfgvx", os.path.join(os.path.dirname(__file__), 'api', 'adfgvx.py'))
                adfgvx_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(adfgvx_module)
                mode = data.get('mode', 'encrypt')
                poly_key = data.get('polyKey', 'privacy')
                trans_key = data.get('transKey', 'cipher')
                if mode == 'encrypt':
                    plaintext = data.get('plaintext', 'attackat1200am')
                    result = adfgvx_module.encrypt_adfgvx_detailed(plaintext, poly_key, trans_key)
                else:
                    ciphertext = data.get('ciphertext', '')
                    result = adfgvx_module.decrypt_adfgvx_detailed(ciphertext, poly_key, trans_key)
            
            elif self.path == '/api/vigenere':
                import importlib.util
                spec = importlib.util.spec_from_file_location("vigenere", os.path.join(os.path.dirname(__file__), 'api', 'vigenere.py'))
                vigenere_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(vigenere_module)
                mode = data.get('mode', 'encrypt')
                cipher_type = data.get('cipherType', 'vigenere')
                key = data.get('key', 'KEY')
                if cipher_type == 'vigenere':
                    if mode == 'encrypt':
                        plaintext = data.get('plaintext', 'HELLO')
                        result = vigenere_module.vigenere_encrypt_detailed(plaintext, key)
                    else:
                        ciphertext = data.get('ciphertext', '')
                        result = vigenere_module.vigenere_decrypt_detailed(ciphertext, key)
                else:  # autokey
                    if mode == 'encrypt':
                        plaintext = data.get('plaintext', 'HELLO')
                        result = vigenere_module.autokey_encrypt_detailed(plaintext, key)
                    else:
                        ciphertext = data.get('ciphertext', '')
                        result = vigenere_module.autokey_decrypt_detailed(ciphertext, key)
            
            elif self.path == '/api/math-ops':
                import importlib.util
                operation = data.get('operation', 'gcd')
                
                if operation == 'gcd':
                    spec = importlib.util.spec_from_file_location("gcd", os.path.join(os.path.dirname(__file__), 'api', 'gcd.py'))
                    gcd_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(gcd_module)
                    a = int(data.get('a', 48))
                    b = int(data.get('b', 18))
                    result = gcd_module.gcd_detailed(a, b)
                    
                elif operation == 'extended-euclidean':
                    spec = importlib.util.spec_from_file_location("extended_euclidean", os.path.join(os.path.dirname(__file__), 'api', 'extended-euclidean.py'))
                    ee_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(ee_module)
                    a = int(data.get('a', 17))
                    m = int(data.get('m', 26))
                    result = ee_module.extended_euclidean_detailed(a, m)
                    
                elif operation == 'mod-exp':
                    spec = importlib.util.spec_from_file_location("mod_exp", os.path.join(os.path.dirname(__file__), 'api', 'mod-exp.py'))
                    me_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(me_module)
                    a = int(data.get('a', 7))
                    n = int(data.get('n', 256))
                    m = int(data.get('m', 13))
                    result = me_module.mod_exp_detailed(a, n, m)
                    
                elif operation == 'euler':
                    spec = importlib.util.spec_from_file_location("euler", os.path.join(os.path.dirname(__file__), 'api', 'euler.py'))
                    euler_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(euler_module)
                    base = int(data.get('base', 7))
                    exponent = int(data.get('exponent', 256))
                    modulus = int(data.get('modulus', 13))
                    result = euler_module.euler_theorem_detailed(base, exponent, modulus)
                    
                elif operation == 'fermat':
                    spec = importlib.util.spec_from_file_location("fermat", os.path.join(os.path.dirname(__file__), 'api', 'fermat.py'))
                    fermat_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(fermat_module)
                    base = int(data.get('base', 3))
                    exponent = int(data.get('exponent', 100))
                    modulus = int(data.get('modulus', 7))
                    result = fermat_module.fermat_theorem_detailed(base, exponent, modulus)
                    
                else:
                    result = {"success": False, "error": f"Unknown operation: {operation}"}
            
            else:
                self.send_response(404)
                self.end_headers()
                return
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'success': False, 'error': str(e)}).encode('utf-8'))


if __name__ == '__main__':
    PORT = 8000
    with socketserver.TCPServer(("", PORT), DevHandler) as httpd:
        print(f"Cryptography Tools Dev Server running at http://localhost:{PORT}")
        print("Press Ctrl+C to stop")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
