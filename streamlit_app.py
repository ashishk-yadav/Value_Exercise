

import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from PIL import Image

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
if "page_selections" not in st.session_state:
    # Store sets of selected core values per page
    st.session_state.page_selections = {i: set() for i in range(1, 6)}

def get_values_for_page(page):
    if page == 1:
        return core_values
    # Show selected values from previous page
    return list(st.session_state.page_selections.get(page - 1, set()))

def start_over():
    st.session_state.page = 1
    st.session_state.page_selections = {i: set() for i in range(1, 6)}
    # st.experimental_rerun()

def go_back():
    st.session_state.page -= 1
    # st.experimental_rerun()

def go_next():
    st.session_state.page += 1
    # st.experimental_rerun()

# ---------- Main UI ----------
logo = Image.open('resource/logo.png')
st.image(logo)
st.title('Values Exercise')

st.header(f"Step {st.session_state.page}")
if st.session_state.page == 1:
    st.markdown('''Below is a list of Core Values. 
                Select the values that resonate with you the most. 
                Click the Next button once you have completed this step.''')
elif st.session_state.page == 2:
    st.markdown('''Below are the values you selected. 
                Now select the values that stand out best to you. 
                If the total chosen values is less than twenty-five, you may select additional values but no more than twenty-five. 
                Click the Next button once you have completed this step.''')
elif st.session_state.page == 3:
    st.markdown('''Below are your top twenty-five values. 
                From the list below, select the values that matter the most to you. 
                There is no right or wrong answer. 
                If the total chosen values is less than ten, you may select additional values but no more than ten. 
                Click the Next button once you have completed this step.''')
elif st.session_state.page == 4:
    st.markdown('''Below are your top values. 
                These values are important to you and play a role in how you view yourself and the world. 
                From the list below, select the five values that stand out best to you. 
                There is no right or wrong selection.
                Click the Next button once you have completed this step.''')
elif st.session_state.page == 5:
    st.markdown('''Below are your top five values. 
                Each of the values listed helps make up your value system the most. 
                They are the driving force behind what matters most to you and will 
                often be the foundation for your actions, behavior, and decisions. ''')

values_to_show = get_values_for_page(st.session_state.page)
if len(values_to_show) == 0:
    st.warning("No values carried over from the previous page.")

if st.session_state.page < 5 and len(values_to_show) > 0:
    # Prepare DataFrame for AgGrid with editable checkbox column
    df_ag = pd.DataFrame({
        "Core Value": values_to_show,
        "Value Selected": [val in st.session_state.page_selections[st.session_state.page] for val in values_to_show]
    })

    gb = GridOptionsBuilder.from_dataframe(df_ag)
    gb.configure_column("Value Selected", editable=True, cellEditor='agCheckboxCellEditor', cellRenderer='agCheckboxCellRenderer')
    grid_options = gb.build()

    grid_response = AgGrid(
        df_ag,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.VALUE_CHANGED,
        allow_unsafe_jscode=True,
        key=f"aggrid_{st.session_state.page}",
        height=300,
        fit_columns_on_grid_load=True,
        reload_data=False,
    )

    updated_df = grid_response.get("data")
    if updated_df is not None:
        selected_vals = set(updated_df[updated_df["Value Selected"] == True]["Core Value"].tolist())
        st.session_state.page_selections[st.session_state.page] = selected_vals

    st.markdown(f"### 📋 Values Selected: {len(st.session_state.page_selections[st.session_state.page])}")

elif st.session_state.page == 5:
    final_values = st.session_state.page_selections.get(4, set())
    if not final_values:
        st.warning("No values selected from the previous page.")
    else:
        cols_available = [col_core]
        if col_cat:
            cols_available.append(col_cat)
        if col_def:
            cols_available.append(col_def)

        result_df = df[df[col_core].isin(final_values)][cols_available].reset_index(drop=True)
        st.markdown("### Final Selected Core Values with Details")
        st.dataframe(result_df, use_container_width=True)
        st.download_button(
            label="📥 Download Final Values (CSV)",
            data=result_df.to_csv(index=False).encode("utf-8"),
            file_name="final_values.csv",
            mime="text/csv"
        )
    st.markdown(f"### 📋 Values Selected: {len(final_values)}")

# ---------- Navigation ----------
col1, col2, col3 = st.columns([1, 6, 1])

with col1:
    if st.button("🔄 Start Over"):
        start_over()
with col2:
    if st.session_state.page > 1:
        if st.button("⬅ Back"):
            go_back()
with col3:
    can_go_next = len(st.session_state.page_selections.get(st.session_state.page, [])) > 0
    if st.session_state.page < 5:
        st.button("Next ➡", disabled=not can_go_next, on_click=go_next)
