# Git

We use git for version control. The repository is hosted on github. The repository can be found [here](https://github.com/jackgpalfrey/horizon-restaurants). 


## Pulling
Before starting any work you should pull the latest changes from the repository. This can be done with the `git pull` command. 

## Branches
When developing a new feature you should use a new branch. This can be done with the `git checkout -b <branch_name>` command. The branch name should be descriptive of the feature you are working on. If you wish to navigate to a branch that already exists you can use the `git checkout <branch_name>` command. `-b` means create a new branch.

## Committing
When you have made changes to the code you should commit them. This can be done with the `git commit` command. This will open a text editor where you can write a commit message. If you wish to change this to VSCode use `git config core.editor "code --wait"`. The commit messages should follow [Conventional Commits](https://www.conventionalcommits.org). A good simple guide can be found [here](https://gist.github.com/levibostian/71afa00ddc69688afebb215faab48fd7). We use the following types

- `feat` - A new feature
- `fix` - A bug fix
- `docs` - Documentation only changes
- `style` - Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
- `refactor` - A code change that neither fixes a bug nor adds a feature
- `perf` - A code change that improves performance
- `test` - Adding missing tests or correcting existing tests
- `chore` - Changes to the build process or auxiliary tools and libraries such as documentation generation
- `ci` - Changes to our CI configuration files and scripts (example scopes: Travis, Circle, BrowserStack, SauceLabs)

## Pushing
When you have made commits you should push them to the remote repository. This can be done with the `git push` command. If you have not pushed to the branch before you will need to use `git push --set-upstream origin <branch_name>`. This will create the branch on the remote repository.

## Pull Requests
When you have finished working on a feature you should create a pull request. This can be done on the github website. The pull request name should be descriptive and the description should give a brief overview of the changes. When a pull request is made the tests will be run automatically and if they fail the pull request will not be able to be merged. This is to ensure that the code is always in a working state.

## Code Reviews
When a pull request is made it must be reviewed by at least one other person. This is to ensure that the code is of a high quality and that there are no bugs. When reviewing a pull request you should check that the code is well written and that it works as intended. If you find any issues you should comment on the pull request. If you are happy with the code you should approve the pull request. If you are not happy with the code you should request changes. When requesting changes you should explain what changes you would like to see. When the changes have been made you should review the code again. If you are happy with the code you should approve the pull request. If you are not happy with the code you should request changes again. This process should continue until you are happy with the code. DO NOT merge a pull request unless it is your own. 

## Merge Conflicts
If you have a merge conflict just tell me and i'll fix it. 