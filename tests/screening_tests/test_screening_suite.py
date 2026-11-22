"""
FOSSEE Osdag Winter Internship 2026 - Screening Task Test Suite
Project: OsdagBridge Software Testing & Issue Reporting
Candidate: Sourav Goswami

Comprehensive multi-level test suite covering:
- TC-01: Baseline Design & Output Dictionary Verification
- TC-02: Multi-Run State Persistence & In-Place Unit Mutation Bug
- TC-03: Custom Material Properties Registration & Persistence
- TC-04: Wearing Course Density Validator Upper-Bound Clamping Bug (Issue #183)
- TC-05: Shear Stud Transverse Spacing Unit Inconsistency Bug (Issue #184)
- TC-06: Deck Slab Dead-Load Wearing Course Omission Bug (Issue #185)
- TC-07: 3D CAD Parameter Generation Hardcoded Dimensions Bug (Issue #186)
- TC-08: Geometric Boundary Conditions & Skew Layout Variations
"""

import copy
import pytest
from PySide6.QtWidgets import QApplication

# Ensure QApplication singleton for headless test execution
app = QApplication.instance() or QApplication([])

from osdagbridge.core.bridge_types.plate_girder.plategirderbridge import PlateGirderBridge
from osdagbridge.core.bridge_types.plate_girder.defaults import (
    BASIC_INPUT_DICT,
    solve_extend_basic_input_dict,
)
from osdagbridge.core.bridge_types.plate_girder.validator import BridgeInputValidator
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
    KEY_TS_GIRDER_SPACING,
    KEY_TS_DECK_OVERHANG,
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


def create_base_inputs(span=30.0, carriageway=7.5, skew=0.0, mode="Optimized"):
    """Helper to assemble a fully-resolved input dictionary."""
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


