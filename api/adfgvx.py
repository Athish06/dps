from http.server import BaseHTTPRequestHandler
import json

def adfgvx_cipher_detailed(plaintext, grid_key, trans_key):
    """ADFGVX cipher with detailed bilateral substitution and columnar transposition"""
    all_sections = []
    
    # Section 1: Input Parameters
    input_lines = []
    input_lines.append(f"Plaintext: \"{plaintext}\"")
    input_lines.append(f"Polybius Square Key: \"{grid_key}\"")
    input_lines.append(f"Transposition Key: \"{trans_key}\"")
    input_lines.append("")
    input_lines.append("ADFGVX Cipher Overview:")
    input_lines.append("  Step 1: Create 6×6 Polybius Square (substitution table)")
    input_lines.append("  Step 2: Bilateral Substitution (each char → 2 letters from ADFGVX)")
    input_lines.append("  Step 3: Columnar Transposition (rearrange columns by key order)")
    input_lines.append("")
    input_lines.append("The letters A, D, F, G, V, X are used because they are")
    input_lines.append("easily distinguishable in Morse code during WWI.")
    
    all_sections.append({
        "section": "Input Parameters",
        "subsections": [{"title": "Given Values", "content": '\n'.join(input_lines)}]
    })
    
    # Section 2: Generate 6x6 Polybius Square
    alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"
    labels = "ADFGVX"
    
    poly_lines = []
    poly_lines.append("Building 6×6 Polybius Square:")
    poly_lines.append("")
    poly_lines.append("Alphabet used: a-z (26 letters) + 0-9 (10 digits) = 36 characters")
    poly_lines.append("Grid size: 6×6 = 36 cells ✓")
    poly_lines.append("")
    
    # Remove duplicates from key
    key_dedup = ""
    for ch in grid_key.lower():
        if ch in alphabet and ch not in key_dedup:
            key_dedup += ch
    
    poly_lines.append(f"Step 1: Extract unique characters from keyword \"{grid_key}\"")
    poly_lines.append(f"  Unique characters: \"{key_dedup}\"")
    poly_lines.append("")
    
    # Fill remaining
    matrix_str = key_dedup
    for ch in alphabet:
        if ch not in matrix_str:
            matrix_str += ch
    
    poly_lines.append("Step 2: Fill remaining cells with unused alphabet/digits")
    poly_lines.append(f"  Complete sequence: \"{matrix_str}\"")
    poly_lines.append("")
    
    # Create 6x6 grid
    matrix = []
    for i in range(0, 36, 6):
        row = list(matrix_str[i:i+6])
        matrix.append(row)
    
    poly_lines.append("Step 3: Arrange into 6×6 grid")
    poly_lines.append("")
    poly_lines.append("Final Polybius Square:")
    poly_lines.append("        A     D     F     G     V     X")
    poly_lines.append("      " + "-" * 36)
    for i, row in enumerate(matrix):
        poly_lines.append(f"  {labels[i]}  |  {row[0]}  |  {row[1]}  |  {row[2]}  |  {row[3]}  |  {row[4]}  |  {row[5]}  |")
    poly_lines.append("      " + "-" * 36)
    
    all_sections.append({
        "section": "Generate 6×6 Polybius Square",
        "subsections": [{"title": "Substitution Table Construction", "content": '\n'.join(poly_lines)}]
    })
    
    # Section 3: Bilateral Substitution (Fractionation)
    sub_lines = []
    sub_lines.append("BILATERAL SUBSTITUTION (Fractionation)")
    sub_lines.append("")
    sub_lines.append("Each plaintext character is replaced by TWO letters from ADFGVX:")
    sub_lines.append("  - First letter: Row label")
    sub_lines.append("  - Second letter: Column label")
    sub_lines.append("")
    sub_lines.append("This 'fractionates' each character into two parts,")
    sub_lines.append("making frequency analysis much harder!")
    sub_lines.append("")
    sub_lines.append("-" * 50)
    
    fractionated = ""
    for char in plaintext.lower():
        if not char.isalnum():
            continue
        
        # Find position in matrix
        found = False
        for r in range(6):
            for c in range(6):
                if matrix[r][c] == char:
                    row_label = labels[r]
                    col_label = labels[c]
                    pair = row_label + col_label
                    fractionated += pair
                    
                    sub_lines.append("")
                    sub_lines.append(f"Character: '{char}'")
                    sub_lines.append(f"  Position in grid: Row {r} ({row_label}), Column {c} ({col_label})")
                    sub_lines.append(f"  Substitution: '{char}' → '{pair}'")
                    found = True
                    break
            if found:
                break
    
    sub_lines.append("")
    sub_lines.append("-" * 50)
    sub_lines.append("")
    sub_lines.append(f"Fractionated Ciphertext: \"{fractionated}\"")
    sub_lines.append(f"Length: {len(plaintext.replace(' ', ''))} chars → {len(fractionated)} chars (doubled)")
    
    all_sections.append({
        "section": "Bilateral Substitution",
        "subsections": [{"title": "Fractionation Process", "content": '\n'.join(sub_lines)}]
    })
    
    # Section 4: Columnar Transposition - Grid Setup
    trans_lines = []
    trans_lines.append(f"COLUMNAR TRANSPOSITION with Key \"{trans_key}\"")
    trans_lines.append("")
    trans_lines.append("Step 1: Write fractionated text under the key (row by row)")
    trans_lines.append("")
    
    col_len = len(trans_key)
    rows = []
    
    for i in range(0, len(fractionated), col_len):
        chunk = fractionated[i:i+col_len]
        if len(chunk) < col_len:
            padding = "X" * (col_len - len(chunk))
            trans_lines.append(f"  Last row needs padding: '{chunk}' + '{padding}'")
            chunk += padding
        rows.append(list(chunk))
    
    trans_lines.append("")
    trans_lines.append("Transposition Grid:")
    trans_lines.append("")
    
    # Header with key
    header = "      " + "   ".join(list(trans_key.upper()))
    trans_lines.append(header)
    trans_lines.append("      " + "-" * (col_len * 4))
    
    for idx, row in enumerate(rows):
        row_str = "   ".join(row)
        trans_lines.append(f"  R{idx+1}:  {row_str}")
    
    trans_lines.append("      " + "-" * (col_len * 4))
    
    all_sections.append({
        "section": "Columnar Transposition - Grid Setup",
        "subsections": [{"title": "Write Text Under Key", "content": '\n'.join(trans_lines)}]
    })
    
    # Section 5: Column Ordering
    order_lines = []
    order_lines.append("Step 2: Determine column reading order")
    order_lines.append("")
    order_lines.append("Columns are read in ALPHABETICAL order of the key letters")
    order_lines.append("")
    
    # Create list of (key_char, original_index)
    key_indices = [(k, i) for i, k in enumerate(trans_key.upper())]
    sorted_indices = sorted(key_indices, key=lambda x: x[0])
    
    order_lines.append("Key analysis:")
    for i, char in enumerate(trans_key.upper()):
        order_lines.append(f"  Position {i}: '{char}'")
    
    order_lines.append("")
    order_lines.append("Alphabetical sorting:")
    reading_order = []
    for rank, (char, orig_idx) in enumerate(sorted_indices):
        reading_order.append((char, orig_idx))
        order_lines.append(f"  {rank + 1}. '{char}' (original position {orig_idx})")
    
    order_lines.append("")
    order_lines.append(f"Reading order: {' → '.join([f\"'{c}'\" for c, _ in reading_order])}")
    
    all_sections.append({
        "section": "Columnar Transposition - Column Order",
        "subsections": [{"title": "Alphabetical Key Sorting", "content": '\n'.join(order_lines)}]
    })
    
    # Section 6: Read Columns
    read_lines = []
    read_lines.append("Step 3: Read columns in alphabetical key order")
    read_lines.append("")
    
    final_cipher_parts = []
    
    for rank, (char, orig_idx) in enumerate(sorted_indices):
        col_data = ""
        for row in rows:
            col_data += row[orig_idx]
        
        read_lines.append(f"Column {rank + 1}: Key letter '{char}' (position {orig_idx})")
        read_lines.append(f"  Reading top to bottom:")
        for row_idx, row in enumerate(rows):
            read_lines.append(f"    Row {row_idx + 1}: '{row[orig_idx]}'")
        read_lines.append(f"  Column content: \"{col_data}\"")
        read_lines.append("")
        
        final_cipher_parts.append(col_data)
    
    final_ciphertext = ' '.join(final_cipher_parts)
    
    all_sections.append({
        "section": "Columnar Transposition - Read Columns",
        "subsections": [{"title": "Column Extraction", "content": '\n'.join(read_lines)}]
    })
    
    # Section 7: Final Result
    result_lines = []
    result_lines.append("ADFGVX CIPHER COMPLETE")
    result_lines.append("")
    result_lines.append(f"Original Plaintext:     \"{plaintext}\"")
    result_lines.append(f"Polybius Square Key:    \"{grid_key}\"")
    result_lines.append(f"Transposition Key:      \"{trans_key}\"")
    result_lines.append("")
    result_lines.append(f"After Substitution:     \"{fractionated}\"")
    result_lines.append(f"After Transposition:    \"{final_ciphertext}\"")
    result_lines.append("")
    result_lines.append(f"★ FINAL CIPHERTEXT: {final_ciphertext}")
    result_lines.append("")
    result_lines.append("Security Notes:")
    result_lines.append("  1. Fractionation breaks frequency patterns")
    result_lines.append("  2. Transposition scrambles position information")
    result_lines.append("  3. Combined, these make cryptanalysis very difficult")
    
    all_sections.append({
        "section": "Final Result",
        "subsections": [{"title": "Summary", "content": '\n'.join(result_lines)}]
    })
    
    return {
        "success": True,
        "plaintext": plaintext,
        "grid_key": grid_key,
        "trans_key": trans_key,
        "fractionated": fractionated,
        "ciphertext": final_ciphertext,
        "matrix": matrix,
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
        self.wfile.write(json.dumps({"status": "ADFGVX Cipher API ready"}).encode('utf-8'))
    
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            plaintext = data.get('plaintext', 'attackat1200am')
            grid_key = data.get('grid_key', 'privacy')
            trans_key = data.get('trans_key', 'cipher')
            
            result = adfgvx_cipher_detailed(plaintext, grid_key, trans_key)
            
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