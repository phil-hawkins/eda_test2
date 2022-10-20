import snowflake.connector
from pandas import DataFrame
from np_exploration_python.vscode_settings import VSCodeSettings


def query_to_pandas(sql_query: str) -> DataFrame:
    config_dict = VSCodeSettings().get_snowflake_connection_config()
    ctx = snowflake.connector.connect(**config_dict)

    cs = ctx.cursor()
    try:
        cs.execute(sql_query)

        # Fetch the result set from the cursor and deliver it as the
        # Pandas DataFrame.
        df = cs.fetch_pandas_all()
    finally:
        cs.close()
    ctx.close()

    return df
