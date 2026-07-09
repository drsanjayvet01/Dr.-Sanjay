import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Set up page layout
st.set_page_config(page_title="Livestock Database Registry", layout="wide")

DB_FILE = "consolidated_livestock_data.csv"

# Safe Data Loader
def load_data():
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        
        # Core safety: Ensure Tag ID handles full numeric strings
        df['Tag ID'] = df['Tag ID'].astype(str).str.replace('.0', '', regex=False)
        
        # DYNAMIC COLUMN UPDATES: Inject new tracking columns safely if they aren't in the CSV yet
        if 'Aadhaar No.' not in df.columns:
            df['Aadhaar No.'] = ""
        if 'Other Details' not in df.columns:
            df['Other Details'] = ""
            
        return df
    else:
        st.error(f"Database file '{DB_FILE}' not found. Please place your consolidated database file here first.")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # App Header Tabs
    tab1, tab2, tab3 = st.tabs(["📊 Analytics Dashboard", "➕ Register New Entry", "🗑️ Manage & Remove Records"])

    # ==========================================
    # TAB 1: VISUALS & REGISTRY LEDGER
    # ==========================================
    with tab1:
        st.title("🐾 Livestock Development & Registration Dashboard")
        
        # Sidebar filters
        st.sidebar.header("🔍 Global Filter Tools")
        all_villages = sorted(df['Owner Village'].dropna().astype(str).unique().tolist())
        selected_villages = st.sidebar.multiselect("Filter by Owner Village:", all_villages, default=all_villages[:3] if len(all_villages) > 3 else all_villages)
        
        all_species = sorted(df['Species'].dropna().astype(str).unique().tolist())
        selected_species = st.sidebar.multiselect("Filter by Species:", all_species, default=all_species)

        # Apply Filters
        filtered_df = df[(df['Owner Village'].isin(selected_villages)) & (df['Species'].isin(selected_species))]

        # KPI Summary metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Active Records", len(filtered_df))
        col2.metric("Unique Owners Enrolled", filtered_df['Owner Name'].nunique() if 'Owner Name' in filtered_df else 0)
        col3.metric("Villages Monitored", filtered_df['Owner Village'].nunique() if 'Owner Village' in filtered_df else 0)

        # Chart
        if not filtered_df.empty:
            fig = px.histogram(filtered_df, x="Owner Village", color="Species", barmode="group", title="Livestock Population Share")
            st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("📋 Filtered Registry Ledger View")
            # Rearrange view columns to bring Aadhaar and customized notes to a scannable spot
            display_cols = ['Tag ID', 'Species', 'Breed', 'Owner Name', 'Aadhaar No.', 'Owner Village', 'Owner Mobile No', 'Other Details']
            remaining_cols = [c for c in filtered_df.columns if c not in display_cols]
            
            st.dataframe(filtered_df[display_cols + remaining_cols], use_container_width=True)
        else:
            st.info("Select options from the sidebar to visualize demographic records.")

    # ==========================================
    # TAB 2: INSERT / ADD NEW LIVESTOCK DATA
    # ==========================================
    with tab2:
        st.header("📝 Register New Livestock Entry")
        st.write("Fill out the electronic form below to inject a brand-new row into your primary dataset.")
        
        with st.form("insert_form", clear_on_submit=True):
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                new_tag = st.text_input("Tag ID (Unique Identifier)*")
                new_date = st.date_input("Tagging Date")
                new_species = st.selectbox("Species", ["Cattle", "Buffalo", "Goat", "Sheep", "Other"])
                new_breed = st.text_input("Breed (e.g., Non-descript, Murrah, Gir)")
            
            with col_b:
                new_sex = st.selectbox("Animal Sex", ["Female", "Male"])
                new_status = st.selectbox("Animal Status", ["Active", "Inactive", "Died"])
                new_preg = st.selectbox("Pregnancy Status", ["N", "Y", "NA"])
                new_milk = st.selectbox("Milking Status", ["NA", "In Milk", "Dry"])
                
            with col_c:
                new_owner_name = st.text_input("Owner Full Name*")
                new_aadhaar = st.text_input("Owner Aadhaar Card No. (12 digits)")
                new_village = st.text_input("Owner Village*")
                new_mobile = st.text_input("Owner Mobile No")
            
            st.markdown("---")
            new_other = st.text_area("Other Details / Remarks (e.g., vaccination notes, loan status, or description)")

            submit_button = st.form_submit_button("💾 Save Entry to Database")
            
            if submit_button:
                if not new_tag or not new_owner_name or not new_village:
                    st.error("Submission failed. 'Tag ID', 'Owner Name', and 'Owner Village' are mandatory fields.")
                elif new_tag in df['Tag ID'].values:
                    st.error(f"A livestock entry with Tag ID {new_tag} already exists in your registry records.")
                else:
                    # Construct matching dictionary object aligned perfectly with schema
                    new_row = {col: "" for col in df.columns}
                    new_row.update({
                        'Tag ID': str(new_tag),
                        'Tagging Date': str(new_date),
                        'Species': new_species,
                        'Breed': new_breed,
                        'Animal Sex': new_sex,
                        'Animal Status': new_status,
                        'Pregnancy Status': new_preg,
                        'Milking Status': new_milk,
                        'Owner Name': new_owner_name,
                        'Aadhaar No.': str(new_aadhaar),
                        'Owner Village': new_village,
                        'Owner Mobile No': str(new_mobile),
                        'Other Details': str(new_other)
                    })
                    
                    # Convert to dataframe row and append safely
                    new_row_df = pd.DataFrame([new_row])
                    updated_df = pd.concat([df, new_row_df], ignore_index=True)
                    updated_df.to_csv(DB_FILE, index=False)
                    st.success(f"Successfully saved records! Tag ID {new_tag} assigned to {new_owner_name} has been recorded.")
                    st.rerun()

    # ==========================================
    # TAB 3: REMOVE / DELETE DATA RECORDS
    # ==========================================
    with tab3:
        st.header("🗑️ Database Management & Entry Eviction")
        st.write("Search for an animal entry by its unique Tag ID to purge or erase it completely from the file system database.")
        
        delete_search = st.text_input("Enter Tag ID to Target for Removal:")
        
        if delete_search:
            target_record = df[df['Tag ID'] == delete_search.strip()]
            
            if not target_record.empty:
                st.warning("⚠️ Match Found! Please confirm details carefully before clicking remove.")
                st.table(target_record[['Tag ID', 'Species', 'Breed', 'Owner Name', 'Aadhaar No.', 'Owner Village']])
                
                confirm_check = st.checkbox("Yes, I understand this action is permanent and cannot be undone.")
                
                if st.button("🔴 Permanently Delete Record"):
                    if confirm_check:
                        purged_df = df[df['Tag ID'] != delete_search.strip()]
                        purged_df.to_csv(DB_FILE, index=False)
                        st.success(f"Success! Record corresponding to Tag ID {delete_search} was wiped out.")
                        st.rerun()
                    else:
                        st.error("Please click the confirmation checkbox above to authorize deletion execution.")
            else:
                st.info("No matching registration entry found under that Tag ID.")
