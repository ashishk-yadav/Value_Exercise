import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from PIL import Image
import re

# ----- standard field validation -----
def is_valid_name(name):
    return bool(re.match(r"^[A-Za-z\s'-]{1,50}$", name.strip()))

def is_valid_email(email):
    return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email.strip()))

# ---------- Load data ----------
@st.cache_data
def load_data():
    df = pd.read_csv(
        "Values Categories and Definition_Updated-070723.csv",
        quotechar='"', skipinitialspace=True, on_bad_lines='skip'
    )
    df.columns = df.columns.str.strip()
    return df

df = load_data()
core_values = sorted(df["Core Values"].dropna().unique().tolist())

def find_column(df, keys):
    for k in keys:
        for col in df.columns:
            if col.strip().lower() == k.lower():
                return col
    return None

col_core = find_column(df, ["core values"])
col_cat = find_column(df, ["categories", "category"])
col_def = find_column(df, ["definition of the value", "definition of value", "value definition", "definition"])

# ---------- Session state ----------
if "page" not in st.session_state:
    st.session_state.page = 1

if "user_info" not in st.session_state:
    st.session_state.user_info = {
        "first_name": "",
        "last_name": "",
        "email": ""
    }

if "touched_fields" not in st.session_state:
    st.session_state.touched_fields = {
        "first_name": False,
        "last_name": False,
        "email": False
    }


if "page_selections" not in st.session_state:
    st.session_state.page_selections = {i: set() for i in range(1, 6)}

def get_values_for_page(page):
    if page == 1:
        return core_values
    return list(st.session_state.page_selections.get(page - 1, set()))

def start_over():
    st.session_state.page = 1
    st.session_state.page_selections = {i: set() for i in range(1, 6)}
    st.rerun()

def go_back():
    st.session_state.page = max(1, st.session_state.page - 1)
    st.rerun()

def go_next():
    st.session_state.page += 1
    st.rerun()

# ---------- Main UI ----------
logo = Image.open('resource/logo.png')
st.image(logo)
st.title('Values Exercise')

st.header(f"Step {st.session_state.page}")
if st.session_state.page == 1:
    st.markdown("### 👤 Your Information")


    def touch_field(field):
        st.session_state.touched_fields[field] = True


    first_name = st.text_input(
        "First Name",
        value=st.session_state.user_info["first_name"],
        key="first_name_input",
        on_change=touch_field,
        args=("first_name",)
    )

    last_name = st.text_input(
        "Last Name",
        value=st.session_state.user_info["last_name"],
        key="last_name_input",
        on_change=touch_field,
        args=("last_name",)
    )

    email = st.text_input(
        "Email",
        value=st.session_state.user_info["email"],
        key="email_input",
        on_change=touch_field,
        args=("email",)
    )

    # Update session state with current input
    st.session_state.user_info["first_name"] = st.session_state["first_name_input"]
    st.session_state.user_info["last_name"] = st.session_state["last_name_input"]
    st.session_state.user_info["email"] = st.session_state["email_input"]

    # --- Validation flags ---
    errors = {
        "first_name": not is_valid_name(first_name),
        "last_name": not is_valid_name(last_name),
        "email": not is_valid_email(email),
    }

    # Display validation messages
    if st.session_state.touched_fields["first_name"] and errors["first_name"]:
        st.warning("⚠️ First name must contain only letters, spaces, apostrophes, or hyphens.")

    if st.session_state.touched_fields["last_name"] and errors["last_name"]:
        st.warning("⚠️ Last name must contain only letters, spaces, apostrophes, or hyphens.")

    if st.session_state.touched_fields["email"] and errors["email"]:
        st.warning("⚠️ Please enter a valid email address.")

    # Check if all fields are non-empty AND valid
    required_fields_filled = all([
        first_name.strip(),
        last_name.strip(),
        email.strip()
    ]) and not any(errors.values())

    st.markdown('''Below is a list of Core Values. 
                Select the values that resonate with you the most. 
                Click the Next button once you have completed this step.''')

elif st.session_state.page == 2:

    st.markdown("### 👤 Your Information")
    st.write(f"**Name:** {st.session_state.user_info['first_name']} {st.session_state.user_info['last_name']}")
    st.write(f"**Email:** {st.session_state.user_info['email']}")

    st.markdown('''Below are the values you selected. 
                Now select the values that stand out best to you. 
                If the total chosen values is less than twenty-five, you may select additional values but no more than twenty-five. 
                Click the Next button once you have completed this step.''')

elif st.session_state.page == 3:
    st.markdown("### 👤 Your Information")
    st.write(f"**Name:** {st.session_state.user_info['first_name']} {st.session_state.user_info['last_name']}")
    st.write(f"**Email:** {st.session_state.user_info['email']}")
    st.markdown('''Below are your top twenty-five values. 
                From the list below, select the values that matter the most to you. 
                There is no right or wrong answer. 
                You may select a maximum of 15 values. Click the Next button once you have completed this step.''')

elif st.session_state.page == 4:
    st.markdown("### 👤 Your Information")
    st.write(f"**Name:** {st.session_state.user_info['first_name']} {st.session_state.user_info['last_name']}")
    st.write(f"**Email:** {st.session_state.user_info['email']}")
    st.markdown('''Below are your top values. 
                These values are important to you and play a role in how you view yourself and the world. 
                From the list below, select the five values that stand out best to you. Select 5 values in the order of importance.
                There is no right or wrong selection.
                Click the Next button once you have completed this step.''')

