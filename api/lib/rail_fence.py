from http.server import BaseHTTPRequestHandler
import json

def rail_fence_encrypt_detailed(plaintext, num_rails):
    """Rail Fence Cipher Encryption with detailed steps"""
    all_sections = []
    
    # Clean plaintext
    text = plaintext.upper().replace(" ", "")
    n = len(text)
    
    # Section 1: Input Parameters
    input_lines = []
    input_lines.append(f"Plaintext: \"{plaintext}\"")
    input_lines.append(f"Cleaned Text: \"{text}\"")
    input_lines.append(f"Text Length: {n}")
    input_lines.append(f"Number of Rails: {num_rails}")
    input_lines.append("")
    input_lines.append("Rail Fence Cipher:")
    input_lines.append("  - Write plaintext diagonally down and up across rails")
    input_lines.append("  - Read off each rail from top to bottom to get ciphertext")
    
    all_sections.append({
        "section": "Input Parameters",
        "subsections": [{"title": "Given Values", "content": '\n'.join(input_lines)}]
    })
    
    # Section 2: Create the Zig-Zag Pattern
    pattern_lines = []
    pattern_lines.append("Creating the zig-zag pattern by writing characters diagonally:")
    pattern_lines.append("")
    
    # Create empty rails
    rails = [['.' for _ in range(n)] for _ in range(num_rails)]
    
    # Fill the rails in zig-zag pattern
    rail = 0
    direction = 1  # 1 = down, -1 = up
    
    rail_positions = []  # Track which rail each character goes to
    
    for i, char in enumerate(text):
        rails[rail][i] = char
        rail_positions.append(rail)
        
        # Change direction at top or bottom rail
        if rail == 0:
            direction = 1
        elif rail == num_rails - 1:
            direction = -1
        
        rail += direction
    
    # Display the zig-zag pattern with position tracking
    pattern_lines.append("Step-by-step character placement:")
    pattern_lines.append("")
    for i, char in enumerate(text):
        pattern_lines.append(f"  Position {i+1}: '{char}' → Rail {rail_positions[i] + 1}")
    
    pattern_lines.append("")
    pattern_lines.append("─" * 50)
    pattern_lines.append("")
    
    # Display the visual grid
    pattern_lines.append("Visual Zig-Zag Pattern:")
    pattern_lines.append("")
    
    # Create a visual representation
    for r in range(num_rails):
        rail_str = f"Rail {r+1}: "
        for c in range(n):
            rail_str += rails[r][c] + " "
        pattern_lines.append(rail_str)
    
    all_sections.append({
        "section": "Zig-Zag Pattern Construction",
        "subsections": [{"title": "Building the Rail Fence", "content": '\n'.join(pattern_lines)}]
    })
    
    # Section 3: Reading the Rails
    read_lines = []
    read_lines.append("Reading each rail from left to right:")
    read_lines.append("")
    
    ciphertext = ""
    for r in range(num_rails):
        rail_chars = ""
        for c in range(n):
            if rails[r][c] != '.':
                rail_chars += rails[r][c]
        
        read_lines.append(f"Rail {r+1}: {rail_chars}")
        ciphertext += rail_chars
    
    read_lines.append("")
    read_lines.append("─" * 50)
    read_lines.append(f"Concatenating all rails: {ciphertext}")
    
    all_sections.append({
        "section": "Reading Rails",
        "subsections": [{"title": "Extracting Ciphertext", "content": '\n'.join(read_lines)}]
    })
    
    # Section 4: Final Result
    result_lines = []
    result_lines.append("RAIL FENCE ENCRYPTION COMPLETE")
    result_lines.append("")
    result_lines.append(f"Input Plaintext:  \"{text}\"")
    result_lines.append(f"Number of Rails:  {num_rails}")
    result_lines.append(f"Output Ciphertext: \"{ciphertext}\"")
    
    all_sections.append({
        "section": "Final Result",
        "subsections": [{"title": "Summary", "content": '\n'.join(result_lines)}]
    })
    
    return {
        "success": True,
        "plaintext": text,
        "ciphertext": ciphertext,
        "num_rails": num_rails,
        "mode": "encrypt",
        "sections": all_sections
    }


