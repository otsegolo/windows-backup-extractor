# Windows Backup Extractor

This Python tool extracts files from Windows backups (the ones that are a collection of `.zip` archives) and reconstructs the original folder structure. It supports both local directories and SMB shares for input and output.

## Requirements
- Python 3.6 or higher
- Required Python libraries:
  - `smbprotocol`
  - `pathlib`
  - `zipfile`
  - `re`

Install the required libraries using:
```bash
pip install smbprotocol
```

## Usage

### Command-Line Arguments
```bash
python extract_backup.py <backup_root> <output_dir> [--smb-config <smb_config_file>]
```

- `<backup_root>`: Path to the root of the backup set (local or SMB).
- `<output_dir>`: Path to the output directory where files will be reconstructed.
- `--smb-config`: (Optional) Path to a JSON file containing SMB configuration.

### Example: Local Extraction
```bash
python extract_backup.py "/path/to/backup/root" "/path/to/output/directory"
```

### Example: SMB Extraction
Create an SMB configuration file (e.g., `smb_config.json`):
```json
{
    "server_name": "SERVER_NAME",
    "server_ip": "192.168.1.1",
    "username": "USERNAME",
    "password": "PASSWORD",
    "input_share": "INPUT_SHARE_NAME",
    "output_share": "OUTPUT_SHARE_NAME"
}
```

Run the script with the SMB configuration:
```bash
python extract_backup.py "input_share_path" "output_share_path" --smb-config smb_config.json
```

## License
This project is licensed under the MIT License.
