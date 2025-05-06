import streamlit as st
import json
import pandas as pd
from math import sqrt

with open("climate_zones.json", "r") as f:
    zipcode_to_zone = json.load(f)

# Define tables 140.10-A and 140.10-B as dictionaries
table_140_10_A = {
    "Events & Exhibits": {
        1: 3.48, 2: 4.28, 3: 3.66, 4: 4.32, 5: 3.77, 6: 4.05, 7: 4.28, 8: 4.83,
        9: 4.63, 10: 4.80, 11: 5.04, 12: 4.44, 13: 4.95, 14: 4.36, 15: 5.48, 16: 3.38
    },
    "Library": {
        1: 0.39, 2: 3.23, 3: 2.59, 4: 3.25, 5: 2.48, 6: 2.74, 7: 3.04, 8: 3.49,
        9: 3.32, 10: 3.69, 11: 3.79, 12: 3.32, 13: 3.79, 14: 3.37, 15: 4.49, 16: 2.84
    },
    "Hotel/Motel": {
        1: 1.69, 2: 1.90, 3: 1.66, 4: 1.97, 5: 1.69, 6: 1.87, 7: 1.94, 8: 2.22,
        9: 2.09, 10: 2.20, 11: 2.30, 12: 2.05, 13: 2.30, 14: 2.02, 15: 2.72, 16: 1.73
    },
    "Office": {  # Includes Office, Financial, Unleased Tenant, Medical
        1: 2.59, 2: 3.13, 3: 2.59, 4: 3.13, 5: 2.59, 6: 3.13, 7: 3.13, 8: 3.13,
        9: 3.13, 10: 3.13, 11: 3.13, 12: 3.13, 13: 3.13, 14: 3.13, 15: 3.80, 16: 2.59
    },
    "Restaurants": {
        1: 8.55, 2: 9.32, 3: 8.16, 4: 9.65, 5: 8.21, 6: 8.73, 7: 9.11, 8: 10.18,
        9: 9.75, 10: 10.28, 11: 10.85, 12: 9.73, 13: 10.69, 14: 9.73, 15: 12.25, 16: 8.47
    },
    "Retail, Grocery": {
        1: 3.14, 2: 3.49, 3: 3.01, 4: 3.61, 5: 3.05, 6: 3.27, 7: 3.45, 8: 3.83,
        9: 3.65, 10: 3.81, 11: 4.09, 12: 3.64, 13: 3.99, 14: 3.71, 15: 4.60, 16: 3.21
    },
    "School": {
        1: 1.27, 2: 1.63, 3: 1.27, 4: 1.63, 5: 1.27, 6: 1.63, 7: 1.63, 8: 1.63,
        9: 1.63, 10: 1.63, 11: 1.63, 12: 1.63, 13: 1.63, 14: 1.63, 15: 2.46, 16: 1.27
    },
    "Warehouse": {
        1: 0.39, 2: 0.44, 3: 0.39, 4: 0.44, 5: 0.39, 6: 0.44, 7: 0.44, 8: 0.44,
        9: 0.44, 10: 0.44, 11: 0.44, 12: 0.44, 13: 0.44, 14: 0.44, 15: 0.58, 16: 0.39
    },
    "Religious Worship": {
        1: 4.25, 2: 4.65, 3: 3.49, 4: 4.52, 5: 3.72, 6: 4.29, 7: 4.64, 8: 5.89,
        9: 5.30, 10: 5.67, 11: 5.89, 12: 4.99, 13: 5.78, 14: 4.63, 15: 7.57, 16: 3.90
    },
    "Sports & Recreation": {
        1: 2.47, 2: 1.97, 3: 1.54, 4: 2.03, 5: 1.60, 6: 1.84, 7: 1.98, 8: 2.63,
        9: 2.47, 10: 2.60, 11: 2.75, 12: 2.20, 13: 2.72, 14: 2.15, 15: 4.03, 16: 1.81
    },
    "Multifamily > 3 stories": {
        1: 1.82, 2: 2.21, 3: 1.82, 4: 2.21, 5: 1.82, 6: 2.21, 7: 2.21, 8: 2.21,
        9: 2.21, 10: 2.21, 11: 2.21, 12: 2.21, 13: 2.21, 14: 2.21, 15: 2.77, 16: 1.82
    }
}