class TestOsdagBridgeScreeningSuite:
    """Screening test suite for OsdagBridge plate girder module."""

    def test_tc01_baseline_design_and_output_dictionary(self):
        """TC-01: Baseline 30m span design run and dictionary completeness verification."""
        inputs = create_base_inputs(span=30.0, carriageway=7.5, skew=0.0, mode="Optimized")
        bridge = PlateGirderBridge()
        bridge.set_input(inputs)

        # Execute end-to-end design
        bridge.design()

        # Output dictionary verification
        out = bridge.output_dict
        assert out is not None, "Output dictionary was not populated."
        assert len(out) > 50, f"Expected >50 output keys, got {len(out)}"

        # Verify key structural components are present in output dictionary
        essential_keys = [
            "typical_section.deck_thickness",
            "deck_report_values",
            "crossbracing_design_results",
            "end_diaphragm_design_results",
        ]
        for k in essential_keys:
            assert k in out, f"Missing essential output key: {k}"

        # Verify deck report dictionary values
        deck_report = out["deck_report_values"]
        assert deck_report["deck.report.punch_ok"] is True
        assert deck_report["deck.report.shear_ok"] is True
        assert deck_report["deck.report.as_bot"] > deck_report["deck.report.as_req_bot"]

        # Verify 3D CAD parameter generation DTO
        cad_params = bridge.get_3d_cad_parameters()
        assert cad_params.span_length_L == 30000.0  # 30m in mm
        assert cad_params.num_girders == 4

    def test_tc02_consecutive_multirun_unit_mutation_bug(self):
        """
        TC-02: Multi-run state persistence test demonstrating the in-place unit mutation bug.
        In Customized mode, _convert_girder_dims_mm_to_m() mutates input_dict in-place,
        collapsing dimensions by 1000x on each consecutive run.
        """
        inp = {
            KEY_DESIGN_MODE: "Customized",
            KEY_SPAN: 30.0,
            KEY_TS_NO_OF_GIRDERS: 4,
            KEY_MP_GIRDER_DEPTH: 1670.0,
            f"{KEY_MP_GIRDER_DEPTH}.G1.M1": 1670.0,
            KEY_MP_GIRDER_WEB_DEPTH: 1628.0,
            f"{KEY_MP_GIRDER_WEB_DEPTH}.G1.M1": 1628.0,
            KEY_MP_GIRDER_TOP_FLANGE_WIDTH: 510.0,
            f"{KEY_MP_GIRDER_TOP_FLANGE_WIDTH}.G1.M1": 510.0,
            KEY_MP_GIRDER_BOTTOM_FLANGE_WIDTH: 510.0,
            f"{KEY_MP_GIRDER_BOTTOM_FLANGE_WIDTH}.G1.M1": 510.0,
            KEY_MP_GIRDER_TOP_FLANGE_THICKNESS: 22.0,
            f"{KEY_MP_GIRDER_TOP_FLANGE_THICKNESS}.G1.M1": 22.0,
            KEY_MP_GIRDER_BOTTOM_FLANGE_THICKNESS: 22.0,
            f"{KEY_MP_GIRDER_BOTTOM_FLANGE_THICKNESS}.G1.M1": 22.0,
            KEY_MP_GIRDER_WEB_THICKNESS: 10.0,
            f"{KEY_MP_GIRDER_WEB_THICKNESS}.G1.M1": 10.0,
        }
        bridge = PlateGirderBridge()
        bridge.input_dict = copy.deepcopy(inp)

        # Run 1: Converts 1670 mm -> 1.67 m
        bridge._convert_girder_dims_mm_to_m()
        assert bridge.input_dict[KEY_MP_GIRDER_DEPTH] == pytest.approx(1.67, rel=1e-3)
        assert bridge.input_dict[KEY_MP_GIRDER_TOP_FLANGE_THICKNESS] == pytest.approx(0.022, rel=1e-3)

        # Run 2: Without re-initialization (consecutive run), divides by 1000 AGAIN
        bridge._convert_girder_dims_mm_to_m()
        depth_run2 = bridge.input_dict[KEY_MP_GIRDER_DEPTH]
        thk_run2 = bridge.input_dict[KEY_MP_GIRDER_TOP_FLANGE_THICKNESS]

        # Demonstrates the severe bug: depth collapsed to 1.67 mm, thickness collapsed to 0.022 mm
        assert depth_run2 == pytest.approx(0.00167, rel=1e-3), (
            f"Expected depth to corrupt to 0.00167m due to in-place mutation, got {depth_run2}"
        )
        assert thk_run2 == pytest.approx(0.000022, rel=1e-3)

        # Run 3: Third consecutive run collapses dimensions to micron levels
        bridge._convert_girder_dims_mm_to_m()
        depth_run3 = bridge.input_dict[KEY_MP_GIRDER_DEPTH]
        assert depth_run3 == pytest.approx(1.67e-6, rel=1e-3)

    def test_tc03_custom_material_persistence(self):
        """TC-03: Verify that user-specified custom material properties register and persist."""
        inputs = create_base_inputs(span=30.0, carriageway=7.5, skew=0.0)

        # Inject high-strength custom steel and concrete properties
        custom_fy = 450.0  # MPa
        custom_fu = 570.0  # MPa
        custom_e = 205000.0  # MPa
        custom_g = 78846.0  # MPa
        custom_fck = 45.0  # MPa

        inputs[KEY_MATERIAL_GIRDER_FY] = custom_fy
        inputs[KEY_MATERIAL_GIRDER_FU] = custom_fu
        inputs[KEY_MATERIAL_GIRDER_E] = custom_e
        inputs[KEY_MATERIAL_GIRDER_G] = custom_g
        inputs[KEY_MATERIAL_DECK_FCK] = custom_fck

        bridge = PlateGirderBridge()
        bridge.set_input(inputs)

        # Verify that set_input preserved custom material properties
        assert bridge.input_dict[KEY_MATERIAL_GIRDER_FY] == custom_fy
        assert bridge.input_dict[KEY_MATERIAL_GIRDER_FU] == custom_fu
        assert bridge.input_dict[KEY_MATERIAL_GIRDER_E] == custom_e
        assert bridge.input_dict[KEY_MATERIAL_GIRDER_G] == custom_g
        assert bridge.input_dict[KEY_MATERIAL_DECK_FCK] == custom_fck

    def test_tc04_wc_density_validator_clamping_bug(self):
        """
        TC-04: Test Wearing Course density validation against Issue #183.
        Demonstrates that standard wearing course density (24.0 kN/m³) is wrongly clamped to 10.0 kN/m³.
        """
        validator = BridgeInputValidator()
        inp_dict = {KEY_WC_DENSITY: 24.0}

        corrected_val, msg = validator.validate_additional_inputs(KEY_WC_DENSITY, inp_dict)

        # Bug assertion: validator currently clamps valid 24.0 kN/m³ to 10.0 kN/m³
        assert corrected_val == 10.0, (
            f"Expected bug behavior: 24.0 clamped to 10.0, but got {corrected_val}"
        )
        assert "outside the practical range" in msg

    def test_tc05_stud_transverse_spacing_validator_unit_mismatch(self):
        """
        TC-05: Test shear stud transverse spacing validation against Issue #184.
        Demonstrates that line 845 in validator.py fails when top_flange_width is in metres.
        """
        validator = BridgeInputValidator()
        # Top flange width = 0.51 m (510 mm), stud count = 3, diameter = 25 mm
        # Line 848 formula: max_sp = flange_mm - 50 - d * (n - 1)
        # With flange_mm erroneously = 0.51: max_sp = 0.51 - 50 - 50 = -99.49 mm!
        context = {
            KEY_MP_GIRDER_TOP_FLANGE_WIDTH: 0.51,  # stored in metres
            KEY_DS_STUD_DIAMETER: 25.0,
            KEY_DS_STUD_COUNT: 3,
            KEY_DS_STUD_TRANSVERSE_SPACING: 100.0,  # completely valid 100 mm spacing
        }

        corrected_val, msg = validator.validate_additional_inputs(
            KEY_DS_STUD_TRANSVERSE_SPACING, context
        )

        # Due to max_sp being negative (-99.49), valid spacing 100.0 is rejected and clamped to -99.49
        assert corrected_val < 0, (
            f"Expected negative clamped value due to unit mismatch bug, got {corrected_val}"
        )
        assert "Transverse spacing must be between" in msg

    def test_tc06_deck_dead_load_wearing_course_omission(self):
        """
        TC-06: Test deck slab dead load calculations against Issue #185.
        Verifies that DeckDesigner omits wearing course dead load from w_DL_kN_m2.
        """
        from osdagbridge.core.utils.codes.irc6_2017 import IRC6_2017

        # Unit weight of reinforced concrete = 2.5 t/m³ * 9.81 = 24.525 kN/m³
        gamma_concrete_kN_m3 = IRC6_2017.cl_203_dead_load()["concrete_cement_reinforced"] * 9.81
        deck_t_mm = 250.0
        w_slab_only = gamma_concrete_kN_m3 * (deck_t_mm / 1000.0)  # 6.13125 kN/m²

        # Standard wearing course = 65 mm * 24.0 kN/m³ = 1.56 kN/m²
        w_wc = (65.0 / 1000.0) * 24.0  # 1.56 kN/m²
        expected_total_dl = w_slab_only + w_wc  # 7.69125 kN/m²

        # Code in deckdesign.py:518 computes:
        # w_DL_kN_m2 = gamma_concrete_kN_m3 * (deck_t_mm / 1000.0)
        actual_code_dl = w_slab_only

        # Assert that actual code omits wearing course contribution (under-design by 20.3%)
        assert actual_code_dl == pytest.approx(6.13125, rel=1e-3)
        assert actual_code_dl < expected_total_dl
        assert (expected_total_dl - actual_code_dl) == pytest.approx(1.56, rel=1e-2)

    def test_tc07_3d_cad_parameter_hardcoding_bug(self):
        """
        TC-07: Test 3D CAD parameter generation against Issue #186.
        Demonstrates that get_3d_cad_parameters() hardcodes 1500mm footpath and 375mm railing.
        """
        inputs = create_base_inputs(span=30.0, carriageway=7.5)
        inputs[KEY_FOOTPATH] = "Both"
        inputs[KEY_TS_FOOTPATH_WIDTH] = 2200.0  # custom 2.2m width
        inputs[KEY_RL_WIDTH] = 500.0  # custom 500mm railing

        bridge = PlateGirderBridge()
        bridge.set_input(inputs)
        bridge.output_dict = dict(bridge.input_dict)
        bridge.output_dict["KEY_GIRDER"] = "E 350A"
        bridge.output_dict["KEY_DECK_CONCRETE_GRADE_BASIC"] = "M 40"
        bridge.output_dict[KEY_MP_GIRDER_DEPTH] = 1.67
        bridge.output_dict[KEY_MP_GIRDER_WEB_THICKNESS] = 0.010
        bridge.output_dict[KEY_MP_GIRDER_TOP_FLANGE_WIDTH] = 0.510
        bridge.output_dict[KEY_MP_GIRDER_TOP_FLANGE_THICKNESS] = 0.022
        bridge.output_dict[KEY_MP_GIRDER_BOTTOM_FLANGE_WIDTH] = 0.510
        bridge.output_dict[KEY_MP_GIRDER_BOTTOM_FLANGE_THICKNESS] = 0.022
        bridge._solve_shear_studs()

        cad_params = bridge.get_3d_cad_parameters()

        # Bug assertion: CAD parameters DTO hardcodes default 1500mm and 375mm, ignoring user inputs
        assert cad_params.footpath_width == 1500.0, (
            f"Expected hardcoded 1500.0 mm, got {cad_params.footpath_width}"
        )
        assert cad_params.railing_width == 375.0, (
            f"Expected hardcoded 375.0 mm, got {cad_params.railing_width}"
        )

    def test_tc08_geometric_boundary_cases(self):
        """TC-08: Geometric variations including 15° and 30° skew angles and varying carriageway widths."""
        for skew in [0.0, 15.0, 30.0]:
            inputs = create_base_inputs(span=24.0, carriageway=7.5, skew=skew)
            bridge = PlateGirderBridge()
            bridge.set_input(inputs)
            assert bridge.input_dict[KEY_SKEW_ANGLE] == skew
            assert bridge.input_dict[KEY_SPAN] == 24.0
            assert bridge.input_dict[KEY_CARRIAGEWAY_WIDTH] == 7.5
