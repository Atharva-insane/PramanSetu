import abc
import hashlib
import hmac
import time
from datetime import datetime, timezone
from typing import Dict, Any, Optional, Tuple
from services.crypto_service import canonical_json_bytes

# Mock Private Key Seed for Development Software PKI Provider
DEV_PKI_PRIVATE_KEY_SEED = b"pramansetu-institutional-root-ca-rsa4096-dev-seed-2026"


class BaseSignatureProvider(abc.ABC):
    """
    Abstract Provider Interface for Cryptographic Digital Signatures (DSC).
    Decouples signature creation and verification from hardware vs. software implementations.
    """

    @abc.abstractmethod
    def sign_document_digest(
        self,
        document_payload: Dict[str, Any],
        officer_dn: str,
        token_id: str
    ) -> Dict[str, Any]:
        """Signs the canonical JSON digest and returns structured signature metadata."""
        pass

    @abc.abstractmethod
    def verify_document_signature(
        self,
        document_payload: Dict[str, Any],
        signature_block: Dict[str, Any]
    ) -> Tuple[bool, str]:
        """Verifies the digital signature block against the document payload."""
        pass


class DevelopmentSoftwareSignatureProvider(BaseSignatureProvider):
    """
    Development & Testing Software PKI Provider:
    Performs asymmetric/keyed cryptographic signing over canonical document bytes.
    Generates genuine, verifiable cryptographic signatures without requiring physical USB drivers.
    """

    def sign_document_digest(
        self,
        document_payload: Dict[str, Any],
        officer_dn: str,
        token_id: str
    ) -> Dict[str, Any]:
        canonical_bytes = canonical_json_bytes(document_payload)
        doc_hash = hashlib.sha256(canonical_bytes).hexdigest()

        # Sign document hash with institutional private key seed
        sig_bytes = hmac.new(DEV_PKI_PRIVATE_KEY_SEED, canonical_bytes, hashlib.sha256).digest()
        sig_hex = sig_bytes.hex()
        cert_serial = f"CERT-IN-NIC-2026-{token_id.replace('-', '')[-8:]}"

        now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

        return {
            "provider_type": "DEVELOPMENT_SOFTWARE_ADAPTER",
            "signature_algorithm": "SHA256withHMAC (Dev Keypair)",
            "document_sha256": doc_hash,
            "certificate_serial": cert_serial,
            "signer_dn": officer_dn,
            "token_id": token_id,
            "signature_timestamp_utc": now_utc,
            "signature_value": sig_hex,
            "public_key_fingerprint": hashlib.sha256(DEV_PKI_PRIVATE_KEY_SEED).hexdigest()[:32].upper(),
            "status": "VALID_SIGNATURE"
        }

    def verify_document_signature(
        self,
        document_payload: Dict[str, Any],
        signature_block: Dict[str, Any]
    ) -> Tuple[bool, str]:
        try:
            canonical_bytes = canonical_json_bytes(document_payload)
            expected_sig = hmac.new(DEV_PKI_PRIVATE_KEY_SEED, canonical_bytes, hashlib.sha256).hexdigest()
            provided_sig = signature_block.get("signature_value", "")

            if hmac.compare_digest(expected_sig, provided_sig):
                return True, "Software cryptographic digital signature verified successfully."
            else:
                return False, "Digital signature mismatch: Document contents have been altered after signing."
        except Exception as e:
            return False, f"Signature verification error: {str(e)}"


class HardwarePKCS11SignatureProvider(BaseSignatureProvider):
    """
    Production Hardware Token Adapter (PKCS#11):
    Direct interface template for physical Class-3 USB Cryptographic Tokens (ePass2003 / SafeNet HSM).
    """

    def __init__(self, pkcs11_lib_path: str = "/usr/lib/libeToken.so"):
        self.pkcs11_lib_path = pkcs11_lib_path

    def sign_document_digest(
        self,
        document_payload: Dict[str, Any],
        officer_dn: str,
        token_id: str
    ) -> Dict[str, Any]:
        # Production HSM adapter interface placeholder
        raise NotImplementedError(
            "Hardware PKCS#11 token signing requires physical USB smartcard driver connection. "
            "Use DevelopmentSoftwareSignatureProvider for software verification."
        )

    def verify_document_signature(
        self,
        document_payload: Dict[str, Any],
        signature_block: Dict[str, Any]
    ) -> Tuple[bool, str]:
        raise NotImplementedError("Hardware PKCS#11 verification not configured in local environment.")


def get_signature_provider(mode: str = "DEV_SOFTWARE") -> BaseSignatureProvider:
    """Factory helper to obtain the active PKI signature provider."""
    if mode.upper() == "HARDWARE_PKCS11":
        return HardwarePKCS11SignatureProvider()
    return DevelopmentSoftwareSignatureProvider()
