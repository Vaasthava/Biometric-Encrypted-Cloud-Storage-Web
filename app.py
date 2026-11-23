import os
import sys

# Add project root directory to path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app import app, init_db

if __name__ == "__main__":
    init_db()
    print("=" * 70)
    print(" 5 GB AES-256 Vault with Integrated Cam Face Recognition")
    print(" Server URL: http://localhost:5000")
    print("=" * 70)
    app.run(host="0.0.0.0", port=5000, debug=True)
