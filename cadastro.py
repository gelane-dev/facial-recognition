import cv2
from deepface import DeepFace
import json
import sqlite3

nome = input("digite seu nome: ")

webcam = cv2.VideoCapture(0)


while True:

    verificador, frame = webcam.read()
    if not verificador:
        break

    cv2.imshow("rosto na webcam", frame)
    
    if cv2.waitKey(5) == 113:
        cv2.imwrite("foto.png", frame)
        print("foto salva!")
        break

webcam.release()
cv2.destroyAllWindows()

embedding = DeepFace.represent(
        img_path="foto.png",
        model_name="Facenet",
        detector_backend="retinaface",
        enforce_detection=False
    )

vetor = embedding[0]["embedding"]
embedding_json = json.dumps(vetor)

conn = sqlite3.connect("banco.db")
cursor = conn.cursor()

cursor.execute("""INSERT INTO pessoas
    (nome, embedding) VALUES (?, ?)""", (nome, embedding_json))

conn.commit()
conn.close()