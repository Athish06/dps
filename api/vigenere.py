from http.server import BaseHTTPRequestHandler
import json

def prepare_input(text, key):
    """Clean inputs - uppercase, letters only"""
    text = "".join([c.upper() for c in text if c.isalpha()])
    key = "".join([c.upper() for c in key if c.isalpha()])
    return text, key


def vigenere_encrypt_detailed(plaintext, key):
    """Standard Vigenere encryption with detailed steps"""
    all_sections = []
    
    # Clean inputs
    text, key = prepare_input(plaintext, key)
    
    # Section 1: Input Parameters
    input_content = f"""Original Plaintext: {plaintext}
Cleaned Plaintext: {text}
Keyword: {key}

Vigenère Cipher Overview:
  • Polyalphabetic substitution cipher
  • Key repeats to match plaintext length
  • Formula: C = (P + K) mod 26
  
  Letter values: A=0, B=1, C=2, ... Z=25"""
    
    all_sections.append({
        "section": "Input Parameters",
        "subsections": [{"title": "Standard Vigenère Encryption", "content": input_content}]
    })
    
    # Section 2: Key Expansion
    key_lines = []
    key_lines.append("═" * 60)
    key_lines.append("STEP 1: KEY EXPANSION")
    key_lines.append("═" * 60)
    key_lines.append("")
    key_lines.append(f"Plaintext length: {len(text)}")
    key_lines.append(f"Keyword: {key} (length = {len(key)})")
    key_lines.append("")
    key_lines.append("Repeat keyword to match plaintext length:")
    
    expanded_key = ""
    for i in range(len(text)):
        expanded_key += key[i % len(key)]
    
    key_lines.append(f"  {key} → {expanded_key}")
    key_lines.append("")
    key_lines.append("Alignment:")
    key_lines.append(f"  Plaintext: {text}")
    key_lines.append(f"  Key:       {expanded_key}")
    key_lines.append("")
    
    all_sections.append({
        "section": "Step 1: Key Expansion",
        "subsections": [{"title": "Repeat Keyword", "content": '\n'.join(key_lines)}]
    })
    
    # Section 3: Letter-by-letter encryption
    enc_lines = []
    enc_lines.append("═" * 60)
    enc_lines.append("STEP 2: LETTER-BY-LETTER ENCRYPTION")
    enc_lines.append("═" * 60)
    enc_lines.append("")
    enc_lines.append("Formula: C = (P + K) mod 26")
    enc_lines.append("")
    enc_lines.append("─" * 60)
    enc_lines.append("")
    
    result = ""
    for i, char in enumerate(text):
        p_val = ord(char) - 65
        k_char = expanded_key[i]
        k_val = ord(k_char) - 65
        c_val = (p_val + k_val) % 26
        c_char = chr(c_val + 65)
        result += c_char
        
        enc_lines.append(f"Position {i + 1}: '{char}' + '{k_char}'")
        enc_lines.append(f"  P = {char} → {p_val}")
        enc_lines.append(f"  K = {k_char} → {k_val}")
        enc_lines.append(f"  C = ({p_val} + {k_val}) mod 26 = {p_val + k_val} mod 26 = {c_val} → '{c_char}'")
        enc_lines.append("")
    
    enc_lines.append("─" * 60)
    enc_lines.append("")
    enc_lines.append(f"<b>★ CIPHERTEXT: {result}</b>")
    enc_lines.append("")
    
    all_sections.append({
        "section": "Step 2: Encryption",
        "subsections": [{"title": "C = (P + K) mod 26", "content": '\n'.join(enc_lines)}]
    })
    
    return {
        "success": True,
        "mode": "encrypt",
        "cipher_type": "vigenere",
        "ciphertext": result,
        "sections": all_sections
    }


