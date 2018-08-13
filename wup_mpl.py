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
from matplotlib.colors import Normalize
import numpy as np

class MidpointNormalize(Normalize):
    """
    Used to force a zero level in a colormap.
    Neat for forcing reds to negative urban growth.

    Taken from Joe Kington's answer on StackOverflow:
    https://stackoverflow.com/a/20146989/4118756
    """
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        # I'm ignoring masked values and all kinds of edge cases to make a
        # simple example...
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y))

def basemap_worldscatter(df, savepdf=False):
    import matplotlib.pyplot as plt
    from mpl_toolkits.basemap import Basemap

    plt.rc('text', usetex=True)

    # scale markers by absolute growth
    growth_to_msize = lambda p: np.abs(p)**0.7 + 10
    m_size = df['growthabs'].apply(growth_to_msize)

    # color markers by relative growth
    m_col = df['growthperc']
    vmin, vmax = np.percentile(m_col, 1), np.percentile(m_col, 95)
    normalize = MidpointNormalize(vmin=vmin, vmax=vmax, midpoint=0)

    # Basemap takes plt.gcf() as a figure but doesn't pass kwargs to figures
    plt.figure(figsize=(16, 8))
    bmap = Basemap(resolution='l', projection='mbtfpq', lon_0=45, lat_0=0)
    bmap.drawmapboundary(fill_color='#c6dbef')
    bmap.fillcontinents(color='#f2e0c9', lake_color='#c6dbef',
                        zorder=0.8, alpha=0.5)
    bmap.etopo(alpha=0.3, zorder=0.9)
    bmap.drawcoastlines(linewidth=0.6, zorder=0.9, color='#525252')
    bmap.drawcountries(linewidth=0.6, zorder=0.9, color='#525252')
    x, y = bmap(df['Longitude'].values, df['Latitude'].values)
    bmap.scatter(x, y, c=m_col,
                s=m_size, marker='.', alpha=0.9, edgecolor='#737373',
                cmap=plt.cm.RdYlGn, norm=normalize, zorder=1)
    cbar = bmap.colorbar(size='2%', extend='max')
    cbar.set_label(r'$\mathrm{Relative~city~size~growth~(\%)}$',
                   fontsize='large')
    plt.gca().set_title(r'$\mathrm{Projected~growth~of~cities~with~over'
                  '~300\,000~inhabitants~(2018-2035)}$', fontsize='x-large')

    bmap.drawparallels(np.arange(-90.,120.,30.), zorder=0.7,
                       color='#969696', linewidth=0.3)
    bmap.drawmeridians(np.arange(0.,360.,60.), zorder=0.7,
                       color='#969696', linewidth=0.3)

    # display size scale of the scatter points
    for dp, lab in zip([10, 100, 1000, 10000],
            [r'$10\,000$', r'$100\,000$',
             r'$1~\mathrm{million}$', r'$10~\mathrm{million}$']):
        plt.scatter([], [], facecolor='none', edgecolor='#737373', alpha=0.9,
                    s=growth_to_msize(dp), marker='.', label=lab)
    plt.legend(scatterpoints=1, frameon=False, labelspacing=1, loc='lower left')

    # basemap issue:
    # https://stackoverflow.com/questions/15003353
    cbar.set_alpha(1)
    cbar.draw_all()

    if savepdf:
        plt.savefig("graphics/wup-upban-growth.pdf", dpi=140)
    plt.show()

if __name__=='__main__':
    from wup_io import preprocess_wup2018
    df = preprocess_wup2018()

    basemap_worldscatter(df)
