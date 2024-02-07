import cv2


def drawBoxes(img, boxes, names):
    for b in boxes:
        c = b.xywh[0].tolist()
        x, y, w, h = int(c[0]), int(c[1]), int(c[2]) // 2, int(c[3]) // 2
        vertices = [(x - w, y + h), (x + w, y + h), (x + w, y - h), (x - w, y - h)]
        for i in range(len(vertices) - 1):
            img = cv2.line(img, vertices[i], vertices[i+1], (255, 0, 0), 8)
        img = cv2.line(img, vertices[0], vertices[len(vertices) - 1], (255, 0, 0), 8)

        cv2.putText(img, names[int(b.cls)], vertices[0], cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))
    cv2.imshow('cam', img)