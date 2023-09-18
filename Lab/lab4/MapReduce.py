from pyspark import SparkContext, SparkConf

conf = SparkConf().setAppName("DistributedSort")
sc = SparkContext(conf=conf)

records = [
    ("fruit", "apple", 30),
    ("fruit", "banana", 20),
    ("fruit", "orange", 15),
    ("fruit", "grape", 25),
    ("fruit", "melon", 10),
    ("vegetable", "carrot", 5),
    ("vegetable", "broccoli", 8),
    ("vegetable", "tomato", 12),
    ("vegetable", "cabbage", 7),
    ("meat", "chicken", 50),
    ("meat", "beef", 70),
    ("meat", "pork", 45),
]

rdd = sc.parallelize(records)


# First MapReduce step: Group by category
def group_func(record):
    category = record[0]
    name = record[1]
    price = record[2]
    return (category, [(name, price)])


def reduce_func(pair1, pair2):
    return pair1 + pair2


grouped_rdd = rdd.map(group_func).reduceByKey(reduce_func)


# Second MapReduce step: Sort records within each category
def sort_func(pair):
    category = pair[0]
    items = pair[1]
    # Sort by price (third element)
    sorted_items = sorted(items, key=lambda x: x[1])
    return (category, sorted_items)


sorted_rdd = grouped_rdd.map(sort_func)


# Collect the results
sorted_records = sorted_rdd.collect()


# Print the results
for record in sorted_records:
    category = record[0]
    print("Category:", category)
    for item in record[1]:
        name, price = item
        print("  Name:", name, "Price:", price)
