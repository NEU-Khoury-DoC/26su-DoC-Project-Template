# Important Tips

## Hot Reloading

In general, any changes you make to the API code base (REST API) or the Streamlit app code should be *hot reloaded* when the files are saved — the changes should be immediately available without restarting containers.

- Don't forget to click the **Always Rerun** button in the browser tab of the Streamlit app for it to reload with changes.
- Sometimes, a bug in the code will cause a container to crash. Fix the bug in the code, then restart the `app` container in Docker Desktop or restart all containers with `docker compose restart` (no `-d` flag).

## The MySQL Container

The MySQL container behaves differently from the app and API containers — be aware of the following:

- When the MySQL container is ***created*** for the first time, it will execute any `.sql` files in the `./database-files` folder. **Important:** it will execute them in alphabetical order, so name your files accordingly (e.g. `01_schema.sql`, `02_data.sql`).
- The MySQL container's log files are your friend. Access them in Docker Desktop by selecting the MySQL container and clicking the **Logs** tab. If there are errors in your `.sql` files, they will appear here. Use the search 🔍 to look for `Error` to find them quickly.
- If you need to update anything in any of your SQL files, you **must** recreate the MySQL container rather than just stopping and restarting it. Use the following command:

  ```bash
  docker compose down db -v && docker compose up db -d
  ```

  - `docker compose down db -v` stops and deletes the MySQL container and the volume attached to it.
  - `docker compose up db -d` creates a new container and re-runs all the files in the `database-files` folder.
