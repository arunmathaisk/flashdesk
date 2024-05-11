To terminate all running Docker containers, you can use the following command:

```bash
docker stop $(docker ps -q)
```

This command uses `docker ps -q` to list the IDs of all running containers, and `docker stop` is used to stop each container by its ID.

If you also want to remove the containers after stopping them, you can use:

```bash
docker rm $(docker ps -aq)
```

This command uses `docker ps -aq` to list the IDs of all containers (both running and stopped), and `docker rm` is used to remove each container by its ID.


---

To remove all Docker volumes forcefully, including those that are currently in use, you can use the following command:

```bash
docker volume rm -f $(docker volume ls -q)
```

The `-f` flag is used to force the removal of the volumes. This command will remove all volumes, including those that are currently in use, so use it with caution to avoid losing important data.