from itertools import product
from pathlib import Path
import shlex

from metpy import calc as metcalc
from metpy.units import units as metunits
import numpy as np
import pandas as pd
from plotly.offline import iplot, plot
import plotly.io as pio
import plotly.graph_objects as go
import seaborn as sns
import toml


lineprop = lambda num, dash, width: dict(color=f"rgb{tuple(np.array(col_pal[num])*255)}", dash=dash, width=width)
sns.set_context('paper')
sns.set(style="ticks")
sns.set_palette('colorblind')
col_pal = sns.color_palette("colorblind")
VN_LOOKUP = dict(
     tas=('2m Temperature [K]', 'RdYlBu_r'),
     cllvi=('Vertically Integrated Cloud Water [kg/m²]', 'BuPu'),
     clivi=('Vertically Integrated Cloud Ice [kg/m²]', 'BuPu'),
     qsvi=('Vertically Integrated Snow [kg/m²]', 'BuPu'),
     qgvi=('Vertically Integrated Graupel [kg/m²]', 'BuPu'),
     qrvi=('Vertically Integrated Rain [kg/m²]', 'BuPu'),
     clt=('Total Cloud Cover [ ]', 'Greys_r'),
     cl=('Low Cloud Cover [ ]', 'Greys_r'),
     hfls=('Surface Latent Heat Flux [W/m²]', 'RdYlBu_r'),
     hfss=('Surfce Sensible Heat Flux [W/m²]', 'RdYlBu_r'),
     rlut=('OLR [W/m²]', 'RdYlBu_r'),
     rsut=('Shortwave upward flux [W/m²]', 'RdYlBu_r'),
     rsds=('Shortwave downward flux surf. [W/m²]', 'RdYlBu_r'),
     rlds=('Longwave downward flux surf. [W/m²]', 'RdYlBu_r'),
     rsus=('Shortwave upward flux surf. [W/m²]', 'RdYlBu_r'),
     rlus=('Longwave upward flux surf. [W/m²]', 'RdYlBu_r'),
     net_surf_energy=('Net surf. Energy [W/m²]', 'RdYlBu_r'),
     rsdt=('Shortwave downward flux [W/m²]', 'RdYlBu_r'),
     net_toa=('Net TOA radiation flux [W/m²]', 'RdYlBu_r'),
     net_surf=('Net surf radiation flux [W/m²]', 'RdYlBu_r'),
     prw=('Vertically Integrated Water Vapor [kg/m²]', 'BuPu'),
     pr=('Precipitation [mm/h]', 'Blues'),
     ts=('Surf. Temperature [K]', 'RdYlBu_r'),
     vas=('10 V-wind [m/s]', 'RdYlBu_r'),
     uas=('10 U-wind [m/s]', 'RdYlBu_r'),
     qs=('Spec. Humidity [kg/kg]', 'BuPu'),
     uas_ice=('10 U-wind ice [m/s]', 'RdYlBu_r'),
     vas_ice=('10 V-wind ice [m/s]', 'RdYlBu_r'),
     uas_lnd=('10 U-wind land [m/s]', 'RdYlBu_r'),
     vas_lnd=('10 V-wind land [m/s]', 'RdYlBu_r'),
     uas_wtr=('10 U-wind water [m/s]', 'RdYlBu_r'),
     vas_wtr=('10 V-wind water [m/s]', 'RdYlBu_r'),
)


