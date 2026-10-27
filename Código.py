import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests

#CLASSES: abrir link via requests
class Linksbusca:
  def __init__(self, url):
    self.url = url
  def buscardados2(self):
    try:
      resposta = requests.get(self.url)
      resposta.raise_for_status()
      return resposta.json()
    except requests.exceptions.RequestException as erro:
      print(f"Erro na requisição: {erro}")
    return None

#CLASSES: tratamento inicial
class Tratamento:
  def __init__(self, Dados):
    self.Dados = Dados
    self.Datas = []
    self.TemperaturaMax = []
    self.TemperaturaMin = []
    self.TemperaturaMedia = []
    self.Temperatura = []

  def processo(self):
    self.Datas = [hora for hora in self.Dados["hourly"]["time"]]
    self.Temperatura = [
        temp for temp in self.Dados["hourly"]["temperature_2m"]
    ]
    return self.Datas, self.Temperatura

  def Estatistica(temp):
    TemperaturaMax = max(temp)
    TemperaturaMin = min(temp)
    TemperaturaMedia = sum(temp) / len(temp)
    return TemperaturaMax, TemperaturaMin, TemperaturaMedia

#CLASSES: finalização com matplotlib
class Plottst:
  def __init__(self, datas, temperatura, estatisticas):
    # Convertendo as datas para o formato datetime do pandas para facilitar o eixo X
    self.datas = pd.to_datetime(datas)
    self.temperatura = temperatura
    self.max_temp, self.min_temp, self.media_temp = estatisticas

  def plotar(self):
    # Criando uma figura com 2 subplots (o principal maior e o de estatísticas menor)
    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(12, 8), gridspec_kw={"height_ratios": [3, 1]}
    )

    #Evolução tempo
    ax1.plot(
        self.datas,
        self.temperatura,
        color="#ff7f0e",
        linewidth=1.2,
        label="Temperatura (°C)",
    )
    ax1.set_title(
        "Evolução da Temperatura ao Longo do Tempo",
        fontsize=14,
        fontweight="bold",
    )
    ax1.set_ylabel("Temperatura (°C)", fontsize=11)
    ax1.grid(True, linestyle="--", alpha=0.6)
    ax1.legend(loc="upper left")

    #Estatísticas (Máxima, Mínima e Média)
    labels = ["Máxima", "Mínima", "Média"]
    valores = [self.max_temp, self.min_temp, self.media_temp]
    cores = ["#d62728", "#1f77b4", "#2ca02c"]

    bars = ax2.bar(labels, valores, color=cores, width=0.4)
    ax2.set_title("Resumo Estatístico", fontsize=12, fontweight="bold")
    ax2.set_ylabel("°C", fontsize=11)
    ax2.grid(axis="y", linestyle="--", alpha=0.6)
    for bar in bars:
      height = bar.get_height()
      ax2.annotate(
          f"{height:.2f}°C",
          xy=(bar.get_x() + bar.get_width() / 2, height),
          xytext=(0, 4),  # Deslocamento vertical de 4 pontos
          textcoords="offset points",
          ha="center",
          va="bottom",
          fontsize=10,
          fontweight="bold",
      )

    plt.tight_layout()
    plt.show()


#Executivo
url = "https://archive-api.open-meteo.com/v1/era5?latitude=-15.793889&longitude=-47.882778&start_date=2026-09-01&end_date=2026-09-30&hourly=temperature_2m"
resultado = Linksbusca(url)
resposta = resultado.buscardados2()
if resposta:
  op = Tratamento(resposta)
  resultado2 = op.processo()
  resultado3 = Tratamento.Estatistica(resultado2[1])
  graficos = Plottst(resultado2[0], resultado2[1], resultado3)
  graficos.plotar()
else:
  print("Não foi possível obter os dados da API.")
