
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats

def calculate_arrears_rate(df):
    arrears_rate = len(df[df['Arrears Status'] == 'Active']) / len(df) * 100
    return f"{arrears_rate:.2f}%"

def app(df, st):
    # Helper Functions
    def plot_pies(st=""):
        bus = df.groupby([st, 'Arrears Status'], as_index=False)['Tenant Age'].count()
        bus.rename(columns={'Tenant Age': 'Count'}, inplace=True)
        fig = go.Figure()
        fig = make_subplots(rows=1, cols=4,
                            specs=[[{"type": "pie"}, {"type": "pie"}, {"type": "pie"}, {"type": "pie"}]],
                            subplot_titles=('Very High', 'High', 'Medium', 'Low'))

        for i, status in enumerate(['Very High', 'High', 'Medium', 'Low']):
            pie_data = bus[bus[st] == status]
            fig.add_trace(
                go.Pie(values=pie_data['Count'], labels=pie_data['Arrears Status'],
                       pull=[0, 0.1], showlegend=False),
                row=1, col=i + 1
            )

        fig.update_layout(template='plotly', showlegend=True,
                          legend_title_text="Arrears Status", title_text=f"Tenant Arrears Status based on {st}",
                          font_family="Times New Roman", title_font_family="Times New Roman")
        return fig

    # Metrics
    st.title("Tenant Analytics")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric(":red[Total Tenants]", len(df))
    col2.metric(":red[Male Tenants]", len(df[df['Gender'] == 'Male']))
    col3.metric(":red[Female Tenants]", len(df[df['Gender'] == 'Female']))
    col4.metric(":red[Arrears Rate]", calculate_arrears_rate(df))

    # Sample of data
    btn = st.button("Show Sample")
    if btn:
        st.dataframe(df.iloc[:, :-2].sample(5))

    # Bar Plots
    st.header("Counts and Percentages")
    c1, c2 = st.columns(2)
    selected = c1.selectbox('Select', ['Employment Status', 'Income Level', 'Socio-economic Background',
                                       'Highest Education', 'Location', 'Property Type', 'Property Size',
                                       'Num Amenities', 'Rental Price', 'Property Age', 'Property Condition',
                                       'Tenancy by Entirety', 'Benefit Cap', 'Satisfaction', 'Income to Debt Ratio',
                                       'Timeliness Score', 'Credit Score', 'Household Size', 'Presence of Guarantor',
                                       'Rental Price to Income Ratio'])
    colored = c2.selectbox('Filter By', ['Arrears Status', 'Satisfaction', 'Income to Debt Ratio', 'Credit Score'])

    subData = df.groupby([selected, colored])["Tenant Age"].count().reset_index(name='Counts')
    fig = px.bar(subData, y="Counts", x=selected, color=colored, template='plotly',
                 title=f"{selected} with {colored}")
    fig.update_layout(xaxis_title=selected, yaxis_title='Counts')
    st.plotly_chart(fig, use_container_width=True)

    # Box Plots
    st.header("Distributions by different aspects")
    cc1, cc2, cc3 = st.columns(3)

    Numerical = cc1.selectbox('Select', ['Tenant Age', 'Property Size', 'Rental Price', 'Property Age'])
    Category = cc2.selectbox('Filter By', ['Arrears Status', 'JobSatisfaction', 'WorkLifeBalance'])
    By = cc3.selectbox('Select', [None, 'Arrears Status'])

    fig = px.box(df, x=Category, y=Numerical, color=By, template='plotly',
                 title=f"{Numerical} distribution by different {Category}s")
    fig.update_layout(xaxis_title=Category, yaxis_title=Numerical)
    st.plotly_chart(fig, use_container_width=True)

    # Pie Plots
    st.header("Socio-economic Background and arrears status rates")
    sel = st.selectbox('Choose', ['Socio-economic Background', 'Arrears Status'])

    fig = plot_pies(sel)
    st.plotly_chart(fig, use_container_width=True)

    # Scatter with Correlation
    st.header("Correlation Between numerical features")
    ccc1, ccc2, ccc3, ccc4 = st.columns(4)

    Numerical1 = ccc1.selectbox('Between', options=['Tenant Age', 'Rental Price', 'Property Age'])
    Numerical2 = ccc2.selectbox('And', options=['Rental Price', 'Tenant Age', 'Property Age'])
    By2 = ccc3.selectbox('Filtered By', options=[None, 'Arrears Status', 'Tenancy by Entirety'])

    Corr = round(stats.pearsonr(df[Numerical1], df[Numerical2]).statistic, 4)
    ccc4.metric("Correlation", Corr)

    fig = px.scatter(df, x=Numerical1, y=Numerical2, color=By2, trendline='ols',
                     opacity=0.5, template='plotly',
                     title=f'Correlation between {Numerical1} and {Numerical2}')
    fig.update_layout(xaxis_title=Numerical1, yaxis_title=Numerical2)
    st.plotly_chart(fig, use_container_width=True)
