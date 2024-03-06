#import libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt



#upload csv file
data=pd.read_csv("startup_cleaned.csv")
data['date']=pd.to_datetime(data['date'], errors='coerce')
data['month']=data['date'].dt.month
data['year']=data['date'].dt.year

#set page config
st.set_page_config(layout='wide')


#create a function for investor details
def load_investors_details(investor):
    #investor name
    st.title(investor)
    #biggest investments
    st.subheader('Biggest Investment ')
    col1, col2=st.columns(2)
    with col1:
        biggest_investment = data[data['investors'].str.contains(investor)].groupby('startup')[
            'amount'].sum().sort_values(ascending=False).head()
        st.dataframe(biggest_investment)
    with col2:
        fig, ax = plt.subplots()
        ax.bar(biggest_investment.index, biggest_investment.values)
        st.pyplot(fig)


    #genrally invests in
    st.subheader('Generally invests in')
    cl1, cl2, cl3=st.columns(3)
    with cl1:
        st.subheader('1. Sector')
        genral_investment1=  data[data['investors'].str.contains(investor)].groupby('verticals')['amount'].sum()
        fig1, ax1 = plt.subplots()
        ax1.pie(genral_investment1, labels=genral_investment1.index)
        st.pyplot(fig1)
    with cl2:
        st.subheader('2. Stage')
        genral_investment2= data[data['investors'].str.contains(investor)].groupby('InvestmentnType')['amount'].sum()
        fig2, ax2 = plt.subplots()
        ax2.pie(genral_investment2, labels=genral_investment2.index)
        st.pyplot(fig2)
    with cl3:
        st.subheader('3. City')
        genral_investment3= data[data['investors'].str.contains(investor)].groupby('city')['amount'].sum()
        fig3, ax3 = plt.subplots()
        ax3.pie(genral_investment3, labels=genral_investment3.index)
        st.pyplot(fig3)



    #Year on year graph -> line graph
    st.subheader('Year on Year investment')
    data['year'] = data['date'].dt.year
    column1, column2 =st.columns(2)
    with column1:
        year_series = data[data['investors'].str.contains(investor)].groupby('year')['amount'].sum()

        fig4, ax4 = plt.subplots()
        ax4.plot(year_series.index, year_series.values)

        st.pyplot(fig4)

