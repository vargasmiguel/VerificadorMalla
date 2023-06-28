import streamlit as st
import pandas as pd
import numpy as np

st.title('Verificador de Malla')
st.write('by: Miguel Vargas - Linda Rocha')

st.header('Datos de CORE:')
core=pd.DataFrame({'Código':['1'], 
                   'Curso':['Curso'],
                   'Tipo':['Tipo'],
                   'Creditos':['3'],
                   'Nivel':['1'],
                   'Nota final':['5'],
                   'Estado':['Aprobado'] })


core = st.data_editor(core, num_rows= "dynamic")


st.header('Datos de RyC:')
ryc=pd.DataFrame({'Reg. Académico':['1'],
                  'Código':['2'],
                  'Curso Académico':['Curso'],
                  'Créditos':['3'],
                  'Tipo Curso':['T'],
                  'Nota 75%':['4'],
                  'Nota 25%':['3'],
                  'Calificación Final':['3'],
                  'Fecha Grabación':['01-01-2023'],
                  'Observación':['Aprobado']}

)

ryc = st.data_editor(ryc, num_rows= "dynamic")


if st.button('Analizar'):
    ryc=ryc.set_index('Código')
    core=core.set_index('Código')

    core=core.replace(r'^\s*$', np.nan, regex=True)
    ryc=ryc.replace(r'^\s*$', np.nan, regex=True)


    result = core.join(ryc, lsuffix="_core", rsuffix=("_ryc"), how='outer')
    result['Estado']=result['Estado'].fillna('Falta')
    result['Observación']=result['Observación'].fillna('Falta')
    traductor={
    'Disponible Para Matricula':['Reprobado','Falta'],
    'Aprobado':['Aprobado'],
    'No requerido':['Reprobado','Falta'],
    'Falta':['Falta']}

    def comparing(x):
        comp=0
        c=x['Estado']
        r=x['Observación']
        if r in traductor[c]:
            comp='Coincide'
        else:
            comp='No coincide'
        return comp
    
    result['Resultado']=result.apply(lambda x: comparing(x), axis=1)

    result['Curso']=result['Curso'].fillna(result['Curso Académico'])
    result['Créditos']=result['Créditos'].fillna(result['Creditos'])


    result=result[['Curso','Créditos', 'Estado','Observación', 'Resultado']]

    #result=result.reset_index(names='Código')

    st.header('Resultados')

    def color_coding(x):
        style=0
        if x.Resultado== 'No coincide':
           style='background-color:red'
        elif x.Resultado== 'Coincide':
            style='background-color:green'
        return [0]*(len(x)-1)+[style]

    result = st.dataframe(result.style.apply(color_coding, axis=1))