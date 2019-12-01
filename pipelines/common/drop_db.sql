/**
 * Drop a database with the given name under the warehouse dir.
 *
 * Variables:
 *  `dbname`: the name of the database to drop
 */
 DROP DATABASE IF EXISTS ${dbname} CASCADE;
