#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import io
from io import BytesIO
import math

# Define your CSV file paths here (use raw strings or double backslashes)
swl_csv = 'excavator_swl.csv'  # Ensure this file exists
bucket_csv = 'bucket_data.csv'  # Make sure this file exists
bhc_bucket_csv = 'bhc_bucket_data.csv'  # Make sure this file exists
dump_truck_csv = 'dump_trucks.csv'  # Path to dump truck CSV

# Function to generate Excel file
def generate_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Productivity Study')
    # Return the Excel content as bytes
    return output.getvalue()

# Load datasets
def load_bucket_data(bucket_csv):
    return pd.read_csv(bucket_csv)

def load_bhc_bucket_data(bhc_bucket_csv):
    return pd.read_csv(bhc_bucket_csv)

def load_dump_truck_data(dump_truck_csv):
    return pd.read_csv(dump_truck_csv)

def load_excavator_swl_data(swl_csv):
    swl_data = pd.read_csv(swl_csv)
    swl_data['boom_length'] = pd.to_numeric(swl_data['boom_length'], errors='coerce')
    swl_data['arm_length'] = pd.to_numeric(swl_data['arm_length'], errors='coerce')
    swl_data['CWT'] = pd.to_numeric(swl_data['CWT'], errors='coerce')
    swl_data['shoe_width'] = pd.to_numeric(swl_data['shoe_width'], errors='coerce')
    swl_data['reach'] = pd.to_numeric(swl_data['reach'], errors='coerce')
    swl_data['class'] = pd.to_numeric(swl_data['class'], errors='coerce')
    return swl_data

def generate_html_table(data, title):
    """
    Generate a simple HTML table from a dictionary where keys are column headers
    and values are lists of data. The table will have a dynamic title.
    """
    # Extract headers dynamically from the keys of the data dictionary
    headers = list(data.keys())
    
    # Find the maximum length of the lists (rows) in the data dictionary
    num_rows = max(len(data[header]) for header in headers)
    
    # Start the HTML table structure with fixed table width
    html = """
    <style>
        table {
            width: 100%; /* Set a fixed width for the table */
            margin: 25px auto; /* Center the table horizontally */
            border-collapse: collapse;
            font-size: 16px;
            text-align: left;
        }
        th, td {
            padding: 12px 15px;
            border: 1px solid #ddd;
        }
        th {
            background-color: #f4f4f4;
            color: #333;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        tr:hover {
            background-color: #f1f1f1;
        }
        h3 {
            font-size: 22px;
            color: #0044cc;
            font-weight: bold;
            border-bottom: 2px solid #0044cc;
            padding-bottom: 5px;
            margin-bottom: 15px;
        }
    </style>
    """
    
    # Use the title for both the h3 and table
    html += f"<h3>{title}</h3>"
    html += "<table><thead><tr>"
    
    # Add table headers
    for header in headers:
        html += f"<th>{header}</th>"
    
    html += "</tr></thead><tbody>"
    
    # Add rows to the table, ensuring to handle any missing data gracefully
    for i in range(num_rows):
        html += "<tr>"
        for header in headers:
            value = data[header][i] if i < len(data[header]) else ""
            html += f"<td>{value}</td>"
        html += "</tr>"
    
    html += "</tbody></table>"
    
    return html


# Load the data
dump_truck_data = load_dump_truck_data(dump_truck_csv)
swl_data = load_excavator_swl_data(swl_csv)

#APP
# Main Streamlit App UI
def app():
    st.write("Copyright © ONTRAC Group Pty Ltd 2024.")

# Streamlit UI
st.title("ONTRAC XMOR® Bucket Solution\n\n")
st.title("Excavator Selection")

# Step 1: Select Excavator Make
excavator_make = st.selectbox("Select Excavator Make", swl_data['make'].unique())

# Step 2: Filter by selected make and select Excavator Model
filtered_data_make = swl_data[swl_data['make'] == excavator_make]
excavator_model = st.selectbox("Select Excavator Model", filtered_data_make['model'].unique())

# Step 3: Filter by selected model and select Boom Length
filtered_data_model = filtered_data_make[filtered_data_make['model'] == excavator_model]
boom_length = st.selectbox("Select Boom Length (m)", filtered_data_model['boom_length'].unique())

