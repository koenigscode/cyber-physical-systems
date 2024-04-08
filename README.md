# 2024-group-22
![Pipeline Status Main](https://git.chalmers.se/courses/dit638/students/2024-group-22/badges/main/pipeline.svg)


## Requirements
- Docker


## How to check out the repository into a clean folder and how to build it
1. Go to the location where you want to store this project
2. Copy to your terminal
```bash
git clone git@git.chalmers.se:courses/dit638/students/2024-group-22.git
```
3. Now a directory 2024-group-22 will be created in your current directory
4. Go to the project directory (cd 2024-group-22)
```bash
cd 2024-group-22
```
5. Build the Docker Image
```bash
./build.sh # or build -t group-22/main:latest -f Dockerfile .
```
6. Run Your Project Inside a Docker Container
```bash
./run.sh # or docker run --rm group-22/main:latest 
```



## Commit messages style


All commit messages should start with a capital letter, use imperative voice and not use dots in the end of the sentence. The subject line should be concise and clear. If more complex things were changed, a commit body can be added, explaining why and how the change was made, but it is not mandatory for self-explanatory commits, such as e.g. fixing typos. All commit messages should link to the issue with # if there is an issue associated with it.


Example: `Create .gitignore #8`


## How to add new features
- The main branch should be protected - no commmits directly to main, only merges acceptable
- Remember to git pull before starting to work on a feature branch
- Every commit must be reviewed by another team member and only then merged. If merge conflicts appear, the person who commited the change fixes the merge conflicts locally and then commits again
- The branches will be created for different features
- An issue must be linked in the merge request. The merge request must follow the same naming convention as the subject line of the commit messages
- A merge requests must be peer reviewed and approved by another team member. If the team member finds any issued with the commited code, they should provide their feedback in the comments for the merge request, staying polite and constructive


## How to fix unexpected behaviour in existing features
- If a bug is discovered, a new issue with the label "bug" should be created
- If a bug is small, e.g. a typo that can be fixed by one person, one person can fix it
- If it is a big bug, we can have a discussion in a team on how to fix the problem and carefully review the code that caused the bug
