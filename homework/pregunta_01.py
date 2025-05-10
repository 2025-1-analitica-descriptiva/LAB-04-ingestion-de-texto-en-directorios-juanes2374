# pylint: disable=import-outside-toplevel
# pylint: disable=line-too-long
# flake8: noqa
"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

import os
import zipfile
import tempfile
import pandas as pd


def pregunta_01():
    """
    La información requerida para este laboratio esta almacenada en el
    archivo "files/input.zip" ubicado en la carpeta raíz.
    Descomprima este archivo.

    Como resultado se creara la carpeta "input" en la raiz del
    repositorio, la cual contiene la siguiente estructura de archivos:

    ```
    train/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    test/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    ```

    A partir de esta informacion escriba el código que permita generar
    dos archivos llamados "train_dataset.csv" y "test_dataset.csv". Estos
    archivos deben estar ubicados en la carpeta "output" ubicada en la raiz
    del repositorio.

    Estos archivos deben tener la siguiente estructura:

    * phrase: Texto de la frase. hay una frase por cada archivo de texto.
    * sentiment: Sentimiento de la frase. Puede ser "positive", "negative"
      o "neutral". Este corresponde al nombre del directorio donde se
      encuentra ubicado el archivo.

    Cada archivo tendria una estructura similar a la siguiente:

    ```
    |    | phrase                                                                                                                                                                 | target   |
    |---:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------|
    |  0 | Cardona slowed her vehicle , turned around and returned to the intersection , where she called 911                                                                     | neutral  |
    |  1 | Market data and analytics are derived from primary and secondary research                                                                                              | neutral  |
    |  2 | Exel is headquartered in Mantyharju in Finland                                                                                                                         | neutral  |
    |  3 | Both operating profit and net sales for the three-month period increased , respectively from EUR16 .0 m and EUR139m , as compared to the corresponding quarter in 2006 | positive |
    |  4 | Tampere Science Parks is a Finnish company that owns , leases and builds office properties and it specialises in facilities for technology-oriented businesses         | neutral  |
    ```
    """
    # Crear carpeta de salida si no existe
    out_dir = os.path.join("files", "output")
    os.makedirs(out_dir, exist_ok=True)

    # Extraer archivo input.zip a un directorio temporal
    zip_path = os.path.join("files", "input.zip")
    tmp_dir = tempfile.mkdtemp()
    with zipfile.ZipFile(zip_path, 'r') as zf:
        zf.extractall(tmp_dir)

    # Determinar directorio base extraído
    root_items = os.listdir(tmp_dir)
    if 'train' in root_items and 'test' in root_items:
        base_dir = tmp_dir
    elif 'input' in root_items and os.path.isdir(os.path.join(tmp_dir, 'input')):
        base_dir = os.path.join(tmp_dir, 'input')
    else:
        base_dir = tmp_dir

    def collect_dataset(split):
        records = []
        split_dir = os.path.join(base_dir, split)
        # recorrer cada sentimiento
        for sentiment in ['negative', 'positive', 'neutral']:
            sentiment_dir = os.path.join(split_dir, sentiment)
            if not os.path.isdir(sentiment_dir):
                continue
            for filename in os.listdir(sentiment_dir):
                if filename.lower().endswith('.txt'):
                    file_path = os.path.join(sentiment_dir, filename)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text = f.read().strip()
                    records.append({'phrase': text, 'target': sentiment})
        return pd.DataFrame(records)

    # Generar datasets
    train_df = collect_dataset('train')
    test_df = collect_dataset('test')

    # Guardar CSVs
    train_df.to_csv(os.path.join(out_dir, 'train_dataset.csv'), index=False)
    test_df.to_csv(os.path.join(out_dir, 'test_dataset.csv'), index=False)
