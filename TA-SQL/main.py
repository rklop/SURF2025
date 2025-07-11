import sys
sys.path.append('/Users/rklop/text2sql model/TA-SQL/verieql')
sys.path.append('/Users/rklop/text2sql model/TA-SQL/verieql/z3py_libs')

from run import parser, main
from verieql.verieql import verify_sql_equivalence
from join_csv import join_csv_files
import json
import csv
from src.modules import TASL, TALOG
import tqdm
import traceback
import subprocess
from join_csv import join_csv_files

# I give it a .json path containing each question, a .json path containing the table definitions, and a .json path containing the constraints.
# It will then run the TA-SQL modes on each question, and then verify the SQL equivalence of the generated SQL and the gold SQL.
# It will then save the results to a .csv file.

if __name__ == '__main__':
    
    opt = parser()
    #output_dic = main(opt)

    output_dic = json.load(open('./outputs/temp_test.json'))

    csv_path = './outputs/verification_results.csv'
    csv_headers = ['bound_size', 'question_id', 'equivalent', 'counterexample', 'time_cost', 'generated_sql', 'gold_sql']

    print(f"Finished running TA-SQL" + "*"*100)
    
    cmd = [
        'python', 'evaluation/evaluation_ex.py',
        '--predicted_sql_path', './outputs/temp_test.json',
        '--ground_truth_path', './data/test_gold.sql',
        '--db_root_path', './temp_data/temp_databases/',
        '--diff_json_path', './data/mini_dev_sqlite.json',
        '--output_log_path', './data/output.log',
        '--sql_dialect', 'SQLite'
    ]

    result = subprocess.run(cmd, capture_output = True, text = True)

    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
        writer.writeheader()
        
        for question_idx in output_dic.keys():  

            print(f"Running veriEQL on question {question_idx}" + "*"*100)
            
            try:
                generated_sql = output_dic[question_idx]  
                gold_sql_path = './temp_data/temp_databases/' + opt.mode + '.json'

                with open(gold_sql_path, 'r') as f:
                    data = json.load(f)
                
                i = int(question_idx) 
                #print(f"I: {i}") 
                gold_sql = data[i]['SQL']
                gold_sql = gold_sql.upper()
                print(f"GOLD_SQL: {gold_sql}")

                question_id = data[i]['question_id']
                #print(f"QUESTION_ID: {question_id}")
                database_id = data[i]['db_id']
                #print(f"DATABASE_ID: {database_id}")

                stopper = '\t'
                generated_sql = generated_sql.split(stopper)[0]
                generated_sql = ' '.join(generated_sql.split())
                generated_sql = generated_sql.upper()
                print(f"GENERATED_SQL: {generated_sql}")

                schema_path = './temp_data/temp_databases/table_definitions.json'
                with open(schema_path, 'r') as f:
                    schema = json.load(f)

                tables_definitions = schema[str(database_id)]  
                #print(f"TABLES_DEFINITIONS: {tables_definitions}")
                
                constraints_path = './temp_data/temp_databases/constraints.json'
                with open(constraints_path, 'r') as f:
                    constraints = json.load(f)

                integrity_constraints = constraints[str(database_id)][0]
                #print(f"INTEGRITY_CONSTRAINTS: {integrity_constraints}")

                for bound_size in range(1, 4):

                    #print(f"Testing with bound_size = {bound_size}")

                    config = {'generate_code': True, 'timer': True, 'show_counterexample': True}
                    verification_result = verify_sql_equivalence(generated_sql, gold_sql, tables_definitions, bound_size, integrity_constraints, **config)
                
                    #print(f"VERIFICATION_RESULT for bound_size {bound_size}: {verification_result}")

                    csv_row = {
                        'bound_size': bound_size,
                        'question_id': question_id,
                        'equivalent': verification_result['equivalent'],
                        'counterexample': str(verification_result['counterexample']) if verification_result['counterexample'] else '',
                        'time_cost': verification_result['time_cost'] if verification_result['time_cost'] else '',
                        'generated_sql': generated_sql,
                        'gold_sql': gold_sql
                    }

                    writer.writerow(csv_row)
                    csvfile.flush() 
                    
                    print(f"Processed question {question_idx}: {question_id} with bound_size {bound_size}")
                
            except Exception as e:
                #print(f"Error processing question {question_idx}: {type(e).__name__}: {str(e)}")
                #print(f"Full traceback:")
                traceback.print_exc()

                # Write error row for all bound sizes
                for bound_size in range(1, 4):
                    csv_row = {
                        'bound_size': bound_size,
                        'question_id': question_id if 'question_id' in locals() else question_idx,
                        'equivalent': 'ERROR',
                        'counterexample': f"{type(e).__name__}: {str(e)}",
                        'time_cost': '',
                        'generated_sql': generated_sql if 'generated_sql' in locals() else '',
                        'gold_sql': gold_sql if 'gold_sql' in locals() else ''
                    }
                    writer.writerow(csv_row)
                    csvfile.flush()
    
    print(f"all results saved to {csv_path}")

    join_csv_files()

    print("Done!")





    

    

    
   
    
    