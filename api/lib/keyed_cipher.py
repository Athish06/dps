from http.server import BaseHTTPRequestHandler
import json
import math

def get_key_order(keyword):
    """
    Calculate column read order from keyword using alphabetical ranking.
    Tie-breaker: left-to-right order for duplicate letters.
    Returns: list of (original_index, rank) and the sorted order
    """
    indexed = [(i, char) for i, char in enumerate(keyword.upper())]
    # Sort by character, then by original index (stable sort)
    sorted_indexed = sorted(indexed, key=lambda x: (x[1], x[0]))
    
    # Create rank array: rank[original_index] = read_position (1-indexed)
    rank = [0] * len(keyword)
    for read_pos, (orig_idx, char) in enumerate(sorted_indexed):
        rank[orig_idx] = read_pos + 1  # 1-indexed
    
    # Read order: which original column to read at each step
    read_order = [item[0] for item in sorted_indexed]
    
    return rank, read_order


def keyed_encrypt_detailed(plaintext, keyword, column_order=None):
    """Keyed Columnar Transposition Cipher Encryption with detailed steps"""
    all_sections = []
    
    # Clean plaintext
    text = plaintext.upper().replace(" ", "").replace("_", "")
    text = ''.join(c for c in text if c.isalpha())
    keyword = keyword.upper()
    
    # Section 1: Input Parameters
    input_lines = []
    input_lines.append(f"Plaintext: \"{plaintext}\"")
    input_lines.append(f"Cleaned Text: \"{text}\"")
    input_lines.append(f"Text Length: {len(text)}")
    input_lines.append(f"Keyword: \"{keyword}\"")
    input_lines.append(f"Keyword Length: {len(keyword)}")
    input_lines.append("")
    input_lines.append("Keyed Columnar Transposition Cipher:")
    input_lines.append("  1. Determine column order from keyword (or use custom order)")
    input_lines.append("  2. Write plaintext row-by-row into grid")
    input_lines.append("  3. Read columns in the sorted order")
    
    all_sections.append({
        "section": "Input Parameters",
        "subsections": [{"title": "Given Values", "content": '\n'.join(input_lines)}]
    })
    
    # Section 2: Key Order Calculation
    # Use custom column_order if provided, otherwise calculate from keyword
    if column_order and len(column_order) == len(keyword):
        # User provided custom column order (1-indexed ranks)
        rank = column_order
        # Convert rank to read_order: read_order[i] = column to read at step i
        # Sort columns by their rank to get read order
        indexed_ranks = list(enumerate(rank))
        sorted_by_rank = sorted(indexed_ranks, key=lambda x: x[1])
        read_order = [item[0] for item in sorted_by_rank]
        using_custom = True
    else:
        rank, read_order = get_key_order(keyword)
        using_custom = False
    
    key_lines = []
    key_lines.append("Step 1: Determine column read order")
    key_lines.append("")
    
    if using_custom:
        key_lines.append("Using CUSTOM column order provided by user:")
        key_lines.append(f"  Rank values: {rank}")
    else:
        key_lines.append("Calculating from keyword (alphabetical ranking):")
        key_lines.append("")
        key_lines.append("Keyword letters with original positions:")
        for i, char in enumerate(keyword):
            key_lines.append(f"  Position {i+1}: '{char}'")
        key_lines.append("")
        key_lines.append("Alphabetical ranking (with left-to-right tie-breaker):")
        sorted_chars = sorted(enumerate(keyword), key=lambda x: (x[1], x[0]))
        for read_pos, (orig_idx, char) in enumerate(sorted_chars):
            key_lines.append(f"  Rank {read_pos+1}: '{char}' (original position {orig_idx+1})")
    
    key_lines.append("")
    key_lines.append("─" * 50)
    key_lines.append("")
    key_lines.append("Column Read Order (by original position):")
    
    header = "  Keyword:  " + "  ".join(f"{c:>3}" for c in keyword)
    rank_row = "  Rank:     " + "  ".join(f"{r:>3}" for r in rank)
    key_lines.append(header)
    key_lines.append(rank_row)
    key_lines.append("")
    key_lines.append(f"Read order: {[r+1 for r in read_order]}")
    key_lines.append("(Columns are read in this order: " + 
                    " → ".join(f"Col {r+1} ({keyword[r]})" for r in read_order) + ")")
    
    all_sections.append({
        "section": "Key Order Calculation",
        "subsections": [{"title": "Determining Column Read Order", "content": '\n'.join(key_lines)}]
    })
    
    # Section 3: Grid Construction
    col_count = len(keyword)
    row_count = math.ceil(len(text) / col_count)
    
    # Pad text
    padding_needed = row_count * col_count - len(text)
    padded_text = text + 'X' * padding_needed
    
    grid_lines = []
    grid_lines.append("Step 2: Construct the grid")
    grid_lines.append("")
    grid_lines.append(f"Grid Dimensions: {row_count} rows × {col_count} columns")
    grid_lines.append(f"Total cells: {row_count * col_count}")
    grid_lines.append(f"Plaintext length: {len(text)}")
    if padding_needed > 0:
        grid_lines.append(f"Padding needed: {padding_needed} characters (using 'X')")
        grid_lines.append(f"Padded text: \"{padded_text}\"")
    grid_lines.append("")
    grid_lines.append("─" * 50)
    grid_lines.append("")
    grid_lines.append("Writing plaintext row-by-row:")
    grid_lines.append("")
    
    # Create grid
    grid = []
    for r in range(row_count):
        row = padded_text[r * col_count : (r + 1) * col_count]
        grid.append(list(row))
    
    # Display grid with header
    col_header = "       " + "  ".join(f"{keyword[c]:>3}" for c in range(col_count))
    rank_header = "       " + "  ".join(f"({rank[c]:>1})" for c in range(col_count))
    grid_lines.append(col_header)
    grid_lines.append(rank_header)
    grid_lines.append("       " + "─" * (col_count * 4))
    
    for r, row in enumerate(grid):
        row_str = f"Row {r+1}: " + "  ".join(f"{c:>3}" for c in row)
        grid_lines.append(row_str)
    
    all_sections.append({
        "section": "Grid Construction",
        "subsections": [{"title": "Building the Transposition Grid", "content": '\n'.join(grid_lines)}]
    })
    
    # Section 4: Reading Columns
    read_lines = []
    read_lines.append("Step 3: Read columns in sorted order")
    read_lines.append("")
    read_lines.append("Reading columns based on keyword ranking:")
    read_lines.append("")
    
    ciphertext = ""
    for step, col_idx in enumerate(read_order):
        col_content = "".join(grid[r][col_idx] for r in range(row_count))
        read_lines.append(f"Step {step+1}: Read Column {col_idx+1} ('{keyword[col_idx]}', Rank {rank[col_idx]})")
        read_lines.append(f"         Content: {col_content}")
        read_lines.append("")
        ciphertext += col_content
    
    read_lines.append("─" * 50)
    read_lines.append(f"Concatenated Ciphertext: {ciphertext}")
    
    all_sections.append({
        "section": "Reading Columns",
        "subsections": [{"title": "Extracting Ciphertext", "content": '\n'.join(read_lines)}]
    })
    
    # Section 5: Final Result
    result_lines = []
    result_lines.append("KEYED COLUMNAR ENCRYPTION COMPLETE")
    result_lines.append("")
    result_lines.append(f"Input Plaintext:   \"{text}\"")
    result_lines.append(f"Keyword:           \"{keyword}\"")
    result_lines.append(f"Column Order:      {rank}")
    result_lines.append(f"Output Ciphertext: \"{ciphertext}\"")
    
    all_sections.append({
        "section": "Final Result",
        "subsections": [{"title": "Summary", "content": '\n'.join(result_lines)}]
    })
    
    return {
        "success": True,
        "plaintext": text,
        "ciphertext": ciphertext,
        "keyword": keyword,
        "mode": "encrypt",
        "sections": all_sections
    }


