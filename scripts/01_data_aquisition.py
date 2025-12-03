def main():
    """
    Defines functions for reading and saving CSV data files.
    
    Contains get_data() to read CSV files into DataFrames and 
    save_data() to write DataFrames to CSV files.
    """
    import pandas as pd
    def get_data(path):
        df = pd.read_csv(path)
        return df

    def save_data(df, path, name):
        full_path = f"{path}/{name}"
        df.to_csv(full_path, index=False)
        
if __name__ == "__main__":
    main()