elif st.session_state.page == 5:
    st.markdown("### 👤 Your Information")
    st.write(f"**Name:** {st.session_state.user_info['first_name']} {st.session_state.user_info['last_name']}")
    st.write(f"**Email:** {st.session_state.user_info['email']}")
    st.markdown('''Below are your top five values. 
                Each of the values listed helps make up your value system the most. 
                They are the driving force behind what matters most to you and will 
                often be the foundation for your actions, behavior, and decisions. ''')

values_to_show = get_values_for_page(st.session_state.page)
if len(values_to_show) == 0:
    st.warning("No values carried over from the previous page.")

max_selections = {2: 25, 3: 15, 4: 5}
current_page = st.session_state.page

if current_page < 5 and len(values_to_show) > 0:
    df_ag = pd.DataFrame({
        "Core Value": values_to_show,
        "Value Selected": [val in st.session_state.page_selections[current_page] for val in values_to_show]
    })
    gb = GridOptionsBuilder.from_dataframe(df_ag)
    gb.configure_column("Value Selected", editable=True, cellEditor='agCheckboxCellEditor', cellRenderer='agCheckboxCellRenderer')
    grid_options = gb.build()

    grid_response = AgGrid(
        df_ag,
        gridOptions=grid_options,
        # update_mode=GridUpdateMode.VALUE_CHANGED, # 👈 DEPRECATED
        update_on=["cellValueChanged"],  # ✅ NEW PARAM
        allow_unsafe_jscode=True,
        key=f"aggrid_{current_page}",
        height=min(48 + 35 * len(df_ag), 800),  # Auto-fit height
        fit_columns_on_grid_load=True,
        reload_data=False,
    )

    updated_df = grid_response.get("data")
    can_go_next = False
    if updated_df is not None:
        # selected_vals = set(updated_df[updated_df["Value Selected"] == True]["Core Value"].tolist())
        # st.session_state.page_selections[current_page] = selected_vals
        selected_list = list(st.session_state.page_selections.get(current_page, []))
        current_selected = updated_df[updated_df["Value Selected"] == True]["Core Value"].tolist()

        # Keep order of selection, remove unselected
        selected_vals = [val for val in selected_list if val in current_selected]

        # Add newly selected items at the end
        for val in current_selected:
            if val not in selected_vals:
                selected_vals.append(val)

        st.session_state.page_selections[current_page] = selected_vals

        max_allowed = max_selections.get(current_page)
        if max_allowed is not None and len(selected_vals) > max_allowed:
            st.warning(f"You can select a maximum of {max_allowed} values on this page. Please deselect {len(selected_vals) - max_allowed} value(s) to continue.")
            can_go_next = False
        else:
            can_go_next = len(selected_vals) > 0

        st.markdown(f"### 📋 Values Selected: {len(selected_vals)}")
    else:
        st.markdown(f"### 📋 Values Selected: 0")
        can_go_next = False

elif current_page == 5:
    final_values = st.session_state.page_selections.get(4, [])
    st.markdown(f"### 📋 Values Selected: {len(final_values)}")
    if not final_values:
        st.warning("No values selected from the previous page.")
    else:
        # Ensure the required columns are available
        required_columns = {
            "Core Values": col_core,
            "Categories": col_cat,
            "Definition of the Value": col_def
        }

        # Filter out any missing columns
        selected_cols = {label: col for label, col in required_columns.items() if col is not None}

        # Build and rename DataFrame
        # result_df = df[df[col_core].isin(final_values)][list(selected_cols.values())].reset_index(drop=True)
        # Create a filtered DataFrame
        filtered_df = df[df[col_core].isin(final_values)][list(selected_cols.values())]

        # Preserve user selection order
        result_df = pd.DataFrame(columns=filtered_df.columns)
        for val in final_values:
            row = filtered_df[filtered_df[col_core] == val]
            result_df = pd.concat([result_df, row], ignore_index=True)

        result_df.columns = list(selected_cols.keys())

        st.markdown("### Final Selected Core Values with Details")
        st.dataframe(result_df, width= "stretch", hide_index=True)

        # Add user info as first row (repeated for each value)
        user_info = st.session_state.user_info
        result_df.insert(0, "First Name", user_info["first_name"])
        result_df.insert(1, "Last Name", user_info["last_name"])
        result_df.insert(2, "Email", user_info["email"])

        st.download_button(
            label="📥 Download Final Values (CSV)",
            data=result_df.to_csv(index=False).encode("utf-8"),
            file_name="final_values.csv",
            mime="text/csv"
        )


# ---------- Navigation ----------
col1, col2, col3 = st.columns([1, 6, 1])

with col1:
    if st.button("🔄 Start Over"):
        start_over()  # start_over() already calls st.rerun()

with col2:
    if st.session_state.page > 1:
        if st.button("⬅ Back"):
            st.session_state.page = max(1, st.session_state.page - 1)
            st.rerun()

with col3:
    if st.session_state.page < 5:
        can_proceed = can_go_next and (required_fields_filled if st.session_state.page == 1 else True)
        if st.button("Next ➡", disabled=not can_proceed):
            st.session_state.page += 1
            st.rerun()



