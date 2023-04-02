import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from awsglue import DynamicFrame
from pyspark.sql import functions as SqlFuncs


def sparkSqlQuery(glueContext, query, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)


args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node S3 bucket
S3bucket_node1 = glueContext.create_dynamic_frame.from_options(
    format_options={
        "quoteChar": '"',
        "withHeader": True,
        "separator": ",",
        "optimizePerformance": False,
    },
    connection_type="s3",
    format="csv",
    connection_options={"paths": ["s3://bmi6016/lab_result.csv"], "recurse": True},
    transformation_ctx="S3bucket_node1",
)

# Script generated for node Drop Duplicates
DropDuplicates_node1680466364543 = DynamicFrame.fromDF(
    S3bucket_node1.toDF().dropDuplicates(),
    glueContext,
    "DropDuplicates_node1680466364543",
)

# Script generated for node Drop Fields
DropFields_node1680467245466 = DropFields.apply(
    frame=DropDuplicates_node1680466364543,
    paths=["derived_by_TriNetX", "lab_result_text_val"],
    transformation_ctx="DropFields_node1680467245466",
)

# Script generated for node SQL Query
SqlQuery42 = """
select * from myDataSource WHERE code_system = 'LOINC';


"""
SQLQuery_node1680467531285 = sparkSqlQuery(
    glueContext,
    query=SqlQuery42,
    mapping={"myDataSource": DropFields_node1680467245466},
    transformation_ctx="SQLQuery_node1680467531285",
)

# Script generated for node Spigot
Spigot_node1680468920116 = Spigot.apply(
    frame=DropFields_node1680467245466,
    path="s3://bmi6016",
    options={"topk": 100, "prob": 1.0},
    transformation_ctx="Spigot_node1680468920116",
)

# Script generated for node SQL Query
SqlQuery44 = """
select * from myDataSource WHERE lab_result_num_val IS NOT NULL;

"""
SQLQuery_node1680468119539 = sparkSqlQuery(
    glueContext,
    query=SqlQuery44,
    mapping={"myDataSource": SQLQuery_node1680467531285},
    transformation_ctx="SQLQuery_node1680468119539",
)

# Script generated for node Spigot
Spigot_node1680468902043 = Spigot.apply(
    frame=SQLQuery_node1680467531285,
    path="s3://bmi6016",
    options={"topk": 100, "prob": 1.0},
    transformation_ctx="Spigot_node1680468902043",
)

# Script generated for node SQL Query
SqlQuery43 = """
select * from myDataSource WHERE date >= '20170101';

"""
SQLQuery_node1680468204016 = sparkSqlQuery(
    glueContext,
    query=SqlQuery43,
    mapping={"myDataSource": SQLQuery_node1680468119539},
    transformation_ctx="SQLQuery_node1680468204016",
)

# Script generated for node Spigot
Spigot_node1680468885623 = Spigot.apply(
    frame=SQLQuery_node1680468119539,
    path="s3://bmi6016",
    options={"topk": 100, "prob": 1.0},
    transformation_ctx="Spigot_node1680468885623",
)

# Script generated for node Spigot
Spigot_node1680468869270 = Spigot.apply(
    frame=SQLQuery_node1680468204016,
    path="s3://bmi6016",
    options={"topk": 100, "prob": 1.0},
    transformation_ctx="Spigot_node1680468869270",
)

# Script generated for node Drop Fields
DropFields_node1680468319133 = DropFields.apply(
    frame=SQLQuery_node1680468204016,
    paths=["code_system"],
    transformation_ctx="DropFields_node1680468319133",
)

# Script generated for node Spigot
Spigot_node1680468842998 = Spigot.apply(
    frame=DropFields_node1680468319133,
    path="s3://bmi6016",
    options={"topk": 100, "prob": 1.0},
    transformation_ctx="Spigot_node1680468842998",
)

# Script generated for node Amazon S3
AmazonS3_node1680468584069 = glueContext.write_dynamic_frame.from_options(
    frame=DropFields_node1680468319133,
    connection_type="s3",
    format="csv",
    connection_options={
        "path": "s3://bmi6016",
        "compression": "gzip",
        "partitionKeys": [],
    },
    transformation_ctx="AmazonS3_node1680468584069",
)

job.commit()