def update_layout(fig, varnames, surftypes, vn_lookup=None):
    var_buttons, surf_buttons = [], []
    vn_lookup = vn_lookup or VN_LOOKUP
    annotations = fig.layout.annotations
    plot_array = np.array(list(product(varnames, surftypes.keys())))
    for nn, vn in enumerate(varnames):
        visible = len(varnames)*[False]
        visible[nn] = True
        var_text = vn_lookup[vn][0]
        ann = dict(x=0, y=1.15, xanchor='left', yanchor='top', showarrow=False,
                       xref='paper', yref='paper', font=dict(size=18), text=var_text)
        var_buttons.append(dict(label=vn, method='update', 
                            args=[{'visible': visible}, {"annotations": (ann,)+annotations}]))
    for surftype, data in surftypes.items():    
        x, y = [ts.x for ts in data], [ts.y for ts in data]
        surf_buttons.append(dict(label=surftype, method='update', args=[{'y':y, 'x':x}]))
    text = vn_lookup[varnames[0]][0]
    ann = dict(x=0, y=1.15, xanchor='left', yanchor='top', showarrow=False,
               xref='paper', yref='paper', font=dict(size=18), text=text)
    fig.update_layout(
        annotations=annotations+ (ann,),
        updatemenus=[
                dict(
                    buttons=var_buttons,
                    direction="down",
                    pad={"r": 10, "t": 25},
                    #showactive=True,
                    active=0,
                    x=0.97,
                    xanchor="left",
                    y=1.35,
                    yanchor="top"
                ),
            dict(
                    buttons=surf_buttons,
                    direction="right",
                    pad={"r": 10, "t": 25},
                    #showactive=True,
                    active=0,
                    x=0.4,
                    xanchor="left",
                    y=1.35,
                    yanchor="top"
                ),
        ]
    )
    return fig


import plotly.graph_objects as go
from plotly.subplots import make_subplots

def add_trace(data, exp, lineprop, row=1, col=1, visible=True, showlegend=True):
    if len(exp) == 0:
        showlegend = False
    ts  = go.Scatter(x=data.index,
                     y=data.values,
                     name=exp,
                     showlegend=showlegend,
                     line=lineprop,
                     legendgroup=exp,
                     visible=visible,
                     mode='lines'
                    )
    return ts

def get_varnames(filename, key_only=False):

    p = Path(filename).with_suffix('').name
    for key in VN_LOOKUP.keys():
        if key in p:
            if key_only:
                return key
            return VN_LOOKUP[key][0]
    return ''

def get_animation(tmpl, suffix, config):
    p = Path('.') / 'media'
    sub_dirs = sorted([x for x in p.iterdir() if x.is_dir() if 'ceres' not in str(x)])
    map_section = ''
    map_files = []
    for sub_dir in sub_dirs:
        map_files += [f for f in sub_dir.rglob(f'*.{suffix}')]
    if not map_files:
        return ''

    header = f'Animations'
    desc = f'This section contains animations of assorted variables.'
    desc += ' Click left and right of the figure or swipe left and right to navigate. Click into the animation to enlarge.'
    map_section += f'''
    <h3>{header}</h3>
        <p>{desc}</p>
        <section class="project tall">
            <div class="pages">
                <div class="page-scroll">'''
    for map_file in map_files:
        mfile = map_file
        caption = get_varnames(map_file.name)
        exp = mfile.parent.name
        if 'net_surf' in str(mfile).lower():
            caption = (f'Net surface energy = R<sub>net<sub>surf</sub></sub> + LH + SH')
        elif 'cl_' in str(mfile).lower():
            caption = ('Low-cloud cover has been calculated based on cloud water'
                       ' and ice within the lower 20 model level. The calculation'
                       ' might be subsect to improvements')
        map_section += f'''
            <div class="page  video" style="background-color: #FFF ">
            <div class="media loader-parent"  style="color:#3c6caf">
            <div>
            <video loop preload="none">
            <source src="{mfile}" type="video/mp4">
            </video>
            </div>
            <svg class="loading-spinner" width="64" height="64" viewbox="0 0 64 64">
            <circle cx="32" cy="32" r="20" fill="none" stroke-width="6" stroke-miterlimit="10" stroke="#ccc" />
            </svg>
            </div>
            <div class="caption">
            <p><em>{exp}</em>: {caption}</p>
            </div>
            </div>'''
    map_section +=  '</div></div></section>'
    return map_section

