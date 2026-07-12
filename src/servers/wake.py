from wakeonlan import wake

from core.logging import get_logger

log = get_logger()

def wake_server(mac_address: str) -> None:
    log.info(f"Sending Magic Packet to '{mac_address}'")
    wake(mac_address)