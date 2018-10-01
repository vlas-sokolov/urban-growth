"""
==== Source for the data used in this visualization ====
    United Nations, Department of Economic and Social
    Affairs, Population Division (2018).
    World Urbanization Prospects: The 2018 Revision, Online Edition.

File 22: Annual Population of Urban Agglomerations
         with 300,000 Inhabitants or More in 2018,
         by Country, 1950-2035 (thousands)

====  Original license used for the UN data ====
Copyright © 2018 by United Nations, made available under
a Creative Commons license CC BY 3.0 IGO:
http://creativecommons.org/licenses/by/3.0/igo/
"""
import numpy as np
from plotly.offline import plot

def make_plotly_data(df):
    """ Set data point properties """
    growth_to_msize = lambda p: np.abs(p)**0.7 + 5
    m_col = df['growthperc']
    cmin, cmax = np.percentile(m_col, 1), np.percentile(m_col, 95)

    df['growth_abs_str'] = df.growthabs.apply(lambda n: f'{n*1000:+,d}')
    df['growth_perc_str'] = df.growthperc.apply(lambda p: f'{p:+.1f}%')
    # using hiddent atttributes is bad and I should feed bad
    df['growth_str'] = df[['growth_abs_str', 'growth_perc_str']].apply(
                lambda x: f'{x._name}: {x[0]} ({x[1]})', axis=1)

    urban_growth = [dict(
        lon=df['Longitude'],
        lat=df['Latitude'],
        marker=dict(
            color=df['growthperc'], # color by fractional increase
            colorscale='Portland', # palette name
            colorbar={'ticksuffix': '%'},
            reversescale=True, # invert the colorbar mapping
            showscale=True, # show colorbar?
            cmin=cmin,
            cmax=cmax,
            sizemode='area', # could play with power scale instead
            size=growth_to_msize(df['growthabs'])
            ),
        type='scattergeo',
        showlegend=False,
        text=df['growth_str'],
        hoverinfo='text'
    )]

    return urban_growth

def make_plotly_layout(geokwargs={}, **kwargs):
    """ Set global plotting options """
    urban_layout = dict(
        title='Projected growth of cities with over'
              ' 300,000 inhabitants (2018-2035)'
              '<br>Source: <a href="https://esa.un.org/unpd/wup/">'
              ' UN World Urbanization Prospects 2018</a>',
        showlegend=True,
        geo=dict(
            scope='world',
            projection=dict(type='orthographic'),
            showland=True,
            showcoastlines=True,
            resolution=110, # the only other available option is too slow!
            showcountries=True,
            countrycolor='#525252',
            showocean=True,
            oceancolor='#c6dbef',
            showlakes=True,
            lakecolor='#c6dbef',
            showrivers=True,
            rivercolor='#c6dbef',
            landcolor='#f2e0c9',
            subunitwidth=1,
            countrywidth=1,
            #subunitcolor = "rgb(255, 255, 255)", # que es?
        ))
    # update the defaults with keyword arguments, if any
    urban_layout.update(kwargs)
    urban_layout['geo'].update(geokwargs)

    return urban_layout

def main():
    """ Call plot.ly and display the interactive figure """
    from wup_io import preprocess_wup2018
    wup_df = preprocess_wup2018()

    fig = dict(data=make_plotly_data(wup_df), layout=make_plotly_layout())
    plot(fig, filename='graphics/wup-urban-growth.html', auto_open=True)

if __name__ == '__main__':
    main()
