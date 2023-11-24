import {Entity} from "./Entity";
import {Link} from "./Link";
import {Table} from "./Table";

/**
 * This model represents a system configuration.
 * The configuration is made up of a list of entities,
 * a list of links and a list of tables.
 */
export class Configuration {

  entities: Entity[] = []

  links: Link[] = []

  tables: Table[] = []
}
