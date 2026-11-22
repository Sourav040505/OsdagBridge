"""
Script to generate screening test case OSI files for OsdagBridge.
FOSSEE Osdag Winter Internship 2026
Candidate: Sourav Goswami
"""

import os
import copy
import yaml
from PySide6.QtWidgets import QApplication

app = QApplication.instance() or QApplication([])

from osdagbridge.core.bridge_types.plate_girder.defaults import (
    BASIC_INPUT_DICT,
    solve_extend_basic_input_dict,
)
from osdagbridge.core.utils.common import (
    KEY_PROJECT_LOCATION,
    KEY_SPAN,
    KEY_CARRIAGEWAY_WIDTH,
    KEY_SKEW_ANGLE,
    KEY_DESIGN_MODE,
    KEY_FOOTPATH,
    KEY_TS_FOOTPATH_WIDTH,
    KEY_RL_WIDTH,
    KEY_TS_NO_OF_GIRDERS,
    KEY_MP_GIRDER_DEPTH,
    KEY_MP_GIRDER_WEB_DEPTH,
    KEY_MP_GIRDER_TOP_FLANGE_WIDTH,
    KEY_MP_GIRDER_BOTTOM_FLANGE_WIDTH,
    KEY_MP_GIRDER_TOP_FLANGE_THICKNESS,
    KEY_MP_GIRDER_BOTTOM_FLANGE_THICKNESS,
    KEY_MP_GIRDER_WEB_THICKNESS,
    KEY_WC_DENSITY,
    KEY_WC_THICKNESS,
    KEY_DS_STUD_TRANSVERSE_SPACING,
    KEY_DS_STUD_COUNT,
    KEY_DS_STUD_DIAMETER,
    KEY_MATERIAL_GIRDER_FY,
    KEY_MATERIAL_GIRDER_FU,
    KEY_MATERIAL_GIRDER_E,
    KEY_MATERIAL_GIRDER_G,
    KEY_MATERIAL_DECK_FCK,
    KEY_MATERIAL_DECK_ECM,
    KEY_MATERIAL_DECK_DENSITY,
)
from osdagbridge.desktop.ui.dialogs.material_properties import MaterialPropertiesDialog


def get_base_inputs(span=30.0, carriageway=7.5, skew=0.0, mode="Optimized"):
    inputs = copy.deepcopy(BASIC_INPUT_DICT)
    inputs[KEY_PROJECT_LOCATION] = "Mumbai"
    inputs[KEY_SPAN] = float(span)
    inputs[KEY_CARRIAGEWAY_WIDTH] = float(carriageway)
    inputs[KEY_SKEW_ANGLE] = float(skew)
    inputs[KEY_DESIGN_MODE] = mode

    for m in ["Girder", "Cross Bracing", "End Diaphragm"]:
        dlg = MaterialPropertiesDialog(read_only=True, member=m, selected_material="E 350A")
        inputs.update(dlg.get_export_fields())
    dlg_conc = MaterialPropertiesDialog(read_only=True, member="Deck", selected_material="M 40")
    inputs.update(dlg_conc.get_export_fields())

    solve_extend_basic_input_dict(inputs)
    return inputs


