import pandas as pd
import geopandas as gpd


def load_map():
    return gpd.read_file('world-countries.json')


def load_data():
    fields = [
        'Entity',
        'Year',
        'Deaths - Meningitis - Sex: Both - Age: All Ages (Number)',
        'Deaths - Lower respiratory infections - Sex: Both - Age: All Ages (Number)',
        'Deaths - Intestinal infectious diseases - Sex: Both - Age: All Ages (Number)',
        'Deaths - Protein-energy malnutrition - Sex: Both - Age: All Ages (Number)',
        'Deaths - Cardiovascular diseases - Sex: Both - Age: All Ages (Number)',
        'Deaths - Alzheimer disease and other dementias - Sex: Both - Age: All Ages (Number)',
        'Deaths - Chronic kidney disease - Sex: Both - Age: All Ages (Number)',
        'Deaths - Chronic respiratory diseases - Sex: Both - Age: All Ages (Number)',
        'Deaths - Cirrhosis and other chronic liver diseases - Sex: Both - Age: All Ages (Number)',
        'Deaths - Digestive diseases - Sex: Both - Age: All Ages (Number)',
        'Deaths - Hepatitis - Sex: Both - Age: All Ages (Number)',
        'Deaths - Neoplasms - Sex: Both - Age: All Ages (Number)',
        'Deaths - Parkinson disease - Sex: Both - Age: All Ages (Number)',
        'Deaths - Fire, heat, and hot substances - Sex: Both - Age: All Ages (Number)',
        'Deaths - Malaria - Sex: Both - Age: All Ages (Number)',
        'Deaths - Drowning - Sex: Both - Age: All Ages (Number)',
        'Deaths - Interpersonal violence - Sex: Both - Age: All Ages (Number)',
        'Deaths - HIV/AIDS - Sex: Both - Age: All Ages (Number)',
        'Deaths - Drug use disorders - Sex: Both - Age: All Ages (Number)',
        'Deaths - Tuberculosis - Sex: Both - Age: All Ages (Number)',
        'Deaths - Road injuries - Sex: Both - Age: All Ages (Number)',
        'Deaths - Maternal disorders - Sex: Both - Age: All Ages (Number)',
        'Deaths - Neonatal disorders - Sex: Both - Age: All Ages (Number)',
        'Deaths - Alcohol use disorders - Sex: Both - Age: All Ages (Number)',
        'Deaths - Exposure to forces of nature - Sex: Both - Age: All Ages (Number)',
        'Deaths - Diarrheal diseases - Sex: Both - Age: All Ages (Number)',
        'Deaths - Environmental heat and cold exposure - Sex: Both - Age: All Ages (Number)',
        'Deaths - Nutritional deficiencies - Sex: Both - Age: All Ages (Number)',
        'Deaths - Self-harm - Sex: Both - Age: All Ages (Number)',
        'Deaths - Conflict and terrorism - Sex: Both - Age: All Ages (Number)',
        'Deaths - Diabetes mellitus - Sex: Both - Age: All Ages (Number)',
        'Deaths - Poisonings - Sex: Both - Age: All Ages (Number)',
    ]
    df = pd.read_csv('annual-number-of-deaths-by-cause.csv').loc[:, fields]
    for field in fields[2:]:
        new_field = field.replace('Deaths - ', '')
        new_field = new_field.replace(' - Sex: Both - Age: All Ages (Number)', '')
        df[new_field] = df[field]
        df = df.drop(columns=[field])

    df['country'] = df['Entity'].apply(_correct_country)
    df = df.drop(columns=['Entity'])
    return df.round(0)


def _correct_country(name):
    if name == 'Russian Federation':
        # It was better without russia on map
        return 'Russia'
    elif name == 'Bolivia (Plurinational State of)':
        return 'Bolivia'
    elif name == 'Venezuela (Bolivarian Republic of)':
        return 'Venezuela'
    elif name == 'Congo':
        return 'Republic of the Congo'
    elif name == 'Iran (Islamic Republic of)':
        return 'Iran'
    elif name == 'Guinea-Bissau':
        return 'Guinea Bissau'
    elif name == 'Cote d\'Ivoire':
        return 'Ivory Coast'
    elif name == 'Republic of Korea':
        return 'North Korea'
    elif name == 'Dem. People\'s Republic of Korea':
        return 'South Korea'
    elif name == 'Czechia':
        return 'Czech Republic'
    elif name == 'Republic of Moldova':
        return 'Moldova'
    elif name == 'Viet Nam':
        return 'Vietnam'
    elif name == 'Lao People\'s Democratic Republic':
        return 'Laos'
    elif name == 'Serbia':
        return 'Republic of Serbia'
    elif name == 'North Macedonia':
        return 'Macedonia'
    elif name == 'Eswatini':
        return 'Swaziland'
    elif name == 'Syrian Arab Republic':
        return 'Syria'
    elif name == 'China, Taiwan Province of China':
        return 'Taiwan'
    elif name == 'Brunei Darussalam':
        return 'Brunei'
    elif name == 'Timor-Leste':
        return 'East Timor'
    elif name == 'Bahamas':
        return 'The Bahamas'
    elif name == 'United States':
        return 'United States of America'
    elif name == 'Tanzania':
        return 'United Republic of Tanzania'
    elif name == 'Somalia':
        return 'Somaliland'
    else:
        return name


