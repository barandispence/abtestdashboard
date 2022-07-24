import streamlit as st
from statsmodels.stats.power import zt_ind_solve_power
from statsmodels.stats.proportion import proportions_ztest, proportion_confint

def abtesting():
    alpha = 1-int(significance.strip('%'))/100
    sample_size = zt_ind_solve_power(
        effect_size=target_uplift/100, 
        nobs1=None, 
        alpha=alpha,
        power=0.8)
    converterted_list = [converted_a, converted_b]
    total_list = [total_a, total_b]
    z_stat, p_val = proportions_ztest(
        count=converterted_list,
        nobs=total_list
    )
    status = 'success' if (converted_b/total_b > converted_a/total_a) and (p_val < alpha) else 'fail'
    (lower_con, lower_test), (upper_con, upper_test) = proportion_confint(converterted_list, nobs=total_list, alpha=alpha)
    return status, converted_a/total_a, (converted_a/total_a)*(1+(target_uplift/100)), converted_b/total_b, sample_size, p_val, z_stat, lower_con, upper_con, lower_test, upper_test

st.set_page_config(
    page_title = "A/B Test Calculator",
    layout = "wide"
    )

st.header('A/B Test Calculator')

with st.expander('Input Data', expanded=True):
    with st.form('datainput'):
        a, b = st.columns([1,1])
        a.subheader('Control Group')
        total_a = a.number_input('Total Entry', key='total-control', step=1)
        converted_a = a.number_input('Total Converted', key='converted-control', step=1)
        b.subheader('Test Group')
        total_b = b.number_input('Total Entry', key='total-test', step=1)
        converted_b = b.number_input('Total Converted', key='converted-test', step=1)
        target_uplift = st.slider('Target Uplift (%)', key='target-uplift', min_value=0, max_value=100, value=10, step=1)
        significance = st.selectbox('Significance Level:', ('95%', '99%'), key='significance-level')
        submitted = st.form_submit_button("Submit")

if submitted:
    if total_a == 0 or total_b == 0:
        st.error('Netiher of totals can be zero.')
    else:
        status, cr_a, cr_lift, cr_b, sample_size, p_val, z_stat, lower_con, upper_con, lower_test, upper_test = abtesting()
        if status == 'fail':
            st.warning('There is no statistically significant difference between control and test group.')
        else:
            st.success('There is a statistically significant difference between control and test group.')
        st.subheader('Statistics')
        st.write(f'P Value: {p_val}')
        st.subheader('Confidence Interval')
        st.write(f'Lower Bound: {lower_con}')
        st.write(f'Mean: {cr_a}')
        st.write(f'Upper Bound: {upper_con}')
        st.write(f'Actual Conversion Rate: {cr_b}')
        
        





