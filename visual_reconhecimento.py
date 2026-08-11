import cv2

def desenhar_textos(frame, texto_exibido, cor_texto, acesso, tempo_ms):

    cv2.putText(
        frame,
        texto_exibido,
        (50, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        cor_texto,
        2
    )
    cv2.putText(
        frame,
        acesso,
        (50, 150),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.5,
        cor_texto,
        3
    )
    cv2.putText(
        frame,
        f"{tempo_ms:.1f} ms",
        (50, 220),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2
    )

    return frame