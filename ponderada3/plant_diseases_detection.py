# -*- coding: utf-8 -*-
"""Plant-diseases-detection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10PafAMx9_IMwsR0NafdVQVYMdOjH-sOj
"""

#Visualização de Sistema de Processamento
!nvidia-smi

# Instalação das bibliotecas necessárias

# Instalação de Lib para YoloV8 
!pip install ultralytics

# Instalação da Lib - Roboflow, onde serão chamados os datasets de base
!pip install roboflow --quiet

# Importando as libs necessárias
 
from ultralytics import YOLO
from IPython.display import display, Image

# Importe para integração e aplicação do Sistema Operacional
import os

# Retorna o diretório de trabalho atual (current working directory), que é o diretório em que o script Python está sendo executado,e define a ele o valor da variável HOME 
HOME = os.getcwd()
print(HOME)

# Commented out IPython magic to ensure Python compatibility.
# Cria na HOME o arquivo em pasta que irá abrigar o "dataset" 
!mkdir {HOME}/dataset

# Acessa a pasta "dataset"
# %cd {HOME}/dataset



# Importa lib Roboflow
from roboflow import Roboflow

# Definição de chaves e propriedades de comunicação com o dataset do Roboflow (api_key, nome da área de trabalho e nome do projeto) 
rf = Roboflow(api_key="lXW0Eii94q1D4pndbud0")
project = rf.workspace("final-year-project-zorqg").project("plants-diseases-detection-model")
dataset = project.version(8).download("yolov8")

# Commented out IPython magic to ensure Python compatibility.
# Treinamento do modelo de aprendizado 

# %cd {HOME}

!yolo task=detect mode=train model=yolov8s.pt data={dataset.location}/data.yaml epochs=6 imgsz=800 plots=True

# Visualização dos Modelos Treinados
!ls {HOME}/runs/detect/train/

# Commented out IPython magic to ensure Python compatibility.
# Visualização da relação entre cada um dos datasets - Modelo, Treino e Predição
# %cd {HOME}
Image(filename=f'{HOME}/runs/detect/train/confusion_matrix.png', width=600)

# Commented out IPython magic to ensure Python compatibility.
# %cd {HOME}
Image(filename=f'{HOME}/runs/detect/train/results.png', width=600)

# Commented out IPython magic to ensure Python compatibility.
# %cd {HOME}
Image(filename=f'{HOME}/runs/detect/train/val_batch1_pred.jpg', width=600)

# Commented out IPython magic to ensure Python compatibility.
# %cd {HOME}

!yolo task=detect mode=val model={HOME}/runs/detect/train/weights/best.pt data={dataset.location}/data.yaml

# Commented out IPython magic to ensure Python compatibility.
# %cd {HOME}
!yolo task=detect mode=predict model={HOME}/runs/detect/train/weights/best.pt conf=0.25 source={dataset.location}/test/images save=True

"""# Detectando em Imagens Internas do Dataset"""

import glob
from IPython.display import Image, display

for image_path in glob.glob(f'{HOME}/runs/detect/predict/*.jpg')[:3]:
      display(Image(filename=image_path, width=600))
      print("\n")

"""# Detectando em Imagens Externas do Dataset"""

for image_path in glob.glob(f'{HOME}/runs/detect/predict/plantas-doencas.jpg'):
      display(Image(filename=image_path, width=600))
      print("\n")

for image_path in glob.glob(f'{HOME}/runs/detect/predict/planta-doente3.jpg'):
      display(Image(filename=image_path, width=600))
      print("\n")

for image_path in glob.glob(f'{HOME}/runs/detect/predict/planta-doente4.jpg'):
      display(Image(filename=image_path, width=600))
      print("\n")