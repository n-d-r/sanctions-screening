This is a little tool I am building to screen individuals, entities, vessels, and/or aircraft against two sanctions lists provided by the U.S. Office of Foreign Assets Control:

- the Specially Designated Nationals and Blocked Persons Lists ("SDN List")
- the Consolidated Sanctions List

For more information on those two lists, see here:
https://www.treasury.gov/resource-center/sanctions/SDN-List/Pages/default.aspx
https://www.treasury.gov/resource-center/sanctions/SDN-List/Pages/consolidated.aspx

This project is a work-in-progress.

The repository contains the following files:

- ss_constants.py: contains constants
- ss_variables.py: contains variables that are initialized empty and filled during execution of ss_parsing.py
- ss_functions.py: contains functions used in multiple files
- ss_downloading.py: downloads the two XML source files, each corresponding to one of the two lists above
- ss_parsing_classes.py: contains classes used for parsing the XML files
- ss_parsing.py: parses XML files and commits them to a SQLite database
- ss_create_db_tables.sql: SQLite commands to create the database tables