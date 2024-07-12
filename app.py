import cv2
import numpy as np
import streamlit as st
from keras.models import model_from_json

# Load sign language recognition model
json_file = open("C:\\Users\\91701\\Desktop\\YAM\\signlanguagedetectionmodel48x48.json", "r")
model_json = json_file.read()
json_file.close()
model = model_from_json(model_json)
model.load_weights("C:\\Users\\91701\\Desktop\\YAM\signlanguagedetectionmodel48x48.h5")

# Define sign labels
label = ['Happy', 'Help', 'Goodluck', 'Sad', 'T','Hello']

def extract_features(image):
    feature = np.array(image)
    feature = feature.reshape(1, 48, 48, 1)
    return feature / 255.0

def detect_sign(frame):
    cv2.rectangle(frame, (0, 40), (300, 300), (0, 165, 255), 1)
    cropframe = frame[40:300, 0:300]
    cropframe = cv2.cvtColor(cropframe, cv2.COLOR_BGR2GRAY)
    cropframe = cv2.resize(cropframe, (48, 48))
    cropframe = extract_features(cropframe)
    pred = model.predict(cropframe)
    prediction_label = label[pred.argmax()]

    return prediction_label

def main():

    # Title
    st.title('Sign Language Recognition App')

    # Center the "Check Your Sign" checkbox
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        use_webcam = st.checkbox('Check Your Sign', value=False, key='checkbox')

    st.markdown('## Output')
    stframe = st.empty()
    detected_sign = st.empty()

    if use_webcam:
        # Start webcam
        vid = cv2.VideoCapture(0)
        while vid.isOpened():
            ret, frame = vid.read()

            if not ret:
                break

            sign_label = detect_sign(frame)

            # Display detected sign
            detected_sign.markdown(f'The detected sign is <span class="highlight">{sign_label}</span>.', unsafe_allow_html=True)

            # Display webcam frame
            stframe.image(frame, channels="BGR", use_column_width=True)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        vid.release()
        cv2.destroyAllWindows()

        st.success('Video is Processed')
    else:
        st.write('Click "Check Your Sign" to activate the webcam.')

if __name__ == '__main__':
    main()
