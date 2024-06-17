
#%%
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio 
pio.renderers.default = "browser"


#%%
def graficar_2(Datos_comp,df_2=None):
    if df_2 is not None:
        traces1 = []
        traces2 = []

        for col in Datos_comp.columns:
            traces1.append(go.Scatter(x=Datos_comp.index, y=Datos_comp[col], visible=True, name=f'df 1: {col}'))
        for col in df_2.columns:
            traces2.append(go.Scatter(x=df_2.index, y=df_2[col], visible=True, name=f'df 2: {col}', yaxis='y2'))

        layout = go.Layout(
            yaxis=dict(title='Eje para df 1'),yaxis2=dict(title='Eje para df 2', overlaying='y', side='right'),
            legend=dict(x=1.1, y=1.1),title=dict(text='Todos los graficos', x=0.5),showlegend=True,
            updatemenus=[
            dict(type='buttons',direction='right',x=1.4,y=1.3,showactive=True,buttons=[
            dict(method='restyle',label='Mostrar todos',visible=True,args=[{'visible': True}],args2=[{'visible': 'legendonly'}])])])

        fig = go.Figure(data=traces1 + traces2, layout=layout)

    else:
        traces = []
        for col in Datos_comp.columns:
            traces.append(go.Scatter(x=Datos_comp.index, y=Datos_comp[col], visible=True, name=col))

        layout = go.Layout(
            updatemenus=[
                dict(type='buttons',direction='right',x=1.4,y=1.3,showactive=True,buttons=[
                        dict(method='restyle',label='Mostrar todos',visible=True,args=[{'visible': True}],
                            args2=[{'visible': 'legendonly'}])])],title=dict(text='Todos los graficos', x=0.5),showlegend=True)

        fig = go.Figure(data=traces, layout=layout)
    return(fig)