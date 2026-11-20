# FOSSEE Osdag Winter Internship 2026 - Screencast Demonstration Script
**Project:** OsdagBridge Software Testing & Issue Reporting  
**Candidate:** Sourav Mukherjee  
**Target Video Duration:** 3 to 5 minutes  
**Format:** Silent screen recording (no voiceover required, optional background music/captions)

---

## Pre-Recording Checklist & Setup
1. **Screen Resolution:** Recommended $1920 \times 1080$ (1080p).
2. **Terminal Ready:** Open a clean terminal window with `osdagbridge-env` activated:
   ```bash
   conda activate osdagbridge-env
   cd /Users/sourav/Web-Dev-Projects/OsdagBridge
   ```
3. **Screen Recorder:** Use QuickTime Player on macOS (File $\to$ New Screen Recording) or OBS Studio.

---

## Step-by-Step Recording Timeline

### Scene 1: Launching OsdagBridge (0:00 - 0:30)
1. In terminal, launch the desktop application:
   ```bash
   cd src && python -m osdagbridge.desktop
   ```
2. The main window opens displaying the Bridge Module selector.
3. Click on **Plate Girder Bridge** module to load the workspace.

---

### Scene 2: Custom Material Properties & Persistence (0:30 - 1:15)
1. In the left **Input Dock**, locate the **Material Properties** section.
2. Click on **Material Properties** button to open the material dialog.
3. For **Girder Steel**:
   - Change from default `E 250` or `E 350` to **`E 450`**.
   - Show that Yield Strength ($f_y = 450\text{ MPa}$) and Ultimate Tensile Strength ($f_u = 570\text{ MPa}$) update dynamically.
4. For **Deck Concrete**:
   - Change from default `M 30` to **`M 45`**.
   - Show characteristic cube strength ($f_{ck} = 45\text{ MPa}$) and elastic modulus ($E_{cm} = 34500\text{ MPa}$).
5. Click **OK / Save** to close the dialog.
6. Re-open the **Material Properties** dialog to visually demonstrate **Property Persistence** — verify that the inputs do NOT default back to initial values.

---

### Scene 3: First Design Run & 3D CAD / Plot Verification (1:15 - 2:15)
1. In the Input Dock:
   - Span Length: `30.0` m
   - Carriageway Width: `7.5` m
   - Skew Angle: `0.0` degrees
   - Design Mode: `Optimized`
2. Click the **Design** button in the bottom dock.
3. Allow the design engine (OpenSees moving vehicle load analysis & IRC 22:2015 checks) to execute.
4. When computation finishes:
   - **3D CAD View:** Switch to the 3D CAD tab. Click and drag to rotate the 3D bridge model. Zoom in to show structural components:
     - Longitudinal Plate Girders with tapered/flanged profiles.
     - Intermediate and Bearing Stiffeners.
     - Transverse Cross Bracing (X-type trusses).
     - Concrete Deck Slab.
   - **Structural Plots:** Switch to the **Plots** tab. Display:
     - ULS Bending Moment Envelope.
     - ULS Shear Force Envelope.
     - Deflection Profiles.

---

### Scene 4: Multi-Run Consecutive Design Cycles (2:15 - 3:15)
1. Click **Unlock Design** in the UI to enable inputs for redesign.
2. **Run 2:**
   - Change Span Length from `30.0` m to `28.0` m (or adjust girder spacing).
   - Click **Design** again.
   - Verify that results and 3D CAD update dynamically for the second consecutive run.
3. **Run 3:**
   - Click **Unlock Design**.
   - Change Skew Angle to `15.0` degrees.
   - Click **Design**.
   - Showcase that the grillage solver adapts to skewed geometry.
4. *(Testing Note)*: Highlight that under `Customized` mode, consecutive runs without clearing state trigger the in-place unit mutation bug documented in the testing report.

---

### Scene 5: Loading OSI Test Cases (3:15 - 4:00)
1. Go to **File $\to$ Load Design Inputs (OSI)**.
2. Navigate to `submission/test_cases/TC01_baseline_30m_pass.osi` and load it.
   - Show the success pop-up: *"Loaded OSI Successfully!"*.
   - Verify that all docks populate with the baseline 30m configuration.
3. Next, load `submission/test_cases/TC04_fail_wc_density_clamp.osi`.
   - Show the Additional Inputs dialog where Wearing Course Density ($24.0\text{ kN/m}^3$) is clamped to $10.0\text{ kN/m}^3$ (demonstrating Issue #183).

---

### Scene 6: Automated Test Suite Verification (4:00 - 4:30)
1. Switch to terminal and run the full screening test suite:
   ```bash
   QT_QPA_PLATFORM=offscreen pytest -v tests/screening_tests/test_screening_suite.py
   ```
2. Show all 8 test cases executing and passing:
   - `test_tc01_baseline_design_and_output_dictionary PASSED`
   - `test_tc02_consecutive_multirun_unit_mutation_bug PASSED`
   - `test_tc03_custom_material_persistence PASSED`
   - `test_tc04_wc_density_validator_clamping_bug PASSED`
   - `test_tc05_stud_transverse_spacing_validator_unit_mismatch PASSED`
   - `test_tc06_deck_dead_load_wearing_course_omission PASSED`
   - `test_tc07_3d_cad_parameter_hardcoding_bug PASSED`
   - `test_tc08_geometric_boundary_cases PASSED`
   - Result: `8 passed in ~80s`

---

## Post-Recording & Upload Instructions
1. Save the screencast video file (e.g. `OsdagBridge_Testing_Demo_Sourav.mp4`).
2. Upload the video to:
   - **YouTube:** Set privacy to *Unlisted* (or Public).
   - **Google Drive:** Set access to *"Anyone with the link can view"*.
3. Copy the URL and paste it into the submission form field:
   `Link to a short video of your work (URL)`.
