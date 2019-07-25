import boto3
from decimal import Decimal
from boto3.dynamodb.conditions import Key, Attr

    

#Update
def updateTable(event,context):
    dyDB = boto3.resource('dynamodb')
    table = dyDB.Table('Hoang-table')
    table.update_item(
        Key={
            'MSV': 'B15DCCN236'
        },
        UpdateExpression='SET Score = :val1',
        ExpressionAttributeValues={
            ':val1': Decimal('3.63')
        }
    )
    print("Update Complete")


def handler(event, context):
    action = event["action"]
    dyDB = boto3.resource('dynamodb')
    if action == "createTable":
        name = event["name"]
        partition = event["pa-key"]
        if event.get("so-key")!=None:
            soft = event["so-key"]
            table = dyDB.create_table(
                TableName = name,
                KeySchema=[
                    {
                        'AttributeName': partition,
                        'KeyType': 'HASH'
                    },
                    {   
                        'AttributeName': soft,
                        'KeyType': 'RANGE'
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': partition,
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': soft,
                        'AttributeType': 'S'
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits' : 5,
                    'WriteCapacityUnits' : 5
                }      
            )
        else:
            table = dyDB.create_table(
                TableName = name,
                KeySchema=[
                    {
                        'AttributeName': partition,
                        'KeyType': 'HASH'
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': partition,
                        'AttributeType': 'S'
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits' : 5,
                    'WriteCapacityUnits' : 5
                }      
            )
        table.meta.client.get_waiter('table_exists').wait(TableName=name)
        print("Create Complete")
    elif action == 'deleteTable':
        name = event['name']
        table = dyDB.Table(name)
        table.delete()
        table.meta.client.get_waiter('table_not_exists').wait(TableName=name)
        print("Delete Complete")
    elif action == 'insertTable':
        table = dyDB.Table(event['name'])
        try:
            table.put_item(
                Item = event['item'],
                Expected={
                    "MSV": { "Exists": False } 
                }
            )
            print("Insert Complete")
        except:
            return "Not complete"
    elif action == 'getTable':
        table = dyDB.Table(event['name'])
        response = table.get_item(
            Key = event['key']
        )
        try:
            item = response['Item']
            print(item)
            return item
        except KeyError:
            print('No item found')
            return 'No item found'
    elif action == 'querryTable':
        table = dyDB.Table(event['name'])
        response = table.scan()
        items = response['Items']
        print(items)
        return items
    elif action == 'deleteitem':
        table = dyDB.Table(event['name'])
        table.delete_item(
            Key= event['key']
        )
    elif action == 'querryItem':
        table = dyDB.Table(event['name'])
        response = table.scan(
            FilterExpression=Attr(event['key']).eq(event['value'])
        )
        items = response['Items']
        return items