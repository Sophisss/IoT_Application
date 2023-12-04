/**
 * This model represents a table.
 * Each table consists of an id, a name,
 * partition key and sort key.
 */
export class Table {

  id: number

  name: string

  partition_key: string | undefined

  sort_Key: string | undefined


  constructor(id: number, name: string) {
    this.id = id
    this.name = name
  }


  setPartitionKey(partition_key: string): void {
    this.partition_key = partition_key;
  }

  setSortKey(sort_Key: string): void {
    this.sort_Key = sort_Key;
  }

}
