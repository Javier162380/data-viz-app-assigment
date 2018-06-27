from pandas import read_csv,melt

international_transparency_data = read_csv('data/international_transparency.csv')
international_transparency_pivot_data = melt(international_transparency_data,
                                             id_vars=['Country','Code','Region'])
international_transparency_pivot_data['variable'].astype(int)
international_transparency_pivot_data.rename(columns={'variable':'year','value':'cpi_score'}, inplace=True)
CPI_regions = {'AP':'Asia & the Pacific','AME':'America',
               'WE/EU':'Western Europe',
               'ECA':'Eastern Europe and Central Asia',
               'MENA':'Middle East and North Africa',
               'SSA': 'Sub-Saharan Africa'}

def regions(acronym):
    return CPI_regions.get(acronym,None)
international_transparency_pivot_data['Region_Full_Name']=(international_transparency_pivot_data['Region'].
                                                                                                apply(regions))
spain_corruption = read_csv('data/spain_corruption.csv')
def filter_year(date):
    if date[0] in ('\t',' '):
        return int(date[1:5])
    else:
        return int(date[0:4])
spain_corruption['year'] = spain_corruption['fecha'].apply(filter_year)
all_kpis = read_csv('data/kpis_related_with_transparency.csv')