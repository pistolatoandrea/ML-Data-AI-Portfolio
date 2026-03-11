# src/inference.py
# Inference script — carica il modello fine-tunato e predice il sentiment di una frase

import sys
import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# ── Path del modello ──────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "distilbert-sst2-finetuned")

# ── Device ────────────────────────────────────────────────────────────────────
if torch.backends.mps.is_available():
    device = torch.device("mps")
elif torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")

# ── Caricamento modello e tokenizer (una volta sola) ──────────────────────────
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
model = model.to(device)
model.eval()

# ── Funzione di predizione ────────────────────────────────────────────────────
def predict(text: str) -> dict:
    """
    Predice il sentiment di una frase.

    Args:
        text: stringa di testo da classificare

    Returns:
        dict con chiavi: label (POSITIVE/NEGATIVE), confidence (float)
    """
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=128,
        padding=True
    )
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)

    probs = torch.softmax(outputs.logits, dim=-1)
    predicted_class = torch.argmax(probs, dim=-1).item()
    confidence = probs[0][predicted_class].item()

    label = "POSITIVE" if predicted_class == 1 else "NEGATIVE"

    return {"label": label, "confidence": round(confidence * 100, 2)}


# ── Esecuzione da terminale ───────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python src/inference.py \"testo da classificare\"")
        sys.exit(1)

    text = sys.argv[1]
    result = predict(text)

    print(f"\nInput:      {text}")
    print(f"Sentiment:  {result['label']}")
    print(f"Confidence: {result['confidence']}%\n")