#creat a function for overall analysis
def load_overall_analysis():
    # total funding in the Indian startups
    total=round(data['amount'].sum())

    #maximum amount invested
    max=round(data.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0])

    #average amount inveted
    avg=round(data.groupby('startup')['amount'].sum().mean())

    #Total funded startup
    total_startups=data['startup'].nunique()



    col1, col2, col3, col4= st.columns(4)
    with col1:
        st.metric('Total funding on Indian startup',str(total)+' cr')
    with col2:
        st.metric('Maximum funding',str(max)+' cr')
    with col3:
        st.metric('Average funding',str(avg)+ ' cr')
    with col4:
        st.metric('Total funded startups',str(total_startups))

    #mom funding graphs
    st.subheader('1. Month-on-Month analysis')
    selected_op=st.selectbox('select type',['total' , 'counts'])
    #for sum
    if selected_op=='total':
        temp_df = data.groupby(['month', 'year'])['amount'].sum().reset_index()
    else:
        temp_df = data.groupby(['month', 'year'])['amount'].count().reset_index()

    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
    #col1, col2 = st.columns(2)
    #with col1:
    fig6, ax6 = plt.subplots()
    ax6.plot(temp_df['x_axis'], temp_df['amount'],)
    ax6.set_xticklabels(labels=temp_df['x_axis'], rotation=90)
    st.pyplot(fig6)


    #Sector Analysis-> using Pie daigram
    st.subheader('2. Sector Analysis')
    selct_option=st.selectbox('Select the option', ['Total', 'Count'])
    if selct_option=='Total':
        top_sector = data.groupby('verticals')['amount'].sum().sort_values(ascending=False).head(10)
        st.text('The pie chart represent the Top-10 sector which have got maximum funding')

    else:
        top_sector = data.groupby('verticals')['amount'].count().sort_values(ascending=False).head(10)
        st.text('The pie chart represent the Top-10 sectors where maximum number of investors have invested')

    col1, col2=st.columns(2)
    with col1:
        fig7, ax7 = plt.subplots()
        ax7.pie(top_sector, labels=top_sector.index)
        st.pyplot(fig7)

    #types of funding
    st.subheader('3. Types of funding')
    #li = data['InvestmentnType'].unique().tolist()
    #investment_type_df = pd.DataFrame(li, columns=['Investment type']).set_index('Investment type')
    #st.dataframe(investment_type_df
    li = data['InvestmentnType'].unique().tolist()
    investment_type_df = pd.DataFrame(li, columns=['Investment type'])
    st.dataframe(investment_type_df)


    #city wise funding
    st.subheader('4. City wise Funding')
    tem_df = data.groupby('city')['InvestmentnType'].unique().reset_index()
    st.dataframe(tem_df)

    #top sector ->year wise and overall
    #top sector can the sector where lot of investors have invested
    st.subheader('5. Top startups')
    st.subheader('Year wise Top Startup')
    selected_year=st.selectbox('Select the year',data['year'].unique())
    year_df=data[data['year'] == selected_year][data[data['year'] == selected_year]['amount'] == data[data['year'] == selected_year]['amount'].max()]
    st.dataframe(year_df)

    st.subheader('Overall analysis')
    new_df=data.groupby('startup')['amount'].max().sort_values(ascending=False).head(10).reset_index()
    col1, col2=st.columns(2)
    with col1:
        st.subheader('DatFrame')
        st.dataframe(new_df)
    with col2:
        st.subheader('Bar Graph')
        fig8, ax8 = plt.subplots()
        ax8.bar(new_df['startup'], new_df['amount'])
        ax8.set_xticklabels(labels=new_df['startup'], rotation=90)
        st.pyplot(fig8)

    #Top investors
    st.subheader('6. Top investors')
    df1=data.groupby('investors')['amount'].sum().sort_values(ascending=False).head(10)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('DatFrame')
        st.dataframe(df1)
    with col2:
        st.subheader('Bar Graph')
        fig9, ax9 = plt.subplots()
        ax9.bar(df1.index, df1.values)
        ax9.set_xticklabels(labels=df1.index, rotation=90)
        st.pyplot(fig9)
def load_startup_analysis(startup):
    #1. name
    st.header(startup)

    #2. The company wokrs in the industrial sectors like
    st.subheader('1. Industrial sectors of comapny')
    industry_df=data[data['startup'].str.contains(startup)]['verticals'].unique()
    st.dataframe(industry_df)

    # 2. The company wokrs in the industrial subsectors like
    st.subheader('2. Industrial sub-sectors of comapny')
    industry_subdf = data[data['startup'].str.contains(startup)]['SubVertical'].unique()
    st.dataframe(industry_subdf)

    # 3. The company wokrs in the industrial subsectors like
    st.subheader('3. Location of comapny')
    industry_subdf = data[data['startup'].str.contains(startup)]['city'].unique()
    st.dataframe(industry_subdf)

    #4. Funding details of company
    st.subheader('4. Funding details of company')
    inv_df=data[data['startup'] == startup][['date', 'investors', 'InvestmentnType','amount']]
    inv_df.drop_duplicates(subset=['InvestmentnType'])
    st.dataframe(inv_df)







st.sidebar.title("Startup funding Analysis")
opt=st.sidebar.selectbox("Select One",['Overall Analysis', 'Startup Analysis', 'Investors Analysis'])
if opt=='Overall Analysis':
    #bt0=st.sidebar.button('Show overall analysis'
    st.title('Overall Analysis')
    load_overall_analysis()




elif opt=='Startup Analysis':
    selected_startup=st.sidebar.selectbox('Select Startup', data['startup'].unique().tolist() )
    bt1=st.sidebar.button('Find Startup details')
    if bt1:
        load_startup_analysis(selected_startup)

else:
    selected_investor=st.sidebar.selectbox(' Select Investor',sorted(set(data['investors'].str.split(',').sum())))
    bt2=st.sidebar.button('Find Investors details')
    if bt2:
        load_investors_details(selected_investor)