def get_comparison(dirname, config):

    exp1, exp2 = dirname.split('_vs_')
    header = f'{exp2} and {exp1} comparison'
    exp_desc1 = f'{config["overview"][exp1]}'.lower()
    exp_desc2 = f'{config["overview"][exp2]}'.lower()
    return header, f'<em>{exp2}</em> represents the {exp_desc2}, whereas <em>{exp1}</em> stands for {exp_desc1}.'

def get_files(subdir, suffix='.png'):

    if 'ceres' in str(subdir):
        variables = {get_varnames(f.name, key_only=True) for f in subdir.rglob(f'*.{suffix}')}
        mapfiles = []
        for variable in variables:
            mapfiles += [f for f in subdir.rglob(f'*{variable}*.{suffix}')]
    else:
        mapfiles = [f for f in subdir.rglob(f'*.{suffix}')][::-1]
    return mapfiles


def get_figures(tmpl, suffix, config):
   
    p = Path('.') / 'media'
    sub_dirs = sorted([x for x in p.iterdir() if x.is_dir() if 'ceres' not in str(x) and 'vs' in str(x)])
    map_section = ''
    for sub_dir in sub_dirs+[p / 'ceres']:
        map_files = get_files(sub_dir.absolute(), suffix='png')
        if map_files:
            if 'ceres' in sub_dir.name:
                header = 'ceres comparisons'
                desc = ('Here <em>ceres</em> represents the '
                       ' <a href="https://ceres.larc.nasa.gov/data/#cccm" target=_blank>FLASHFlux Gridded Fluxes</a> '
                       ' dataset and is made available for the considered simulation period at 1&#176;'
                       )
            else:
                header, desc = get_comparison(sub_dir.name, config)
            desc += ' Click left/right of the figure or swipe left/right to navigate. Click into the figure to enlarge and use left/right to navigate.'
            map_section += f'''
            <h3>{header}</h3>
                <p>{desc}</p>
                <section class="project tall">
                    <div class="pages">
                        <div class="page-scroll">'''
        for map_file in map_files:
            mfile = map_file
            caption = get_varnames(map_file.name)
            region = ''
            if mfile.parent.name in config['regions'].keys():
                if mfile.parent.name != 'global':
                    region = f"Showing the {config['regions'][mfile.parent.name]['name']} Area: "
            if 'violin' in str(mfile).lower():
                caption = ('Distribution of variables for times and locations of'
                           ' of negative radiation bias (compared to nwp). The'
                           ' distributions have been ranked (quintiles) by their relative'
                           ' magnitude of the radiation bias.')
            elif 'net_surf_energy' in str(mfile).lower():
                caption = ('Net surface energy = R<sub>net<sub>surf</sub></sub> + LH + SH')
            elif 'cl_' in str(mfile).lower():
                caption = ('Low-cloud cover has been calculated based on cloud water'
                           ' and ice within the lower 20 model level. The calculation'
                           ' might be subsect to improvements')
            map_section += f'''
                <div class="page  image" style="background-color: #FFF ">
                <div class="media loader-parent"  style="color:#3c6caf">
                <div>
                <img src="{mfile}">
                </div>
                <svg class="loading-spinner" width="64" height="64" viewbox="0 0 64 64">
                <circle cx="32" cy="32" r="20" fill="none" stroke-width="6" stroke-miterlimit="10" stroke="#ccc" />
                </svg>
                </div>
                <div class="caption">
                <p>{region}{caption}</p>
                </div>
                </div>'''
        map_section +=  '</div></div></section>'
    return map_section

def replace(templ, **kwargs):
    for key, value in kwargs.items():
        templ = templ.replace(f'%{key}', value)
    return templ

