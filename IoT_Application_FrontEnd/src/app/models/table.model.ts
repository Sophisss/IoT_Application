/**
 * This model represents a table.
 * Each table consists of an id, a name,
 * partition key and sort key.
 */
export class Table {

  id: number

  name: string

  type: string

  partition_key: string | undefined

  sort_Key: string | undefined
}
