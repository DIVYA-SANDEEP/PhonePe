import streamlit as st
import pandas as pd
import mysql.connector 
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image

icon = Image.open("Phonepe.png")
st.set_page_config(page_title= "Phonepe Pulse Data",
                   page_icon= icon,
                   layout="wide")


mydb = mysql.connector.connect(                            
host="localhost",
user="root",
password="",
database="phonepe",
port="3306"
)
cursor=mydb.cursor(buffered=True)

st.title(":violet[PHONEPE DATA VISUALIZATION]")
selected = option_menu(None, ["Home","Dashboards","Gathered Data","About"], 
                       default_index=0,
                       orientation="horizontal",
                       styles={"nav-link": {"font-size": "20px", "text-align": "centre", "margin": "-2px", "--hover-color": "#7F00FF"},
                               "icon": {"font-size": "35px"},
                               "container" : {"max-width": "6000px"},
                               "nav-link-selected": {"background-color": "#7F00FF"}})


if selected == "Dashboards":
    chart_type = st.sidebar.selectbox("**Chart Type**", ("Transactions", "Users"))

    
    sidebar = st.sidebar
    
    Year = sidebar.slider("**Year**", min_value=2018, max_value=2023)
    Quarter = sidebar.slider("**Quarter**", min_value=1, max_value=4)
  
