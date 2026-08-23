# 🔄 PramanSetu Multi-Vector Forensic Data Flow

1. **Ingestion**: Evidence JPEG/PNG is received via multipart form-data.
2. **Security Pre-Check**: Validates binary magic bytes and sliding-window rate limit.
3. **Parallel Signal Extraction**:
   - `phash_service.py`: Computes 64-bit DCT perceptual hash.
   - `gps_service.py`: Extracts EXIF IFD0 GPS and calculates Vincenty WGS-84 ellipsoidal distance.
   - `satellite_service.py`: Evaluates Point-in-Polygon geodesic inclusion in fraud anomaly zones.
   - `muster_roll_service.py`: Executes Verhoeff $D_5$ dihedral multiplication on worker Aadhaar IDs.
   - `chrono_service.py`: Runs NOAA Solar Position Algorithm to check solar elevation and shadow ratio.
   - `genai_service.py`: Prompts Gemini 2.0 Flash for structural tampering artifacts.
4. **Scoring & Aggregation**: Adds weighted signal contributions and clamps score to $[0, 100]$.
5. **Dossier & RTI Compilation**: Emits GFR Rule 175 Hold Alerts or Section 6(1) Form A RTI drafts.
6. **Persistence & Sealing**: Computes SHA-256 seal and stores record in SQLite.
