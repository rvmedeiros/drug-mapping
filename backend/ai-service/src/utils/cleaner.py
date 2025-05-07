import re
from collections import OrderedDict
from typing import Dict, List, Optional


def format_text(text):
    # Split the text into lines, strip whitespace, and remove empty lines
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    # Process each line to remove extra spaces between words
    formatted_lines = []
    for line in lines:
        # Collapse multiple spaces into single space
        words = line.split()
        cleaned_line = ' '.join(words)
        
        # Special handling for the "key = value" lines
        if '=' in cleaned_line:
            parts = cleaned_line.split('=', 1)
            cleaned_line = f"{parts[0].strip()}={parts[1].strip()}"
            
        formatted_lines.append(cleaned_line)
    
    # Join the processed lines back together
    formatted_text = '\n'.join(formatted_lines)
    return formatted_text

def parse_text_to_object(text):
    # Initialize the result dictionary
    result = {
        'classification': '',
        'condition': '',
        'description': '',
        'liimitations': ''
    }
    
    # Extract the classification and condition (e.g., "1.2 Asthma")
    header_match = re.search(r'^(\d+\.\d+)\s+(.+)$', text.strip().split('\n')[0])
    if header_match:
        result['classification'] = header_match.group(1)
        result['condition'] = header_match.group(2)
    
    # Find the description (text after header until "Limitations")
    description_end = text.find("Limitations of Use")
    print(description_end)
    if description_end == -1:
        description_end = text.find("Limitations =")
    
    if description_end != -1:
        description_start = text.find('\n', text.find(header_match.group(0))) + 1
        result['description'] = text[description_start:description_end].strip()
    
    # Find limitations text
    limitations_start = text.find("is not indicated")
    if limitations_start != -1:
        limitations_end = text.find('\n', limitations_start)
        result['liimitations'] = text[limitations_start:limitations_end if limitations_end != -1 else None].strip()
    
    return result

    """Process multiple indication texts"""
    results = []
    for text in raw_data:
        parsed = parse_indication_text(text)
        if parsed:
            results.append(parsed)
    return results