if selected == "Dashboards":
     if chart_type == "Transactions":
          st.markdown("### :violet[State]")
          if Year==2023 and Quarter in [4]:
                st.warning('''**-Data is not available for STATES in 2023 Qtr 4**''')
          else:    
               cursor.execute(f"SELECT state, SUM(Transaction_count) AS Total_Transactions_Count, SUM(Transaction_amount) AS Total_Amount "
                    f"FROM agg_transaction WHERE year = {Year} AND quarter = {Quarter} "
                    f"GROUP BY state ORDER BY Total_Amount DESC LIMIT 10")
               df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Transactions_Count', 'Total_Amount'])
               fig = px.bar(df,
                    title='*Top 10* States by Transaction Amount with Transactions_Count',
                    x="State",
                    y="Total_Amount",
                    text='Transactions_Count', 
                    orientation='v',
                    color='Total_Amount',
                    color_continuous_scale=px.colors.sequential.Plasma)
               fig.update_traces(texttemplate='%{text:.2s}', textposition='inside')
               st.plotly_chart(fig, use_container_width=True)   

          st.markdown("### :violet[District]")
          if Year==2023 and Quarter in [4]:
                st.warning('''**-Data is not available for DISTRICTS in 2023 Qtr 4**''')
          else:
               cursor.execute(f"SELECT district, SUM(Count) AS Total_Count,SUM(Amount) AS Total_Amount "
                         f"FROM map_trans WHERE year = {Year} AND quarter = {Quarter} "
                         f"GROUP BY district ORDER BY Total_Amount DESC LIMIT 10")
               df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Transactions_Count','Total_Amount'])
               fig = px.bar(df,
                    title='*Top 10* Districts by Transaction Amount with Transactions_Count',
                    x="District",
                    y="Total_Amount",
                    text='Transactions_Count', 
                    orientation='v',
                    color='Total_Amount',
                    color_continuous_scale=px.colors.sequential.Plotly3_r)
               fig.update_traces(texttemplate='%{text:.2s}', textposition='inside')
               st.plotly_chart(fig, use_container_width=True)   

          st.markdown("### :violet[Pincode]")
          if Year==2023 and Quarter in [4]:
                st.warning('''**-Data is not available for PINCODES in 2023 Qtr 4**''')
          else: 
               cursor.execute(f"SELECT pincode, SUM(Transaction_count) AS Total_Transactions_Count,SUM(Transaction_amount) AS Total_Amount "
                              f"FROM top_trans WHERE year = {Year} AND quarter = {Quarter} "
                              f"GROUP BY pincode ORDER BY Total_Amount DESC LIMIT 10")
               df = pd.DataFrame(cursor.fetchall(), columns=['Pincode', 'Transactions_Count','Total_Amount'])
               fig = px.pie(df, values='Total_Amount',
                                        names='Pincode',
                                        title='*Top 10* Pincodes by Transaction Amount with Transactions_Count',
                                        color_discrete_sequence=px.colors.sequential.Sunsetdark_r,
                                        hover_data=['Transactions_Count'],
                                        labels={'Transactions_Count':'Transactions_Count'})

               fig.update_traces(textposition='inside', textinfo='percent+label')
               st.plotly_chart(fig,use_container_width=True)
     
     if chart_type == "Users":
          st.markdown("### :violet[States]")
          if Year==2023 and Quarter in [4]:
               st.warning('''**-Data is not available for STATE in 2023 Qtr 4**''')
          
          else:
               cursor.execute(f"SELECT state, SUM(Registered_user) AS Total_Users,SUM(App_opens) AS Total_Appopens "
                              f"FROM map_user WHERE year = {Year} AND quarter = {Quarter} "
                              f"AND quarter = {Quarter} GROUP BY State ORDER BY Total_Users DESC LIMIT 10")
               df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Users','Total_AppOpens'])
          
               fig = px.pie(df, values='Total_Users',
                              names='State',
                              title='*Top 10* States by Total Users',
                              color_discrete_sequence=px.colors.sequential.Plotly3,
                              hover_data=['Total_AppOpens'],
                              labels={'Total_Appopens':'Total_Appopens'})
               fig.update_traces(textposition='inside', textinfo='percent+label')         
               st.plotly_chart(fig,use_container_width=True)
                 
          st.markdown("### :violet[Districts]")
          if Year==2023 and Quarter in [4]:
               st.warning('''**-Data is not available for DISTRICTS in 2023 Qtr 4**''')
          
          else:
               cursor.execute(f"SELECT district, SUM(Registered_user) AS Total_Users,SUM(app_opens) AS Total_AppOpens "
                              f"FROM map_user WHERE year = {Year} AND quarter = {Quarter} "
                              f"GROUP BY district ORDER BY Total_Users DESC LIMIT 10")
               df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Total_Users','Total_AppOpens'])
               df.Total_Users = df.Total_Users.astype(float)
               
               fig = px.bar(df,
                         title='*Top 10* Districts by Total Users',
                         x="Total_Users",
                         y="District",
                         text='Total_AppOpens',
                         orientation='h',
                         color='Total_Users',
                         color_continuous_scale=px.colors.sequential.Inferno)
               fig.update_traces(texttemplate='%{text:.2s}', textposition='inside')
               st.plotly_chart(fig, use_container_width=True)

          st.markdown("### :violet[Pincodes]")                
          if Year==2023 and Quarter in [4]:
               st.warning('''**-Data is not available for PINCODES in 2023 Qtr 4**''')
          else:
               cursor.execute(f"SELECT Pincode, SUM(RegisteredUsers) AS Total_Users "
                                   f"FROM top_user WHERE year = {Year} AND quarter = {Quarter} "
                                   f"GROUP BY Pincode ORDER BY Total_Users DESC LIMIT 10")
               df = pd.DataFrame(cursor.fetchall(), columns=['Pincode', 'Total_Users'])
               
               fig = px.pie(df,
                         values='Total_Users',
                         names='Pincode',
                         title='*Top 10* Pincodes by Total Users',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Total_Users'])
               fig.update_traces(textposition='inside', textinfo='percent+label')
               
               st.plotly_chart(fig,use_container_width=True)
               
          st.markdown("### :violet[Brands]")
          if Year == 2022 and Quarter in [2,3,4]:
               st.warning('''**-Data is not available for BRANDS in 2022 Qtr 2,3,4**''')
          elif Year == 2023 and Quarter in [1,2,3,4]:
               st.warning('''**-Data is not available for BRANDS in 2023 Qtr 1,2,3,4**''')
               
          else:
               cursor.execute(f"SELECT brands, SUM(count) AS Total_Count, AVG(percentage)*100 AS Avg_Percentage "
                              f"FROM agg_user WHERE year = {Year} AND quarter = {Quarter} GROUP BY brands "
                              f"ORDER BY Total_Count DESC LIMIT 10")                
               df = pd.DataFrame(cursor.fetchall(), columns=['Brand', 'Total_Users','Avg_Percentage'])
               
               fig = px.bar(df,
                    title='*Top 10* Brands by Total Users',
                    x="Total_Users",
                    y="Brand",
                    orientation='h',
                    color='Avg_Percentage',
                    color_continuous_scale=px.colors.sequential.Sunsetdark)
               st.plotly_chart(fig,use_container_width=True)


if selected == "Gathered Data":
    Year = st.sidebar.slider("**Year**", min_value=2018, max_value=2023)
    Quarter = st.sidebar.slider("Quarter", min_value=1, max_value=4)
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    col1,col2 = st.columns(2)
    

    if Type == "Transactions":
         
        with col1:
            st.header(" :violet[**--Overall State Data-- Transactions Amount**]",divider="violet")
            if Year==2023 and Quarter in [4]:
                    st.warning('''-As of this time, the OVERALL STATE TRANSACTION AMOUNT for Q4 2023 is unavailable.''')
                    
            else:
                cursor.execute(f"SELECT State, SUM(Count) AS Total_Transactions, SUM(Amount) AS Total_Amount FROM map_trans "
                                f"WHERE year = {Year} AND quarter = {Quarter} GROUP BY state ORDER BY state")
                df1 = pd.DataFrame(cursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_Amount'])
                df2 = pd.read_csv('36States.csv')
                df1.State = df2

                fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey='properties.ST_NM',
                        locations='State',
                        color='Total_Amount',
                        hover_data=['State', 'Total_Amount'],
                        projection="orthographic",
                        color_continuous_scale='Sunset')

                fig.update_geos(fitbounds="locations", visible=False)

                st.plotly_chart(fig,use_container_width=True)

        with col2:
            st.header(" :violet[**--Overall State Data-- Transactions Count**]",divider="violet")
            
            if Year==2023 and Quarter in [4]:
                st.warning('''-As of this time, the OVERALL STATE TRANSACTION COUNT for Q4 2023 is unavailable.''')
                    
            else:
                cursor.execute(f"SELECT State, SUM(Count) AS Total_Transactions, SUM(Amount) AS Total_Amount FROM map_trans "
                                f"WHERE year = {Year} AND quarter = {Quarter} GROUP BY state ORDER BY state")
                df1 = pd.DataFrame(cursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_Amount'])
                df2 = pd.read_csv('36States.csv')
                df1.Total_Transactions = df1.Total_Transactions.astype(float)
                df1.State = df2

                fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey='properties.ST_NM',
                        locations='State',
                        color='Total_Transactions',
                        hover_data=['State', 'Total_Transactions'],
                        projection="orthographic",
                        color_continuous_scale='Plasma')

                fig.update_geos(fitbounds="locations", visible=False)
                st.plotly_chart(fig,use_container_width=True)

        st.header(":violet[Top Payment Type]",divider="violet")
        
        if Year==2023 and Quarter in [4]:
            st.warning('''-As of this time, the TOP PAYMENT for Q4 2023 is unavailable.''')
                    
        else:
            cursor.execute(f"SELECT Transaction_type, SUM(Transaction_count) as Total_Transactions, SUM(Transaction_amount) as Total_amount " 
                           f"FROM agg_transaction WHERE year= {Year} AND quarter = {Quarter} GROUP BY transaction_type ORDER BY Transaction_type")
            df = pd.DataFrame(cursor.fetchall(), columns=['Transaction_type', 'Total_Transactions','Total_amount'])

            fig = px.bar(df,
                        title='Transaction_Types (vs) Total_Transactions',
                        x="Transaction_type",
                        y="Total_Transactions",
                        orientation='v',
                        color='Total_amount',
                        color_continuous_scale=px.colors.sequential.Plotly3)
            
            st.plotly_chart(fig,use_container_width=False)           
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("## :violet[Select any State to explore more]")
        selected_state = st.selectbox("",
                             ('Andaman-&-nicobar-islands','Andhra-pradesh','Arunachal-pradesh','Assam','Bihar',
                              'Chandigarh','Chhattisgarh','Dadra-&-Nagar-Haveli-&-Daman-&-Diu','Delhi','Goa','Gujarat','Haryana',
                              'Himachal-pradesh','Jammu-&-kashmir','Jharkhand','Karnataka','Kerala','Ladakh','Lakshadweep',
                              'Madhya-pradesh','Maharashtra','Manipur','Meghalaya','Mizoram',
                              'Nagaland','Odisha','Puducherry','Punjab','Rajasthan','Sikkim',
                              'Tamil-nadu','Telangana','Tripura','Uttar-pradesh','Uttarakhand','West-bengal'),index=30)
        
        if Year==2023 and Quarter in [4]:
            st.warning('''-Unfortunately, we don't have data for Exploring Total Transaction  across all states in the fourth quarter of 2023.''')            
       
        else:
            cursor.execute(f"select State, District,year,quarter, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} and State = '{selected_state}' group by State, District,year,quarter order by state,district")
            
            df1 = pd.DataFrame(cursor.fetchall(), columns=['State','District','Year','Quarter',
                                                            'Total_Transactions','Total_amount'])
            fig = px.bar(df1,
                        title=selected_state,
                        x="District",
                        y="Total_Transactions",
                        orientation='v',
                        color='Total_amount',
                        color_continuous_scale=px.colors.sequential.Plasma)
            st.plotly_chart(fig,use_container_width=True)
        
     
    if Type == "Users":
        st.markdown("## :violet[Overall State Data - User App opening frequency]")
        if Year==2023 and Quarter in [4]:
            st.warning('''-As of this time, the OVERALL STATE APP OPENS for Q4 2023 is unavailable.''')
                    
        else:
            cursor.execute(f"SELECT state, SUM(Registered_user) AS Total_Users, SUM(App_opens) AS Total_Appopens "
                            f"FROM map_user WHERE year = {Year} AND quarter = {Quarter} GROUP BY state ORDER BY state")
            df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
            df2 = pd.read_csv('36States.csv')
            df1.Total_Appopens = df1.Total_Appopens.astype(float)
            df1.State = df2
            
            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State',
                    color='Total_Appopens',
                    hover_data=['State', 'Total_Appopens'],
                    projection="orthographic",
                    color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)
        
       
        st.markdown("## :violet[Select any State to explore more]")
        
        selected_state = st.selectbox("",
                             ('Andaman-&-Nicobar-islands','Andhra-pradesh','Arunachal-pradesh','Assam','Bihar',
                              'Chandigarh','Chhattisgarh','Dadra-&-Nagar-Haveli-&-Daman-&-Diu','Delhi','Goa','Gujarat','Haryana',
                              'Himachal-pradesh','Jammu-&-kashmir','Jharkhand','Karnataka','Kerala','Ladakh','lakshadweep',
                              'Madhya-pradesh','Maharashtra','Manipur','Meghalaya','Mizoram',
                              'Nagaland','Odisha','Puducherry','Punjab','Rajasthan','Sikkim',
                              'Tamil-nadu','Telangana','Tripura','Uttar-pradesh','Uttarakhand','West-bengal'),index=0)
        
        if Year==2023 and Quarter in [4]:
            st.warning('''-Unfortunately, we don't have data for Exploring Total Users across all states in the fourth quarter of 2023.''')            
       
        else:
            cursor.execute(f"SELECT State, year, quarter, District, SUM(Registered_user) AS Total_Users, "
                       f"SUM(App_opens) AS Total_Appopens FROM map_user WHERE year = {Year} AND quarter = {Quarter} "
                       f"AND state = '{selected_state}' GROUP BY State, District, year, quarter ORDER BY state, district")
            
            df = pd.DataFrame(cursor.fetchall(), columns=['State','year', 'quarter', 'District', 'Total_Users','Total_Appopens'])
            df.Total_Users = df.Total_Users.astype(int)
            
            fig = px.bar(df,
                        title=selected_state,
                        x="District",
                        y="Total_Users",
                        orientation='v',
                        color='Total_Users',
                        color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)

