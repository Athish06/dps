from http.server import BaseHTTPRequestHandler
import json

def playfair_cipher_detailed(plaintext, keyword):
    """Playfair cipher with detailed atomic steps"""
    all_sections = []
    
    # Section 1: Input Parameters
    input_content = f"""Original Inputs:
  Keyword: "{keyword}"
  Plaintext: "{plaintext}"

The Playfair cipher uses a 5x5 matrix of letters.
Letters I and J are combined (J → I)."""
    
    all_sections.append({
        "section": "Input Parameters",
        "subsections": [{"title": "Given Values", "content": input_content}]
    })
    
    # Section 2: Convert to lowercase
    lower_lines = ["Converting each character to lowercase:"]
    lower_lines.append("")
    for ch in plaintext:
        if ch.isalpha():
            lower_lines.append(f"  '{ch}' → '{ch.lower()}'")
    plaintext_lower = plaintext.lower()
    keyword_lower = keyword.lower()
    lower_lines.append("")
    lower_lines.append(f"Lowercase Plaintext: \"{plaintext_lower}\"")
    lower_lines.append(f"Lowercase Keyword: \"{keyword_lower}\"")
    
    all_sections.append({
        "section": "Convert to Lowercase",
        "subsections": [{"title": "Case Conversion", "content": '\n'.join(lower_lines)}]
    })
    
    # Section 3: Remove spaces and non-alphabetic characters
    clean_lines = ["Removing spaces and non-alphabetic characters:"]
    clean_lines.append("")
    plaintext_clean = ""
    for ch in plaintext_lower:
        if ch.isalpha():
            plaintext_clean += ch
        elif ch == " ":
            clean_lines.append(f"  Removed space at position {len(plaintext_clean)}")
        else:
            clean_lines.append(f"  Removed '{ch}' at position {len(plaintext_clean)}")
    
    keyword_clean = ""
    for ch in keyword_lower:
        if ch.isalpha():
            keyword_clean += ch
    
    clean_lines.append("")
    clean_lines.append(f"Cleaned Plaintext: \"{plaintext_clean}\"")
    clean_lines.append(f"Cleaned Keyword: \"{keyword_clean}\"")
    
    all_sections.append({
        "section": "Remove Non-Alphabetic Characters",
        "subsections": [{"title": "Cleaning Input", "content": '\n'.join(clean_lines)}]
    })
    
    # Section 4: Replace J with I
    ji_lines = ["In Playfair cipher, I and J share the same cell."]
    ji_lines.append("Replacing all 'j' with 'i':")
    ji_lines.append("")
    
    plaintext_ji = plaintext_clean.replace('j', 'i')
    keyword_ji = keyword_clean.replace('j', 'i')
    
    if 'j' in plaintext_clean:
        ji_lines.append(f"  Plaintext: '{plaintext_clean}' → '{plaintext_ji}'")
    else:
        ji_lines.append(f"  Plaintext: No 'j' found, remains '{plaintext_ji}'")
    
    if 'j' in keyword_clean:
        ji_lines.append(f"  Keyword: '{keyword_clean}' → '{keyword_ji}'")
    else:
        ji_lines.append(f"  Keyword: No 'j' found, remains '{keyword_ji}'")
    
    all_sections.append({
        "section": "Replace J with I",
        "subsections": [{"title": "I/J Substitution", "content": '\n'.join(ji_lines)}]
    })
    
    # Section 5: Prepare digrams (pairs)
    digram_lines = ["Creating digrams (pairs of two letters):"]
    digram_lines.append("")
    digram_lines.append("Rules:")
    digram_lines.append("  1. Split text into pairs of two letters")
    digram_lines.append("  2. If two same letters are adjacent, insert 'x' between them")
    digram_lines.append("  3. If final pair has only one letter, add 'z' as padding")
    digram_lines.append("")
    
    prepared = ""
    i = 0
    step = 1
    while i < len(plaintext_ji):
        char1 = plaintext_ji[i]
        digram_lines.append(f"Step {step}: Read character '{char1}'")
        
        if i + 1 < len(plaintext_ji):
            char2 = plaintext_ji[i + 1]
            if char1 == char2:
                prepared += char1 + 'x'
                digram_lines.append(f"  Next character is '{char2}' (SAME as current)")
                digram_lines.append(f"  → Insert filler 'x' to separate repeated letters")
                digram_lines.append(f"  → Digram: '{char1}x'")
                i += 1
            else:
                prepared += char1 + char2
                digram_lines.append(f"  Next character is '{char2}'")
                digram_lines.append(f"  → Digram: '{char1}{char2}'")
                i += 2
        else:
            prepared += char1 + 'z'
            digram_lines.append(f"  No next character (odd length)")
            digram_lines.append(f"  → Add padding 'z'")
            digram_lines.append(f"  → Digram: '{char1}z'")
            i += 1
        
        step += 1
        digram_lines.append("")
    
    # Show final digrams
    digrams = [prepared[k:k+2] for k in range(0, len(prepared), 2)]
    digram_lines.append(f"Final Prepared Text: \"{prepared}\"")
    digram_lines.append(f"Digrams: {' | '.join(digrams)}")
    
    all_sections.append({
        "section": "Create Digrams (Pairs)",
        "subsections": [{"title": "Pair Formation with Filler Insertion", "content": '\n'.join(digram_lines)}]
    })
    
    # Section 6: Generate 5x5 Key Matrix
    matrix_lines = ["Building 5x5 Playfair Matrix:"]
    matrix_lines.append("")
    matrix_lines.append("Process:")
    matrix_lines.append("  1. Add unique letters from keyword (left to right)")
    matrix_lines.append("  2. Fill remaining cells with unused alphabet letters")
    matrix_lines.append("  3. Skip 'j' (combined with 'i')")
    matrix_lines.append("")
    
    matrix = []
    used = []
    
    matrix_lines.append("Adding keyword letters:")
    for ch in keyword_ji:
        if ch not in used and ch.isalpha():
            used.append(ch)
            matrix.append(ch)
            matrix_lines.append(f"  + '{ch}' added at position {len(used)}")
    
    matrix_lines.append("")
    matrix_lines.append("Adding remaining alphabet letters:")
    for ch in "abcdefghiklmnopqrstuvwxyz":  # no 'j'
        if ch not in used:
            used.append(ch)
            matrix.append(ch)
            matrix_lines.append(f"  + '{ch}' added at position {len(used)}")
    
    # Form 5x5 matrix
    key_matrix = []
    for r in range(5):
        row = matrix[r*5:(r+1)*5]
        key_matrix.append(row)
    
    matrix_lines.append("")
    matrix_lines.append("Final 5×5 Key Matrix:")
    matrix_lines.append("     Col0  Col1  Col2  Col3  Col4")
    for r, row in enumerate(key_matrix):
        matrix_lines.append(f"Row{r}:  {row[0]}     {row[1]}     {row[2]}     {row[3]}     {row[4]}")
    
    all_sections.append({
        "section": "Generate 5×5 Key Matrix",
        "subsections": [{"title": "Matrix Construction", "content": '\n'.join(matrix_lines)}]
    })
    
    # Helper function to find position
    def find_pos(ch):
        if ch == 'j':
            ch = 'i'
        for r in range(5):
            for c in range(5):
                if key_matrix[r][c] == ch:
                    return r, c
        return None, None
    
    # Section 7: Encryption with Rules
    enc_lines = ["Encrypting each digram using Playfair rules:"]
    enc_lines.append("")
    enc_lines.append("Three Rules of Playfair:")
    enc_lines.append("  Rule 1 (Same Row): Take letters to the RIGHT (wrap around)")
    enc_lines.append("  Rule 2 (Same Column): Take letters BELOW (wrap around)")
    enc_lines.append("  Rule 3 (Rectangle): Swap columns, keep rows")
    enc_lines.append("")
    enc_lines.append("-" * 60)
    
    ciphertext = ""
    for idx, (a, b) in enumerate([(prepared[k], prepared[k+1]) for k in range(0, len(prepared), 2)]):
        r1, c1 = find_pos(a)
        r2, c2 = find_pos(b)
        
        enc_lines.append("")
        enc_lines.append(f"Digram {idx + 1}: '{a}{b}'")
        enc_lines.append(f"  Position of '{a}': Row {r1}, Col {c1}")
        enc_lines.append(f"  Position of '{b}': Row {r2}, Col {c2}")
        
        if r1 == r2:
            # Same Row Rule
            enc_a = key_matrix[r1][(c1 + 1) % 5]
            enc_b = key_matrix[r2][(c2 + 1) % 5]
            enc_lines.append("")
            enc_lines.append(f"  ★ RULE 1: SAME ROW (Row {r1})")
            enc_lines.append(f"  Action: Take letter to the RIGHT of each (wrap around)")
            enc_lines.append(f"    '{a}' at Col {c1} → RIGHT → Col {(c1+1)%5} → '{enc_a}'")
            enc_lines.append(f"    '{b}' at Col {c2} → RIGHT → Col {(c2+1)%5} → '{enc_b}'")
        
        elif c1 == c2:
            # Same Column Rule
            enc_a = key_matrix[(r1 + 1) % 5][c1]
            enc_b = key_matrix[(r2 + 1) % 5][c2]
            enc_lines.append("")
            enc_lines.append(f"  ★ RULE 2: SAME COLUMN (Col {c1})")
            enc_lines.append(f"  Action: Take letter BELOW each (wrap around)")
            enc_lines.append(f"    '{a}' at Row {r1} → BELOW → Row {(r1+1)%5} → '{enc_a}'")
            enc_lines.append(f"    '{b}' at Row {r2} → BELOW → Row {(r2+1)%5} → '{enc_b}'")
        
        else:
            # Rectangle Rule
            enc_a = key_matrix[r1][c2]
            enc_b = key_matrix[r2][c1]
            enc_lines.append("")
            enc_lines.append(f"  ★ RULE 3: RECTANGLE (Different Row & Column)")
            enc_lines.append(f"  Action: Stay in same row, swap columns")
            enc_lines.append(f"    '{a}' at (Row {r1}, Col {c1}) → (Row {r1}, Col {c2}) → '{enc_a}'")
            enc_lines.append(f"    '{b}' at (Row {r2}, Col {c2}) → (Row {r2}, Col {c1}) → '{enc_b}'")
        
        ciphertext += enc_a + enc_b
        enc_lines.append(f"  Encrypted Digram: '{enc_a}{enc_b}'")
        enc_lines.append(f"  Ciphertext so far: \"{ciphertext}\"")
    
    all_sections.append({
        "section": "Encryption Process",
        "subsections": [{"title": "Applying Playfair Rules", "content": '\n'.join(enc_lines)}]
    })
    
    # Section 8: Final Result
    result_lines = []
    result_lines.append("PLAYFAIR CIPHER COMPLETE")
    result_lines.append("")
    result_lines.append(f"Original Plaintext:  \"{plaintext}\"")
    result_lines.append(f"Keyword:             \"{keyword}\"")
    result_lines.append(f"Prepared Text:       \"{prepared}\"")
    result_lines.append(f"Digrams:             {' '.join(digrams)}")
    result_lines.append("")
    result_lines.append(f"★ CIPHERTEXT: \"{ciphertext.upper()}\"")
    
    all_sections.append({
        "section": "Final Result",
        "subsections": [{"title": "Summary", "content": '\n'.join(result_lines)}]
    })
    
    return {
        "success": True,
        "plaintext": plaintext,
        "keyword": keyword,
        "prepared": prepared,
        "ciphertext": ciphertext.upper(),
        "matrix": key_matrix,
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
        self.wfile.write(json.dumps({"status": "Playfair Cipher API ready"}).encode('utf-8'))
    
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            plaintext = data.get('plaintext', 'instruments')
            keyword = data.get('keyword', 'monarchy')
            
            result = playfair_cipher_detailed(plaintext, keyword)
            
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