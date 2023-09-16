from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL = tf.keras.models.load_model("models/13")

# Define the expected input shape for the model
INPUT_SHAPE = (256, 256, 3)
CLASS_NAMES = ["Early Blight", "Late Blight", "Healthy"]

# Dictionary to store disease information
disease_info = {
    "Early Blight": {
        "description": "Early blight is a common fungal disease in potato plants, causing brown, target-like spots on leaves. It's caused by Alternaria solani and can reduce yields. Management involves removing infected leaves, using fungicides, and practicing crop rotation.",

        "symptoms": "Early blight in potato plants is characterized by dark brown to black spots with concentric rings on leaves. These spots enlarge and may cause yellowing, leading to leaf withering. This fungal disease can harm potato yield if not managed promptly.",

        "causes": "Early blight, caused by the fungus Alternaria solani, is a common and damaging disease affecting potato plants. It appears as dark concentric ring-shaped lesions on the leaves. This fungal disease thrives in warm and humid conditions and can rapidly spread, leading to reduced crop yields if not managed properly. Control measures include crop rotation, fungicides, and the removal of infected leaves.",

        "treatments": "Early blight on potato plant leaves, caused by the fungus Alternaria solani, results in brown spots with concentric rings. To treat it, promptly remove infected leaves, apply fungicides as needed, maintain proper plant spacing, ventilation, and soil moisture levels to prevent its spread and ensure healthy plant growth.",
    },
    "Late Blight": {
        "description": "Late blight is caused by the fungal-like oomycete pathogen Phytophthora infestans. The primary host is potato, but P. infestans also can infect other solanaceous plants, including tomatoes, petunias and hairy nightshade. These infected species can act as source of inoculum to potato.",

        "symptoms": "Late blight is a devastating disease that affects potato plants. Symptoms include dark green to black spots on leaves, a fuzzy white to gray growth on the underside of leaves, rapid lesion spread, leaf yellowing and curling, stem and tuber infection, and rapid plant decline. Early detection and treatment with fungicides are crucial for managing this disease and protecting potato crops.",

        "causes": "Late blight is a destructive disease affecting potato plants, caused by the water mold Phytophthora infestans. It thrives in cool, wet conditions and spreads via airborne spores. Symptoms include dark lesions on leaves, white fungal growth, leaf curling, and wilting. Tubers can also be infected, leading to rotting. Late blight progresses rapidly and can result in significant crop losses. Management involves fungicides, crop rotation, and monitoring for early detection and treatment.",

        "treatments": "Late blight is a destructive fungal disease that affects potato plants. To manage late blight, apply fungicides promptly, such as copper-based or chlorothalonil products, as they can help control the disease's spread. Additionally, avoid overhead irrigation and opt for drip or soaker hoses to keep foliage dry, minimizing favorable conditions for late blight. Proper spacing between plants can also reduce the risk of infection. Early detection and rapid treatment are crucial to protect your potato crop from the devastating effects of late blight.",
    },
    "Healthy": {
        "description": "The plant appears to be healthy...",
        "symptoms": "No visible symptoms...",
        "causes": "No known causes...",
        "treatments": "No treatment required...",
    },
}


@app.get("/ping")
async def ping():
    return "Hello, I am alive"


def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image = read_file_as_image(await file.read())

    # Resize the image to the expected input shape
    image = tf.image.resize(image, INPUT_SHAPE[:2])
    img_batch = np.expand_dims(image, 0)

    predictions = MODEL.predict(img_batch)

    predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
    confidence = float(np.max(predictions[0]))

    # Get disease information based on the detected class
    disease_information = disease_info.get(predicted_class, {})

    return {
        'class': predicted_class,
        'confidence': confidence,
        **disease_information,  # Include disease information in the response
    }

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)