table_140_10_B = {
    "Events & Exhibits": {
        1: 1.82, 2: 1.95, 3: 1.74, 4: 2.12, 5: 1.91, 6: 2.13, 7: 2.24, 8: 2.30,
        9: 2.36, 10: 2.47, 11: 2.62, 12: 2.16, 13: 2.64, 14: 2.68, 15: 3.22, 16: 1.89
    },
    "Library": {
        1: 0.37, 2: 7.17, 3: 5.97, 4: 6.75, 5: 5.64, 6: 6.08, 7: 6.19, 8: 7.13,
        9: 7.18, 10: 7.56, 11: 7.17, 12: 6.93, 13: 6.88, 14: 6.81, 15: 7.93, 16: 6.40
    },
    "Hotel/Motel": {
        1: 0.86, 2: 0.84, 3: 0.77, 4: 0.92, 5: 0.81, 6: 0.89, 7: 0.90, 8: 1.01,
        9: 1.00, 10: 1.11, 11: 1.14, 12: 0.96, 13: 1.18, 14: 1.18, 15: 1.49, 16: 0.85
    },
    "Office": {  # Includes Office, Financial Institution, Unleased Tenant Space, Medical Office
        1: None, 2: 5.26, 3: 4.35, 4: 5.26, 5: 4.35, 6: 5.26, 7: 5.26, 8: 5.26,
        9: 5.26, 10: 5.26, 11: 5.26, 12: 5.26, 13: 5.26, 14: 5.26, 15: 6.39, 16: 4.35
    },
    "Restaurants": {
        1: 4.36, 2: 4.11, 3: 3.78, 4: 4.37, 5: 3.89, 6: 4.02, 7: 4.11, 8: 4.49,
        9: 4.47, 10: 4.82, 11: 5.05, 12: 4.43, 13: 5.05, 14: 5.24, 15: 6.23, 16: 4.11
    },
    "Retail, Grocery": {
        1: 1.89, 2: 1.82, 3: 2.70, 4: 1.82, 5: 1.72, 6: 1.80, 7: 1.76, 8: 1.92,
        9: 1.97, 10: 2.05, 11: 2.22, 12: 1.95, 13: 2.16, 14: 2.29, 15: 2.66, 16: 1.91
    },
    "School": {
        1: None, 2: 3.05, 3: 2.38, 4: 3.05, 5: 2.38, 6: 3.05, 7: 3.05, 8: 3.05,
        9: 3.05, 10: 3.05, 11: 3.05, 12: 3.05, 13: 3.05, 14: 3.05, 15: 4.60, 16: 2.38
    },
    "Warehouse": {
        1: 0.37, 2: 0.41, 3: 0.37, 4: 0.41, 5: 0.37, 6: 0.41, 7: 0.41, 8: 0.41,
        9: 0.41, 10: 0.41, 11: 0.41, 12: 0.41, 13: 0.41, 14: 0.41, 15: 0.54, 16: 0.37
    },
    "Religious Worship": {
        1: 2.21, 2: 2.25, 3: 1.74, 4: 2.42, 5: 2.08, 6: 2.75, 7: 2.94, 8: 3.37,
        9: 3.17, 10: 3.37, 11: 3.58, 12: 2.72, 13: 3.62, 14: 3.21, 15: 4.89, 16: 2.37
    },
    "Sports & Recreation": {
        1: 1.26, 2: 0.98, 3: 0.76, 4: 1.14, 5: 0.86, 6: 1.20, 7: 1.23, 8: 1.57,
        9: 1.53, 10: 1.65, 11: 1.83, 12: 1.27, 13: 1.86, 14: 1.57, 15: 3.02, 16: 1.13
    },
    "Multifamily > 3 stories": {
        1: 1.88, 2: 2.27, 3: 1.88, 4: 2.27, 5: 1.88, 6: 2.27, 7: 2.27, 8: 2.27,
        9: 2.27, 10: 2.27, 11: 2.27, 12: 2.27, 13: 2.27, 14: 2.27, 15: 2.85, 16: 1.88
    }
}


