export class Table {

    name : String

    partition_key : String

    sort_Key : String


    constructor(name: String, pk: String, sk: String){
        this.name = name
        this.partition_key = pk
        this.sort_Key = sk
    }

}