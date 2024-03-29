import numpy as np
from prophet import Prophet
import plotly.graph_objs as go
import streamlit as st
from sklearn.metrics import mean_absolute_error, mean_squared_error
import pandas as pd
from acuracy import mean_absolute_percentage_error
from feriados import create_feriados_sp
import streamlit as st


def modelo(df1, data_selecionada, hora_selecionada):
    # Adicionando feriados nacionais brasileiros

    # Call the function to create the DataFrame with missing dates as holidays
    feriados_sp_missing = create_feriados_sp(df1)

    feriados_sp = pd.DataFrame({
        'holiday': 'feriados_sp',
        'ds': pd.to_datetime(['2024-01-25', '2024-02-25', '2024-03-25', '2024-04-25', '2024-05-25',
                              '2024-06-25', '2024-07-25', '2024-08-25', '2024-09-25', '2024-10-25',
                              '2024-11-25', '2024-12-25']),
        'lower_window': 0,
        'upper_window': 0,
    })

    # Criando o modelo Prophet
    m = Prophet(holidays=feriados_sp_missing)

    # Converter 'ds' para o formato de data, se necessário
    df1['ds'] = pd.to_datetime(df1['ds'])

    # Adicionando feriados semanais (sábados e domingos)
    # Criar campo 'is_weekend' com 0 e 1 - significando fim de semana
    # df1['is_weekend'] = (df1['ds'].dt.weekday >= 5).astype(int)
    # m.add_regressor('is_weekend')

    # Criando o dataframe para previsão futura
    # Certifique-se de que a data inicial seja igual à última data em df1
    data_inicial = df1['ds'].max()

    m.fit(df1)

    # Ajuste do período de previsão para que seja igual a df1
    future = m.make_future_dataframe(periods=0, freq='D')
    # future['is_weekend'] = (future['ds'].dt.weekday >= 5).astype(int)
    forecast = m.predict(future)

    # Conversão para arrays para uso em plotagem
    fcst_t = np.array(forecast['ds'].dt.to_pydatetime())
    history_ds = np.array(m.history['ds'].dt.to_pydatetime())

    # Criando o gráfico com Plotly
    fig = go.Figure()

    # Adicionando os dados do histórico
    fig.add_trace(go.Scatter(x=history_ds, y=m.history['y'], mode='markers', name='Histórico'))

    # Adicionando os dados da previsão
    fig.add_trace(go.Scatter(x=fcst_t, y=forecast['yhat'], mode='lines', name='Previsão'))

    # Adicionando a faixa de intervalo
    fig.add_trace(go.Scatter(
        x=np.concatenate([fcst_t, fcst_t[::-1]]),
        y=np.concatenate([forecast['yhat_lower'], forecast['yhat_upper'][::-1]]),
        fill='toself',
        fillcolor='rgba(255, 0, 0, 0.2)',
        line=dict(color='rgba(255, 255, 255, 0)'),
        name='Intervalo de Confiança'
    ))

    # Personalizando o layout do gráfico
    fig.update_layout(
        xaxis_title='Data',
        yaxis_title='Valores',
        title='Previsão com Prophet e Intervalo de Confiança'
    )

    # Exibindo o gráfico no Streamlit
    st.plotly_chart(fig)

    # Mostrando

    # Calculando métricas de desempenho
    # df_cv = performance_metrics(df)
    # st.write(df_cv)
    # este procedimento está dando erro

    from sklearn.metrics import mean_absolute_error, mean_squared_error

    # Verificar se os DataFrames têm o mesmo número de amostras
    # df e forecast são diferentes pois forecast foi levado em conta os feridos e fins de semana
    # Verificar duplicatas no DataFrame df1
    num_duplicatas_df1 = df1[df1.duplicated()].shape[0]
    st.write(f"Número de duplicatas em df1: {num_duplicatas_df1}")

    # Verificar duplicatas no DataFrame forecast
    #num_duplicatas_forecast = forecast[forecast.duplicated()].shape[0]
    #st.write(f"Número de duplicatas em forecast: {num_duplicatas_forecast}")
    #st.write("Tamanho dos shape")
    #a = df1.shape[0]
    #b = forecast.shape[0]
    #st.write(f"df1.shape[0]: {a}")
    #st.write(f"forecast.shape[0]: {b}")
    if df1.shape[0] == forecast.shape[0]:
        # Calcular métricas
        mae1 = mean_absolute_error(df1['y'], forecast['yhat'])
        mae_rounded1 = round(mae1, 2)
        mse1 = mean_squared_error(df1['y'], forecast['yhat'])
        mse_rounded1 = round(mse1, 2)
        rmse1 = np.sqrt(mse1)
        rmse_rounded1 = round(rmse1, 2)
        st.write(f"MAE: {mae_rounded1}")
        st.write(f"MSE: {mse_rounded1}")
        st.write(f"RMSE: {rmse_rounded1}")
    else:
        st.write("Os DataFrames não têm o mesmo número de amostras. Verifique os dados.")
    # Calculando as previsões do modelo para os dados de teste
    # Calculando novamente forecast para todos os dados, vai ser prossivel calcular as métricas
    # forecast = m.predict(df1)

    # Calculando o MAE entre as previsões e os valores reais
    # mae = mean_absolute_error(df1['y'], forecast['yhat'])
    #mae_rounded = round(mae, 2)

    #st.write(f'MAE: {mae_rounded}')
    #mse = mean_squared_error(df1['y'], forecast['yhat'])
    ##rmse = mean_squared_error(df1['y'], forecast['yhat'], squared=False)
    #rmse_rounded = round(rmse, 2)
    #st.write(f'MSE: {mse_rounded}')
    #st.write(f'RMSE: {rmse_rounded}')

    # Supondo que 'forecast' seja o resultado da previsão do Prophet
    # y_true é a série real do seu DataFrame, você pode usar df['y'] ou qualquer outra coluna correspondente
    y_true = df1['y']

    # Obtendo os valores previstos a partir do forecast
    y_pred = forecast['yhat']

    # Calculando o MAPE usando a função importada
    mape = mean_absolute_percentage_error(y_true, y_pred)
    mape = round(mape, 2)
    st.write(f"MAPE: {mape}")

    if data_selecionada is not None and hora_selecionada is not None:
        # Convert the selected date to the DataFrame's format
        data_formatada_interna = pd.to_datetime(data_selecionada).strftime('%Y-%m-%d')
        # Create a datetime combining the selected date with the default time
        data_hora_interna = pd.to_datetime(data_formatada_interna + ' ' + str(hora_selecionada))
        # Filter the DataFrame based on the selected date and time
        df_filtrado_interno = forecast[forecast['ds'] == data_hora_interna]
        st.dataframe(df_filtrado_interno)
    else:
        st.warning("Não há dados para a data selecionada.")
    return forecast
