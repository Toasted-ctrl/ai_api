from wakeonlan import wake

def boot_server(mac_address: str) -> None:
    wake(mac_address)