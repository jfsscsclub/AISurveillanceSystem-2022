import cv2
from time import time, strftime

from predict import load_model, predict_image, annotate_image
from mailer import notifyUserWithAttachment

fps = 0

lastDetection = 0

if __name__ == "__main__":
    # Load the model
    model = load_model()

    cap = cv2.VideoCapture("rtsp://aritro:rattlesnak@192.168.2.233/live")

    while cap.isOpened():
        ret, frame = cap.read()

        if ret:
            startTime = time()

            # Predict on image
            preds = predict_image(frame, model)
            im_annotated = annotate_image(frame, preds)

            # Calculate FPS
            fps = 1 / (time() - startTime)

            # Display FPS
            cv2.putText(im_annotated, f"FPS: {fps}", (25, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            # Display the resulting frame
            cv2.imshow("Camera", im_annotated)

            # People predictions
            peoplePreds = [pred for pred in preds if pred['label'] == "car" and pred['score'] > 0.5]

            if len(peoplePreds) > 0:
                if time() - lastDetection > 60 * 3:
                    formattedTimestamp = strftime("%Y%m%d-%H%M%S")
                    cv2.imwrite(f"{formattedTimestamp}.jpg", im_annotated)

                    notifyUserWithAttachment("sahaaritro21@gmail.com", formattedTimestamp)

                    lastDetection = time()

            # Press Q on keyboard to exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

cap.release()
cv2.destroyAllWindows()
