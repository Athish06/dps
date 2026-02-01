from http.server import BaseHTTPRequestHandler
import json
import math

def generate_polybius_square_detailed(keyword):
    """Generate 6x6 Polybius square with detailed steps"""
    lines = []
    lines.append("═" * 60)
    lines.append("POLYBIUS SQUARE GENERATION (6×6 Grid)")
    lines.append("═" * 60)
    lines.append("")
    lines.append("ADFGVX uses a 6×6 grid containing:")
    lines.append("  • 26 letters (a-z)")
    lines.append("  • 10 digits (0-9)")
    lines.append("  • Total: 36 characters")
    lines.append("")
    lines.append("Row/Column headers: A, D, F, G, V, X")
    lines.append("(Chosen because they sound distinct in Morse code)")
    lines.append("")
    lines.append("─" * 60)
    lines.append("")
    
    # Define alphabet
    alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"
    
    # Clean keyword
    lines.append(f"Step 1: Process keyword '{keyword}'")
    key_clean = ""
    for char in keyword.lower():
        if char in alphabet and char not in key_clean:
            key_clean += char
    
    lines.append(f"  Remove duplicates: '{key_clean}'")
    lines.append("")
    
    # Fill grid content
    lines.append("Step 2: Fill grid with keyword first, then remaining characters")
    grid_content = key_clean
    remaining = ""
    for char in alphabet:
        if char not in key_clean:
            remaining += char
            grid_content += char
    
    lines.append(f"  Keyword chars: {key_clean}")
    lines.append(f"  Remaining: {remaining[:20]}..." if len(remaining) > 20 else f"  Remaining: {remaining}")
    lines.append(f"  Full grid order: {grid_content}")
    lines.append("")
    
    # Create mappings
    headers = "ADFGVX"
    char_to_coords = {}
    coords_to_char = {}
    
    # Display the grid
    lines.append("Step 3: Create the 6×6 grid")
    lines.append("")
    lines.append("      A   D   F   G   V   X")
    lines.append("    ┌───┬───┬───┬───┬───┬───┐")
    
    index = 0
    for r in range(6):
        row_chars = []
        for c in range(6):
            char = grid_content[index]
            pair = headers[r] + headers[c]
            char_to_coords[char] = pair
            coords_to_char[pair] = char
            row_chars.append(char)
            index += 1
        
        row_display = " │ ".join(row_chars)
        lines.append(f"  {headers[r]} │ {row_display} │")
        if r < 5:
            lines.append("    ├───┼───┼───┼───┼───┼───┤")
    
    lines.append("    └───┴───┴───┴───┴───┴───┘")
    lines.append("")
    
    return char_to_coords, coords_to_char, '\n'.join(lines), grid_content


