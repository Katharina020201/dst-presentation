# SETUP

from vega_datasets import data
import streamlit as st
import pandas as pd
import altair as alt


# colors
dark_grey = "#9698B4"
sage_green = "#A1D6C6"
dark_red = "#982D4D"
blue_highlight = "#6B68F9"

red_scale = ['#F9CEDB', '#C55979',  '#81072B']

# Title of our app
st.title("Urban Butcher Stuttgart")
st.subheader(
    "Produktstrategie für unsere Filialeröffnung - Wie können wir uns als Metzgerei nachhaltig positionieren?")

st.markdown("**Urban Butcher** ist ein junges Unternehmen, das sich auf die Herstellung von Fleischprodukten spezialisiert hat und die Neueröffnung der Filiale in Stuttgart steht kurz bevor. Um die Eröffnung zu einem Erfolg zu machen, sollten innovative Ansätze zur **Etablierung eines guten Brand Image** vorgenommen werden. Um die Kunden von heute begeistern zu können, darf der Faktor 'Nachhaltigkeit' nicht außer Acht gelassen werden. Unseren Kunden ist bewusst, dass die Fleischproduktion einen großen Einfluss auf die Umwelt hat. Daher ist es wichtig, dass sich Urban Butcher Stuttgart **als nachhaltiges Unternehmen positioniert**. ")

# # SIDEBAR
st.sidebar.image("images/Logo.svg", width=200)
st.sidebar.subheader("Wähle die Produktart um zu vergleichen")
is_animal = st.sidebar.checkbox("Tierische Produkte")
is_plant = st.sidebar.checkbox("Pflanzliche Produkte")

# st.sidebar.subheader("")
# is_ghg = st.sidebar.checkbox("Emmissionen")
# is_land = st.sidebar.checkbox("Landnutzung")
# is_water = st.sidebar.checkbox("Wasserverbrauch")

selected_impact_types = st.sidebar.multiselect(
    'Wähle den Umwelt-Impact', ['Emissions', 'Land Use', 'Water Use'])

# --------------------------------------------------------------#
# Data Import

# setup

# colors
dark_grey = "#9698B4"
sage_green = "#A1D6C6"
dark_red = "#982D4D"
blue_highlight = "#6B68F9"

red_scale = ['#F9CEDB', '#C55979',  '#81072B']

# ---------------------------------------------------- #
# Pie Chart GHG Emmisions of Food

# creating data for a simple pie chart
df_food = pd.read_csv(
    '../code/cleaned-data/environmental-impact-food.csv')

# Colors for food and non-food
df_food['Category'] = df_food['Category'].astype('category')

GHG_TYPE = df_food['Category'].cat.categories.to_list()

colors = alt.Scale(
    domain=GHG_TYPE,
    range=[blue_highlight, dark_grey]
)

# Plot Pie Chart
pie_base = alt.Chart(df_food).encode(
    alt.Theta("Percent:Q").stack(True),
    alt.Color("Category:N", scale=colors).legend(None),
    alt.Tooltip(['Category', 'Emissions'])
)

pie = pie_base.mark_arc(outerRadius=120)
pie_text = pie_base.mark_text(radius=160, size=16).encode(text="Category:N")

pie_chart = pie + pie_text

# --------------------------------------------------- #
# Meat Consumption in Germany

df_consumption = pd.read_csv(
    '../code/cleaned-data/versorgungsbilanz-fleisch.csv')

# Convert column Year to date time
df_consumption['Year'] = pd.to_datetime(
    df_consumption['Year'], format='%Y-%m-%d')


# Plotting points and 2 dotted line graphs -> one for max_consumption and one for min_consumption
# points

# function for points, fill date with either '2011-01-01' or '2021-01-01'
def create_point(date, p_color):

    point = alt.Chart(df_consumption[df_consumption['Year'] == date]).mark_circle(opacity=1, size=200).encode(
        x=alt.X('Year:T'),
        y=alt.Y('Consumption per Person:Q'),
        color=alt.value(p_color)
    )
    return point


# function for dotted lines, fill with 'MaxConsumption:Q' or 'MinConsumption:Q'
def create_dotted_line(column, l_color):

    dotted_line = alt.Chart(df_consumption).mark_rule(strokeDash=[12, 6], size=1).encode(
        y=alt.Y(column, scale=alt.Scale(domain=(40, 75))),
        color=alt.value(l_color)
    )
    return dotted_line


