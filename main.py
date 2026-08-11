import cv2
from deepface import DeepFace
import sqlite3
import json
import numpy as np
from deepface.modules.verification import find_threshold
from datetime import datetime
from visual_reconhecimento import desenhar_textos
import time

webcam = cv2.VideoCapture(0)

conn = sqlite3.connect("banco.db")
cursor = conn.cursor()

cursor.execute("""SELECT id, nome, embedding FROM pessoas""")
pessoas = cursor.fetchall()

pessoas_carregadas = {}

for pessoa in pessoas:
    pessoas_carregadas[pessoa[0]] = {
    "nome": pessoa[1],
    "embedding": json.loads(pessoa[2])
    }

conn.close()

texto_exibido = "aguardando..."
cor_texto = (255, 255, 255)
acesso = "aguardando"
contador = 0
tempo_ms = 0
while True:

    verificador, frame = webcam.read()

    frame = desenhar_textos(frame, texto_exibido, cor_texto, acesso, tempo_ms)

    contador += 1
    if contador % 10 == 0:
        inicio = time.perf_counter()
        embedding = DeepFace.represent(
            img_path=frame,
            model_name="Facenet",
            detector_backend="retinaface",
            enforce_detection=False
        )
        vetor = np.array(embedding[0]["embedding"])

        distancia = []

        for id_pessoa, dados_pessoa in pessoas_carregadas.items():
            embedding_salvo = np.array(dados_pessoa["embedding"])
            dist = np.linalg.norm(embedding_salvo - vetor)
            distancia.append((id_pessoa, dist))

        threshold = find_threshold("Facenet", "euclidean")

        menor = min(distancia, key=lambda x: x[1])
        fim = time.perf_counter()
        tempo_ms = (fim - inicio) * 1000

        if menor[1] <= threshold:
            resultado = "reconhecido"
            acesso = "Acesso liberado"
            cor_texto = (0, 255, 0)
            texto_exibido = pessoas_carregadas[menor[0]]["nome"]

            nome_arquivo = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            nome_pessoa = pessoas_carregadas[menor[0]]['nome']
            caminho_foto = f"reconhecido_{nome_pessoa}_{nome_arquivo}.png"
            cv2.imwrite(caminho_foto, frame)
            
            conn = sqlite3.connect("banco.db")
            cursor = conn.cursor()

            cursor.execute("""INSERT INTO acessos
            (pessoa_id, resultado, foto_path)
            VALUES(?, ?, ?)""",(menor[0], resultado, caminho_foto))
            
            conn.commit()
            conn.close()
        else:
            texto_exibido = "desconhecida"
            acesso = "Acesso negado"
            cor_texto = (0, 0, 255)
            nome = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            caminho_foto = f"desconhecido_{nome}.png"
            cv2.imwrite(caminho_foto, frame)

            resultado = "desconhecido"
            conn = sqlite3.connect("banco.db")
            cursor = conn.cursor()

            cursor.execute("""INSERT INTO acessos
            (resultado, foto_path)
            VALUES(?, ?)""",(resultado, caminho_foto))

            conn.commit()
            conn.close()

    if not verificador:
        break
    
    cv2.imshow("rosto na webcam", frame)
    
    if cv2.waitKey(5) == 113:
        break

webcam.release()
cv2.destroyAllWindows()
