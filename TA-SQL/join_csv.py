import csv
import pandas as pd

def join_csv_files():

    final_results = pd.read_csv('data/final_results.csv')
    verification_results = pd.read_csv('outputs/verification_results.csv')
    
    final_results['question_id'] = final_results['question_id'].astype(str)
    verification_results['question_id'] = verification_results['question_id'].astype(str)
    
    joined_df = pd.merge(verification_results, final_results, on='question_id', how='left')
    
    output_path = 'outputs/combined_results.csv'
    joined_df.to_csv(output_path, index = False)
    
    return joined_df

if __name__ == "__main__":
    join_csv_files() 