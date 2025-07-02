import sys
sys.path.append('/Users/rklop/text2sql model/TA-SQL/verieql')
sys.path.append('/Users/rklop/text2sql model/TA-SQL/verieql/z3py_libs')
from verieql.verieql import verify_sql_equivalence
import json


def test_verieql():
    sql1, sql2 = [
        "SELECT T2.CITY FROM FRPM AS T1 INNER JOIN SCHOOLS AS T2 ON T1.CDSCODE = T2.CDSCODE GROUP BY T2.CITY ORDER BY SUM(T1.ENROLLMENT_K12) ASC LIMIT 5",
        "SELECT T1.CITY FROM SCHOOLS AS T1 INNER JOIN SATSCORES AS T2 ON T1.CDSCODE = T2.CDS ORDER BY T2.ENROLL12 ASC LIMIT 5",
    ]

    print(f"SQL1: {sql1}")
    print(f"SQL2: {sql2}")

    schema_path = './temp_data/temp_databases/table_definitions.json'
    with open(schema_path, 'r') as f:
        table_defs = json.load(f)

        schema = table_defs["california_schools"] 

    print(f"SCHEMA: {schema}")

    constraints_path = './temp_data/temp_databases/constraints.json'
    with open(constraints_path, 'r') as f:
        integrity_constraints = json.load(f)

    constants = integrity_constraints["california_schools"][0]
    
    print(f"CONSTANTS: {constants}")

    bound_size = 2
    
    config = {'generate_code': True, 'timer': True, 'show_counterexample': True}
    return verify_sql_equivalence(sql1, sql2, schema, ROW_NUM=bound_size, constraints=constants, **config)


if __name__ == '__main__':
    print(test_verieql())