def vigenere_decrypt_detailed(ciphertext, key):
    """Standard Vigenere decryption with detailed steps"""
    all_sections = []
    
    text, key = prepare_input(ciphertext, key)
    
    # Section 1: Input
    input_content = f"""Ciphertext: {text}
Keyword: {key}

Decryption Formula: P = (C - K) mod 26
(Add 26 before mod to handle negatives)"""
    
    all_sections.append({
        "section": "Input Parameters",
        "subsections": [{"title": "Standard Vigenère Decryption", "content": input_content}]
    })
    
    # Section 2: Key Expansion
    expanded_key = ""
    for i in range(len(text)):
        expanded_key += key[i % len(key)]
    
    key_content = f"""Ciphertext length: {len(text)}
Keyword: {key}
Expanded: {expanded_key}

Alignment:
  Ciphertext: {text}
  Key:        {expanded_key}"""
    
    all_sections.append({
        "section": "Step 1: Key Expansion",
        "subsections": [{"title": "Repeat Keyword", "content": key_content}]
    })
    
    # Section 3: Decryption
    dec_lines = []
    dec_lines.append("═" * 60)
    dec_lines.append("STEP 2: LETTER-BY-LETTER DECRYPTION")
    dec_lines.append("═" * 60)
    dec_lines.append("")
    dec_lines.append("Formula: P = (C - K + 26) mod 26")
    dec_lines.append("")
    dec_lines.append("─" * 60)
    dec_lines.append("")
    
    result = ""
    for i, char in enumerate(text):
        c_val = ord(char) - 65
        k_char = expanded_key[i]
        k_val = ord(k_char) - 65
        p_val = (c_val - k_val + 26) % 26
        p_char = chr(p_val + 65)
        result += p_char
        
        dec_lines.append(f"Position {i + 1}: '{char}' - '{k_char}'")
        dec_lines.append(f"  C = {char} → {c_val}")
        dec_lines.append(f"  K = {k_char} → {k_val}")
        dec_lines.append(f"  P = ({c_val} - {k_val} + 26) mod 26 = {c_val - k_val + 26} mod 26 = {p_val} → '{p_char}'")
        dec_lines.append("")
    
    dec_lines.append("─" * 60)
    dec_lines.append("")
    dec_lines.append(f"<b>★ PLAINTEXT: {result}</b>")
    dec_lines.append("")
    
    all_sections.append({
        "section": "Step 2: Decryption",
        "subsections": [{"title": "P = (C - K) mod 26", "content": '\n'.join(dec_lines)}]
    })
    
    return {
        "success": True,
        "mode": "decrypt",
        "cipher_type": "vigenere",
        "plaintext": result,
        "sections": all_sections
    }


def autokey_encrypt_detailed(plaintext, keyword):
    """Autokey cipher encryption with detailed steps"""
    all_sections = []
    
    text, keyword = prepare_input(plaintext, keyword)
    
    # Section 1: Input
    input_content = f"""Plaintext: {text}
Keyword: {keyword}

Autokey Cipher Overview:
  • More secure than standard Vigenère
  • Key = Keyword + Plaintext characters
  • No key repetition - no repeating patterns
  • Formula: C = (P + K) mod 26"""
    
    all_sections.append({
        "section": "Input Parameters",
        "subsections": [{"title": "Autokey Cipher Encryption", "content": input_content}]
    })
    
    # Section 2: Key Construction
    full_key = keyword + text
    used_key = full_key[:len(text)]
    
    key_lines = []
    key_lines.append("═" * 60)
    key_lines.append("STEP 1: AUTOKEY CONSTRUCTION")
    key_lines.append("═" * 60)
    key_lines.append("")
    key_lines.append("Key = Keyword + Plaintext itself")
    key_lines.append("")
    key_lines.append(f"Keyword: {keyword}")
    key_lines.append(f"Plaintext: {text}")
    key_lines.append("")
    key_lines.append("Key stream construction:")
    key_lines.append(f"  Positions 1-{len(keyword)}: from keyword → {keyword}")
    if len(text) > len(keyword):
        key_lines.append(f"  Positions {len(keyword)+1}-{len(text)}: from plaintext → {text[:len(text)-len(keyword)]}")
    key_lines.append("")
    key_lines.append(f"Full autokey: {used_key}")
    key_lines.append("")
    key_lines.append("Alignment:")
    key_lines.append(f"  Plaintext: {text}")
    key_lines.append(f"  Autokey:   {used_key}")
    key_lines.append("")
    
    all_sections.append({
        "section": "Step 1: Autokey Construction",
        "subsections": [{"title": "Key = Keyword + Plaintext", "content": '\n'.join(key_lines)}]
    })
    
    # Section 3: Encryption
    enc_lines = []
    enc_lines.append("═" * 60)
    enc_lines.append("STEP 2: LETTER-BY-LETTER ENCRYPTION")
    enc_lines.append("═" * 60)
    enc_lines.append("")
    enc_lines.append("Formula: C = (P + K) mod 26")
    enc_lines.append("")
    enc_lines.append("─" * 60)
    enc_lines.append("")
    
    result = ""
    for i in range(len(text)):
        p_val = ord(text[i]) - 65
        k_char = full_key[i]
        k_val = ord(k_char) - 65
        c_val = (p_val + k_val) % 26
        c_char = chr(c_val + 65)
        result += c_char
        
        key_source = "keyword" if i < len(keyword) else f"plaintext[{i - len(keyword)}]='{text[i - len(keyword)]}'"
        enc_lines.append(f"Position {i + 1}: '{text[i]}' + '{k_char}' (key from {key_source})")
        enc_lines.append(f"  P = {text[i]} → {p_val}")
        enc_lines.append(f"  K = {k_char} → {k_val}")
        enc_lines.append(f"  C = ({p_val} + {k_val}) mod 26 = {c_val} → '{c_char}'")
        enc_lines.append("")
    
    enc_lines.append("─" * 60)
    enc_lines.append("")
    enc_lines.append(f"<b>★ CIPHERTEXT: {result}</b>")
    enc_lines.append("")
    
    all_sections.append({
        "section": "Step 2: Encryption",
        "subsections": [{"title": "C = (P + K) mod 26", "content": '\n'.join(enc_lines)}]
    })
    
    return {
        "success": True,
        "mode": "encrypt",
        "cipher_type": "autokey",
        "ciphertext": result,
        "sections": all_sections
    }