# label for dotted lines
# Max // adding +kg with the help of Copilot
label_base_max = alt.Chart(df_consumption).transform_calculate(
    MaxConsumption_kg="datum.MaxConsumption + ' kg'").mark_text().encode(
    x=alt.X('Year:T', aggregate='max'),
    y=alt.Y('MaxConsumption:Q',
            aggregate={'argmax': 'Year'}),
    color=alt.value(blue_highlight),
    text=alt.Text('MaxConsumption_kg:N')
)

label_max = label_base_max.mark_text(
    align='left',
    dx=-70,
    dy=18,
    size=20,
)


# Min
label_base_min = alt.Chart(df_consumption).transform_calculate(
    MinConsumption_kg="datum.MinConsumption + ' kg'").mark_text().encode(
    x=alt.X('Year:T', aggregate='max'),
    y=alt.Y('MinConsumption:Q',
            aggregate={'argmax': 'Year'}),
    color=alt.value(blue_highlight),
    text=alt.Text('MinConsumption_kg:N')
)

label_min = label_base_min.mark_text(
    align='left',
    dx=-70,
    dy=18,
    size=20,
)


# Add a new column with text
df_consumption['consumption_text'] = "- 7.34 kg"

text = alt.Chart(df_consumption).mark_text().encode(
    x=alt.X('Year:T', aggregate='max'),
    y=alt.Y('MinConsumption:Q', aggregate={'argmax': 'Year'}),
    color=alt.value(blue_highlight),
    text=alt.Text('consumption_text:N')
)

label_text = text.mark_text(
    align='left',
    dx=-115,
    dy=-35,
    size=30,
)


# Creating an area chart that fills the space between line_min and line_max
area = alt.Chart(df_consumption).mark_area(opacity=0.2, color=blue_highlight).encode(
    x='Year:T',
    y='MinConsumption:Q',
    y2='MaxConsumption:Q'
)


# plotting the base line_chart
line_chart = alt.Chart(df_consumption).mark_line(color=blue_highlight).encode(
    x=alt.X('Year:T').axis(
        title="Year",
        titleColor='grey',
        titleAnchor='start',
        labelAngle=0,
        grid=False,
        tickColor='grey',
        format='%Y'),
    y=alt.Y('Consumption per Person').scale(domain=(40, 75)).axis(
        title='Consumption per Person in kg',
        titleColor='grey',
        titleAnchor='end',
        grid=False,
        tickColor='grey',
    ),
    strokeWidth=alt.value(2)
).properties(
    width=750,
    height=400
)

# slide 1: just the line chart

meat_chart_1 = alt.layer(line_chart).configure_view(
    strokeWidth=0
).configure_title(
    fontSize=20,
    font='Arial',
    anchor='start',
    fontWeight='normal',
    color='grey'
).configure_axis(
    labelFont='Arial',
    titleFont='Arial',
    labelFontSize=14,
    titleFontSize=14,
    titleFontWeight='normal',
    titleColor='grey'
)

# slide 2: line chart + point and label for 2011

line_chart = line_chart.mark_line(color=dark_grey)

meat_chart_2 = alt.layer(line_chart, create_point('2011-01-01', blue_highlight), create_dotted_line('MaxConsumption:Q', blue_highlight), label_max).configure_view(
    strokeWidth=0
).configure_title(
    fontSize=20,
    font='Arial',
    anchor='start',
    fontWeight='normal',
    color='grey'
).configure_axis(
    labelFont='Arial',
    titleFont='Arial',
    labelFontSize=14,
    titleFontSize=14,
    titleFontWeight='normal',
    titleColor='grey'
)


# slide chart 3: line chart + both points and labels for min and max

meat_chart_3 = alt.layer(line_chart, create_point('2011-01-01', dark_grey), create_dotted_line('MaxConsumption:Q', dark_grey), create_point('2021-01-01', blue_highlight), create_dotted_line('MinConsumption:Q', blue_highlight), label_max, label_min).configure_view(
    strokeWidth=0
).configure_title(
    fontSize=20,
    font='Arial',
    anchor='start',
    fontWeight='normal',
    color='grey'
).configure_axis(
    labelFont='Arial',
    titleFont='Arial',
    labelFontSize=14,
    titleFontSize=14,
    titleFontWeight='normal',
    titleColor='grey'
)

# slide chart 4: area with text