def keyed_decrypt_detailed(ciphertext, keyword, column_order=None):
    """Keyed Columnar Transposition Cipher Decryption with detailed steps"""
    all_sections = []
    
    # Clean ciphertext
    text = ciphertext.upper().replace(" ", "")
    text = ''.join(c for c in text if c.isalpha())
    keyword = keyword.upper()
    
    # Section 1: Input Parameters
    input_lines = []
    input_lines.append(f"Ciphertext: \"{ciphertext}\"")
    input_lines.append(f"Cleaned Text: \"{text}\"")
    input_lines.append(f"Text Length: {len(text)}")
    input_lines.append(f"Keyword: \"{keyword}\"")
    input_lines.append(f"Keyword Length: {len(keyword)}")
    input_lines.append("")
    input_lines.append("Decryption Process:")
    input_lines.append("  1. Calculate grid dimensions and column order")
    input_lines.append("  2. Determine how many chars go in each column")
    input_lines.append("  3. Fill columns with ciphertext")
    input_lines.append("  4. Read grid row-by-row")
    
    all_sections.append({
        "section": "Input Parameters",
        "subsections": [{"title": "Given Values", "content": '\n'.join(input_lines)}]
    })
    
    # Section 2: Calculate dimensions and order
    col_count = len(keyword)
    row_count = math.ceil(len(text) / col_count)
    total_cells = row_count * col_count
    short_cols = total_cells - len(text)  # Columns with one less char
    full_cols = col_count - short_cols  # Columns with full height
    
    # Use custom column_order if provided, otherwise calculate from keyword
    if column_order and len(column_order) == len(keyword):
        # User provided custom column order (1-indexed ranks)
        rank = column_order
        # Convert rank to read_order: read_order[i] = column to read at step i
        indexed_ranks = list(enumerate(rank))
        sorted_by_rank = sorted(indexed_ranks, key=lambda x: x[1])
        read_order = [item[0] for item in sorted_by_rank]
        using_custom = True
    else:
        rank, read_order = get_key_order(keyword)
        using_custom = False
    
    dim_lines = []
    dim_lines.append("Step 1: Calculate grid dimensions")
    dim_lines.append("")
    dim_lines.append(f"Ciphertext length: {len(text)}")
    dim_lines.append(f"Columns (keyword length): {col_count}")
    dim_lines.append(f"Rows: ceil({len(text)} / {col_count}) = {row_count}")
    dim_lines.append(f"Total grid cells: {total_cells}")
    dim_lines.append("")
    
    if short_cols > 0:
        dim_lines.append(f"Raggedness calculation:")
        dim_lines.append(f"  Full columns (height {row_count}): {full_cols}")
        dim_lines.append(f"  Short columns (height {row_count - 1}): {short_cols}")
    else:
        dim_lines.append("Grid is perfectly filled (no ragged columns)")
    
    dim_lines.append("")
    dim_lines.append("─" * 50)
    dim_lines.append("")
    
    if using_custom:
        dim_lines.append("Using CUSTOM column order provided by user:")
        dim_lines.append(f"  Rank values: {rank}")
    else:
        dim_lines.append("Column read order from keyword:")
    
    header = "  Keyword:  " + "  ".join(f"{c:>3}" for c in keyword)
    rank_row = "  Rank:     " + "  ".join(f"{r:>3}" for r in rank)
    dim_lines.append(header)
    dim_lines.append(rank_row)
    dim_lines.append("")
    dim_lines.append(f"Read order: {[r+1 for r in read_order]}")
    
    all_sections.append({
        "section": "Dimension Calculation",
        "subsections": [{"title": "Grid Setup", "content": '\n'.join(dim_lines)}]
    })
    
    # Section 3: Determine column heights and fill
    fill_lines = []
    fill_lines.append("Step 2: Calculate characters per column")
    fill_lines.append("")
    
    # Calculate which columns are short (based on original position)
    # Short columns are the ones at position >= full_cols (rightmost in grid)
    col_heights = []
    for orig_idx in range(col_count):
        if orig_idx < full_cols:
            col_heights.append(row_count)
        else:
            col_heights.append(row_count - 1)
    
    for i in range(col_count):
        fill_lines.append(f"  Column {i+1} ('{keyword[i]}'): {col_heights[i]} characters")
    
    fill_lines.append("")
    fill_lines.append("─" * 50)
    fill_lines.append("")
    fill_lines.append("Step 3: Fill columns with ciphertext (in read order)")
    fill_lines.append("")
    
    # Fill columns based on read order
    grid = [[''] * col_count for _ in range(row_count)]
    cipher_idx = 0
    
    for step, col_idx in enumerate(read_order):
        height = col_heights[col_idx]
        segment = text[cipher_idx : cipher_idx + height]
        
        fill_lines.append(f"Step {step+1}: Fill Column {col_idx+1} ('{keyword[col_idx]}', Rank {rank[col_idx]})")
        fill_lines.append(f"         Takes {height} chars: \"{segment}\"")
        fill_lines.append(f"         From ciphertext positions {cipher_idx+1} to {cipher_idx+height}")
        fill_lines.append("")
        
        for r, char in enumerate(segment):
            grid[r][col_idx] = char
        
        cipher_idx += height
    
    all_sections.append({
        "section": "Filling Columns",
        "subsections": [{"title": "Distributing Ciphertext", "content": '\n'.join(fill_lines)}]
    })
    
    # Section 4: Display filled grid
    grid_lines = []
    grid_lines.append("Reconstructed Grid:")
    grid_lines.append("")
    
    col_header = "       " + "  ".join(f"{keyword[c]:>3}" for c in range(col_count))
    rank_header = "       " + "  ".join(f"({rank[c]:>1})" for c in range(col_count))
    grid_lines.append(col_header)
    grid_lines.append(rank_header)
    grid_lines.append("       " + "─" * (col_count * 4))
    
    for r, row in enumerate(grid):
        row_str = f"Row {r+1}: " + "  ".join(f"{c if c else '.':>3}" for c in row)
        grid_lines.append(row_str)
    
    all_sections.append({
        "section": "Reconstructed Grid",
        "subsections": [{"title": "Grid After Filling Columns", "content": '\n'.join(grid_lines)}]
    })
    
    # Section 5: Read row-by-row
    read_lines = []
    read_lines.append("Step 4: Read grid row-by-row")
    read_lines.append("")
    
    plaintext = ""
    for r in range(row_count):
        row_text = "".join(grid[r][c] for c in range(col_count) if grid[r][c])
        read_lines.append(f"Row {r+1}: {row_text}")
        plaintext += row_text
    
    # Remove padding
    plaintext_clean = plaintext.rstrip('X')
    
    read_lines.append("")
    read_lines.append("─" * 50)
    read_lines.append(f"Combined text: {plaintext}")
    if plaintext != plaintext_clean:
        read_lines.append(f"After removing padding (X): {plaintext_clean}")
    
    all_sections.append({
        "section": "Reading Rows",
        "subsections": [{"title": "Reconstructing Plaintext", "content": '\n'.join(read_lines)}]
    })
    
    # Section 6: Final Result
    result_lines = []
    result_lines.append("KEYED COLUMNAR DECRYPTION COMPLETE")
    result_lines.append("")
    result_lines.append(f"Input Ciphertext:  \"{text}\"")
    result_lines.append(f"Keyword:           \"{keyword}\"")
    result_lines.append(f"Column Order:      {rank}")
    result_lines.append(f"Output Plaintext:  \"{plaintext_clean}\"")
    
    all_sections.append({
        "section": "Final Result",
        "subsections": [{"title": "Summary", "content": '\n'.join(result_lines)}]
    })
    
    return {
        "success": True,
        "ciphertext": text,
        "plaintext": plaintext_clean,
        "keyword": keyword,
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
        self.wfile.write(json.dumps({"status": "Keyed Columnar Cipher API ready"}).encode('utf-8'))
    
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            mode = data.get('mode', 'encrypt')
            keyword = data.get('keyword', 'KEY')
            column_order = data.get('columnOrder', None)
            
            if mode == 'encrypt':
                plaintext = data.get('plaintext', 'WEAREDISCOVEREDFLEEATONCE')
                result = keyed_encrypt_detailed(plaintext, keyword, column_order)
            else:
                ciphertext = data.get('ciphertext', '')
                result = keyed_decrypt_detailed(ciphertext, keyword, column_order)
            
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