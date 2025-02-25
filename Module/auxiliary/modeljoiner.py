import numpy as np
import glob

def join_word2vec_parts():
    files = sorted(glob.glob("data/word2vec_part_*.npy"))  # Ensure correct order
    merged_data = np.concatenate([np.load(f) for f in files])

    np.save("data/word2vec_500k.model.vectors.npy", merged_data)
# files = sorted(glob.glob("data/word2vec_part_*.npy"))  # Ensure correct order
# merged_data = np.concatenate([np.load(f) for f in files])

# np.save("data/sword2vec_500k.model.vectors.npy", merged_data)