def encrypt_adfgvx_detailed(plaintext, poly_key, trans_key):
    """ADFGVX Encryption with detailed atomic steps"""
    all_sections = []
    
    # Section 1: Input Parameters
    input_content = f"""Plaintext: {plaintext}
Polybius Key: {poly_key}
Transposition Key: {trans_key}

ADFGVX Cipher Overview:
  Phase 1: Substitution (Fractionation)
    - Each character → pair of ADFGVX letters
    - Message length doubles
  
  Phase 2: Transposition (Columnar)
    - Write fractionated text in columns
    - Reorder columns alphabetically by key
    - Read columns vertically"""
    
    all_sections.append({
        "section": "Input Parameters",
        "subsections": [{"title": "ADFGVX Cipher Settings", "content": input_content}]
    })
    
    # Section 2: Polybius Square Generation
    char_map, coords_map, grid_detail, grid_content = generate_polybius_square_detailed(poly_key)
    
    all_sections.append({
        "section": "Phase 1A: Polybius Square",
        "subsections": [{"title": "6×6 Grid Generation", "content": grid_detail}]
    })
    
    # Section 3: Fractionation (Substitution)
    sub_lines = []
    sub_lines.append("═" * 60)
    sub_lines.append("PHASE 1B: FRACTIONATION (SUBSTITUTION)")
    sub_lines.append("═" * 60)
    sub_lines.append("")
    sub_lines.append("Each plaintext character is replaced by its ADFGVX coordinate pair.")
    sub_lines.append("")
    sub_lines.append("─" * 60)
    sub_lines.append("")
    
    # Clean plaintext
    clean_plain = "".join([c for c in plaintext.lower() if c.isalnum()])
    sub_lines.append(f"Original: '{plaintext}'")
    sub_lines.append(f"Cleaned (alphanumeric only): '{clean_plain}'")
    sub_lines.append("")
    sub_lines.append("Character-by-character substitution:")
    sub_lines.append("")
    
    fractionated_text = ""
    for i, char in enumerate(clean_plain):
        if char in char_map:
            pair = char_map[char]
            fractionated_text += pair
            sub_lines.append(f"  '{char}' → Look up in grid → Row {pair[0]}, Col {pair[1]} → '{pair}'")
    
    sub_lines.append("")
    sub_lines.append("─" * 60)
    sub_lines.append("")
    sub_lines.append(f"<b>Fractionated text: {fractionated_text}</b>")
    sub_lines.append(f"  Length: {len(clean_plain)} chars → {len(fractionated_text)} chars (doubled)")
    sub_lines.append("")
    
    all_sections.append({
        "section": "Phase 1B: Fractionation",
        "subsections": [{"title": "Character Substitution", "content": '\n'.join(sub_lines)}]
    })
    
    # Section 4: Transposition
    trans_lines = []
    trans_lines.append("═" * 60)
    trans_lines.append("PHASE 2: COLUMNAR TRANSPOSITION")
    trans_lines.append("═" * 60)
    trans_lines.append("")
    trans_lines.append(f"Transposition Key: '{trans_key}' (length = {len(trans_key)})")
    trans_lines.append("")
    trans_lines.append("─" * 60)
    trans_lines.append("")
    
    # Create columns
    key_len = len(trans_key)
    columns = {k_index: "" for k_index in range(key_len)}
    
    trans_lines.append("Step 1: Write fractionated text row-by-row under the key")
    trans_lines.append("")
    
    # Fill columns
    for i, char in enumerate(fractionated_text):
        col_idx = i % key_len
        columns[col_idx] += char
    
    # Display the matrix
    num_rows = math.ceil(len(fractionated_text) / key_len)
    trans_lines.append("  " + "   ".join(list(trans_key.upper())))
    trans_lines.append("  " + "─" * (key_len * 4))
    
    for r in range(num_rows):
        row_chars = []
        for c in range(key_len):
            idx = r * key_len + c
            if idx < len(fractionated_text):
                row_chars.append(fractionated_text[idx])
            else:
                row_chars.append(" ")
        trans_lines.append("  " + "   ".join(row_chars))
    
    trans_lines.append("")
    trans_lines.append("─" * 60)
    trans_lines.append("")
    
    # Sort columns
    trans_lines.append("Step 2: Determine alphabetical order of key")
    key_order = sorted([(char, i) for i, char in enumerate(trans_key.upper())])
    
    trans_lines.append(f"  Key: {trans_key.upper()}")
    trans_lines.append(f"  Sorted: {' → '.join([f'{c}(col {i})' for c, i in key_order])}")
    trans_lines.append("")
    
    # Read columns in sorted order
    trans_lines.append("Step 3: Read columns vertically in alphabetical order")
    trans_lines.append("")
    
    ciphertext_parts = []
    for key_char, original_idx in key_order:
        col_content = columns[original_idx]
        ciphertext_parts.append(col_content)
        trans_lines.append(f"  Column '{key_char}' (position {original_idx}): {col_content}")
    
    ciphertext = " ".join(ciphertext_parts)
    
    trans_lines.append("")
    trans_lines.append("─" * 60)
    trans_lines.append("")
    trans_lines.append(f"<b>★ CIPHERTEXT: {ciphertext}</b>")
    trans_lines.append("")
    
    all_sections.append({
        "section": "Phase 2: Transposition",
        "subsections": [{"title": "Columnar Rearrangement", "content": '\n'.join(trans_lines)}]
    })
    
    return {
        "success": True,
        "mode": "encrypt",
        "ciphertext": ciphertext,
        "fractionated": fractionated_text,
        "sections": all_sections
    }