def calculate_pv_system_size(cfa, building_type, climate_zone, sara=None, roof_slope="Low Slope"):
    """
    Calculates the required PV system size in kWdc, including exemptions and SARA limit.
    """
    if cfa < 2000:
        return 0, "PV system exempt: CFA < 2000 ft²"

    a = table_140_10_A[building_type][climate_zone]
    kw_pv_dc = (cfa * a) / 1000  # Equation 140.10-A

    # Apply SARA limit if provided
    if sara is not None:
        slope_factor = 14 if roof_slope.lower() == "low slope" else 18
        sara_limit_kw = (sara * slope_factor) / 1000
        kw_pv_dc = min(kw_pv_dc, sara_limit_kw)

    # Additional PV exemptions
    pv_exempt_msg = ""
    if sara is not None and sara < 80:
        pv_exempt_msg = "PV system exempt: SARA < 80 ft²"
    elif sara is not None and sara < (0.03 * cfa):
        pv_exempt_msg = "PV system exempt: SARA < 3% of CFA"
    elif kw_pv_dc < 4:
        pv_exempt_msg = "PV system exempt: PV capacity < 4 kWdc"


    return kw_pv_dc, pv_exempt_msg


def calculate_bess_energy_capacity(cfa, building_type, climate_zone, c, sara, kw_pv_dc, full_kw_pv_dc):
    """
    Calculates the required BESS energy capacity in kWh using Equation 140.10-C.
    """
    b = table_140_10_B[building_type][climate_zone]
    if b is None:
        return 0, "BESS system exempt: Not Required per Table 140.10-B"

    if full_kw_pv_dc == 0:
        return 0, "BESS system exempt: No PV system required"

    if kw_pv_dc < 0.15 * full_kw_pv_dc:
        return 0, "BESS system exempt: PV system < 15% of Eq. 140.10-A capacity"

    kw_pv_dc_sara = min(kw_pv_dc, full_kw_pv_dc) if sara is not None else kw_pv_dc
    kwh_batt = ((cfa * b) / (1000 * (c ** 0.5))) * (kw_pv_dc_sara / full_kw_pv_dc)

    if kwh_batt < 10:
        return 0, "BESS system exempt: calculated kWh(batt) < 10 kWh"

    return kwh_batt, ""


def calculate_bess_power_capacity(kwh_batt):
    """
    Calculates required BESS power capacity in kW.
    """
    return kwh_batt / 4


st.set_page_config(page_title="Title 24 PV + BESS Sizing Tool", layout="wide")

col_info, col_main = st.columns([1, 3])

with col_info:
    st.markdown("""
    <div style='background-color:#f0f2f6;padding:1em;border-radius:8px;'>
    <strong>ℹ️ About This Tool</strong><br><br>
    This calculator estimates photovoltaic (PV) and battery energy storage system (BESS) sizes for nonresidential buildings under California's **Title 24, Part 6, 2025 Energy Code**.
    <ul>
    <li>Uses CFA, ZIP code, and building types</li>
    <li>Applies Tables 140.10-A & B</li>
    <li>Flags exemptions automatically</li>
    </ul>
    <a href='https://www.energy.ca.gov/programs-and-topics/programs/building-energy-efficiency-standards/2025-building-energy-efficiency' target='_blank'>View official standards ↗</a>
    </div>
    """, unsafe_allow_html=True)

