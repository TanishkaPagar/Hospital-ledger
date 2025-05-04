import streamlit as st
import hashlib

# Initialize the hospital ledger in session state to persist data
if 'hospital_ledger_advanced' not in st.session_state:
    st.session_state.hospital_ledger_advanced = {}

# Function to generate a hash for visit data
def generate_hash(patient_name, treatment, cost, date_of_visit):
    visit_data = patient_name + treatment + str(cost) + date_of_visit
    return hashlib.sha256(visit_data.encode()).hexdigest()

st.title("🏥 Hospital Visit Ledger")

st.header("Add or Update Patient Visit")

# Input fields
patient_name = st.text_input("Enter the patient's name")
treatment = st.text_input("Enter the treatment received")
cost = st.number_input("Enter the cost of the treatment ($)", min_value=0.0, format="%.2f")
date_of_visit = st.date_input("Enter the date of visit")

# Add visit button
if st.button("Add Visit"):
    if patient_name and treatment:
        ledger = st.session_state.hospital_ledger_advanced

        if patient_name in ledger:
            st.info(f"Updating visit record for {patient_name}.")
        else:
            st.success(f"Adding new visit record for {patient_name}.")

        visit_hash = generate_hash(patient_name, treatment, cost, str(date_of_visit))

        visit = {
            "treatment": treatment,
            "cost": cost,
            "date_of_visit": str(date_of_visit),
            "visit_hash": visit_hash
        }

        if patient_name not in ledger:
            ledger[patient_name] = []

        ledger[patient_name].append(visit)
        st.success(f"Visit added for {patient_name} on {date_of_visit} for treatment {treatment} costing ${cost}.")
        st.code(visit_hash, language="text")
    else:
        st.warning("Please enter both patient name and treatment.")

# Search section
st.header("🔍 Search Patient Visits")
search_patient = st.text_input("Enter patient name to search for")

if search_patient:
    ledger = st.session_state.hospital_ledger_advanced
    if search_patient in ledger:
        st.subheader(f"Visit records for {search_patient}:")
        for visit in ledger[search_patient]:
            st.markdown(f"- **Treatment**: {visit['treatment']}")
            st.markdown(f"  - Cost: ${visit['cost']}")
            st.markdown(f"  - Date: {visit['date_of_visit']}")
            st.markdown(f"  - Hash: `{visit['visit_hash']}`")
    else:
        st.error(f"No records found for {search_patient}.")
