# Docker 

## Linux

All docker compose commands can be run through the Makefile

`make prod` - Runs production enviorment with `main.py` as entry point (Ctrl+C to exit)
`make test` - Runs tests once with pytest
`make test-watch` - Runs all tests and reruns automatically when a file changes (includes pgadmin on port 5050) (Ctrl+C to exit)


## Windows

All docker compose commands can be run through bat scrips in bin/

`bin/prod.bat` - Runs production enviorment with `main.py` as entry point (Ctrl+C to exit)
`bin/test.bat` - Runs tests once with pytest
`bin/test-watch.bat` - Runs all tests and includes pgadmin on port 5050 (Ctrl+C to exit)

Note: `bin/test-watch.bat` will not rerun tests automatically when a file changes. This is a limitation of docker on windows.