with col_main:
    st.title("⚡ Title 24 2025 PV & BESS Sizing Tool")

    # Input: Basic Info
    cfa = st.number_input("Conditioned Floor Area (ft²)", min_value=0.0, step=100.0)
    sara = st.number_input("Solar Access Roof Area (SARA, ft²)", min_value=0.0, step=10.0)
    c = st.number_input("BESS Round-Trip Efficiency (0.85 - 1.0)", min_value=0.5, max_value=1.0, value=0.9, step=0.01)

    # Input: Zip Code (text input instead of dropdown)
    zipcode = st.text_input("Enter Zip Code")
    climate_zone = None
    zipcode_valid = False
    if zipcode:
        try:
            climate_zone = next(entry["Building CZ"] for entry in zipcode_to_zone if str(entry["Zip Code"]) == str(zipcode))
            zipcode_valid = True
        except StopIteration:
            st.error("Invalid or unsupported ZIP code.")

    # Input: Dynamic list of building types
    building_types = list(table_140_10_A.keys())
    st.subheader("🏢 Building Types")

    selected_types = []
    proportions = []
    total_proportion = 0

    num_inputs = st.number_input("Number of Building Types", min_value=1, max_value=50, step=1, value=1)
    for i in range(num_inputs):
        col1, col2 = st.columns(2)
        with col1:
            btype = st.selectbox(f"Building Type {i+1}", building_types, key=f"type_{i}")
        with col2:
            prop = st.number_input(f"Proportion of CFA for {btype}", min_value=0.0, max_value=1.0, value=1.0/num_inputs, key=f"prop_{i}", step=0.01)
        selected_types.append(btype)
        proportions.append(prop)
        total_proportion += prop

    proportions_valid = abs(total_proportion - 1.0) <= 0.01
    if not proportions_valid:
        st.warning("⚠️ Proportions do not sum to 1. They will be normalized.")
        proportions = [p/total_proportion for p in proportions]

    # Enable button only if ZIP is valid and proportions are correct
    can_calculate = zipcode_valid and proportions_valid

    st.markdown("---")
    if st.button("📐 Calculate System Sizes", disabled=not can_calculate):
        full_kw_pv_dc = sum(calculate_pv_system_size(cfa * prop, btype, climate_zone)[0] for btype, prop in zip(selected_types, proportions))
        kw_pv_dc_installed = sum(calculate_pv_system_size(cfa * prop, btype, climate_zone, sara, "Low Slope")[0] for btype, prop in zip(selected_types, proportions))

        # Handle PV Exemption
        if kw_pv_dc_installed == 0:
            st.info("🔌 PV System Exempt")
        else:
            # Calculate BESS
            kwh_batt = 0
            for btype, prop in zip(selected_types, proportions):
                cap, msg = calculate_bess_energy_capacity(cfa * prop, btype, climate_zone, c, sara, kw_pv_dc_installed, full_kw_pv_dc)
                kwh_batt += cap

            kw_batt = calculate_bess_power_capacity(kwh_batt) if kwh_batt >= 10 else 0

            st.subheader("📊 Results")
            st.metric("Required PV Size (kWdc)", f"{kw_pv_dc_installed:.2f}")
            st.metric("Required BESS Energy Capacity (kWh)", f"{kwh_batt:.2f}" if kwh_batt else "Exempt")
            st.metric("Required BESS Power Output (kW)", f"{kw_batt:.2f}" if kw_batt else "Exempt")