def rail_fence_decrypt_detailed(ciphertext, num_rails):
    """Rail Fence Cipher Decryption with detailed steps"""
    all_sections = []
    
    # Clean ciphertext
    text = ciphertext.upper().replace(" ", "")
    n = len(text)
    
    # Section 1: Input Parameters
    input_lines = []
    input_lines.append(f"Ciphertext: \"{ciphertext}\"")
    input_lines.append(f"Cleaned Text: \"{text}\"")
    input_lines.append(f"Text Length: {n}")
    input_lines.append(f"Number of Rails: {num_rails}")
    input_lines.append("")
    input_lines.append("Decryption Process:")
    input_lines.append("  1. Determine how many characters go on each rail")
    input_lines.append("  2. Fill the rails with ciphertext characters")
    input_lines.append("  3. Read diagonally in zig-zag pattern")
    
    all_sections.append({
        "section": "Input Parameters",
        "subsections": [{"title": "Given Values", "content": '\n'.join(input_lines)}]
    })
    
    # Section 2: Calculate characters per rail
    calc_lines = []
    calc_lines.append("Step 1: Calculate how many characters belong to each rail")
    calc_lines.append("")
    calc_lines.append("Simulating the zig-zag pattern to count positions per rail:")
    calc_lines.append("")
    
    # Count characters per rail by simulating the zig-zag
    rail_counts = [0] * num_rails
    rail = 0
    direction = 1
    rail_order = []  # Track the order of rails visited
    
    for i in range(n):
        rail_counts[rail] += 1
        rail_order.append(rail)
        
        if rail == 0:
            direction = 1
        elif rail == num_rails - 1:
            direction = -1
        
        rail += direction
    
    for r in range(num_rails):
        calc_lines.append(f"  Rail {r+1}: {rail_counts[r]} characters")
    
    calc_lines.append("")
    calc_lines.append(f"Total: {sum(rail_counts)} characters (matches ciphertext length)")
    
    all_sections.append({
        "section": "Character Distribution",
        "subsections": [{"title": "Characters per Rail", "content": '\n'.join(calc_lines)}]
    })
    
    # Section 3: Fill the rails with ciphertext
    fill_lines = []
    fill_lines.append("Step 2: Distribute ciphertext characters to rails")
    fill_lines.append("")
    
    # Create rails array
    rails = [['.' for _ in range(n)] for _ in range(num_rails)]
    
    # Mark positions in each rail
    rail = 0
    direction = 1
    for i in range(n):
        rails[rail][i] = '*'  # Mark position
        
        if rail == 0:
            direction = 1
        elif rail == num_rails - 1:
            direction = -1
        
        rail += direction
    
    # Fill rails with ciphertext characters
    idx = 0
    rail_contents = []
    for r in range(num_rails):
        rail_chars = ""
        start_idx = idx
        for c in range(n):
            if rails[r][c] == '*':
                rails[r][c] = text[idx]
                rail_chars += text[idx]
                idx += 1
        rail_contents.append(rail_chars)
        fill_lines.append(f"Rail {r+1} gets: \"{rail_chars}\" (positions {start_idx+1}-{idx})")
    
    fill_lines.append("")
    fill_lines.append("Filled rail fence grid:")
    fill_lines.append("")
    
    for r in range(num_rails):
        rail_str = f"Rail {r+1}: "
        for c in range(n):
            rail_str += rails[r][c] + " "
        fill_lines.append(rail_str)
    
    all_sections.append({
        "section": "Filling Rails",
        "subsections": [{"title": "Distributing Ciphertext", "content": '\n'.join(fill_lines)}]
    })
    
    # Section 4: Read in zig-zag order
    read_lines = []
    read_lines.append("Step 3: Read diagonally in zig-zag pattern")
    read_lines.append("")
    
    plaintext = ""
    rail = 0
    direction = 1
    
    read_lines.append("Reading order:")
    read_lines.append("")
    
    for i in range(n):
        char = rails[rail][i]
        plaintext += char
        read_lines.append(f"  Position {i+1}: Rail {rail+1}, Column {i+1} → '{char}'")
        
        if rail == 0:
            direction = 1
        elif rail == num_rails - 1:
            direction = -1
        
        rail += direction
    
    read_lines.append("")
    read_lines.append("─" * 50)
    read_lines.append(f"Reconstructed Plaintext: {plaintext}")
    
    all_sections.append({
        "section": "Reading Zig-Zag",
        "subsections": [{"title": "Reconstructing Plaintext", "content": '\n'.join(read_lines)}]
    })
    
    # Section 5: Final Result
    result_lines = []
    result_lines.append("RAIL FENCE DECRYPTION COMPLETE")
    result_lines.append("")
    result_lines.append(f"Input Ciphertext:  \"{text}\"")
    result_lines.append(f"Number of Rails:   {num_rails}")
    result_lines.append(f"Output Plaintext:  \"{plaintext}\"")
    
    all_sections.append({
        "section": "Final Result",
        "subsections": [{"title": "Summary", "content": '\n'.join(result_lines)}]
    })
    
    return {
        "success": True,
        "ciphertext": text,
        "plaintext": plaintext,
        "num_rails": num_rails,
        "mode": "decrypt",
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
        self.wfile.write(json.dumps({"status": "Rail Fence Cipher API ready"}).encode('utf-8'))
    
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            mode = data.get('mode', 'encrypt')
            num_rails = int(data.get('numRails', 3))
            
            if mode == 'encrypt':
                plaintext = data.get('plaintext', 'WEAREDISCOVEREDFLEEATONCE')
                result = rail_fence_encrypt_detailed(plaintext, num_rails)
            else:
                ciphertext = data.get('ciphertext', '')
                result = rail_fence_decrypt_detailed(ciphertext, num_rails)
            
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