if selected == "Home":      
     st.write(" ")
     st.header(f":violet[*Domain* :] Fintech",divider="violet")
     st.write(f"### Welcome to the PhonePe Pulse Data Visualization and Exploration tool—a user-friendly application designed to empower you with insights into your PhonePe transaction data. This tool combines the simplicity of Streamlit and the robust visualization capabilities of Plotly, offering an intuitive experience for exploring key metrics over time.")
     st.subheader(''':violet[*Technologies used* :] ''')
     st.write(f"#### 🔹Github Cloning")
     st.write(f"#### 🔹Python")
     st.write(f"#### 🔹Pandas")
     st.write(f"#### 🔹MySQL")
     st.write(f"#### 🔹Streamlit")
     st.write(f"#### 🔹Plotly")
     st.subheader(''':violet[*Overview* :]''')
     st.write(f"#### PhonePe Pulse is a treasure trove of information about transaction patterns, and our tool transforms this data into interactive visualizations. Whether you're a business owner, analyst, or enthusiast, this tool provides a convenient way to delve into transaction trends and make informed decisions.")

     st.write(f"### :violet[Phonepe Application Download link:]")
     st.write("https://www.phonepe.com/app-download/")


if selected == "About":
    col1, col2 = st.columns([2, 2], gap="medium")

    # Column 1: PhonePe Pulse Content
    with col1:
        st.markdown("### :violet[About PhonePe Pulse:]")
        st.write("Welcome to PhonePe Pulse, India's pioneering platform for exploring and understanding digital payment trends. With a rich dataset of over 2000+ Crore transactions presented on an interactive map of India, PhonePe Pulse provides a unique perspective on the nation's digital payment landscape.")

        st.markdown("### :violet[Key Features of PhonePe Pulse:]")
        st.write("- Interactive map with real-time transaction insights")
        st.write("- Over 45% market share represented in the data")
        st.write("- More than 300 million registered users")

        st.markdown("### :violet[Additional Insights:]")
        st.write("Embark on a journey to discover fascinating trends and patterns in digital payments through PhonePe Pulse. Navigate through the website to access detailed reports, engaging visualizations, and data-driven stories that unravel the intricacies of India's digital economy.")
        
        st.markdown("### :violet[PhonePe's Impact:]")
        st.write("PhonePe has made a significant impact on the fintech landscape:")
        st.write("- Launched financial services in 2017 with Gold, Mutual Funds, and Insurance products")
        st.write("- Introduced the Switch platform in 2018, providing access to over 600 apps")
        st.write("- Accepted at 20+ million merchant outlets across Bharat")

    
    with col2:
        st.markdown("### :violet[About PhonePe:]")
        st.write("PhonePe is India's leading fintech platform, revolutionizing the digital payment ecosystem with over 300 million registered users. Offering a diverse range of services, including secure money transfers, mobile recharges, utility payments, gold purchases, and smart investments.")
        st.markdown("### :violet[About Project:]")
        st.write(f"This PhonePe Pulse Data Visualization and Exploration tool is crafted with Streamlit and Plotly, offering a seamless blend of user-friendly design and powerful analytics. If you have questions, feedback, or suggestions, please reach out. We're here to make your data exploration journey insightful and enjoyable.")
        
        st.markdown("### :violet[My Project GitHub link]")
        st.write("https://github.com/DIVYA-SANDEEP/PhonePe")
        st.markdown("### :violet[PhonePe Pulse Website]")
        st.write("https://www.phonepe.com/pulse/")
        st.markdown("### :violet[Source: PhonePe]")
        st.write("https://www.phonepe.com/")