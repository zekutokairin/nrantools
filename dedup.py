
import os
import pandas as pd

NRAN_CONTENT_DIR = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\New Retro Arcade Neon\\NewRetroArcade\\Content"

if __name__ == "__main__":
    csv_path = os.path.join(NRAN_CONTENT_DIR, "cartridge_list.csv")
    df = pd.read_csv(csv_path)

    """
    df1 = pd.read(read_csv(original_csv))
    df2 = pd.read(read_csv(csv))
    df = pd.concat(df1, df2)
    """
    df = df.drop_duplicates(keep='first')

    df.to_csv('output.csv')
