import subprocess
import pathlib


def create_dev_ssl_cert():
    ssl_dir = pathlib.Path("ssl")
    cert_file = ssl_dir / "cert.pem"
    key_file = ssl_dir / "key.pem"

    if not ssl_dir.exists():
        ssl_dir.mkdir()
        print(f"[INFO] Created SSL directory at {ssl_dir.resolve()}")

    if not cert_file.exists() or not key_file.exists():
        print("[INFO] Generating self-signed SSL certificate...")
        try:
            subprocess.run([
                "openssl", "req", "-x509", "-nodes", "-days", "365",
                "-newkey", "rsa:2048",
                "-keyout", str(key_file),
                "-out", str(cert_file),
                "-subj", "/CN=localhost"
            ], check=True)
            print(f"[SUCCESS] SSL certificate created at {cert_file}")
        except Exception as e:
            print("[ERROR] Failed to generate SSL certificate:", e)
    else:
        print("[INFO] SSL certificate already exists. Skipping generation.")


if __name__ == "__main__":
    create_dev_ssl_cert()