def autokey_decrypt_detailed(ciphertext, keyword):
    """Autokey cipher decryption with detailed steps"""
    all_sections = []
    
    text, keyword = prepare_input(ciphertext, keyword)
    
    # Section 1: Input
    input_content = f"""Ciphertext: {text}
Keyword: {keyword}

Autokey Decryption:
  • Start with keyword only
  • Recover plaintext letters one by one
  • Each recovered letter becomes part of the key!
  • Formula: P = (C - K + 26) mod 26"""
    
    all_sections.append({
        "section": "Input Parameters",
        "subsections": [{"title": "Autokey Cipher Decryption", "content": input_content}]
    })
    
    # Section 2: Progressive Decryption
    dec_lines = []
    dec_lines.append("═" * 60)
    dec_lines.append("STEP 1: PROGRESSIVE DECRYPTION")
    dec_lines.append("═" * 60)
    dec_lines.append("")
    dec_lines.append("The key is built as we decrypt!")
    dec_lines.append("  • Start with keyword")
    dec_lines.append("  • Each decrypted letter extends the key")
    dec_lines.append("")
    dec_lines.append("─" * 60)
    dec_lines.append("")
    
    current_key = list(keyword)
    result = ""
    
    for i in range(len(text)):
        c_val = ord(text[i]) - 65
        k_char = current_key[i]
        k_val = ord(k_char) - 65
        p_val = (c_val - k_val + 26) % 26
        p_char = chr(p_val + 65)
        result += p_char
        
        # Add recovered plaintext to key stream
        current_key.append(p_char)
        
        key_source = "keyword" if i < len(keyword) else f"recovered plaintext[{i - len(keyword)}]"
        dec_lines.append(f"Position {i + 1}: '{text[i]}' - '{k_char}' (key from {key_source})")
        dec_lines.append(f"  C = {text[i]} → {c_val}")
        dec_lines.append(f"  K = {k_char} → {k_val}")
        dec_lines.append(f"  P = ({c_val} - {k_val} + 26) mod 26 = {p_val} → '{p_char}'")
        dec_lines.append(f"  → Key now: {''.join(current_key)}")
        dec_lines.append("")
    
    dec_lines.append("─" * 60)
    dec_lines.append("")
    dec_lines.append(f"<b>★ PLAINTEXT: {result}</b>")
    dec_lines.append("")
    
    all_sections.append({
        "section": "Step 1: Progressive Decryption",
        "subsections": [{"title": "Recover and Extend Key", "content": '\n'.join(dec_lines)}]
    })
    
    return {
        "success": True,
        "mode": "decrypt",
        "cipher_type": "autokey",
        "plaintext": result,
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
        self.wfile.write(json.dumps({"status": "Vigenère & Autokey Cipher API ready"}).encode('utf-8'))
    
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            mode = data.get('mode', 'encrypt')
            cipher_type = data.get('cipherType', 'vigenere')
            key = data.get('key', 'KEY')
            
            if cipher_type == 'vigenere':
                if mode == 'encrypt':
                    plaintext = data.get('plaintext', 'HELLO')
                    result = vigenere_encrypt_detailed(plaintext, key)
                else:
                    ciphertext = data.get('ciphertext', '')
                    result = vigenere_decrypt_detailed(ciphertext, key)
            else:  # autokey
                if mode == 'encrypt':
                    plaintext = data.get('plaintext', 'HELLO')
                    result = autokey_encrypt_detailed(plaintext, key)
                else:
                    ciphertext = data.get('ciphertext', '')
                    result = autokey_decrypt_detailed(ciphertext, key)
            
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
