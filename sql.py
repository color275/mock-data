connection_check_sql=\
"""
SELECT 'DB Connected'
FROM DUAL
"""


table_list_sql =\
"""
select column_name,
       data_type,
       data_length,
       data_precision,
       data_scale
from all_tab_columns 
where owner = '{owner}'
  and table_name = '{table_name}' 
"""

insert_sql =\
"""
INSERT INTO {owner}.{table_name} ( {insert_column} )
values
(
{insert_value}
)"""


check_start_id =\
"""
select nvl(max(id),0) id
from {owner}.{table_name}
"""