def main():
    # User inputs
    cfa = float(input("Enter conditioned floor area (CFA) in ft²: "))
    sara = float(input("Enter SARA in ft²: "))
    num_types = int(input("Enter number of different building types (1 or more): "))
    building_types = []
    proportions = []

    total_proportion = 0
    if num_types > 0:
        if num_types == 1:
            building_type = input("Enter building type (match table name): ")
            while building_type not in table_140_10_A.keys():
                print("Invalid building type. Please enter a valid building type from the table.")
                building_type = input("Enter building type (match table name): ")
            building_types = [building_type]
            proportions = [1.0]
            total_proportion = 1.0
        else:
            for i in range(num_types):
                print(f"\nBuilding Type {i + 1}:")
                building_type = input("Enter building type (match table name): ")
                while building_type not in table_140_10_A.keys():
                    print("Invalid building type. Please enter a valid building type from the table.")
                    building_type = input("Enter building type (match table name): ")

                proportion = float(input(f"Enter proportion for {building_type} (0-1): "))
                while proportion < 0 or proportion > 1:
                    print("Invalid proportion. Please enter a value between 0 and 1.")
                    proportion = float(input(f"Enter proportion for {building_type} (0-1): "))

                total_proportion += proportion
                building_types.append(building_type)
                proportions.append(proportion)

        if abs(total_proportion - 1.0) > 0.001:
            print("Warning: Proportions do not sum to 1. Normalizing values...")
            proportions = [p/total_proportion for p in proportions]
    else:
        building_type = input("Enter building type (match table name): ")
        while building_type not in table_140_10_A.keys():
            print("Invalid building type. Please enter a valid building type from the table.")
            building_type = input("Enter building type (match table name): ")
        building_types = [building_type]
        proportions = [1.0]
    with open('climate_zones.json', 'r') as f:
        zipcode_to_zone = json.load(f)

    zipcode = input("Enter zipcode: ")
    while str(zipcode) not in [str(entry["Zip Code"]) for entry in zipcode_to_zone]:
        print("Invalid or unsupported zipcode. Please enter a valid zipcode.")
        zipcode = input("Enter zipcode: ")

    climate_zone = next(entry["Building CZ"] for entry in zipcode_to_zone if str(entry["Zip Code"]) == str(zipcode))
    c = float(input("Enter BESS round-trip efficiency (e.g. 0.90): "))

    # Calculate total system requirements
    full_kw_pv_dc = 0
    kw_pv_dc_installed = 0
    kwh_batt = 0
    bess_exempt_msg = None

    # Calculate total system size before exemptions
    total_full_kw = sum(calculate_pv_system_size(cfa * prop, btype, climate_zone)[0] 
                       for btype, prop in zip(building_types, proportions))

    # Check PV system exemption for total system
    if cfa < 2000:
        print("Warning: PV system exempt: Total CFA < 2000 ft²")
        full_kw_pv_dc = 0
        kw_pv_dc_installed = 0
    else:
        # Calculate installed PV considering SARA
        kw_pv_dc_installed = sum(calculate_pv_system_size(cfa * prop, btype, climate_zone, sara, "Low Slope")[0] 
                                for btype, prop in zip(building_types, proportions))
        full_kw_pv_dc = total_full_kw

    # Calculate BESS requirements if PV system is required
    if kw_pv_dc_installed > 0:
        for building_type, proportion in zip(building_types, proportions):
            type_kwh_batt, type_bess_msg = calculate_bess_energy_capacity(
                cfa * proportion, building_type, climate_zone, c, sara, kw_pv_dc_installed, full_kw_pv_dc
            )
            if not type_bess_msg:
                kwh_batt += type_kwh_batt
    if bess_exempt_msg:
        print(bess_exempt_msg)
        return

    # Step 4: BESS Power Capacity
    kw_batt = calculate_bess_power_capacity(kwh_batt)

    if kwh_batt < 10:
        print("BESS system exempt: Energy capacity < 10 kWh")
        kwh_batt = 0
        kw_batt = 0

    # Output
    print("\n--- Title 24 2025 System Sizing ---")
    print(f"Required PV system size: {kw_pv_dc_installed:.2f} kWdc")
    print(f"Required BESS energy capacity: {kwh_batt:.2f} kWh")
    print(f"Required BESS power output: {kw_batt:.2f} kW")


if __name__ == "__main__":
    main()