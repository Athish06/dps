from http.server import BaseHTTPRequestHandler
import json

def char_to_num(ch):
    """Convert character to number (A=0, B=1, ... Z=25)"""
    return ord(ch.upper()) - ord('A')

def num_to_char(num):
    """Convert number to character"""
    return chr((num % 26) + ord('A'))

def matrix_multiply(A, B, mod=26):
    """Multiply matrix A with vector B, return result mod 26"""
    n = len(A)
    result = []
    for i in range(n):
        total = 0
        for j in range(n):
            total += A[i][j] * B[j]
        result.append(total % mod)
    return result

def determinant(matrix, mod=26):
    """Calculate determinant of a matrix"""
    n = len(matrix)
    if n == 2:
        return (matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]) % mod
    
    det = 0
    for j in range(n):
        minor = []
        for i in range(1, n):
            row = []
            for k in range(n):
                if k != j:
                    row.append(matrix[i][k])
            minor.append(row)
        cofactor = ((-1) ** j) * matrix[0][j] * determinant(minor, mod)
        det += cofactor
    return det % mod

def mod_inverse(a, m):
    """Find modular inverse of a mod m"""
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def adjugate(matrix):
    """Calculate adjugate (adjoint) matrix"""
    n = len(matrix)
    adj = [[0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            # Get minor
            minor = []
            for mi in range(n):
                if mi == i:
                    continue
                row = []
                for mj in range(n):
                    if mj != j:
                        row.append(matrix[mi][mj])
                minor.append(row)
            
            # Calculate cofactor
            if len(minor) == 1:
                cofactor = minor[0][0]
            elif len(minor) == 2:
                cofactor = minor[0][0] * minor[1][1] - minor[0][1] * minor[1][0]
            else:
                cofactor = determinant(minor)
            
            adj[j][i] = ((-1) ** (i + j)) * cofactor
    
    return adj

def matrix_mod(matrix, mod=26):
    """Apply modulus to all elements of matrix"""
    n = len(matrix)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[i][j] = matrix[i][j] % mod
            if result[i][j] < 0:
                result[i][j] += mod
    return result

def format_matrix(matrix, indent=""):
    """Format matrix for display"""
    lines = []
    for row in matrix:
        lines.append(indent + "[ " + "  ".join(f"{x:3}" for x in row) + " ]")
    return '\n'.join(lines)

def hill_cipher_detailed(plaintext, key_matrix, m):
    """Hill Cipher with detailed steps"""
    all_sections = []
    
    # Section 1: Alphabet Mapping
    mapping_content = """Alphabet to Number Mapping:
A=0   B=1   C=2   D=3   E=4   F=5   G=6   H=7   I=8
J=9   K=10  L=11  M=12  N=13  O=14  P=15  Q=16  R=17
S=18  T=19  U=20  V=21  W=22  X=23  Y=24  Z=25"""
    
    all_sections.append({
        "section": "Alphabet Mapping",
        "subsections": [{"title": "A=0, B=1, ..., Z=25", "content": mapping_content}]
    })
    
    # Section 2: Input Parameters
    input_lines = []
    input_lines.append(f"Plaintext: {plaintext}")
    input_lines.append(f"Matrix Size: {m}×{m}")
    input_lines.append("")
    input_lines.append("Key Matrix K:")
    input_lines.append(format_matrix(key_matrix, "  "))
    
    all_sections.append({
        "section": "Input Parameters",
        "subsections": [{"title": "Given Values", "content": '\n'.join(input_lines)}]
    })
    
    # Section 3: Convert Plaintext to Numbers
    plaintext_nums = [char_to_num(c) for c in plaintext]
    conv_lines = []
    conv_lines.append("Converting each letter to its numeric value:")
    conv_lines.append("")
    for i, c in enumerate(plaintext):
        conv_lines.append(f"  {c} → {char_to_num(c)}")
    conv_lines.append("")
    conv_lines.append(f"Plaintext Vector P = [{', '.join(map(str, plaintext_nums))}]")
    
    all_sections.append({
        "section": "Convert Plaintext to Numbers",
        "subsections": [{"title": "Character to Number", "content": '\n'.join(conv_lines)}]
    })
    
    # Section 4: Encryption - Matrix Multiplication
    enc_lines = []
    enc_lines.append("Encryption Formula: C = K × P (mod 26)")
    enc_lines.append("")
    
    # Process in blocks of m characters
    cipher_nums = []
    block_count = len(plaintext) // m
    
    for block in range(block_count):
        block_start = block * m
        P_block = plaintext_nums[block_start:block_start + m]
        
        enc_lines.append(f"Block {block + 1}: P = [{', '.join(map(str, P_block))}]")
        enc_lines.append("")
        enc_lines.append("Matrix Multiplication:")
        
        C_block = []
        for i in range(m):
            row = key_matrix[i]
            products = [f"{row[j]}×{P_block[j]}" for j in range(m)]
            total = sum(row[j] * P_block[j] for j in range(m))
            result = total % 26
            C_block.append(result)
            enc_lines.append(f"  Row {i+1}: ({' + '.join(products)}) = {total} mod 26 = {result}")
        
        cipher_nums.extend(C_block)
        enc_lines.append("")
        enc_lines.append(f"Block {block + 1} Cipher: [{', '.join(map(str, C_block))}]")
        enc_lines.append("")
    
    all_sections.append({
        "section": "Encryption - Matrix Multiplication",
        "subsections": [{"title": "C = K × P (mod 26)", "content": '\n'.join(enc_lines)}]
    })
    
    # Section 5: Convert to Ciphertext
    ciphertext = ''.join(num_to_char(n) for n in cipher_nums)
    cipher_conv_lines = []
    cipher_conv_lines.append("Converting cipher numbers to letters:")
    cipher_conv_lines.append("")
    for i, n in enumerate(cipher_nums):
        cipher_conv_lines.append(f"  {n} → {num_to_char(n)}")
    cipher_conv_lines.append("")
    cipher_conv_lines.append(f"Ciphertext = {ciphertext}")
    
    all_sections.append({
        "section": "Convert Numbers to Ciphertext",
        "subsections": [{"title": "Number to Character", "content": '\n'.join(cipher_conv_lines)}]
    })
    
    # Section 6: Determinant Calculation
    det = determinant(key_matrix)
    det = det % 26
    if det < 0:
        det += 26
    
    det_lines = []
    det_lines.append("Calculating determinant of Key Matrix:")
    det_lines.append("")
    if m == 2:
        det_lines.append(f"det(K) = ({key_matrix[0][0]}×{key_matrix[1][1]}) - ({key_matrix[0][1]}×{key_matrix[1][0]})")
        det_lines.append(f"det(K) = {key_matrix[0][0]*key_matrix[1][1]} - {key_matrix[0][1]*key_matrix[1][0]}")
    det_lines.append(f"det(K) mod 26 = {det}")
    
    all_sections.append({
        "section": "Calculate Determinant",
        "subsections": [{"title": "det(K)", "content": '\n'.join(det_lines)}]
    })
    
    # Section 7: Modular Inverse of Determinant
    det_inv = mod_inverse(det, 26)
    inv_lines = []
    inv_lines.append(f"Finding modular inverse of {det} mod 26:")
    inv_lines.append(f"We need d such that: {det} × d ≡ 1 (mod 26)")
    inv_lines.append("")
    if det_inv:
        inv_lines.append(f"Checking: {det} × {det_inv} = {det * det_inv}")
        inv_lines.append(f"{det * det_inv} mod 26 = {(det * det_inv) % 26}")
        inv_lines.append("")
        inv_lines.append(f"det⁻¹ mod 26 = {det_inv}")
    else:
        inv_lines.append("No modular inverse exists! Matrix is not invertible mod 26.")
    
    all_sections.append({
        "section": "Modular Inverse of Determinant",
        "subsections": [{"title": "det⁻¹ mod 26", "content": '\n'.join(inv_lines)}]
    })
    
    # Section 8: Inverse Key Matrix (if possible)
    if det_inv:
        adj = adjugate(key_matrix)
        K_inv = matrix_mod([[det_inv * adj[i][j] for j in range(m)] for i in range(m)])
        
        kinv_lines = []
        kinv_lines.append("K⁻¹ = det⁻¹ × adj(K) mod 26")
        kinv_lines.append("")
        kinv_lines.append("Adjugate Matrix adj(K):")
        kinv_lines.append(format_matrix(adj, "  "))
        kinv_lines.append("")
        kinv_lines.append(f"Multiply by det⁻¹ = {det_inv} and apply mod 26:")
        kinv_lines.append("")
        kinv_lines.append("Inverse Key Matrix K⁻¹:")
        kinv_lines.append(format_matrix(K_inv, "  "))
        
        all_sections.append({
            "section": "Calculate Inverse Key Matrix",
            "subsections": [{"title": "K⁻¹ = det⁻¹ × adj(K) mod 26", "content": '\n'.join(kinv_lines)}]
        })
        
        # Section 9: Decryption
        dec_lines = []
        dec_lines.append("Decryption Formula: P = K⁻¹ × C (mod 26)")
        dec_lines.append("")
        
        decrypted_nums = []
        for block in range(block_count):
            block_start = block * m
            C_block = cipher_nums[block_start:block_start + m]
            
            dec_lines.append(f"Block {block + 1}: C = [{', '.join(map(str, C_block))}]")
            dec_lines.append("")
            
            P_block = []
            for i in range(m):
                row = K_inv[i]
                total = sum(row[j] * C_block[j] for j in range(m))
                result = total % 26
                P_block.append(result)
                dec_lines.append(f"  Row {i+1}: result = {total} mod 26 = {result}")
            
            decrypted_nums.extend(P_block)
            dec_lines.append("")
            dec_lines.append(f"Block {block + 1} Decrypted: [{', '.join(map(str, P_block))}]")
            dec_lines.append("")
        
        decrypted_text = ''.join(num_to_char(n) for n in decrypted_nums)
        dec_lines.append(f"Decrypted Text = {decrypted_text}")
        
        all_sections.append({
            "section": "Decryption - Matrix Multiplication",
            "subsections": [{"title": "P = K⁻¹ × C (mod 26)", "content": '\n'.join(dec_lines)}]
        })
    else:
        decrypted_text = "Cannot decrypt - matrix not invertible"
        K_inv = None
    
    # Section 10: Final Result
    result_lines = []
    result_lines.append("HILL CIPHER COMPLETE")
    result_lines.append("")
    result_lines.append(f"Plaintext:   {plaintext}")
    result_lines.append(f"Ciphertext:  {ciphertext}")
    if det_inv:
        result_lines.append(f"Decrypted:   {decrypted_text}")
        result_lines.append("")
        if decrypted_text == plaintext:
            result_lines.append("✓ Verification: Decrypted text matches original!")
        else:
            result_lines.append("✗ Error: Texts don't match!")
    
    all_sections.append({
        "section": "Final Result",
        "subsections": [{"title": "Summary", "content": '\n'.join(result_lines)}]
    })
    
    return {
        "success": True,
        "plaintext": plaintext,
        "ciphertext": ciphertext,
        "decrypted": decrypted_text if det_inv else None,
        "sections": all_sections
    }

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "Hill Cipher API ready"}).encode('utf-8'))
    
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            plaintext = data.get('plaintext', 'ACT').upper()
            key_matrix = data.get('keyMatrix', [[6,24,1],[13,16,10],[20,17,15]])
            m = data.get('m', 3)
            
            # Validate
            if len(plaintext) % m != 0:
                return self.send_error_response(f"Plaintext length ({len(plaintext)}) must be a multiple of {m}")
            
            if len(key_matrix) != m or any(len(row) != m for row in key_matrix):
                return self.send_error_response(f"Key matrix must be {m}×{m}")
            
            result = hill_cipher_detailed(plaintext, key_matrix, m)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode('utf-8'))
            
        except Exception as ex:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'success': False,
                'error': str(ex)
            }).encode('utf-8'))
    
    def send_error_response(self, message):
        self.send_response(400)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({
            'success': False,
            'error': message
        }).encode('utf-8'))