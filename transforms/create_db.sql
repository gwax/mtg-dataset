/**
 * Create a database with the given name under the warehouse dir.
 *
 * Variables:
 *  `name`: the name of the database to create
 *  `location`: the path to the database storage
 */
CREATE DATABASE ${name}
LOCATION '${location}';
