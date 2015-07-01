from functools import wraps
from docker import Client
import docker

client = Client(base_url="unix://var/run/docker.sock")

def dockerator(image="fedora",
                      base_url="unix://var/run/docker.sock",
                      command=None,
                      stop=False,
                      ports=None,
                      host_config=None,
                      wait_for=None):
    def middle(func):
        @wraps(func)
        def inner(*args, **kwargs):

            # First, check to see if we have the image running
            if any([image in x["Image"] for x in client.containers()]):
                # If there is one running, use it
                container = [x for x in client.containers() if image in x["Image"]][0]

            else:
                # There is not one running, so let's start it
                # Check to see if we have the image
                if not any(["{}:latest".format(image) in x["RepoTags"] for x in client.images()]):
                    # If not, pull it
                    client.pull(image)

                # Create the container
                container = client.create_container(
                    image=image,
                    command=command,
                    ports=ports,
                    host_config=host_config)

                # Start the container
                response = client.start(container=container)

            # If a wait_for callable was passed in execute it, it should wait until
            # The necessary service is running
            if wait_for:
                wait_for()

            # Our container is running, execute the function
            ret = func(*args, **kwargs)

            if stop:
                # stop is True, stop the container and block until it's stopped
                client.stop(container)
                client.wait(container)
            return ret
        return inner
    return middle