meat_chart_4 = alt.layer(line_chart, area, create_dotted_line('MaxConsumption:Q', blue_highlight), create_dotted_line('MinConsumption:Q', blue_highlight), label_text).configure_view(
    strokeWidth=0
).configure_title(
    fontSize=20,
    font='Arial',
    anchor='start',
    fontWeight='normal',
    color='grey'
).configure_axis(
    labelFont='Arial',
    titleFont='Arial',
    labelFontSize=14,
    titleFontSize=14,
    titleFontWeight='normal',
    titleColor='grey'
)


# -----------------------------------------------------------------------------------#
# Environmental Impact of Food: Emissions and Land Use per weight

df_streamlit = pd.read_csv(
    '../code/cleaned-data/environmental-impact-streamlit.csv')

# Converting Impact Type and Product Type to Categories
df_streamlit['Impact Type'] = df_streamlit['Impact Type'].astype('category')
df_streamlit['Product Type'] = df_streamlit['Product Type'].astype('category')

IMPACT_TYPE = df_streamlit['Impact Type'].cat.categories.to_list()

impact_colors = alt.Scale(
    domain=IMPACT_TYPE,
    range=[dark_red, sage_green, blue_highlight]
)

PRODUCT_TYPE = df_streamlit['Product Type'].cat.categories.to_list()

# Filter df based on selection
if is_plant and is_animal:
    product_opacity = alt.Scale(
        domain=PRODUCT_TYPE,
        range=[1, 1]
    )

elif is_plant:
    product_opacity = alt.Scale(
        domain=PRODUCT_TYPE,
        range=[0.2, 1]
    )

elif is_animal:
    product_opacity = alt.Scale(
        domain=PRODUCT_TYPE,
        range=[1, 0.2]
    )


else:
    product_opacity = alt.Scale(
        domain=PRODUCT_TYPE,
        range=[1, 1]
    )

# df_filtered = df_streamlit.copy()

# if is_ghg:
#     df_filtered = df_filtered[df_filtered['Impact Type'] == 'Emissions']
# if is_land:
#     df_filtered = df_filtered[df_filtered['Impact Type'] == 'Land Use']
# if is_water:
#     df_filtered = df_filtered[df_filtered['Impact Type'] == 'Water Use']
# else:
#     filtered_df = df_streamlit  # default

# impact_types = []
# if is_ghg:
#     impact_types.append('Emissions')
# if is_land:
#     impact_types.append('Land Use')
# if is_water:
#     impact_types.append('Water Use')

# if impact_types:
#     df_filtered = df_streamlit[df_streamlit['Impact Type'].isin(impact_types)]
# else:
#     df_filtered = df_streamlit


# Help from Copilot
if selected_impact_types:
    df_filtered = df_streamlit[df_streamlit['Impact Type'].isin(
        selected_impact_types)]
else:
    df_filtered = df_streamlit

# Plotting Bar Chart

if df_filtered['Impact'].nunique() > 1:
    impact_chart = alt.Chart(df_filtered).mark_bar(cornerRadiusTopRight=10, cornerRadiusBottomRight=10).encode(
        x=alt.X('Impact:Q', scale=alt.Scale(domain=[df_filtered['Impact'].min(), df_filtered['Impact'].max()])).sort('-y').axis(
            labelAngle=0,
            titleAnchor='start',
            title='Median Impact per 1kg/ 1l'),
        y=alt.Y('Impact Type:N', title=None).axis(
            labels=False,
            titleAnchor='end',
            grid=False),
        opacity=alt.Opacity(
            'Product Type:N', scale=product_opacity, legend=None),
        color=alt.Color('Impact Type:N', scale=impact_colors)
    ).facet(
        row=alt.Row('Product:N', title=None, header=alt.Header(
            labelAngle=0, labelAlign='left')),
        spacing=5,  # Set facet label angle to 45 degrees
    )
else:
    st.write("Not enough data to create chart.")

# ----------------------------------------------------------------------------------#
# Environmental Impact of Food: Emissions per 100g Protein

df_nu = pd.read_csv('../code/cleaned-data/environmental-impact-nu.csv')

df_nu['Product'] = df_nu['Product'].astype('category')


# defining color and opacity ranges
df_nu['Product Type'] = df_nu['Product Type'].astype('category')

PRODUCT_TYPE_NU = df_nu['Product Type'].cat.categories.to_list()

product_colors = alt.Scale(
    domain=PRODUCT_TYPE_NU,
    range=[dark_red, sage_green]
)