def zone_avg(config):
    zone_data = {}
    for exp in config['titles']['datasets']:
        outf = Path('.') / 'data' / 'zonal_avg.h5'
        zone_data[exp] = pd.read_hdf(outf, key=exp)
    varnames = []
    for exp, data in zone_data.items():
        if len(data.keys()) > len(varnames) and exp != 'ceres':
            varnames = list(data.keys())
    surftypes = {'Land+Ocean':[], 'Ocean':[], 'Land':[]}
    plot_array = np.array(list(product(varnames, surftypes.keys())))
    for nn, (exp, data) in enumerate(zone_data.items()):
        if exp == 'ceres':
            dash = 'dash'
        else:
            dash = 'solid'
        for tt, (vn, surftype) in enumerate(plot_array):
            if tt == 0:
                visible = True
            else:
                visible = False
            try:
                dd = data[vn].xs(surftype, level='surf')
            except KeyError:
                dd = data['rlut'].xs(surftype, level='surf')*np.nan
                visible=False
            dd = dd.reindex(index=np.arange(-90, 91, 2), method='nearest')
            ts = add_trace(dd, exp, lineprop(nn, dash, 3), visible=visible)
            surftypes[surftype].append(ts)
    fig = go.Figure(data=surftypes['Land+Ocean'])
    fig = update_layout(fig, varnames, surftypes)
    fig.update_layout(xaxis_title='Latitude [&#176;N]',)
    return fig.to_html(full_html=False)


def get_vertical_vars(df):
    df['clx'] = df['cli'] + df['clw']
    df['rh'] = metcalc.relative_humidity_from_specific_humidity(
        df['hus'].values * metunits('kg/kg'),
        df['ta'].values * metunits('K'),
        df['pfull'].values * metunits('Pa')
    ).magnitude
    df['td'] = metcalc.dewpoint_from_specific_humidity(
        df['hus'].values * metunits('kg/kg'),
        df['ta'].values * metunits('K'),
        df['pfull'].values * metunits('Pa')
    ).magnitude
    df['tv'] = metcalc.virtual_temperature(
        df['ta'].values * metunits('K'),
        metcalc.mixing_ratio_from_specific_humidity(df['hus'].values * metunits('kg/kg'))
    ).magnitude
    return df

def vert_profile(config):
    varnames_x = ['cli', 'clw', 'clx', 'hus', 'ta', 'ua', 'va', 'wz', 'rh', 'td', 'tv']
    varnames_y = ['zg']
    var_lookup = {
        'cli':('Cloud Ice [kg/kg]', ''),
        'clw': ('Cloud Water [kg/kg]', ''),
        'clx': ('Cloud Water + Cloud Ice [kg/kg]', ''),
        'hus':( 'Specific Humidity [kg/kg]', ''),
        'ta': ('Temperature [K]', ''),
        'ua': ('U-Wind [m/s]', ''),
        'va': ('V-Wind [m/s]', ''),
        'wz': ('W-Wind [m/s]', ''),
        'wap': ('Omega [Pa/s]', ''),
        'zg': ('Height [m]', ''),
        'td': ('Dew Point Temperature [&#8451;]', ''),
        'rh': ('Relative Humidity [ ]',''),
        'tv': ('Virtual Temperature [K]', ''),
        'pfull': ('Pressure [Pa]', '')
    }
    vert_data = {}
    for region in config['regions']:
        outf = Path('.') / 'data' / 'vertical_avg.h5'
        try:
             vert_data[region] = get_vertical_vars(pd.read_hdf(outf, key=region))
        except KeyError:
            pass
    exps = []
    for region, data in vert_data.items():
        exp_data =  data.index.get_level_values(0).unique()
        if len(exp_data) > len(exps):
            exps = exp_data.values

    plot_array = np.array(list(product(varnames_x, vert_data.keys())))
    regions = {config['regions'][region]['name']: [] for region in vert_data.keys()}
    for nn, exp in enumerate(exps):
        if exp == 'ceres':
            dash = 'dash'
        else:
            dash = 'solid'
        for tt, (vn, region) in enumerate(plot_array):
            if tt == 0:
                visible = True
            else:
                visible = False
            region_name = config['regions'][region]['name']
            try:
                dd = vert_data[region][[vn]+varnames_y].xs(exp, level='exp')
                dd.index = dd[varnames_y[0]]
                dd = dd[vn]
            except KeyError:
                idx = vart_data[region][varnames_y[0]].xs(exp, level='exp')
                dd = pd.Series(len(idx)*[np.nan], index=idx)
                visible = False
            ts = add_trace(pd.Series(dd.index, index=dd.values), exp, lineprop(nn, dash, 3), visible=visible)
            regions[region_name].append(ts)
    fig = go.Figure(data=regions[region_name])
    fig = update_layout(fig, varnames_x, regions, vn_lookup=var_lookup)
    fig.update_layout(yaxis_title=var_lookup[varnames_y[0]][0])
    return fig.to_html(full_html=False)

