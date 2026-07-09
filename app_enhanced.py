import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from datetime import datetime, timedelta
import json

# Set up page layout
st.set_page_config(
    page_title="Livestock Database Registry",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 15px;
        color: #155724;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 15px;
        color: #856404;
    }
    </style>
""", unsafe_allow_html=True)

DB_FILE = "consolidated_livestock_data.csv"
BACKUP_DIR = "backups"

# Create backup directory if it doesn't exist
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

# Safe Data Loader with Backup
def load_data():
    """Load livestock data with validation and backup creation"""
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        df['Tag ID'] = df['Tag ID'].astype(str).str.replace('.0', '', regex=False)
        
        # Dynamic column updates
        required_cols = ['Aadhaar No.', 'Other Details', 'Health Status', 'Vaccination Date', 'Last Check Date']
        for col in required_cols:
            if col not in df.columns:
                df[col] = ""
        
        return df
    else:
        st.warning(f"Database file '{DB_FILE}' not found. Please place your consolidated database file here first.")
        return pd.DataFrame()

def create_backup():
    """Create automatic backup of current database"""
    if os.path.exists(DB_FILE):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(BACKUP_DIR, f"backup_{timestamp}.csv")
        df = pd.read_csv(DB_FILE)
        df.to_csv(backup_file, index=False)
        return backup_file
    return None

def get_backup_files():
    """Get list of all backup files"""
    if os.path.exists(BACKUP_DIR):
        files = [f for f in os.listdir(BACKUP_DIR) if f.endswith('.csv')]
        return sorted(files, reverse=True)
    return []

def restore_backup(backup_file):
    """Restore database from backup"""
    backup_path = os.path.join(BACKUP_DIR, backup_file)
    if os.path.exists(backup_path):
        df = pd.read_csv(backup_path)
        df.to_csv(DB_FILE, index=False)
        return True
    return False

df = load_data()

if not df.empty:
    # Sidebar Navigation
    st.sidebar.title("🐾 Livestock Registry")
    page = st.sidebar.radio(
        "Select View:",
        ["📊 Dashboard", "➕ Add Entry", "🔍 Search & Edit", "📈 Analytics", "🗑️ Management", "⚙️ Settings"]
    )
    
    # ==========================================
    # PAGE 1: DASHBOARD
    # ==========================================
    if page == "📊 Dashboard":
        st.title("🐾 Livestock Development & Registration Dashboard")
        
        # Global Filters
        col1, col2 = st.columns(2)
        with col1:
            all_villages = sorted(df['Owner Village'].dropna().astype(str).unique().tolist())
            selected_villages = st.multiselect(
                "Filter by Owner Village:",
                all_villages,
                default=all_villages[:3] if len(all_villages) > 3 else all_villages
            )
        
        with col2:
            all_species = sorted(df['Species'].dropna().astype(str).unique().tolist())
            selected_species = st.multiselect(
                "Filter by Species:",
                all_species,
                default=all_species
            )
        
        # Apply Filters
        filtered_df = df[
            (df['Owner Village'].isin(selected_villages)) & 
            (df['Species'].isin(selected_species))
        ]
        
        # KPI Metrics
        st.subheader("📊 Key Performance Indicators")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Total Records", len(filtered_df))
        with col2:
            st.metric("Unique Owners", filtered_df['Owner Name'].nunique())
        with col3:
            st.metric("Villages", filtered_df['Owner Village'].nunique())
        with col4:
            active_count = len(filtered_df[filtered_df['Animal Status'] == 'Active'])
            st.metric("Active Animals", active_count)
        with col5:
            in_milk = len(filtered_df[filtered_df['Milking Status'] == 'In Milk'])
            st.metric("In Milk", in_milk)
        
        # Visualizations
        st.subheader("📈 Visualization Charts")
        
        col1, col2 = st.columns(2)
        
        if not filtered_df.empty:
            with col1:
                # Species distribution
                fig1 = px.histogram(
                    filtered_df,
                    x="Owner Village",
                    color="Species",
                    barmode="group",
                    title="Livestock Population by Village & Species",
                    height=400
                )
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                # Status distribution
                status_counts = filtered_df['Animal Status'].value_counts()
                fig2 = px.pie(
                    values=status_counts.values,
                    names=status_counts.index,
                    title="Animal Status Distribution",
                    height=400
                )
                st.plotly_chart(fig2, use_container_width=True)
        
        # Registry Table
        st.subheader("📋 Filtered Registry Ledger")
        if not filtered_df.empty:
            display_cols = ['Tag ID', 'Species', 'Breed', 'Owner Name', 'Aadhaar No.', 
                          'Owner Village', 'Owner Mobile No', 'Animal Status', 'Health Status']
            remaining_cols = [c for c in filtered_df.columns if c not in display_cols]
            
            st.dataframe(
                filtered_df[display_cols + remaining_cols],
                use_container_width=True,
                height=400
            )
            
            # Export options
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name=f"livestock_data_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        else:
            st.info("No records match the selected filters.")
    
    # ==========================================
    # PAGE 2: ADD NEW ENTRY
    # ==========================================
    elif page == "➕ Add Entry":
        st.header("📝 Register New Livestock Entry")
        st.write("Fill out the form below to add a new animal record to the database.")
        
        with st.form("insert_form", clear_on_submit=True):
            st.subheader("🐄 Animal Details")
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                new_tag = st.text_input("Tag ID (Unique)*", placeholder="e.g., L001")
                new_date = st.date_input("Tagging Date", value=datetime.now())
                new_species = st.selectbox("Species*", ["Cattle", "Buffalo", "Goat", "Sheep", "Other"])
            
            with col_b:
                new_breed = st.text_input("Breed", placeholder="e.g., Gir, Murrah")
                new_sex = st.selectbox("Sex*", ["Female", "Male"])
                new_status = st.selectbox("Status*", ["Active", "Inactive", "Died"])
            
            with col_c:
                new_preg = st.selectbox("Pregnancy Status", ["NA", "Y", "N"])
                new_milk = st.selectbox("Milking Status", ["NA", "In Milk", "Dry"])
                new_health = st.selectbox("Health Status", ["Healthy", "Sick", "Under Treatment"])
            
            st.subheader("👤 Owner Details")
            col_d, col_e, col_f = st.columns(3)
            
            with col_d:
                new_owner_name = st.text_input("Owner Name*", placeholder="Full name")
                new_aadhaar = st.text_input("Aadhaar No.", placeholder="12 digits")
            
            with col_e:
                new_village = st.text_input("Owner Village*", placeholder="Village name")
                new_mobile = st.text_input("Mobile No", placeholder="10 digits")
            
            with col_f:
                new_vaccine_date = st.date_input("Last Vaccination Date")
                new_check_date = st.date_input("Last Health Check")
            
            st.subheader("📝 Additional Information")
            new_other = st.text_area(
                "Remarks/Notes",
                placeholder="e.g., vaccination records, special conditions, loan status",
                height=100
            )
            
            submit_button = st.form_submit_button("💾 Save Entry to Database")
            
            if submit_button:
                # Validation
                if not new_tag or not new_owner_name or not new_village:
                    st.error("❌ Mandatory fields missing: Tag ID, Owner Name, and Village are required.")
                elif new_tag in df['Tag ID'].values:
                    st.error(f"❌ Tag ID {new_tag} already exists. Use a unique identifier.")
                elif new_mobile and len(new_mobile) != 10:
                    st.warning("⚠️ Mobile number should be 10 digits (validation skipped if empty).")
                else:
                    # Create new row
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
                        'Health Status': new_health,
                        'Vaccination Date': str(new_vaccine_date),
                        'Last Check Date': str(new_check_date),
                        'Other Details': str(new_other)
                    })
                    
                    # Save with backup
                    new_row_df = pd.DataFrame([new_row])
                    updated_df = pd.concat([df, new_row_df], ignore_index=True)
                    create_backup()
                    updated_df.to_csv(DB_FILE, index=False)
                    st.success(f"✅ Successfully saved! Tag ID {new_tag} registered to {new_owner_name}.")
                    st.rerun()
    
    # ==========================================
    # PAGE 3: SEARCH & EDIT
    # ==========================================
    elif page == "🔍 Search & Edit":
        st.header("🔍 Search & Edit Records")
        
        search_type = st.radio("Search by:", ["Tag ID", "Owner Name", "Owner Village"])
        
        if search_type == "Tag ID":
            search_query = st.text_input("Enter Tag ID:")
            if search_query:
                results = df[df['Tag ID'] == search_query.strip()]
        elif search_type == "Owner Name":
            search_query = st.text_input("Enter Owner Name:")
            if search_query:
                results = df[df['Owner Name'].str.contains(search_query, case=False, na=False)]
        else:
            search_query = st.text_input("Enter Village Name:")
            if search_query:
                results = df[df['Owner Village'].str.contains(search_query, case=False, na=False)]
        
        if 'search_query' in locals() and search_query:
            if not results.empty:
                st.subheader(f"Found {len(results)} record(s)")
                st.dataframe(results, use_container_width=True)
                
                if len(results) == 1:
                    st.subheader("Edit Record")
                    idx = results.index[0]
                    record = results.iloc[0]
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        new_health = st.selectbox(
                            "Update Health Status:",
                            ["Healthy", "Sick", "Under Treatment"],
                            index=["Healthy", "Sick", "Under Treatment"].index(record['Health Status']) if record['Health Status'] in ["Healthy", "Sick", "Under Treatment"] else 0
                        )
                        new_status = st.selectbox(
                            "Update Animal Status:",
                            ["Active", "Inactive", "Died"],
                            index=["Active", "Inactive", "Died"].index(record['Animal Status']) if record['Animal Status'] in ["Active", "Inactive", "Died"] else 0
                        )
                    
                    with col2:
                        new_vaccine_date = st.date_input("Update Vaccination Date:")
                        new_check_date = st.date_input("Update Last Check Date:")
                    
                    new_notes = st.text_area("Update Notes:", value=str(record['Other Details']))
                    
                    if st.button("💾 Update Record"):
                        create_backup()
                        df.loc[idx, 'Health Status'] = new_health
                        df.loc[idx, 'Animal Status'] = new_status
                        df.loc[idx, 'Vaccination Date'] = str(new_vaccine_date)
                        df.loc[idx, 'Last Check Date'] = str(new_check_date)
                        df.loc[idx, 'Other Details'] = new_notes
                        df.to_csv(DB_FILE, index=False)
                        st.success("✅ Record updated successfully!")
                        st.rerun()
            else:
                st.info("No records found matching your search.")
    
    # ==========================================
    # PAGE 4: ANALYTICS
    # ==========================================
    elif page == "📈 Analytics":
        st.header("📈 Advanced Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Species Distribution")
            species_data = df['Species'].value_counts()
            fig = px.bar(
                x=species_data.index,
                y=species_data.values,
                labels={'x': 'Species', 'y': 'Count'},
                color=species_data.values,
                color_continuous_scale='Viridis'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Health Status Overview")
            health_data = df['Health Status'].value_counts()
            fig = px.pie(values=health_data.values, names=health_data.index)
            st.plotly_chart(fig, use_container_width=True)
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.subheader("Milking Status")
            milk_data = df['Milking Status'].value_counts()
            fig = px.bar(
                x=milk_data.index,
                y=milk_data.values,
                labels={'x': 'Status', 'y': 'Count'},
                color=milk_data.values,
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col4:
            st.subheader("Top Villages by Livestock Count")
            village_data = df['Owner Village'].value_counts().head(10)
            fig = px.barh(
                x=village_data.values,
                y=village_data.index,
                labels={'x': 'Count', 'y': 'Village'},
                color=village_data.values,
                color_continuous_scale='Greens'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Summary Statistics
        st.subheader("📊 Summary Statistics")
        stats_col1, stats_col2, stats_col3 = st.columns(3)
        
        with stats_col1:
            st.metric("Total Livestock Records", len(df))
        with stats_col2:
            st.metric("Total Owners", df['Owner Name'].nunique())
        with stats_col3:
            st.metric("Total Villages", df['Owner Village'].nunique())
    
    # ==========================================
    # PAGE 5: MANAGEMENT
    # ==========================================
    elif page == "🗑️ Management":
        st.header("🗑️ Database Management")
        
        management_tab1, management_tab2, management_tab3 = st.tabs(
            ["Delete Record", "Backups", "Database Info"]
        )
        
        with management_tab1:
            st.subheader("Delete a Record")
            delete_search = st.text_input("Enter Tag ID to delete:")
            
            if delete_search:
                target_record = df[df['Tag ID'] == delete_search.strip()]
                
                if not target_record.empty:
                    st.warning("⚠️ Record Found - Please Verify Before Deletion")
                    st.table(target_record[['Tag ID', 'Species', 'Breed', 'Owner Name', 'Owner Village']])
                    
                    confirm_check = st.checkbox("I understand this action is permanent and cannot be undone.")
                    
                    if st.button("🔴 Permanently Delete Record"):
                        if confirm_check:
                            create_backup()
                            purged_df = df[df['Tag ID'] != delete_search.strip()]
                            purged_df.to_csv(DB_FILE, index=False)
                            st.success(f"✅ Record with Tag ID {delete_search} has been deleted.")
                            st.rerun()
                        else:
                            st.error("Please confirm deletion by checking the checkbox.")
                else:
                    st.info("No record found with that Tag ID.")
        
        with management_tab2:
            st.subheader("Backup Management")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("💾 Create Backup Now"):
                    backup_file = create_backup()
                    st.success(f"✅ Backup created: {backup_file}")
            
            with col2:
                backup_files = get_backup_files()
                if backup_files:
                    st.info(f"📦 {len(backup_files)} backup(s) available")
            
            st.subheader("Available Backups")
            backup_files = get_backup_files()
            if backup_files:
                selected_backup = st.selectbox("Select a backup to restore:", backup_files)
                if st.button("🔄 Restore Selected Backup"):
                    if restore_backup(selected_backup):
                        st.success(f"✅ Database restored from {selected_backup}")
                        st.rerun()
                    else:
                        st.error("Failed to restore backup.")
            else:
                st.info("No backups available.")
        
        with management_tab3:
            st.subheader("Database Information")
            
            info_col1, info_col2 = st.columns(2)
            
            with info_col1:
                st.metric("Total Records", len(df))
                st.metric("Total Owners", df['Owner Name'].nunique())
                st.metric("Total Villages", df['Owner Village'].nunique())
            
            with info_col2:
                st.metric("Species Types", df['Species'].nunique())
                st.metric("Database Size", f"{os.path.getsize(DB_FILE) / 1024:.2f} KB")
                st.metric("Last Modified", datetime.fromtimestamp(os.path.getmtime(DB_FILE)).strftime('%Y-%m-%d %H:%M'))
            
            st.subheader("Column Information")
            st.write(f"**Total Columns:** {len(df.columns)}")
            st.write("**Columns:**")
            st.write(", ".join(df.columns))
    
    # ==========================================
    # PAGE 6: SETTINGS
    # ==========================================
    elif page == "⚙️ Settings":
        st.header("⚙️ Application Settings")
        
        st.subheader("Database Configuration")
        st.info(f"📁 Database File: `{DB_FILE}`")
        st.info(f"📦 Backup Directory: `{BACKUP_DIR}`")
        
        st.subheader("Quick Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Reload Database"):
                st.rerun()
        
        with col2:
            if st.button("💾 Create Backup"):
                backup_file = create_backup()
                st.success(f"✅ Backup created: {backup_file}")
        
        with col3:
            if st.button("📊 Refresh Analytics"):
                st.rerun()
        
        st.subheader("About")
        st.write("""
        **🐾 Livestock Development & Registration Dashboard**
        
        Version: 2.0 (Enhanced)
        
        **Features:**
        - 📊 Advanced analytics and visualizations
        - ➕ Easy data entry with validation
        - 🔍 Powerful search and edit capabilities
        - 💾 Automatic backups
        - 📈 Species and location-based reporting
        - 🗑️ Safe deletion with confirmations
        
        **Supported on:**
        - Python 3.8+
        - Streamlit 1.28+
        - Pandas 2.0+
        - Plotly 5.17+
        """)

else:
    st.error("❌ Unable to load database. Please ensure 'consolidated_livestock_data.csv' exists in the application directory.")