def main():
    target_dir = os.path.join(os.path.dirname(__file__), "test_cases")
    os.makedirs(target_dir, exist_ok=True)

    # 1. TC-01: Baseline 30m Span (Pass)
    tc01 = get_base_inputs(span=30.0, carriageway=7.5, skew=0.0, mode="Optimized")
    with open(os.path.join(target_dir, "TC01_baseline_30m_pass.osi"), "w") as f:
        yaml.dump(tc01, f, default_flow_style=False)
    print("Generated TC01_baseline_30m_pass.osi")

    # 2. TC-02: Custom High-Strength Materials (Pass)
    tc02 = get_base_inputs(span=30.0, carriageway=7.5, skew=0.0, mode="Optimized")
    tc02[KEY_MATERIAL_GIRDER_FY] = 450.0  # E450 Steel
    tc02[KEY_MATERIAL_GIRDER_FU] = 570.0
    tc02[KEY_MATERIAL_GIRDER_E] = 205000.0
    tc02[KEY_MATERIAL_GIRDER_G] = 78846.0
    tc02[KEY_MATERIAL_DECK_FCK] = 45.0  # M45 Concrete
    tc02[KEY_MATERIAL_DECK_ECM] = 34500.0
    tc02[KEY_MATERIAL_DECK_DENSITY] = 25.0
    with open(os.path.join(target_dir, "TC02_custom_materials_e450_m45_pass.osi"), "w") as f:
        yaml.dump(tc02, f, default_flow_style=False)
    print("Generated TC02_custom_materials_e450_m45_pass.osi")

    # 3. TC-03: Skew Angle 30 Degrees (Pass)
    tc03 = get_base_inputs(span=28.0, carriageway=7.5, skew=30.0, mode="Optimized")
    with open(os.path.join(target_dir, "TC03_skew_30deg_pass.osi"), "w") as f:
        yaml.dump(tc03, f, default_flow_style=False)
    print("Generated TC03_skew_30deg_pass.osi")

    # 4. TC-04: Wearing Course Density Clamping Bug (Fail / Bug Trigger - Issue #183)
    tc04 = get_base_inputs(span=30.0, carriageway=7.5, skew=0.0, mode="Optimized")
    tc04[KEY_WC_DENSITY] = 24.0  # Clamped to 10.0 kN/m3 erroneously by validator
    with open(os.path.join(target_dir, "TC04_fail_wc_density_clamp.osi"), "w") as f:
        yaml.dump(tc04, f, default_flow_style=False)
    print("Generated TC04_fail_wc_density_clamp.osi")

    # 5. TC-05: Shear Stud Transverse Spacing Unit Mismatch (Fail / Bug Trigger - Issue #184)
    tc05 = get_base_inputs(span=30.0, carriageway=7.5, skew=0.0, mode="Optimized")
    tc05[KEY_DS_STUD_COUNT] = 3
    tc05[KEY_DS_STUD_DIAMETER] = 25.0
    tc05[KEY_DS_STUD_TRANSVERSE_SPACING] = 100.0  # Validator erroneously checks against negative max_sp
    with open(os.path.join(target_dir, "TC05_fail_stud_spacing_unit_mismatch.osi"), "w") as f:
        yaml.dump(tc05, f, default_flow_style=False)
    print("Generated TC05_fail_stud_spacing_unit_mismatch.osi")

    # 6. TC-06: Consecutive Run In-Place Mutation (Fail / Bug Trigger - Issue #187)
    tc06 = get_base_inputs(span=30.0, carriageway=7.5, skew=0.0, mode="Customized")
    tc06[KEY_MP_GIRDER_DEPTH] = 1670.0
    tc06[KEY_MP_GIRDER_WEB_DEPTH] = 1628.0
    tc06[KEY_MP_GIRDER_TOP_FLANGE_WIDTH] = 510.0
    tc06[KEY_MP_GIRDER_BOTTOM_FLANGE_WIDTH] = 510.0
    tc06[KEY_MP_GIRDER_TOP_FLANGE_THICKNESS] = 22.0
    tc06[KEY_MP_GIRDER_BOTTOM_FLANGE_THICKNESS] = 22.0
    tc06[KEY_MP_GIRDER_WEB_THICKNESS] = 10.0
    for g in range(1, 5):
        for m in range(1, 3):
            tc06[f"{KEY_MP_GIRDER_DEPTH}.G{g}.M{m}"] = 1670.0
            tc06[f"{KEY_MP_GIRDER_WEB_DEPTH}.G{g}.M{m}"] = 1628.0
            tc06[f"{KEY_MP_GIRDER_TOP_FLANGE_WIDTH}.G{g}.M{m}"] = 510.0
            tc06[f"{KEY_MP_GIRDER_BOTTOM_FLANGE_WIDTH}.G{g}.M{m}"] = 510.0
            tc06[f"{KEY_MP_GIRDER_TOP_FLANGE_THICKNESS}.G{g}.M{m}"] = 22.0
            tc06[f"{KEY_MP_GIRDER_BOTTOM_FLANGE_THICKNESS}.G{g}.M{m}"] = 22.0
            tc06[f"{KEY_MP_GIRDER_WEB_THICKNESS}.G{g}.M{m}"] = 10.0
    with open(os.path.join(target_dir, "TC06_fail_consecutive_run_mutation.osi"), "w") as f:
        yaml.dump(tc06, f, default_flow_style=False)
    print("Generated TC06_fail_consecutive_run_mutation.osi")


if __name__ == "__main__":
    main()
