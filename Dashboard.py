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

    # Analysis Selection
    st.header("Analysis Selection")
    selected_analysis = []
    if st.checkbox("Univariate Analysis"):
        selected_analysis.append("Univariate")
    if st.checkbox("Bivariate Analysis"):
        selected_analysis.append("Bivariate")

    # Perform Selected Analysis
    if "Univariate" in selected_analysis:
        st.header("Univariate Analysis")
        for column in df.select_dtypes(include=['int64', 'float64']).columns:
            fig = px.histogram(df, x=column, title=f'{column} Distribution')
            st.plotly_chart(fig)

    if "Bivariate" in selected_analysis:
        st.header("Bivariate Analysis")
        for numeric_column in df.select_dtypes(include=['int64', 'float64']).columns:
            for categorical_column in df.select_dtypes(include=['object']).columns:
                if numeric_column != 'Arrears Status' and categorical_column != 'Arrears Status':
                    fig = px.box(df, x=categorical_column, y=numeric_column, color='Arrears Status',
                                 title=f'{numeric_column} vs {categorical_column}')
                    st.plotly_chart(fig)


    
