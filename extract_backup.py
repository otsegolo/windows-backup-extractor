import os
import zipfile
import re
from pathlib import Path
from smbprotocol.connection import Connection
from smbprotocol.session import Session
from smbprotocol.tree import TreeConnect

def setup_smb_connection(smb_config):
    """Setup SMB connection and return input and output paths."""
    connection = Connection(smb_config['server_name'], smb_config['server_ip'])
    connection.connect()

    session = Session(connection, smb_config['username'], smb_config['password'])
    session.connect()

    input_tree = TreeConnect(session, smb_config['input_share'])
    input_tree.connect()

    output_tree = TreeConnect(session, smb_config['output_share'])
    output_tree.connect()

    return Path(input_tree.share_name), Path(output_tree.share_name)

def sanitize_path(path):
    """Sanitize file paths by replacing problematic characters."""
    # Replace percent signs and other special characters with underscores
    sanitized_path = re.sub(r'[\\%]', '_', path)
    return sanitized_path

def extract_zip_file(zip_file, output_dir):
    """Extract a single zip file to the output directory."""
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            for file in zip_ref.namelist():
                # Convert Windows-style backslashes to forward slashes and sanitize the path
                normalized_path = sanitize_path(file.replace('C\\', '').replace('\\', '/'))
                file_path = output_dir / normalized_path
                file_dir = file_path.parent

                if not file_dir.exists():
                    file_dir.mkdir(parents=True)

                with zip_ref.open(file) as source, open(file_path, 'wb') as target:
                    target.write(source.read())
    except zipfile.BadZipFile:
        print(f"Error: {zip_file} is not a valid zip file.")

def extract_backup(backup_root, output_dir, smb_config=None):
    """
    Extracts Windows backup files and reconstructs the original folder structure.

    :param backup_root: Path to the root of the backup set.
    :param output_dir: Path to the output directory where files will be reconstructed.
    :param smb_config: Dictionary containing SMB configuration (optional).
    """
    if smb_config:
        backup_root, output_dir = setup_smb_connection(smb_config)
    else:
        backup_root = Path(backup_root)
        output_dir = Path(output_dir)

    if not backup_root.exists():
        print(f"Backup root directory {backup_root} does not exist.")
        return

    if not output_dir.exists():
        output_dir.mkdir(parents=True)

    for folder in backup_root.glob("Backup Files */"):
        print(f"Processing folder: {folder}")
        for zip_file in folder.glob("*.zip"):
            print(f"Extracting: {zip_file}")
            extract_zip_file(zip_file, output_dir)

    print(f"Extraction complete. Files are located in {output_dir}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Extract Windows backup files and reconstruct folder structure.")
    parser.add_argument("backup_root", help="Path to the root of the backup set.")
    parser.add_argument("output_dir", help="Path to the output directory.")
    parser.add_argument("--smb-config", help="Path to SMB configuration file (optional).", default=None)

    args = parser.parse_args()

    smb_config = None
    if args.smb_config:
        import json
        with open(args.smb_config, 'r') as f:
            smb_config = json.load(f)

    extract_backup(args.backup_root, args.output_dir, smb_config)
