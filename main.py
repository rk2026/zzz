import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

def main():
    '''# Download the template'''
    st.title("ट्री भोलुम क्यालकुलेटर (TVC 1.0)")
    
    '''# Download template file.'''
    tdata = {
        'TID': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
        'species': ['Row Labels', 'Abies spp', 'Acacia catechu', 'Adino cordifolia', 'Albizia spp', 
                    'Alnus nepalensis', 'Anogeissus latifolia', 'Bambax ceiba', 'Cedrela toona', 
                    'Dalbergia sissoo', 'Eugenia Jambolana', 'Hill spp', 'Hymenodictyon excelsum', 
                    'Lagerstroenia parviflora', 'Michelia champaca', 'Pinus roxburghii', 
                    'Pinus wallichiana', 'Quercus spp', 'Schima wallichii', 'Shorea robusta', 
                    'Terai spp', 'Terminalia alata', 'Trewia nudiflora', 'Tsuga spp'],
        'LONGITUDE': [85.3541391, 85.3561959, 85.3522515, 85.3534736, 85.3538313, 85.3531329, 85.3510125, 
                      85.3530499, 85.3564367, 85.3538324, 85.3501465, 85.3566107, 85.3576259, 85.3519618, 
                      85.3512281, 85.3522836, 85.3565306, 85.3551952, 85.3549863, 85.3524398, 85.3502417, 
                      85.3531312, 85.3524961, 85.3531877],
        'LATITUDE': [27.7103062, 27.7086747, 27.7108716, 27.7090673, 27.7091368, 27.7054253, 27.7086372, 
                     27.7076975, 27.7084029, 27.7090919, 27.707315, 27.7065477, 27.7079578, 27.707834, 
                     27.7077806, 27.7115758, 27.7090448, 27.706558, 27.7058551, 27.7055133, 27.7078784, 
                     27.7052758, 27.7059877, 27.7086342],
        'dia_cm': [60, 60, 60, 60, 104, 97, 95, 54, 67, 42, 61, 108, 80, 66, 56, 30, 37, 103, 109, 65, 92, 52, 64, 70],
        'height_m': [25, 25, 25, 25, 21, 27, 30, 28, 23, 21, 15, 16, 15, 26, 28, 26, 24, 18, 26, 15, 16, 29, 30, 22],
        'class': [2, 2, 2, 2, 2, 1, 1, 3, 4, 1, 2, 2, 4, 1, 1, 3, 1, 1, 3, 3, 1, 2, 3, 4]
    }

    # Convert to DataFrame
    tdf = pd.DataFrame(tdata)

    # Display the DataFrame in Streamlit
    st.write("यो टेम्पेलट डाटा डाउनलोड गरी यही अनुसार हुनेगरी डाटा तयार गर्नुहोस, कृपया यस टेवलको कोलम हेडिङ्को नाम परिवर्तन नगर्नुहोस।(Download this template to fill the data. Do not alter the column heading name)")
    st.dataframe(tdf)

    # Download button
    @st.cache_data
    def convert_df_to_csv(tdf):
        return tdf.to_csv(index=False).encode('utf-8')

    csv_data = convert_df_to_csv(tdf)
    st.download_button(
        label="Download Data as template CSV",
        data=csv_data,
        file_name='tree_data_template.csv',
        mime='text/csv'
    )
    
    # File uploader
    uploaded_file = st.file_uploader("निर्दिष्ठ प्रकारको रूखको तथ्याँङ्क तालीका .csv फर्म्याटको अपलोड गर्नुहोस।", type="csv")

    if uploaded_file is not None:
        # Read the CSV file
        df = pd.read_csv(uploaded_file)
        
        # Create the data dictionary
        data = {
            'SN': range(1, 26),
            'scientific_name': ['Abies spp', 'Acacia catechu', 'Adino cordifolia', 'Albizia spp', 'Alnus nepalensis',
                                'Anogeissus latifolia', 'Bambax ceiba', 'Cedrela toona', 'Dalbergia sissoo',
                                'Eugenia Jambolana', 'Hymenodictyon excelsum', 'Lagerstroenia parviflora',
                                'Michelia champaca', 'Pinus roxburghii', 'Pinus wallichiana', 'Quercus spp',
                                'Schima wallichii', 'Shorea robusta', 'Terminalia alata', 'Trewia nudiflora',
                                'Tsuga spp', 'Terai spp', 'Hill spp', 'Coniferious', 'Broadleaved'],
            'a': [-2.4453, -2.3256, -2.5626, -2.4284, -2.7761, -2.272, -2.3856, -2.1832, -2.1959, -2.5693,
                  -2.585, -2.3411, -2.0152, -2.977, -2.8195, -2.36, -2.7385, -2.4554, -2.4616, -2.4585,
                  -2.5293, -2.3993, -2.3204, np.nan, np.nan],
            'b': [1.722, 1.6476, 1.8598, 1.7609, 1.9006, 1.7499, 1.7414, 1.8679, 1.6567, 1.8816,
                  1.9437, 1.7246, 1.8555, 1.9235, 1.725, 1.968, 1.8155, 1.9026, 1.8497, 1.8043,
                  1.7815, 1.7836, 1.8507, np.nan, np.nan],
            'c': [1.0757, 1.0552, 0.8783, 0.9662, 0.9428, 0.9174, 1.0063, 0.7569, 0.9899, 0.8498,
                  0.7902, 0.9702, 0.763, 1.0019, 1.1623, 0.7496, 1.0072, 0.8352, 0.88, 0.922,
                  1.0369, 0.9546, 0.8223, np.nan, np.nan],
            'a1': [5.4433, 5.4401, 5.4681, 4.4031, 6.019, 4.9502, 4.5554, 4.9705, 4.358, 5.1749,
                   5.5572, 5.3349, 3.3499, 6.2696, 5.7216, 4.8511, 7.4617, 5.2026, 4.5968, 5.3475,
                   5.2774, 4.8991, 5.5323, np.nan, np.nan],
            'b1': [-2.6902, -2.491, -2.491, -2.2094, -2.7271, -2.3353, -2.3009, -2.3436, -2.1559, -2.3636,
                   -2.496, -2.4428, -2.0161, -2.8252, -2.6788, -2.4494, -3.0676, -2.4788, -2.2305, -2.4774,
                   -2.6483, -2.3406, -2.4815, np.nan, np.nan],
            's': [0.436, 0.443, 0.443, 0.443, 0.803, 0.443, 0.443, 0.443, 0.684, 0.443,
                  0.443, 0.443, 0.443, 0.189, 0.683, 0.747, 0.52, 0.055, 0.443, 0.443,
                  0.443, 0.443, 0.443, 0.436, 0.443],
            'm': [0.372, 0.511, 0.511, 0.511, 1.226, 0.511, 0.511, 0.511, 0.684, 0.511,
                  0.511, 0.511, 0.511, 0.256, 0.488, 0.96, 0.186, 0.341, 0.511, 0.511,
                  0.511, 0.511, 0.511, 0.372, 0.511],
            'bg': [0.355, 0.71, 0.71, 0.71, 1.51, 0.71, 0.71, 0.71, 0.684, 0.71,
                   0.71, 0.71, 0.71, 0.3, 0.41, 1.06, 0.168, 0.357, 0.71, 0.71,
                   0.71, 0.71, 0.71, 0.355, 0.71],
            'Local_Name': ['Thingre Salla', 'Khayar', 'Karma', 'Siris', 'Uttis', 'Banjhi', 'Simal', 'Tooni',
                           'Sissoo', 'Jamun', 'Bhudkul', 'Botdhayero', 'Chanp', 'Khote Salla', 'Gobre Salla',
                           'Kharsu', 'Chilaune', 'Sal', 'Saj', 'Gamhari', 'Dhupi Salla', 'Terai Spp',
                           'Hill spp', '', '']
        }

        