def get_death_summary_by_country():
    return load_data() \
        .melt(id_vars=['country'], value_name='deaths') \
        .groupby('country').sum().reset_index()


def get_last_year_death_summary_by_country():
    df = load_data()
    df = df[df['Year'] == 2017]
    return df \
        .melt(id_vars=['country'], value_name='deaths') \
        .groupby('country').sum().reset_index()


def get_mean_deaths_by_country():
    return load_data() \
        .melt(id_vars=['country', 'Year'], value_name='deaths') \
        .groupby(['country', 'Year']).sum().reset_index() \
        .groupby('country').mean().reset_index()


def get_deaths_comparison(base, actual, on):
    merged = pd.merge(base, actual, on=on, how='inner')
    merged['deaths_change'] = merged['deaths_y'] - merged['deaths_x']
    return merged


def get_deaths_summary_by_category():
    return load_data()\
        .drop(columns=['country', 'Year'])\
        .melt(var_name='category', value_name='deaths')\
        .groupby('category').sum().reset_index()


def get_deaths_mean_by_category():
    result = load_data()\
        .groupby('Year').sum().reset_index()\
        .drop(columns=['Year'])\
        .melt(var_name='category', value_name='deaths')\
        .groupby('category').mean().reset_index()

    result['mark'] = 'Mean'
    return result


def get_deaths_for_last_year_by_category():
    df = load_data()
    df = df[df['Year'] == 2017]

    result = df\
        .drop(columns=['country', 'Year'])\
        .melt(var_name='category', value_name='deaths')\
        .groupby('category').sum().reset_index()
    
    result['mark'] = '2017'
    return result


def get_deaths_summary_for_2008_crisis():
    df = load_data()
    df = df[(df['Year'] > 2002) & (df['Year'] < 2015)]
    df = df[df['country'] == 'United States of America']

    categories = ['Interpersonal violence', 'Drug use disorders', 'Road injuries', 'Alcohol use disorders', 'Self-harm']
    df = df.loc[:, ['Year', *categories]]

    return df.melt(id_vars=['Year'], var_name='category', value_name='deaths')


def get_deaths_summary_for_maternal_and_neonatal_g6():
    df = load_data()
    g6 = ['England', 'Canada', 'Germany', 'Japan', 'Italy', 'France']
    df = df[df['country'].isin(g6)]

    categories = ['Maternal disorders', 'Neonatal disorders']
    df = df.loc[:, ['country', 'Year', *categories]]

    return df.melt(id_vars=['country', 'Year'], var_name='category', value_name='deaths')


def get_deaths_summary_for_maternal_and_neonatal_bad_countries():
    df = load_data()
    g6 = ['Iraq', 'Malaysia', 'Somaliland', 'Congo', 'Mexico', 'Colombia']
    df = df[df['country'].isin(g6)]

    categories = ['Maternal disorders', 'Neonatal disorders']
    df = df.loc[:, ['country', 'Year', *categories]]

    return df.melt(id_vars=['country', 'Year'], var_name='category', value_name='deaths')


def get_disease_deaths_summary_in_america():
    df = load_data()
    df = df[df['country'] == 'United States of America']

    categories = [
        'Lower respiratory infections',
        'Cardiovascular diseases',
        'Alzheimer disease and other dementias',
        'Chronic kidney disease',
        'Chronic respiratory diseases',
        'Cirrhosis and other chronic liver diseases',
        'Digestive diseases',
        'Neoplasms',
        'HIV/AIDS',
    ]
    df = df.loc[:, ['Year', *categories]]

    return df.melt(id_vars=['Year'], var_name='category', value_name='deaths')


def get_suicide_analysis():
    return load_data().loc[:, ['country', 'Year', 'Self-harm']]


# testing source functions
if __name__ == '__main__':
    data = load_data()
    print(get_disease_deaths_summary_in_america())
