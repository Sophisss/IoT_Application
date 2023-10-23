/**
 * This model represents a table. 
 * Each table consists of an id, a name, 
 * partition key and sort key.
 */
export class Table {

    id : Number

    name: String

    partition_key: String | undefined

    sort_Key: String | undefined


    constructor(id: Number, name: String) {
        this.id = id
        this.name = name
    }


    setPartitionKey(partition_key: String): void {
        this.partition_key = partition_key;
    }

    setSortKey(sort_Key: String): void {
        this.sort_Key = sort_Key;
    }

}