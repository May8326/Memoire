import os
import re

# Les règles de remplacement (motif, remplacement, description)
rules = [
    (r'(\\mae)(\s)', r'\1~\2', r"\\mae suivi d'un espace"),
    (r'(\\minarm)(\s)', r'\1~\2', r"\\minarm suivi d'un espace"),
    (r'(\\maelong)(\s)', r'\1~\2', r"\\maelong suivi d'un espace"),
    (r'(\s):', r'~:', r'" :" remplacé par "~:"')
]

def find_occurrences(content, pattern):
    """Renvoie les 3 premières occurrences du motif dans le contenu, avec leur contexte."""
    return [m.group(0) for m in re.finditer(pattern, content)][:3]

def show_replacements(file_path, content, rules):
    print(f"\nFichier : {file_path}")
    for pattern, replacement, desc in rules:
        # Chercher les occurrences AVANT modif
        occurrences_before = find_occurrences(content, pattern)
        # Appliquer le remplacement pour affichage
        content_modif = re.sub(pattern, replacement, content)
        occurrences_after = find_occurrences(content_modif, pattern)  # utile pour certains patterns
        # Afficher les 3 exemples modifiés
        if occurrences_before:
            print(f"  Modif : {desc}")
            for i, occ in enumerate(occurrences_before):
                # Appliquer la modif sur cette occurrence
                occ_modif = re.sub(pattern, replacement, occ)
                print(f"    {i+1}. '{occ.strip()}' → '{occ_modif.strip()}'")
        else:
            print(f"  Modif : {desc} — aucune occurrence trouvée.")

def process_tex_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    show_replacements(filepath, content, rules)
    # Appliquer toutes les modifs
    for pattern, replacement, _ in rules:
        content = re.sub(pattern, replacement, content)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

def process_all_tex_files(root_dir):
    for foldername, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.tex'):
                process_tex_file(os.path.join(foldername, filename))

if __name__ == "__main__":
    dossier = "parties"  # à adapter selon ton arborescence
    process_all_tex_files(dossier)
