### Fabric database replication

Replicate the production database using the `devtools` docker image.

#### First run
Build the container if first run: `docker-compose build devtools`

#### Running fabric commands

Run the container with the `--rm` flag (so that Docker cleans up afterwards):

- `docker-compose run --rm devtools bash`
- To exit devtools container, use `Ctrl+d`

Run fabric commands in the `devtools` container (these are slugified version of `@tasks` function names in `fabfile.py`).

Reply `y` to confirmation prompt.

##### Replicate production database to local
`fab production-data-to-local`
