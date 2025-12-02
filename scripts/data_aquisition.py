def main():
    import pandas as pd
    def get_data(path):
        df = pd.read_csv(path)
        return df

    def save_data(df, path, name):
        full_path = f"{path}/{name}"
        df.to_csv(full_path, index=False)
        
if __name__ == "__main__":
    main()