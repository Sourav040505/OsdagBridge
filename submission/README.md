# FOSSEE Osdag Winter Internship 2026 --- Screening Task Submission

**Project Category:** Software Development / Civil Engineering  
**Project Topic:** OsdagBridge Software Testing & Issue Reporting  
**Candidate Name:** Sourav Mukherjee  
**GitHub Repository:** [https://github.com/Sourav040505/OsdagBridge](https://github.com/Sourav040505/OsdagBridge) (`dev` branch)  
**Upstream Repository:** [https://github.com/Nidhikhare12/OsdagBridge](https://github.com/Nidhikhare12/OsdagBridge) (`dev` branch)  
**Collaborator Invited:** `Nidhikhare12` (GitHub API Invitation ID: `345151077`, Write Permissions)

---

## 1. Executive Summary
This submission package contains the complete, rigorous verification and code-level bug reporting for the **OsdagBridge** short-span steel girder bridge module. All tasks outlined in the FOSSEE problem statement have been accomplished:
- **Comprehensive Functional Testing:** Verified against basic bridge geometry, advanced stiffener details, shear studs, and custom materials (E 450 steel, M 45 concrete).
- **Multi-Run & State Persistence:** Discovered and documented the critical in-place unit mutation defect in `plategirderbridge.py:578-580` that causes $1000\times$ geometric shrinkage across consecutive design cycles.
- **Data Dictionary Audit:** Completed exhaustive side-by-side verification between UI input dock parameters, internal `input_dict`, SI unit conversions, and `output_dict`.
- **4 Formal GitHub Issues Filed Upstream:**
  1. [Issue #183](https://github.com/Nidhikhare12/OsdagBridge/issues/183): Wearing course density validator upper-bound clamping ($24.0\text{ kN/m}^3 \to 10.0\text{ kN/m}^3$).
  2. [Issue #184](https://github.com/Nidhikhare12/OsdagBridge/issues/184): Contradictory unit assumptions in shear stud transverse spacing validator (negative spacing limit).
  3. [Issue #185](https://github.com/Nidhikhare12/OsdagBridge/issues/185): Deck slab dead-load moment omits wearing course self-weight (20.3% under-design).
  4. [Issue #186](https://github.com/Nidhikhare12/OsdagBridge/issues/186): 3D CAD parameter generation hardcodes default footpath (1500 mm) and railing (375 mm) widths.
- **Automated Regression Suite:** 8 comprehensive test cases in `tests/screening_tests/test_screening_suite.py` achieving 100% pass rate under `pytest`.

---

## 2. Submission Directory Structure
```
submission/
├── OsdagBridge_Testing_Report_Sourav.pdf   # Publication-grade compiled LaTeX report
├── OsdagBridge_Testing_Submission_Sourav.zip # Complete archive for FOSSEE portal submission
├── README.md                                # This document
├── VIDEO_DEMO_SCRIPT.md                     # Step-by-step screencast video guide
├── generate_osi_cases.py                    # Generator script for test-case OSI files
└── test_cases/                              # Runnable OSI test-case files
    ├── TC01_baseline_30m_pass.osi           # Standard 30m span baseline bridge
    ├── TC02_custom_materials_e450_m45_pass.osi # High-strength custom steel & concrete
    ├── TC03_skew_30deg_pass.osi             # 30-degree skew angle layout
    ├── TC04_fail_wc_density_clamp.osi       # Demonstrating Issue #183 validator clamp
    ├── TC05_fail_stud_spacing_unit_mismatch.osi # Demonstrating Issue #184 unit bug
    └── TC06_fail_consecutive_run_mutation.osi # Demonstrating in-place unit mutation bug
```

---

## 3. How to Run the Automated Test Suite
From the root of the repository, execute:
```bash
# Activate conda environment
conda activate osdagbridge-env

# Set environment variables for offscreen execution
export QT_QPA_PLATFORM=offscreen
export QT_PLUGIN_PATH=$CONDA_PREFIX/lib/python3.12/site-packages/PySide6/Qt/plugins
export PYTHONPATH=$(pwd)/src:$(pwd)

# Run full pytest suite
pytest -v tests/screening_tests/test_screening_suite.py
```
**Expected Output:**
```
================== 8 passed, 30 warnings in 80.24s ==================
```

---

## 4. Live GitHub Issues Logged
- **Issue #183:** [https://github.com/Nidhikhare12/OsdagBridge/issues/183](https://github.com/Nidhikhare12/OsdagBridge/issues/183)
- **Issue #184:** [https://github.com/Nidhikhare12/OsdagBridge/issues/184](https://github.com/Nidhikhare12/OsdagBridge/issues/184)
- **Issue #185:** [https://github.com/Nidhikhare12/OsdagBridge/issues/185](https://github.com/Nidhikhare12/OsdagBridge/issues/185)
- **Issue #186:** [https://github.com/Nidhikhare12/OsdagBridge/issues/186](https://github.com/Nidhikhare12/OsdagBridge/issues/186)