# points for mean value - highlighted for comparison
# for streamlit -> opacity is not set for cloumn 'Compare', but for 'Product Type' to match chart with weight
median_points_highlighted = alt.Chart(df_nu).mark_point(filled=False, color='black', size=200).encode(
    x=alt.X('Median:Q'),
    opacity=alt.Opacity('Product Type:N', scale=product_opacity, legend=None),
    y=alt.Y('Product:N'),
    tooltip=['Median:Q', 'Product:N']
)


# plotting range bar chart

# final -> product_colors and opacity are applied
bar_nu_final = alt.Chart(df_nu).mark_bar(cornerRadius=10, height=20).encode(
    x=alt.X('5th pctl:Q').scale(domain=[0, 140]).title(
        'GHG Emissions (kg CO2eq)'),
    x2='95th pctl:Q',
    y=alt.Y('Product:N', axis=alt.Axis(
        title='Per 100g protein...', titleAngle=0, titleY=-5)),
    color=alt.Color('Product Type:N', scale=product_colors),
    opacity=alt.Opacity('Product Type:N', scale=product_opacity, legend=None)
).properties(
    width=720,
    height=500
)


# -------------------------------------------------#
# Alternative Protein Companies

df_founded = pd.read_csv('../code/cleaned-data/alt-protein-founded.csv')

# Convert column Year to date time
df_founded['Year Founded'] = pd.to_datetime(
    df_founded['Year Founded'], format='%Y-%m-%d')


# merge df_consumption and df_founded where "Year" == "Year Founded"

# Merge the dataframes
df_merged = pd.merge(df_consumption, df_founded,
                     left_on='Year', right_on='Year Founded')

# delete column Year Foounded, otherwise it is double
df_merged = df_merged.drop('Year Founded', axis=1)

df_merged['Year'] = pd.to_datetime(df_merged['Year'], format='%Y-%m-%d')

# create double axis chart like https://altair-viz.github.io/gallery/layered_chart_with_dual_axis.html, using df_merged
base = alt.Chart(df_merged).encode(
    x=alt.X('Year:T').axis(
        title="Year",
        titleColor='grey',
        titleAnchor='start',
        labelAngle=0,
        grid=False,
        tickColor='grey',
        format='%Y'),
    strokeWidth=alt.value(2)
).properties(
    width=750,
    height=400
)

line_consumption = base.mark_line(stroke=blue_highlight).encode(
    x=alt.X('Year:T').axis(
        grid=False,
        titleColor='grey',
        titleAnchor='start'),
    y=alt.Y('Consumption per Person:Q').scale(domain=(40, 75)).axis(
        title='Consumption of Meat per Person in Germany (kg)',
        titleColor=blue_highlight,
        grid=False,
        titleAnchor='end',
        titleAngle=270,
        titleX=50,
    )
)

line_founded = base.mark_line(stroke=dark_red).encode(
    x=alt.X('Year:T').axis(
        grid=False,
        titleColor='grey',
        titleAnchor='start'),
    y=alt.Y('Number of Companies Founded:Q').axis(
        title='Number of Companies Founded',
        titleColor=dark_red,
        grid=False,
        titleAnchor='end'
    )
)

merged_chart = alt.layer(line_founded, line_consumption).configure_view(
    strokeWidth=0
).configure_title(
    fontSize=20,
    font='Arial',
    anchor='start',
    fontWeight='normal',
).configure_axis(
    labelFont='Arial',
    titleFont='Arial',
    labelFontSize=14,
    titleFontSize=14,
    titleFontWeight='normal',
).resolve_scale(
    y='independent'
)

# -------------------------------------------------#
# Alternative Protein Companies - COUNTRIES

df_country = pd.read_csv('../code/cleaned-data/alt-protein-country.csv')

## ----!!! Source: https://github.com/bast/altair-geographic-plots/blob/main/choropleth.ipynb  ---- ##

countries = alt.topo_feature(data.world_110m.url, "countries")
# https://en.wikipedia.org/wiki/ISO_3166-1_numeric
country_codes = pd.read_csv(
    "https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/all/all.csv"
)

background = alt.Chart(countries).mark_geoshape(fill="lightgray")

# we transform twice, first from "ISO 3166-1 numeric" to name, then from name to value
foreground = (
    alt.Chart(countries)
    .mark_geoshape()
    .transform_lookup(
        lookup="id",
        from_=alt.LookupData(data=country_codes,
                             key="country-code", fields=["name"]),
    )
    .transform_lookup(
        lookup="name",
        from_=alt.LookupData(data=df_country, key="name", fields=[
                             "Number of Companies per Country"]),
    )
    .encode(
        fill=alt.Color(
            "Number of Companies per Country:Q",
            scale=alt.Scale(range=red_scale),
            title="Number of Companies"
        ),
        tooltip=[alt.Tooltip('name:N', title='Country'), alt.Tooltip(
            'Number of Companies per Country:Q', title='Number of Companies')]
    )
)

