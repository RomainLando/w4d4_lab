from db.run_sql import run_sql
from models.biting import Biting
from repositories import zombie_repository, human_repository



def save(biting):
    sql = """
    INSERT INTO bitings (zombie_id, human_id) VALUES (%s, %s) 
    RETURNING id
    """
    values = [biting.zombie.id, biting.human.id]
    results = run_sql(sql, values)
    id = results[0]['id']
    biting.id = id

def select_all():
    bitings = []
    sql = "SELECT * FROM bitings"
    results = run_sql(sql)
    
    for result in results:
        human_id = result['human_id']
        zombie_id = result['zombie_id']
        human = human_repository.select(human_id)
        zombie = zombie_repository.select(zombie_id)
        biting = Biting(human, zombie, result['id'])
        bitings.append(biting)
    return bitings

def select(id):
    biting = None
    sql = """
    SELECT * FROM bitings
    WHERE id = %s
    """
    values = [id]
    results = run_sql(sql, values)

    if results:
        result = results[0]
        human_id = result['human_id']
        zombie_id = result['zombie_id']
        human = human_repository.select(human_id)
        zombie = zombie_repository.select(zombie_id)
        biting = Biting(human, zombie, result['id'])
    return biting

def delete_all():
    sql= "DELETE FROM bitings"
    run_sql(sql)

def delete(id):
    sql = """
    DELETE FROM bitings
    WHERE id = %s
    """
    values = [id]
    run_sql(sql, values)

def update(biting):
    sql = """
    UPDATE bitings SET (human_id, zombie_id) = (%s, %s) 
    WHERE id = %s
    """
    values = [biting.human.id, biting.zombie.id, biting.id]
    run_sql(sql, values)