def decrypt_adfgvx_detailed(ciphertext, poly_key, trans_key):
    """ADFGVX Decryption with detailed atomic steps"""
    all_sections = []
    
    # Section 1: Input Parameters
    input_content = f"""Ciphertext: {ciphertext}
Polybius Key: {poly_key}
Transposition Key: {trans_key}

Decryption Process (Reverse Order):
  Phase 1: Undo Transposition
    - Reconstruct columns from sorted order
    - Handle ragged columns (unequal heights)
  
  Phase 2: Undo Substitution
    - Convert ADFGVX pairs back to characters"""
    
    all_sections.append({
        "section": "Input Parameters",
        "subsections": [{"title": "ADFGVX Decryption Settings", "content": input_content}]
    })
    
    # Section 2: Polybius Square
    char_map, coords_map, grid_detail, grid_content = generate_polybius_square_detailed(poly_key)
    
    all_sections.append({
        "section": "Step 1: Polybius Square",
        "subsections": [{"title": "6×6 Grid (same as encryption)", "content": grid_detail}]
    })
    
    # Section 3: Undo Transposition
    trans_lines = []
    trans_lines.append("═" * 60)
    trans_lines.append("PHASE 1: UNDO TRANSPOSITION")
    trans_lines.append("═" * 60)
    trans_lines.append("")
    
    # Clean ciphertext
    clean_cipher = ciphertext.replace(" ", "")
    trans_lines.append(f"Ciphertext: '{ciphertext}'")
    trans_lines.append(f"Cleaned: '{clean_cipher}' (length = {len(clean_cipher)})")
    trans_lines.append("")
    trans_lines.append("─" * 60)
    trans_lines.append("")
    
    msg_len = len(clean_cipher)
    key_len = len(trans_key)
    
    # Calculate column heights
    col_height = msg_len // key_len
    remainder = msg_len % key_len
    
    trans_lines.append("Step 1: Calculate column heights")
    trans_lines.append(f"  Message length: {msg_len}")
    trans_lines.append(f"  Key length: {key_len}")
    trans_lines.append(f"  Base height: {msg_len} ÷ {key_len} = {col_height}")
    trans_lines.append(f"  Remainder: {msg_len} mod {key_len} = {remainder}")
    trans_lines.append("")
    trans_lines.append(f"  First {remainder} columns get {col_height + 1} chars")
    trans_lines.append(f"  Remaining {key_len - remainder} columns get {col_height} chars")
    trans_lines.append("")
    trans_lines.append("─" * 60)
    trans_lines.append("")
    
    # Determine key order
    key_order = sorted([(char, i) for i, char in enumerate(trans_key.upper())])
    
    trans_lines.append("Step 2: Determine column reading order (alphabetical)")
    trans_lines.append(f"  Key: {trans_key.upper()}")
    trans_lines.append(f"  Alphabetical order: {' → '.join([f'{c}(pos {i})' for c, i in key_order])}")
    trans_lines.append("")
    
    # Reconstruct columns
    trans_lines.append("Step 3: Slice ciphertext into columns (in alphabetical order)")
    trans_lines.append("")
    
    reconstructed_cols = {}
    current_idx = 0
    
    for key_char, original_idx in key_order:
        # Extra char if original_idx < remainder
        current_col_height = col_height + (1 if original_idx < remainder else 0)
        segment = clean_cipher[current_idx : current_idx + current_col_height]
        reconstructed_cols[original_idx] = segment
        
        trans_lines.append(f"  Column '{key_char}' (original pos {original_idx}):")
        trans_lines.append(f"    Height: {current_col_height}")
        trans_lines.append(f"    Content: '{segment}'")
        current_idx += current_col_height
    
    trans_lines.append("")
    trans_lines.append("─" * 60)
    trans_lines.append("")
    
    # Read row by row
    trans_lines.append("Step 4: Read row-by-row to get fractionated text")
    trans_lines.append("")
    
    fractionated_text = ""
    num_rows = math.ceil(msg_len / key_len)
    
    for r in range(num_rows):
        row_chars = ""
        for c in range(key_len):
            if r < len(reconstructed_cols[c]):
                row_chars += reconstructed_cols[c][r]
        trans_lines.append(f"  Row {r + 1}: {row_chars}")
        fractionated_text += row_chars
    
    trans_lines.append("")
    trans_lines.append(f"<b>Recovered fractionated text: {fractionated_text}</b>")
    trans_lines.append("")
    
    all_sections.append({
        "section": "Phase 1: Undo Transposition",
        "subsections": [{"title": "Reconstruct Original Order", "content": '\n'.join(trans_lines)}]
    })
    
    # Section 4: Undo Substitution
    sub_lines = []
    sub_lines.append("═" * 60)
    sub_lines.append("PHASE 2: UNDO SUBSTITUTION")
    sub_lines.append("═" * 60)
    sub_lines.append("")
    sub_lines.append("Convert ADFGVX pairs back to original characters.")
    sub_lines.append("")
    sub_lines.append("─" * 60)
    sub_lines.append("")
    
    plaintext = ""
    sub_lines.append("Pair-by-pair conversion:")
    sub_lines.append("")
    
    for i in range(0, len(fractionated_text), 2):
        pair = fractionated_text[i : i + 2]
        if pair in coords_map:
            char = coords_map[pair]
            plaintext += char
            sub_lines.append(f"  '{pair}' → Row {pair[0]}, Col {pair[1]} → '{char}'")
    
    sub_lines.append("")
    sub_lines.append("─" * 60)
    sub_lines.append("")
    sub_lines.append(f"<b>★ PLAINTEXT: {plaintext}</b>")
    sub_lines.append("")
    
    all_sections.append({
        "section": "Phase 2: Undo Substitution",
        "subsections": [{"title": "Recover Original Characters", "content": '\n'.join(sub_lines)}]
    })
    
    return {
        "success": True,
        "mode": "decrypt",
        "plaintext": plaintext,
        "fractionated": fractionated_text,
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
            
            mode = data.get('mode', 'encrypt')
            poly_key = data.get('polyKey', 'privacy')
            trans_key = data.get('transKey', 'cipher')
            
            if mode == 'encrypt':
                plaintext = data.get('plaintext', 'attackat1200am')
                result = encrypt_adfgvx_detailed(plaintext, poly_key, trans_key)
            else:
                ciphertext = data.get('ciphertext', '')
                result = decrypt_adfgvx_detailed(ciphertext, poly_key, trans_key)
            
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