# Step 4: Filter further by selected boom length and select Arm Length
filtered_data_boom = filtered_data_model[filtered_data_model['boom_length'] == boom_length]
arm_length = st.selectbox("Select Arm Length (m)", filtered_data_boom['arm_length'].unique())

# Step 5: Filter further by selected arm length and select Counterweight
filtered_data_arm = filtered_data_boom[filtered_data_boom['arm_length'] == arm_length]
cwt = st.selectbox("Select Counterweight (CWT in kg)", filtered_data_arm['CWT'].unique())

# Step 6: Filter further by selected counterweight and select Shoe Width
filtered_data_cwt = filtered_data_arm[filtered_data_arm['CWT'] == cwt]
shoe_width = st.selectbox("Select Shoe Width (mm)", filtered_data_cwt['shoe_width'].unique())

# Step 7: Filter further by selected shoe width and select Reach
filtered_data_shoe = filtered_data_cwt[filtered_data_cwt['shoe_width'] == shoe_width]
reach = st.selectbox("Select Operating Reach (m)", filtered_data_shoe['reach'].unique())

# Dump truck inputs
st.title("Dump Truck Selection")
truck_brand = st.selectbox("Select Dump Truck Brand", dump_truck_data['brand'].unique())
truck_type = st.selectbox("Select Dump Truck Type", dump_truck_data[dump_truck_data['brand'] == truck_brand]['type'].unique())
truck_model = st.selectbox("Select Dump Truck Model", dump_truck_data[(dump_truck_data['brand'] == truck_brand) & 
                                                                     (dump_truck_data['type'] == truck_type)]['model'].unique())
truck_payload = st.selectbox("Select Dump Truck Payload (tonnes)", dump_truck_data[dump_truck_data['model'] == truck_model]['payload'].unique())

# Additional Inputs

st.title("Additional Information")
material_density = st.number_input("Material Density (kg/m³)     e.g. 1500", min_value=0.0)
quick_hitch = st.checkbox("My Machine Uses a Quick Hitch")
quick_hitch_weight = st.number_input("Quick Hitch Weight (kg)", min_value=0.0) if quick_hitch else 0
current_bucket_size = st.number_input("Current Bucket Size (m³)", min_value=0.0)
current_bucket_weight = st.number_input("Current Bucket Weight (kg)", min_value=0.0)
machine_swings_per_minute = st.number_input("Machine Swings per Minute", min_value=0.0)

# Checkbox for BHC buckets
select_bhc = st.checkbox("Select from BHC buckets only (Heavy Duty)")

# Function to calculate SWL match
def find_matching_swl(user_data):
    matching_excavator = swl_data[
        (swl_data['make'] == user_data['make']) &
        (swl_data['model'] == user_data['model']) &
        (swl_data['CWT'] == user_data['cwt']) &
        (swl_data['shoe_width'] == user_data['shoe_width']) &
        (swl_data['reach'] == user_data['reach']) &
        (swl_data['boom_length'] == user_data['boom_length']) &
        (swl_data['arm_length'] == user_data['arm_length'])
    ]
    if matching_excavator.empty:
        return None
    swl = matching_excavator.iloc[0]['swl']
    return swl

# Function to calculate bucket load
def calculate_bucket_load(bucket_size, material_density):
    return bucket_size * material_density

def adjust_payload_for_new_bucket(dump_truck_payload, new_payload):
    max_payload = dump_truck_payload * 1.10  # Allow up to 10% adjustment
    increment = dump_truck_payload * 0.001   # Fine adjustment increments

    # Try to achieve swing values within ±0.14 tolerance
    current_payload = dump_truck_payload
    while current_payload <= max_payload:
        swings_to_fill_truck_new = current_payload / new_payload
        if abs(swings_to_fill_truck_new - math.ceil(swings_to_fill_truck_new)) <= 0.05:
            return current_payload, swings_to_fill_truck_new
        current_payload += increment

    # If no suitable payload is found, return the original payload with calculated swings
    swings_to_fill_truck_new = dump_truck_payload / new_payload
    return dump_truck_payload, swings_to_fill_truck_new

