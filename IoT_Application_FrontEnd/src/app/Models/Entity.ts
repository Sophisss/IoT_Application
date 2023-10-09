import { Field } from "./Field";

export class Entity {

    entity_name: String;

    fields : Field[] = []

    constructor(entity_name: String) {
        this.entity_name = entity_name
    }

}
