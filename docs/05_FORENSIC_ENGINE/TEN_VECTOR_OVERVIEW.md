# 🔬 The 10 Analytical Forensic Vectors of PramanSetu

| Vector # | Vector Name | Core Algorithm | Configured Thresholds | Weight | Output Signal |
|---|---|---|---|---:|---|
| **1** | **Duplicate Asset Recycling** | 64-bit DCT Perceptual Hashing + Horizontal Mirror Ensemble | Hamming distance $\le 5\text{ bits}$ (FLAGGED) | **40 Pts** | `DuplicateCheckResult` |
| **2** | **Web Stock Photo Reuse** | Perceptual Feature Matching against Public Stock Index | Hamming distance $\le 5\text{ bits}$ (FLAGGED) | **40 Pts** | `WebSearchCheckResult` |
| **3** | **WGS-84 Geodesic Distance** | Vincenty Ellipsoidal Inverse Geodetic Problem | $\le 500\text{m}$ (MATCH), $500-1500\text{m}$ (REVIEW), $>1500\text{m}$ (MISMATCH)| **35 Pts** | `LocationCheckResult` |
| **4** | **Satellite Anomaly Zones** | Point-in-Polygon Geodesic Proximity + Copernicus Indices | Geodesic radius $1,000\text{m}-2,000\text{m}$ | **30 Pts** | `SatelliteCheckResult` |
| **5** | **Ghost Labor Muster Roll** | Verhoeff $D_5$ Dihedral Math + CPWD Wage Ceilings | Unskilled $\le ₹550/\text{d}$, Skilled $\le ₹850/\text{d}$ | **30 Pts** | `MusterRollCheckResult` |
| **6** | **Material & Milestone Match** | Surface Texture & Milestone Specification Alignment | Alignment Score $< 0.50 \implies \text{FLAGGED}$ | **25 Pts** | `MaterialCheckResult` |
| **7** | **Visual AI Forensics** | Gemini 2.0 Flash Multimodal + Offline Shannon Entropy | Confidence $\ge 0.70$ & `is_suspicious=True` | **20 Pts** | `GenAIForensicResult` |
| **8** | **Chrono-Solar & Weather** | NOAA Solar Position Algorithm (SPA) + Open-Meteo | Elevation $< 0^\circ$ at daytime or Rain Mismatch | **15 Pts** | `ChronoCheckResult` |
| **9** | **EXIF Hardware GPS Integrity**| Binary IFD0/GPSInfo Tag Extraction | Missing Hardware Coordinates $\implies \text{UNVERIFIABLE}$| **10 Pts** | `GPSExtractionResult` |
| **10** | **Image Quality Outliers** | Laplacian Kernel Convolution Variance & Size Bounds | File Size $< 5\text{ KB} \implies \text{REVIEW}$ | **5 Pts** | `GhostWorkerResult` |
