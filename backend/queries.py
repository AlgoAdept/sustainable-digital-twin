def get_filtered_relationships(conn, product=None):
    base_query = """
    MATCH (n)-[r]->(m)
    RETURN n.name AS from, TYPE(r) AS rel, m.name AS to
    """
    if product:
        base_query = f"""
        MATCH (p:Product {{name: '{product}'}})-[r]->(m)
        RETURN p.name AS from, TYPE(r) AS rel, m.name AS to
        UNION
        MATCH (n)-[r]->(p:Product {{name: '{product}'}})
        RETURN n.name AS from, TYPE(r) AS rel, p.name AS to
        """
    return conn.query(base_query)

def get_all_products(conn):
    query = "MATCH (p:Product) RETURN p.name AS product"
    return [record["product"] for record in conn.query(query)]

def get_relationships_with_labels(conn, product=None):
    if product:
        query = f"""
        MATCH (p:Product {{name: '{product}'}})-[r]->(m)
        RETURN p.name AS from, labels(p) AS from_labels,
               TYPE(r) AS rel,
               m.name AS to, labels(m) AS to_labels
        UNION
        MATCH (n)-[r]->(p:Product {{name: '{product}'}})
        RETURN n.name AS from, labels(n) AS from_labels,
               TYPE(r) AS rel,
               p.name AS to, labels(p) AS to_labels
        """
    else:
        query = """
        MATCH (n)-[r]->(m)
        RETURN n.name AS from, labels(n) AS from_labels,
               TYPE(r) AS rel,
               m.name AS to, labels(m) AS to_labels
        """
    return conn.query(query)

def get_nodes_with_carbon(conn):
    query = """
    MATCH (n)
    WHERE n.carbon_score IS NOT NULL
    RETURN n.name AS name, labels(n)[0] AS type, n.carbon_score AS carbon
    """
    return conn.query(query)

def get_donation_suggestions(conn):
    query = """
    MATCH (p:Product)<-[r:STOCKED_IN]-(s:Store), (n:NGO)
    WHERE r.inventory > 100 OR r.expiry_days < 3
    RETURN p.name AS product,
           s.name AS store,
           n.name AS suggested_ngo,
           r.inventory AS inventory,
           r.expiry_days AS expiry_days
    LIMIT 10
    """
    return conn.query(query)