def timeseries(config):
    ts_data = {}
    start, end = pd.DatetimeIndex(config['titles']['period'])
    for exp in config['titles']['datasets']:
        outf = Path('.') / 'data' / 'time_series_data.h5'
        ts_data[exp] = pd.read_hdf(outf, key=exp)
    varnames = []
    for exp, data in ts_data.items():
        if len(data.keys()) > len(varnames) and exp != 'ceres':
            varnames = list(data.keys())
    try:
        varnames.remove('exp')
    except:
        pass
    sub_titles = {'sea+land':'Land & Ocean', 'sea':'Ocean', 'land':'Land'}
    area_lookup = {'global': 'Global', 'tropics': 'Tropics', 'eureca': 'Eurec4a'}
    areas = {'Global':[], 'Tropics':[], 'Eurec4a':[]}
    plot_array = np.array(list(product(varnames, area_lookup.keys())))
    fig_ts = make_subplots(rows=1, cols=3, subplot_titles=list(sub_titles.values()), shared_yaxes=False)
    for nn, (exp, data) in enumerate(ts_data.items()):
        if exp == 'ceres':
            dash = 'dash'
        else:
            dash = 'solid'
        for col, (surf, surfname) in enumerate(sub_titles.items()):
            if col == 0:
                showl = True
            else:
                showl = False
            for tt, (vn, area) in enumerate(plot_array):
                areaname = area_lookup[area]
                if tt == 0:
                    visible = True
                else:
                    visible = False
                try:
                    plot_data = data[vn].loc[(area, surf)].loc[start:end].iloc[:-1]
                    exp_name = exp
                except KeyError:
                    plot_data = data['rlut'].loc[(area, surf)].loc[start:end].iloc[:-1] * np.nan
                    exp_name = ''
                ts = add_trace(plot_data, exp_name, lineprop(nn,  dash, 3), 
                                visible=visible, showlegend=showl, col=col+1)
                if areaname == list(areas.keys())[0]:
                    fig_ts.add_trace(ts, col=col+1, row=1)
                areas[areaname].append(ts)
    fig_ts = update_layout(fig_ts, varnames, areas)
    return fig_ts.to_html(full_html=False)

def main():
    with open('index.tmpl') as f:
        template  = f.read()#.replace('%map_data', map_section)

    config = toml.load('data/simulations.toml')
    overview_sect=''
    for key in sorted(config['overview'].keys()):
        conf = config['overview'][key]
        res = config['configuration']['resolution'][key]
        overview_sect+=f'<tr><td><b>{key}</b></td><td>{conf} at {res}</td></tr>\n'
    map_data = get_figures(template, 'png', config)
    ext_title = config['titles']['long_title']
    short_title = config['titles']['short_title']
    start, end = pd.DatetimeIndex(config['titles']['period'])
    timeperiod = label_s = f"{pd.Timestamp(start).strftime('%b %e')} - {pd.Timestamp(end).strftime('%b %e')}"
    time_series_plot = timeseries(config)
    zonal_plot = zone_avg(config)
    vert_profile_plot = vert_profile(config)
    animations = get_animation(template, 'mp4', config)
    output = replace(
            template,
            short_title=short_title,
            ext_title=ext_title,
            map_data=map_data,
            overview_sect=overview_sect,
            timeperiod=timeperiod,
            zonal_plot=zonal_plot,
            time_series_plot=time_series_plot,
            vert_profile=vert_profile_plot,
            animations=animations,
            )
    with open('index.html', 'w') as f:
        f.write(output)




if __name__ == '__main__':
    main()