def adjust_payload_for_old_bucket(dump_truck_payload, old_payload):
    max_payload = dump_truck_payload * 1.10  # Allow up to 10% adjustment
    increment = dump_truck_payload * 0.001   # Fine adjustment increments

    # Try to achieve swing values within ±0.14 tolerance
    current_payload = dump_truck_payload
    while current_payload <= max_payload:
        swings_to_fill_truck_old = current_payload / old_payload
        if abs(swings_to_fill_truck_old - math.ceil(swings_to_fill_truck_old)) <= 0.05:
            return current_payload, swings_to_fill_truck_old
        current_payload += increment

    # If no suitable payload is found, return the original payload with calculated swings
    swings_to_fill_truck_old = dump_truck_payload / old_payload
    return dump_truck_payload, swings_to_fill_truck_old

def select_optimal_bucket(user_data, bucket_data, swl):
    current_bucket_size = user_data['current_bucket_size']
    optimal_bucket = None
    highest_bucket_size = 0

    selected_model = user_data['model']
    excavator_class = swl_data[swl_data['model'] == selected_model]['class'].iloc[0]

    for index, bucket in bucket_data.iterrows():
        if bucket['class'] > excavator_class + 10:
            continue

        bucket_load = calculate_bucket_load(bucket['bucket_size'], user_data['material_density'])
        total_bucket_weight = user_data['quick_hitch_weight'] + bucket_load + bucket['bucket_weight']

        if total_bucket_weight <= swl and bucket['bucket_size'] > highest_bucket_size:
            highest_bucket_size = bucket['bucket_size']
            optimal_bucket = {
                'bucket_name': bucket['bucket_name'],
                'bucket_size': highest_bucket_size,
                'bucket_weight': bucket['bucket_weight'],
                'total_bucket_weight': total_bucket_weight
            }

    return optimal_bucket

# Get user input data
user_data = {
    'make': excavator_make,
    'model': excavator_model,
    'boom_length': boom_length,
    'arm_length': arm_length,
    'cwt': cwt,
    'shoe_width': shoe_width,
    'reach': reach,
    'material_density': material_density,
    'quick_hitch_weight': quick_hitch_weight,
    'current_bucket_size': current_bucket_size,
    'current_bucket_weight': current_bucket_weight,
    'dump_truck_payload': truck_payload,
    'machine_swings_per_minute': machine_swings_per_minute
}

# Find matching SWL and optimal bucket
# Add a "Calculate" button
calculate_button = st.button("Calculate")

