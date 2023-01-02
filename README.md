# PhoenixArchiver

Adult metadata scraper and archiver, inspired by DirtyRacer1337/Jellyfin.Plugin.PhoenixAdult.

### What this does:
1. scrapes several sites for new releases (overview / list page only)
2. stores everything in a mongoDB
3. looks for any entry without certain datapoints (e.g. description)
4. scrapes that entries page specifically and updates the whole entry
5. works with the common naming schemes for scenes and searches the database
6. builds nfo files based on the database info

### ToDos:
- refactor everything, again
- split up general functions and site-specific config
- create master script that calls one after the other
- make it scale with available selenium sessions