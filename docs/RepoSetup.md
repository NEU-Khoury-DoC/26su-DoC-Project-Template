# Setting Up the Repos

## Setting Up Your Team's Repo

**Before you start**: As a team, one person needs to assume the role of *Team Project Repo Owner*.

1. The Team Project Repo Owner needs to **fork** this template repo into their own GitHub account **and give the repo a name consistent with your project's name**. If you're worried that the repo is public, don't. Every team is doing a different project.
1. In the newly forked team repo, the Team Project Repo Owner should go to the **Settings** tab, choose **Collaborators and Teams** on the left-side panel. Add each of your team members to the repository with Write access.

**Remaining Team Members**

1. Each of the other team members will receive an invitation to join.
1. Once you have accepted the invitation, you should clone the Team's Project Repo to your local machine.
1. Set up the centralized `.env` file in the `api` folder based on `api/.env.template`.
   1. Make a copy of `api/.env.template` and name it `api/.env`.
   1. Open `api/.env` and fill in all placeholder values: database password, `NEWSDATA_API_KEY`, `ENTSOE_API_KEY`, and `AGSI_API_KEY`. Ask your Team Project Repo Owner for the shared database password — do not commit secrets or share them publicly.
1. For running the containers for your team's repo:
   1. `docker compose up -d` to start all the containers in the background
   1. `docker compose down` to shutdown and delete the containers
   1. `docker compose up db -d` only start the database container (replace `db` with `api` or `app` for the other two services as needed)
   1. `docker compose stop` to "turn off" the containers but not delete them.

**Note:** You can also use the Docker Desktop GUI to start and stop the containers after the first initial run.

---

<details>
<summary>Setting Up a Personal Sandbox Repo (Optional)</summary>

## Setting Up a Personal Sandbox Repo (Optional)

If you want a totally separate copy of the template repo on your laptop to explore and experiment with without affecting your team repo, follow these steps.

**Before you start**: You need to have a GitHub account and a terminal-based git client or GUI Git client such as GitHub Desktop or the Git plugin for VSCode.

1. Clone this repo to your local machine.
   1. You can do this by clicking the green "Code" button on the top right of the repo page and copying the URL. Then, in your terminal, run `git clone <URL>`.
   1. Or, you can use the GitHub Desktop app to clone the repo. See [this page](https://docs.github.com/en/desktop/adding-and-cloning-repositories/cloning-a-repository-from-github-to-github-desktop) of the GitHub Desktop Docs for more info.
1. Open the repository folder in VSCode.
1. Set up the centralized `.env` file in the `api` folder based on `api/.env.template`.
   1. Make a copy of `api/.env.template` and name it `api/.env`.
   1. Open `api/.env` and fill in all placeholder values. Don't reuse passwords you use for other services (email, etc.).
1. For running the sandbox containers, you will tell `docker compose` to use a different configuration file than the typical one. The one you will use for testing is `sandbox.yaml`.
   1. `docker compose -f sandbox.yaml up -d` to start all the containers in the background
   1. `docker compose -f sandbox.yaml down` to shutdown and delete the containers
   1. `docker compose -f sandbox.yaml up db -d` only start the database container (replace `db` with `api` or `app` for the other two services as needed)
   1. `docker compose -f sandbox.yaml stop` to "turn off" the containers but not delete them.

</details>