# Assuming df is your DataFrame and it has 'LATITUDE' and 'LONGITUDE' columns
        if 'LATITUDE' in df.columns and 'LONGITUDE' in df.columns:
            st.subheader("स्थानहरू नक्सामा हेर्नुहोस्:")
        
            # Define the point size
            point_size = 5  # You can change this value to adjust the size of the points
        
            # Start point customization
            layer = pdk.Layer(
                'ScatterplotLayer',
                data=df,
                get_position='[LONGITUDE, LATITUDE]',
                get_color='[100, 30, 0, 230]',
                get_radius=point_size,  # Use the point_size variable here
                pickable=True
            )
        
            # Create a deck.gl map
            view_state = pdk.ViewState(
                latitude=df['LATITUDE'].mean(),
                longitude=df['LONGITUDE'].mean(),
                zoom=10
            )
        
            # Render the map
            r = pdk.Deck(layers=[layer], initial_view_state=view_state)
            st.pydeck_chart(r)
        '''if 'LATITUDE' in df.columns and 'LONGITUDE' in df.columns:
            st.subheader("स्थानहरू नक्सामा हेर्नुहोस्:")
            
        # Start point customization
        layer = pdk.Layer(
            'ScatterplotLayer',
            data=df,
            get_position='[LONGITUDE, LATITUDE]',
            get_color='[100, 30, 0, 230]',
            get_radius=1,
            pickable=True
        )
        st.map(df[['LATITUDE', 'LONGITUDE']])  # Display map with points'''
        sppVal = pd.DataFrame(data)
        joined_df = df.merge(sppVal, left_on='species', right_on='scientific_name')

        def add_calculated_columns(df):
            df['stem_volume'] = np.exp(df['a'] + df['b'] * np.log(df['dia_cm']) + df['c'] * np.log(df['height_m'])) / 1000
            df['branch_ratio'] = df['dia_cm'].apply(lambda x: 0.1 if x < 10 else 0.2)
            df['branch_volume'] = df['stem_volume'] * df['branch_ratio']
            df['tree_volume'] = df['stem_volume'] + df['branch_volume']
            df['cm10diaratio'] = np.exp(df['a1'] + df['b1'] * np.log(df['dia_cm']))
            df['cm10topvolume'] = df['stem_volume'] * df['cm10diaratio']
            df['gross_volume'] = df['stem_volume'] - df['cm10topvolume']
            df['net_volume'] = df.apply(lambda row: row['gross_volume'] * 0.9 if row['class'] == 'A' else row['gross_volume'] * 0.8, axis=1)
            df['net_volum_cft'] = df['net_volume'] * 35.3147
            df['firewood_m3'] = df['tree_volume'] - df['net_volume']
            df['firewood_chatta'] = df['firewood_m3'] * 0.105944
            return df

        result_df = add_calculated_columns(joined_df)
        columns_to_drop = ['SN', 'scientific_name', 'a', 'b', 'c', 'a1', 'b1', 's', 'm', 'bg']
        result_df = result_df.drop(columns=columns_to_drop)

        # Display the updated dataframe
        st.write("तलको विश्लेषण तालीका excel csv को रूपमा डाउनलोड गर्नुहोस:")
        st.dataframe(result_df)

if __name__ == "__main__":
    main()