# Run calculations only when the button is pressed
if calculate_button:
    swl = find_matching_swl(user_data)
    if swl:
        # Load selected bucket data
        selected_bucket_csv = bhc_bucket_csv if select_bhc else bucket_csv
        bucket_data = load_bucket_data(selected_bucket_csv)
    
        optimal_bucket = select_optimal_bucket(user_data, bucket_data, swl)
    
        if optimal_bucket:
            st.success(f"Good news! ONTRAC could improve your productivity!")
            st.success(f"Your ONTRAC XMOR® Bucket Solution is the: {optimal_bucket['bucket_name']} ({optimal_bucket['bucket_size']} m³)")
            #st.write(f"Total Suspended Load (XMOR® Bucket): {optimal_bucket['total_bucket_weight']:.0f}kg")
            #st.write(f"Safe Working Load at {user_data['reach']}m reach ({user_data['make']} {user_data['model']}): {swl:.0f}kg")
            #st.write(" ")
            #st.write(f"Calculations based on the {user_data['make']} {user_data['model']} with a {user_data['boom_length']}m boom, {user_data['arm_length']}m arm, {user_data['cwt']}kg counterweight, {user_data['shoe_width']}mm shoes, operating at a reach of {user_data['reach']}m, and with a material density of {user_data['material_density']:.0f}kg/m³.")
            #st.write(f"Dump Truck: {truck_brand} {truck_model}, Rated payload = {user_data['dump_truck_payload'] * 1000 :.0f}kg")

            # Show table
            old_capacity = user_data['current_bucket_size']
            new_capacity = optimal_bucket['bucket_size']
            old_payload = calculate_bucket_load(old_capacity, user_data['material_density'])
            new_payload = calculate_bucket_load(new_capacity, user_data['material_density'])
    
            dump_truck_payload = user_data['dump_truck_payload'] * 1000
            machine_swings_per_minute = user_data['machine_swings_per_minute']
    
            # Total suspended load
            old_total_load = old_payload + user_data['current_bucket_weight'] + user_data['quick_hitch_weight']
            new_total_load = optimal_bucket['total_bucket_weight']  # Corrected variable

            # Adjust payload for the new bucket using the function
            dump_truck_payload_new, swings_to_fill_truck_new = adjust_payload_for_new_bucket(dump_truck_payload, new_payload)
            dump_truck_payload_old, swings_to_fill_truck_old = adjust_payload_for_old_bucket(dump_truck_payload, old_payload)
    
            # Time to fill truck in minutes
            time_to_fill_truck_old = swings_to_fill_truck_old / machine_swings_per_minute
            time_to_fill_truck_new = swings_to_fill_truck_new / machine_swings_per_minute
    
            # Average number of trucks per hour at 75% efficiency
            avg_trucks_per_hour_old = (60 / time_to_fill_truck_old) * 0.75 if time_to_fill_truck_old > 0 else 0
            avg_trucks_per_hour_new = (60 / time_to_fill_truck_new) * 0.75 if time_to_fill_truck_new > 0 else 0
    
            # Swings per hour
            swings_per_hour_old = swings_to_fill_truck_old * avg_trucks_per_hour_old
            swings_per_hour_new = swings_to_fill_truck_new * avg_trucks_per_hour_new
    
            # Total swings per hour
            total_swings_per_hour = 60 * machine_swings_per_minute

            # Truck Tonnes per hour
            truck_tonnage_per_hour_old = swings_per_hour_old * old_capacity * user_data['material_density'] / 1000
            truck_tonnage_per_hour_new = swings_per_hour_new * new_capacity * user_data['material_density'] / 1000
    
            # Production (t/hr)
            total_tonnage_per_hour_old = total_swings_per_hour * old_capacity * user_data['material_density'] / 1000
            total_tonnage_per_hour_new = total_swings_per_hour * new_capacity * user_data['material_density'] / 1000
    
            # Production (t/hr)
            tonnage_per_hour_old = avg_trucks_per_hour_old * dump_truck_payload_old / 1000
            tonnage_per_hour_new = avg_trucks_per_hour_new * dump_truck_payload_new / 1000
    
            # Assuming 1800 swings in a day
            total_m3_per_day_old = 1000 * old_capacity
            total_m3_per_day_new = 1000 * new_capacity
    
            # Total tonnage per day
            total_tonnage_per_day_old = total_m3_per_day_old * user_data['material_density'] / 1000
            total_tonnage_per_day_new = total_m3_per_day_new * user_data['material_density'] / 1000
    
            # Total number of trucks per day
            total_trucks_per_day_old = total_tonnage_per_day_old / dump_truck_payload * 1000
            total_trucks_per_day_new = total_tonnage_per_day_new / dump_truck_payload * 1000

            Productivity = f"{(1.1 * total_tonnage_per_hour_new - total_tonnage_per_hour_old) / total_tonnage_per_hour_old * 100:.0f}%"
    
            # Side-by-Side Bucket Comparison Data
            side_by_side_data = {
                'Description': [
                     'Capacity (m³)', 'Material Density (kg/m³)', 'Bucket Payload (kg)', 
                    'Total Suspended Load (kg)'
                ],
                'Old Bucket': [
                     f"{old_capacity:.1f}", f"{user_data['material_density']:.0f}", f"{old_payload:.0f}", 
                    f"{old_total_load:.0f}"
                ],
                'XMOR® Bucket': [
                     f"{new_capacity:.1f}", f"{user_data['material_density']:.0f}", f"{new_payload:.0f}", 
                    f"{new_total_load:.0f}"
                ],
                'Difference': [
                     f"{new_capacity - old_capacity:.1f}", '-', f"{new_payload - old_payload:.0f}", 
                    f"{new_total_load - old_total_load:.0f}"
                ],
                '% Difference': [
                     f"{(new_capacity - old_capacity) / old_capacity * 100:.0f}%", '-', f"{(new_payload - old_payload) / old_payload * 100:.0f}%", 
                    f"{(new_total_load - old_total_load) / old_total_load * 100:.0f}%"
                ]
            }
            
            # Loadout Productivity & Truck Pass Simulation Data
            loadout_productivity_data = {
                'Description': [
                     'Dump Truck Payload (kg)', 'Avg No. Swings to Fill Truck', 
                    'Time to Fill Truck (min)', 'Avg Trucks/Hour @ 75% eff', 'Swings/Hour', 'Tonnes/Hour'
                ],
                'Old Bucket': [
                     f"{dump_truck_payload_old:.0f}{'*' if dump_truck_payload_old != dump_truck_payload else ''}", f"{swings_to_fill_truck_old:.1f}", 
                    f"{time_to_fill_truck_old:.1f}", f"{avg_trucks_per_hour_old:.1f}", f"{swings_per_hour_old:.0f}", f"{truck_tonnage_per_hour_old:.0f}"
                ],
                'XMOR® Bucket': [
                     f"{dump_truck_payload_new:.0f}{'*' if dump_truck_payload_new != dump_truck_payload else ''}", f"{swings_to_fill_truck_new:.1f}", 
                    f"{time_to_fill_truck_new:.1f}", f"{avg_trucks_per_hour_new:.1f}", f"{swings_per_hour_new:.0f}", f"{truck_tonnage_per_hour_new:.0f}"
                ],
                'Difference': [
                     f"{dump_truck_payload_new - dump_truck_payload_old:.0f}", f"{swings_to_fill_truck_new - swings_to_fill_truck_old:.1f}", 
                    f"{time_to_fill_truck_new - time_to_fill_truck_old:.1f}", f"{avg_trucks_per_hour_new - avg_trucks_per_hour_old:.1f}",
                    "-", f"{truck_tonnage_per_hour_new - truck_tonnage_per_hour_old:.0f}"
                ],
                '% Difference': [
                     f"{(dump_truck_payload_new - dump_truck_payload_old) / dump_truck_payload_old * 100:.0f}%", 
                    f"{(swings_to_fill_truck_new - swings_to_fill_truck_old) / swings_to_fill_truck_old * 100:.0f}%",
                    f"{(time_to_fill_truck_new - time_to_fill_truck_old) / time_to_fill_truck_old * 100:.0f}%",
                    f"{(avg_trucks_per_hour_new - avg_trucks_per_hour_old) / avg_trucks_per_hour_old * 100:.0f}%",
                    "-",
                    f"{(truck_tonnage_per_hour_new - truck_tonnage_per_hour_old) / truck_tonnage_per_hour_old * 100:.0f}%"
                ]
            }
            
            # 1000 Swings Side-by-Side Simulation Data
            swings_simulation_data = {
                'Description': [
                     'Number of Swings', 'Total Volume (m³)', 
                    'Total Tonnes', 'Total Trucks'
                ],
                'Old Bucket': [
                    '1000', f"{total_m3_per_day_old:.0f}", f"{total_tonnage_per_day_old:.0f}", 
                    f"{total_trucks_per_day_old:.0f}"
                ],
                'XMOR® Bucket': [
                    '1000', f"{total_m3_per_day_new:.0f}", f"{total_tonnage_per_day_new:.0f}", 
                    f"{total_trucks_per_day_new:.0f}"
                ],
                'Difference': [
                    '-', f"{total_m3_per_day_new - total_m3_per_day_old:.0f}", 
                    f"{total_tonnage_per_day_new - total_tonnage_per_day_old:.0f}", 
                    f"{total_trucks_per_day_new - total_trucks_per_day_old:.0f}"
                ],
                '% Difference': [
                    '-', f"{(total_m3_per_day_new - total_m3_per_day_old) / total_m3_per_day_old * 100:.0f}%", 
                    f"{(total_tonnage_per_day_new - total_tonnage_per_day_old) / total_tonnage_per_day_old * 100:.0f}%", 
                    f"{(total_trucks_per_day_new - total_trucks_per_day_old) / total_trucks_per_day_old * 100:.0f}%"
                ]
            }
            
            # 10% Improved Cycle Time Simulation Data
            improved_cycle_data = {
                'Description': [
                     'Number of Swings', 'Total Volume (m³)', 
                    'Total Tonnes', 'Total Trucks'
                ],
                'Old Bucket': [
                    '1000', f"{total_m3_per_day_old:.0f}", f"{total_tonnage_per_day_old:.0f}", 
                    f"{total_trucks_per_day_old:.0f}"
                ],
                'XMOR® Bucket': [
                    '1100', f"{1.1 * total_m3_per_day_new:.0f}", f"{1.1 * total_tonnage_per_day_new:.0f}", 
                    f"{1.1 * total_trucks_per_day_new:.0f}"
                ],
                'Difference': [
                    '100', f"{1.1 * total_m3_per_day_new - total_m3_per_day_old:.0f}", 
                    f"{1.1 * total_tonnage_per_day_new - total_tonnage_per_day_old:.0f}", 
                    f"{1.1 * total_trucks_per_day_new - total_trucks_per_day_old:.0f}"
                ],
                '% Difference': [
                    '10%', f"{(1.1 * total_m3_per_day_new - total_m3_per_day_old) / total_m3_per_day_old * 100:.0f}%", 
                    f"{(1.1 * total_tonnage_per_day_new - total_tonnage_per_day_old) / total_tonnage_per_day_old * 100:.0f}%", 
                    f"{(1.1 * total_trucks_per_day_new - total_trucks_per_day_old) / total_trucks_per_day_old * 100:.0f}%"
                ]
            }
            
            # Convert each section into a DataFrame
            data_tables = {
            'Side-by-Side Bucket Comparison': side_by_side_data,
            'Loadout Productivity & Truck Pass Simulation': loadout_productivity_data,
            '1000 Swings Side-by-Side Simulation': swings_simulation_data,
            '10% Improved Cycle Time Simulation': improved_cycle_data
            }

            # Convert all data sections into individual DataFrames
            df_side_by_side = pd.DataFrame(side_by_side_data)
            df_loadout_productivity = pd.DataFrame(loadout_productivity_data)
            df_swings_simulation = pd.DataFrame(swings_simulation_data)
            df_improved_cycle = pd.DataFrame(improved_cycle_data)
            
            # Concatenate all DataFrames into one
            final_df = pd.concat([df_side_by_side, df_loadout_productivity, df_swings_simulation, df_improved_cycle], ignore_index=True)

            # Create a Pandas Excel writer
            excel_file = BytesIO()
            
            with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
                    # Create DataFrames for each dataset
                    final_df.to_excel(writer, sheet_name='Excavator Simulation Data', index=False)
                    # Ensure the file is saved in memory
                    writer.save()
                    
                # Rewind the buffer to the beginning so it can be read
            excel_file.seek(0)
            
            if df is not None:
                st.title('XMOR® Productivity Comparison')
                
                # Call the function for each table with the appropriate title
                st.markdown(generate_html_table(side_by_side_data, "Side-by-Side Bucket Comparison"), unsafe_allow_html=True)
                st.markdown(generate_html_table(loadout_productivity_data, "Loadout Productivity & Truck Pass Simulation"), unsafe_allow_html=True)
                st.markdown(generate_html_table(swings_simulation_data, "1000 Swings Side-by-Side Simulation"), unsafe_allow_html=True)
                st.markdown(generate_html_table(improved_cycle_data, "10% Improved Cycle Time Simulation"), unsafe_allow_html=True)
               
                if dump_truck_payload_new != dump_truck_payload:
                    st.write(f"*Dump Truck fill factor of {(100*dump_truck_payload_new/dump_truck_payload):.1f}% applied for XMOR® Bucket pass matching.")
                if dump_truck_payload_old != dump_truck_payload:
                    st.write(f"*Dump Truck fill factor of {(100*dump_truck_payload_old/dump_truck_payload):.1f}% applied for Old Bucket pass matching.")
                
                #st.write(f"Total Suspended Load (XMOR® Bucket): {optimal_bucket['total_bucket_weight']:.0f}kg")
                #st.write(f"Safe Working Load at {user_data['reach']}m reach ({user_data['make']} {user_data['model']}): {swl:.0f}kg")
                st.write(f"Calculations based on the {user_data['make']} {user_data['model']} with a {user_data['boom_length']}m boom, {user_data['arm_length']}m arm, {user_data['cwt']}kg counterweight, {user_data['shoe_width']}mm shoes, operating at a reach of {user_data['reach']}m, and with a material density of {user_data['material_density']:.0f}kg/m³.")
                st.write(f"Dump Truck: {truck_brand} {truck_model}, Rated payload = {user_data['dump_truck_payload'] * 1000 :.0f}kg")
                
                st.download_button(
                    label="Download Results In Excel",
                    data=excel_file,
                    file_name="productivity_study.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        else:
            st.write("No suitable bucket found within SWL limits.")
    else:
        st.write("No matching excavator configuration found!")
else:
    st.write("Please select options and press 'Calculate' to proceed.")
    

# Run the Streamlit app
if __name__ == '__main__':
    app()
