import json
import os

def validate_manifest(manifest):
    """
    Manifest dosyasının gerekli alanları içerip içermediğini ve tiplerinin doğru olup olmadığını kontrol eder.
    
    Args:
        manifest (dict): Doğrulanacak manifest dictionary'si
        
    Returns:
        bool: Manifest geçerliyse True, değilse False
    """
    # Gerekli alanlar
    required_fields = {
        'name': str,
        'version': str,
        'language': str,
        'entry': str
    }
    
    # Opsiyonel alanlar
    optional_fields = {
        'description': str,
        'dependencies': list
    }
    
    # Gerekli alanları kontrol et
    for field, expected_type in required_fields.items():
        if field not in manifest:
            return False
        if not isinstance(manifest[field], expected_type):
            return False
    
    # Dil kontrolü
    if manifest['language'] not in ['python', 'lua']:
        return False
    
    # Opsiyonel alanları kontrol et (varsa)
    for field, expected_type in optional_fields.items():
        if field in manifest and not isinstance(manifest[field], expected_type):
            return False
    
    return True

def get_schema():
    """
    Manifest şemasını döndürür.
    
    Returns:
        dict: Manifest şeması
    """
    return {
        "required_fields": {
            "name": "string",
            "version": "string", 
            "language": "string (python or lua)",
            "entry": "string"
        },
        "optional_fields": {
            "description": "string",
            "dependencies": "list"
        }
    } 