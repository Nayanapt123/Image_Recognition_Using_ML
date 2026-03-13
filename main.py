import cv2
import os
import numpy as np

dataset_path = "dataset"

# Create dataset folder if not exists
if not os.path.exists(dataset_path):
    os.makedirs(dataset_path)

def capture_images():
    name = input("Enter name of the student: ")
    path = os.path.join(dataset_path, name)

    if not os.path.exists(path):
        os.makedirs(path)

    cap = cv2.VideoCapture(0)
    count = 0

    print("Press 'y' to save image, 'N' to quit")

    while True:
        ret, frame = cap.read()
        cv2.imshow("Capture", frame)

        key = cv2.waitKey(1)

        if key == ord('y'):
            img_path = os.path.join(path, f"{count}.jpg")
            cv2.imwrite(img_path, frame)
            print("Image saved")
            count += 1

        elif key == ord('N'):
            break

    cap.release()
    cv2.destroyAllWindows()


def recognise_student():
    cap = cv2.VideoCapture(0)

    print("Type N to quit")

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        best_match = "Unknown"
        min_diff = float('inf')

        for person in os.listdir(dataset_path):
            person_folder = os.path.join(dataset_path, person)

            for img_name in os.listdir(person_folder):
                img_path = os.path.join(person_folder, img_name)
                saved_img = cv2.imread(img_path)
                saved_gray = cv2.cvtColor(saved_img, cv2.COLOR_BGR2GRAY)

                saved_gray = cv2.resize(saved_gray, (200, 200))
                test_img = cv2.resize(gray, (200, 200))

                diff = np.sum(cv2.absdiff(saved_gray, test_img))

                if diff < min_diff:
                    min_diff = diff
                    best_match = person

        cv2.putText(frame, best_match, (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 255, 0), 2)

        cv2.imshow("Recognition", frame)

        if cv2.waitKey(1) == ord('N'):
            break

    cap.release()
    cv2.destroyAllWindows()


while True:
    print("\n1. Capture Image")
    print("2. Recognise Image")
    print("3. Exit")

    choice = input("Enter choice: ")

    if choice == '1':
        capture_images()
    elif choice == '2':
        recognise_student()
    elif choice == '3':
        break
    else:
        print("Invalid choice")