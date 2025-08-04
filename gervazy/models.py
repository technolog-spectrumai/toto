from django.db import models
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta
from io import BytesIO
from django.core.files.base import ContentFile
import qrcode
import os


class TLSCertificate(models.Model):
    country_name = models.CharField(max_length=2, verbose_name="Country (C)")
    state_or_province_name = models.CharField(max_length=100, verbose_name="State/Province (ST)")
    locality_name = models.CharField(max_length=100, verbose_name="Locality (L)")
    organization_name = models.CharField(max_length=255, verbose_name="Organization (O)")
    common_name = models.CharField(max_length=255, verbose_name="Common Name (CN)")
    private_key = models.TextField(blank=True, null=True)
    certificate = models.TextField(blank=True, null=True)
    qr_code = models.ImageField(upload_to="qr_codes/", blank=True, null=True)

    def __str__(self):
        return f"TLS Cert for {self.common_name} ({self.organization_name})"

    def get_subject(self):
        """Creates an X.509 subject using model fields"""
        return x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, self.country_name),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, self.state_or_province_name),
            x509.NameAttribute(NameOID.LOCALITY_NAME, self.locality_name),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, self.organization_name),
            x509.NameAttribute(NameOID.COMMON_NAME, self.common_name),
        ])

    def save(self, *args, **kwargs):
        """Generates certificate and QR code before saving"""
        if not self.private_key or not self.certificate:
            self.generate_certificate()
        self.generate_qr_code()  # Generate QR code on save
        super().save(*args, **kwargs)

    def generate_certificate(self):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )

        subject = self.get_subject()

        cert = x509.CertificateBuilder().subject_name(subject).issuer_name(subject).public_key(
            private_key.public_key()).serial_number(
            x509.random_serial_number()).not_valid_before(
            datetime.utcnow()).not_valid_after(
            datetime.utcnow() + timedelta(days=365)
        ).add_extension(
            x509.BasicConstraints(ca=True, path_length=None), critical=True,
        ).sign(private_key, hashes.SHA256())

        self.private_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ).decode()

        self.certificate = cert.public_bytes(serialization.Encoding.PEM).decode()

    def save_certificate_to_files(self, dir_path):
        """Saves the generated certificate and private key to files in the given directory."""

        # Ensure the directory exists
        os.makedirs(dir_path, exist_ok=True)

        cert_file_path = os.path.join(dir_path, f"{self.common_name}.crt")
        key_file_path = os.path.join(dir_path, f"{self.common_name}.key")

        # Save certificate and private key
        with open(cert_file_path, "w") as cert_file:
            cert_file.write(self.certificate)

        with open(key_file_path, "w") as key_file:
            key_file.write(self.private_key)

        print(f"Certificate saved to {cert_file_path}")
        print(f"Private key saved to {key_file_path}")

    def generate_qr_code(self):
        """Generates a QR code from the certificate data"""
        if self.certificate:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(self.certificate)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            buffer = BytesIO()
            img.save(buffer, format="PNG")
            self.qr_code.save(f"qr_{self.common_name}.png", ContentFile(buffer.getvalue()), save=False)
            buffer.close()
