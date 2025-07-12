#!/usr/bin/env python3
"""
publish_command.py - clapp Publish Command

Bu modül 'clapp publish <folder>' komutunu uygular.
Bir uygulama klasörünü validate edip packages/ klasörüne kopyalar
ve index.json'u günceller. Opsiyonel olarak GitHub'a push eder.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Tuple, Optional

from manifest_validator import validate_manifest_verbose
from manifest_schema import load_manifest

def validate_app_folder(folder_path: str) -> Tuple[bool, str, Optional[dict]]:
    """
    Uygulama klasörünü doğrular
    
    Returns:
        (success, message, manifest_data)
    """
    if not os.path.exists(folder_path):
        return False, f"Klasör bulunamadı: {folder_path}", None
    
    if not os.path.isdir(folder_path):
        return False, f"Geçerli bir klasör değil: {folder_path}", None
    
    # manifest.json kontrolü
    manifest_path = os.path.join(folder_path, "manifest.json")
    if not os.path.exists(manifest_path):
        return False, "manifest.json dosyası bulunamadı", None
    
    try:
        manifest = load_manifest(manifest_path)
    except Exception as e:
        return False, f"manifest.json okunamadı: {e}", None
    
    # Manifest doğrulama
    is_valid, errors = validate_manifest_verbose(manifest)
    if not is_valid:
        error_msg = "Manifest doğrulama hatası:\n" + "\n".join(f"  - {error}" for error in errors)
        return False, error_msg, None
    
    # Entry file kontrolü
    entry_file = manifest.get('entry')
    if entry_file:
        entry_path = os.path.join(folder_path, entry_file)
        if not os.path.exists(entry_path):
            return False, f"Entry dosyası bulunamadı: {entry_file}", None
    
    return True, "Doğrulama başarılı", manifest

def copy_app_to_packages(source_folder: str, app_name: str) -> Tuple[bool, str]:
    """
    Uygulama klasörünü packages/ altına kopyalar
    
    Returns:
        (success, message)
    """
    try:
        packages_dir = "./packages"
        target_path = os.path.join(packages_dir, app_name)
        
        # packages klasörünü oluştur
        os.makedirs(packages_dir, exist_ok=True)
        
        # Eğer hedef klasör varsa, sil
        if os.path.exists(target_path):
            shutil.rmtree(target_path)
            print(f"⚠️  Mevcut {app_name} klasörü silindi")
        
        # Kopyala
        shutil.copytree(source_folder, target_path)
        print(f"✅ {app_name} -> packages/{app_name} kopyalandı")
        
        return True, f"Uygulama başarıyla kopyalandı: packages/{app_name}"
        
    except Exception as e:
        return False, f"Kopyalama hatası: {e}"

def update_index() -> Tuple[bool, str]:
    """
    build_index.py script'ini çalıştırarak index.json'u günceller
    
    Returns:
        (success, message)
    """
    try:
        # build_index.py'yi çalıştır
        result = subprocess.run([
            sys.executable, "build_index.py"
        ], capture_output=True, text=True, cwd=".")
        
        if result.returncode == 0:
            return True, "Index başarıyla güncellendi"
        else:
            return False, f"Index güncelleme hatası: {result.stderr}"
            
    except Exception as e:
        return False, f"Index script çalıştırılamadı: {e}"

def push_to_github_repo(app_name: str, app_version: str) -> Tuple[bool, str]:
    """
    Değişiklikleri GitHub'a push eder
    
    Returns:
        (success, message)
    """
    try:
        print("4️⃣ GitHub'a push ediliyor...")
        
        # Git durumunu kontrol et
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, cwd=".")
        
        if not result.stdout.strip():
            return True, "Değişiklik yok, push gerekmiyor"
        
        # Değişiklikleri ekle
        subprocess.run(['git', 'add', 'packages/', 'index.json'], 
                      check=True, cwd=".")
        
        # Commit oluştur
        commit_message = f"📦 Publish {app_name} v{app_version}\n\n- {app_name} uygulaması packages/ klasörüne eklendi\n- index.json güncellendi\n- Otomatik publish işlemi"
        
        subprocess.run(['git', 'commit', '-m', commit_message], 
                      check=True, cwd=".")
        
        # Push et
        subprocess.run(['git', 'push', 'origin', 'main'], 
                      check=True, cwd=".")
        
        return True, "GitHub'a başarıyla push edildi"
        
    except subprocess.CalledProcessError as e:
        return False, f"Git işlemi hatası: {e}"
    except Exception as e:
        return False, f"Push hatası: {e}"

def publish_app(folder_path: str, force: bool = False, push_to_github: bool = False) -> Tuple[bool, str]:
    """
    Ana publish fonksiyonu
    
    Args:
        folder_path: Publish edilecek uygulama klasörü
        force: Zorla üzerine yaz
        push_to_github: GitHub'a push et
        
    Returns:
        (success, message)
    """
    print(f"🚀 Publish başlatılıyor: {folder_path}")
    print("=" * 50)
    
    # 1. Klasörü doğrula
    print("1️⃣ Uygulama doğrulanıyor...")
    is_valid, message, manifest = validate_app_folder(folder_path)
    
    if not is_valid:
        return False, f"Doğrulama hatası: {message}"
    
    app_name = manifest['name']
    app_version = manifest['version']
    print(f"✅ {app_name} v{app_version} doğrulandı")
    
    # 2. Packages klasörüne kopyala
    print("2️⃣ Uygulama kopyalanıyor...")
    copy_success, copy_message = copy_app_to_packages(folder_path, app_name)
    
    if not copy_success:
        return False, copy_message
    
    # 3. Index'i güncelle
    print("3️⃣ Index güncelleniyor...")
    index_success, index_message = update_index()
    
    if not index_success:
        return False, index_message
    
    # 4. GitHub'a push (opsiyonel)
    if push_to_github:
        push_success, push_message = push_to_github_repo(app_name, app_version)
        if not push_success:
            print(f"⚠️  {push_message}")
            return True, f"🎉 '{app_name}' yerel olarak publish edildi! GitHub push başarısız."
    
    return True, f"🎉 '{app_name}' başarıyla publish edildi! Index güncellendi."

def main():
    """CLI entry point"""
    if len(sys.argv) < 2:
        print("Kullanım: python publish_command.py <folder_path> [--push]")
        print("Örnek: python publish_command.py ./my-app")
        print("Örnek: python publish_command.py ./my-app --push")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    force = "--force" in sys.argv
    push_to_github = "--push" in sys.argv
    
    success, message = publish_app(folder_path, force, push_to_github)
    
    print("\n" + "=" * 50)
    if success:
        print(f"✅ {message}")
        sys.exit(0)
    else:
        print(f"❌ {message}")
        sys.exit(1)

if __name__ == "__main__":
    main() 