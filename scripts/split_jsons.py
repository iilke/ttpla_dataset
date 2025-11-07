# Windows-safe rewrite of original split_jsons.py
import os
import argparse
import shutil

# Keep original folder names
output_folder = 'splitting_jsons'
train_folder  = os.path.join(output_folder, 'train_jsons')
val_folder    = os.path.join(output_folder, 'val_jsons')
test_folder   = os.path.join(output_folder, 'test_jsons')

ap = argparse.ArgumentParser()
ap.add_argument('-t', '--path_annotation_jsons', required=True, help='path to jsons annotations (e.g., .\\newjsons)')
args = ap.parse_args()

src_dir = os.path.abspath(args.path_annotation_jsons)
jsons_names = [js for js in os.listdir(src_dir) if js.endswith(".json")]

# --- Helpers ---
def load_list(txt_path):
    # Read list and normalize to base names without extension
    with open(txt_path, 'r', encoding='utf-8') as f:
        items = [ln.strip() for ln in f if ln.strip()]
    bases = []
    for it in items:
        b = it
        for ext in ('.json', '.jpg', '.jpeg', '.png'):
            if b.lower().endswith(ext):
                b = b[: -len(ext)]
                break
        bases.append(b)
    return set(bases)

def base_no_ext(filename):
    # Return filename base without extension
    b = filename
    if b.lower().endswith('.json'):
        b = b[:-5]
    return b

# --- Load splits (expected in current working directory) ---
train_set = load_list('train.txt')
val_set   = load_list('val.txt')
test_set  = load_list('test.txt')

# --- Ensure output dirs exist ---
for p in (output_folder, train_folder, val_folder, test_folder):
    os.makedirs(p, exist_ok=True)

# --- Split copy (use shutil instead of 'cp') ---
count_train = count_val = count_test = 0
for js in jsons_names:
    base = base_no_ext(js)
    src  = os.path.join(src_dir, js)
    if base in train_set:
        shutil.copy2(src, os.path.join(train_folder, js))
        count_train += 1
    elif base in val_set:
        shutil.copy2(src, os.path.join(val_folder, js))
        count_val += 1
    elif base in test_set:
        shutil.copy2(src, os.path.join(test_folder, js))
        count_test += 1

print("train:", count_train, "val:", count_val, "test:", count_test)
