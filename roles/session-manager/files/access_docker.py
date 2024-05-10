import docker
import os
import socket
import uuid
import threading
import logging

from insert_hosts import insert_hosts


def create_client(logger: logging.Logger, base_urls: list[str]) -> docker.APIClient:
    tls_config = docker.tls.TLSConfig(
        ca_cert="/root/.docker/ca.pem",
        verify=True,
        client_cert=("/root/.docker/cert.pem", "/root/.docker/key.pem"),
    )
    for base_url in base_urls:
        try:
            client = docker.APIClient(base_url=base_url, tls=tls_config)
            logger.info("docker host is " + base_url)
            return client
        except Exception as e:
            logger.warning(e)
            continue


def create_service(logger: logging.Logger, work_id: str, http_login_format: str) -> str:
    lock = threading.Lock()

    # 環境変数取得
    webdav_server = os.environ.get("WEBDAV_SERVER")
    webdav_port = os.environ.get("WEBDAV_PORT")
    # webdav_username = os.environ.get("WEBDAV_USERNAME")
    webdav_password = os.environ.get("WEBDAV_PASSWORD")

    image_chrome = "procube/node-chrome"
    swarm_network = ["hive_default_network"]

    base_urls = []
    insert_hosts(base_urls)
    client = create_client(logger, base_urls)

    work_container = "chrome-" + work_id + "-" + str(uuid.uuid4())

    http_login_format_env = "HTTP_LOGIN_FORMAT=" + http_login_format
    selenium_env = [http_login_format_env]

    url = "http://" + webdav_server + ":" + webdav_port + "/" + work_id + "/"
    davfs_driver_opts = {"username": work_id, "password": webdav_password, "url": url}
    driver_config = docker.types.services.DriverConfig(
        "fentas/davfs", options=davfs_driver_opts
    )

    davfs_mount_def = docker.types.Mount(
        "/mnt/" + work_id,
        "davfs-volume-" + work_id,
        type="volume",
        driver_config=driver_config,
    )
    davfs_public_mount_def = docker.types.Mount(
        "/mnt/public", "davfs-volume-public", type="volume"
    )
    shm_mount_def = docker.types.Mount("/dev/shm", "/dev/shm", type="bind")

    container_spec = docker.types.ContainerSpec(
        image_chrome,
        hostname=work_container,
        env=selenium_env,
        mounts=[davfs_mount_def, davfs_public_mount_def, shm_mount_def],
        cap_add=["NET_ADMIN"],
    )
    task_tmpl = docker.types.TaskTemplate(container_spec)

    if lock.locked():
        logger.warning(
            work_container + ": Other process threading lock. Please wait for a while"
        )
    lock.acquire()
    logger.info(work_container + ": Create process lock acquired")

    client.create_service(
        task_tmpl,
        name=work_container,
        networks=swarm_network,
        endpoint_spec=docker.types.EndpointSpec(mode="dnsrr"),
    )
    logger.info(work_container + ": Create successfully")

    lock.release()
    logger.info(work_container + ": Create process lock released")

    with socket.create_connection((work_container, 5900), timeout=15):
        logger.info(work_container + ": Connect successfully")

    return work_container


def delete_service(logger: logging.Logger, work_container: str) -> None:
    base_urls = []
    insert_hosts(base_urls)
    client = create_client(base_urls)
    client.remove_service(work_container)
    logger.info(work_container + ": Delete successfully")
    logger.info(
        work_container + ": Delete VNC connection object from guacamole successfully"
    )
    return