chart_map = (
    (background + foreground)
    .properties(width=700, height=500)
    .project(
        type="equalEarth",
        scale=800,
        translate=[200, 1000],
    )
)

# --------------------------------------------------------------#


# Section 1: Der Impact der Lebensmittelproduktion
st.header('Der Impact der Lebensmittelproduktion', divider='grey')
st.subheader(
    '23% der Treibhausgasemissionen werden durch die Lebensmittelproduktion verursacht')


st.altair_chart(pie_chart, use_container_width=True)

st.markdown('''"Today’s food supply chain creates ~13.7 billion
metric tons of carbon dioxide equivalents (CO2eq),
26% of anthropogenic (man-made) GHG emissions." (Poore & Nemecek, 2018)''')

st.subheader(
    'Greenhouse Gas Emissions (GHG) und die Landnutzung bei tierischen Produkten höher')

st.altair_chart(impact_chart, use_container_width=True)


st.subheader(
    'Auch im Nährwertvergleich sind die Emissionen bei tierischen Proteinen höher')
st.markdown('''Im Vergleich zu tierischen Erzeugnissen haben pflanzliche Produkte einen geringeren Proteinanteil pro 100g. Doch auch hier schneidet 100g pflanzliches Protein besser ab als 100g tierisches Protein.''')

st.altair_chart(bar_nu_final + median_points_highlighted,
                use_container_width=True)


# Section 2: Fleischkonsum + Ersatzprodukte in Deutschland
st.header('Fleischkonsum und Fleischersatzprodukte', divider='grey')

st.subheader('Der Fleischkonsum in Deutschland sinkt seit 2011 stetig')

st.markdown('''Der Fleischkonsum pro Kopf in Deutschland ist seit 2011 stetig gesunken. Im Jahr 2021 lag der Fleischkonsum bei 56.79 kg pro Kopf. Im Vergleich zu 2011 ist das ein Rückgang von 7.34 kg pro Kopf.''')

# Slide show for the meat consumption
slide = st.slider("Steuerung für die Slide-Show",
                  label_visibility='hidden', min_value=1, max_value=4, step=1, value=1)

if slide == 1:
    st.altair_chart(meat_chart_1, use_container_width=True)
elif slide == 2:
    st.altair_chart(meat_chart_2, use_container_width=True)
elif slide == 3:
    st.altair_chart(meat_chart_3, use_container_width=True)
elif slide == 4:
    st.altair_chart(meat_chart_4, use_container_width=True)


st.subheader(
    'Anzahl der Unternehmen in der Fleischersatzprodukt-Branche')

st.altair_chart(chart_map, use_container_width=True)


st.subheader(
    'Ein Trend ist sichtbar: Weniger Fleisch, mehr Ersatzprodukte')
st.markdown('''Der Markt für Fleischersatzprodukte ist in den letzten Jahren stark gewachsen. Im Jahr 2019 wurden weltweit 109 Unternehmen gegründet, die sich auf die Herstellung von Fleischersatzprodukten spezialisiert haben. Im Gegensatz dazu sinkt der Fleischkonsum pro Kopf in Deutschland.''')

st.altair_chart(merged_chart, use_container_width=True)


# Section 3: Ausblick
st.header('Ausblick und Empfehlung', divider='grey')

st.markdown('''
            __Zusammenfassung der Datenanalyse__
* __Pflanzliche Produkte__ sind durchgehend __besser für die Umwelt__ als tierische Produkte 
* Der __Fleischkonsum__ pro Kopf in Deutschland __sinkt seit 2011__
* Der Markt für alternative, pflanzliche Produkte wird immer größer
''')

st.markdown('''
            __Empfehlung für die Produktstrategie:
Testphase mit veganen Produkten (1/2 des Sortiments) in der Filiale in Stuttgart__
            
Potentielle positive Auswirkungen:
* Metzgerei und vegan? Widerspruch sorgt für __mediale Aufsicht__
* __Nachhaltigkeit als Kaufargument__ und zunehmend wichtigem Entscheidungsfaktor bei den Kunden
* Absetzung von der Konkurrenz 
''')
