# Programme d'extraction de dataset Hugging face écrit par intelligence artificielle#
# But : Sortir 100 fichiers textes et les mettre dans ./data

from datasets import load_dataset
import os


# Crée le dossier si pas existant
os.makedirs("data", exist_ok=True)

# Charge le dataset en streaming
ds = load_dataset("debasishraychawdhuri/wikipedia_clean_5GB", split="train", streaming=True)

# Variables de contrôle
target_docs = 1000  # Nombre de documents voulus
saved_count = 0
processed_count = 0
min_length = 500  # Longueur minimale en caractères

print(f"🔍 Recherche de {target_docs} documents Wikipedia avec au moins {min_length} caractères...")

# Itère et sauvegarde seulement les documents non-vides
for item in ds:
    processed_count += 1
    
    # Vérifie si le texte existe et n'est pas vide
    if 'text' in item and item['text'] and len(item['text'].strip()) >= min_length:
        filename = f"data/wiki_{saved_count}.txt"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(item['text'])
        
        # Affiche un aperçu du document sauvegardé
        preview = item['text'][:100].replace('\n', ' ')
        print(f"✅ Document {saved_count}: {len(item['text'])} chars - {preview}...")
        
        saved_count += 1
        
        # Arrête quand on a assez de documents
        if saved_count >= target_docs:
            break
    else:
        # Debug : affiche pourquoi le document est rejeté
        text_len = len(item.get('text', '').strip()) if item.get('text') else 0
        print(f"❌ Document {processed_count} rejeté: {text_len} chars (trop court)")

print(f"\n🎉 Terminé ! {saved_count} documents sauvegardés sur {processed_count} traités.")

# Vérification finale
print("\n📊 Résumé des fichiers créés:")
for i in range(saved_count):
    filename = f"data/wiki_{i}.txt"
    if os.path.exists(filename):
        size = os.path.getsize(filename)
        print(f"  - {filename}: {size} bytes")


